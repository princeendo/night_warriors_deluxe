"""Classify how two versions of a file differ, word by word (DIFF-001).

    ./invenv.sh python -m tools.disc.diff_files DIR_A DIR_B [--json OUT]
    ./invenv.sh python -m tools.disc.diff_files FILE_A FILE_B

For every file present in both directories whose bytes differ (or for the
two files given), the two versions are aligned on 32-bit words (as is, when
the sizes match; with ``difflib`` when they do not) and each differing word
pair is classified:

- **pointer**: both words point into Saturn work RAM (WRAM-L
  ``0x00200000``-``0x002FFFFF`` or WRAM-H ``0x06000000``-``0x060FFFFF``);
  the delta B - A is counted, since a relocation shows as one repeated delta;
- **content**: anything else.

Inserted or deleted words are counted separately. Code is identified two
ways: the first eight instructions decoded as SH-2 (``0.BIN`` and
``MAIN.BIN`` start with code), and, for files that start with a (slot,
offset) table, how many entries point at a function prologue. Output is
offsets, lengths, counts, deltas and hashes only: no file bytes (``AGENTS.md`` rule 21).
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import struct
import sys
from collections import Counter
from collections.abc import Sequence
from pathlib import Path

from tools.sh2.disasm import decode

RAM = ((0x00200000, 0x00300000), (0x06000000, 0x06100000))


def in_ram(value: int) -> bool:
    return any(lo <= value < hi for lo, hi in RAM)


def words(data: bytes) -> list[int]:
    n = len(data) // 4
    return list(struct.unpack(f">{n}I", data[: 4 * n]))


def starts_like_code(data: bytes) -> int:
    """How many of the first eight instructions decode (not ``.word``)."""
    return sum(
        not decode(data, 0, pc)[1].startswith(".word")
        for pc in range(0, min(16, len(data) & ~1), 2)
    )


PROLOGUE = (0x4F22, 0x2FE6, 0x2FD6, 0x2FC6, 0x2FB6, 0x2FA6, 0x2F96, 0x2F86)


def entry_table(data: bytes) -> tuple[int, int]:
    """(entries, entries starting with a push or ``sts.l pr``) of a header.

    Overlays start with (slot, offset) pairs ended by ``FFFFFFFF``, as the
    ``ST`` files do. An offset past the file's end (some overlays have
    them) is counted but not decoded. Returns (0, 0) when the start is not
    such a table.
    """
    code = 0
    for n, i in enumerate(range(0, len(data) - 7, 8)):
        slot, off = struct.unpack(">II", data[i : i + 8])
        if slot == 0xFFFFFFFF:
            return n, code
        if slot > 0xFFFF:
            return 0, 0
        if off < len(data) - 1:
            code += struct.unpack(">H", data[off : off + 2])[0] in PROLOGUE
    return 0, 0


def classify(a: bytes, b: bytes) -> dict[str, object]:
    wa, wb = words(a), words(b)
    pointer: Counter[int] = Counter()
    content = inserted = deleted = 0
    runs: list[list[int]] = []  # [A offset, B offset, A words, B words]
    if len(wa) == len(wb):
        ops = [
            ("replace", i, i + 1, i, i + 1) for i in range(len(wa)) if wa[i] != wb[i]
        ]
    else:
        sm = difflib.SequenceMatcher(None, wa, wb, autojunk=False)
        ops = [op for op in sm.get_opcodes() if op[0] != "equal"]
    for _tag, i1, i2, j1, j2 in ops:
        if (
            runs
            and runs[-1][0] + 4 * runs[-1][2] == 4 * i1
            and runs[-1][1] + 4 * runs[-1][3] == 4 * j1
        ):
            runs[-1][2] += i2 - i1
            runs[-1][3] += j2 - j1
        else:
            runs.append([4 * i1, 4 * j1, i2 - i1, j2 - j1])
        for x, y in zip(wa[i1:i2], wb[j1:j2], strict=False):
            if in_ram(x) and in_ram(y):
                pointer[y - x] += 1
            else:
                content += 1
        deleted += max(0, (i2 - i1) - (j2 - j1))
        inserted += max(0, (j2 - j1) - (i2 - i1))
    tail = len(a) % 4 or len(b) % 4
    return {
        "size_a": len(a),
        "size_b": len(b),
        "sha256_a": hashlib.sha256(a).hexdigest(),
        "sha256_b": hashlib.sha256(b).hexdigest(),
        "differing_bytes": sum(x != y for x, y in zip(a, b, strict=True))
        if len(a) == len(b)
        else None,
        "runs": len(runs),
        "run_list": runs,
        "first_run": runs[0][:2] if runs else None,
        "last_run_end_a": runs[-1][0] + 4 * runs[-1][2] if runs else None,
        "pointer_words": sum(pointer.values()),
        "pointer_deltas": {f"{d:+#x}": n for d, n in pointer.most_common(4)},
        "content_words": content,
        "inserted_words": inserted,
        "deleted_words": deleted,
        "unaligned_tail": bool(tail),
        "code_start_a": starts_like_code(a),
        "code_start_b": starts_like_code(b),
        "entries_a": entry_table(a),
    }


def compare_dirs(da: Path, db: Path) -> dict[str, dict[str, object]]:
    out = {}
    for fa in sorted(da.iterdir()):
        fb = db / fa.name
        if fa.is_file() and fb.is_file():
            a, b = fa.read_bytes(), fb.read_bytes()
            if a != b:
                out[fa.name] = classify(a, b)
    return out


def main(argv: Sequence[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("a", type=Path)
    p.add_argument("b", type=Path)
    p.add_argument("--json", type=Path, help="write the full result here")
    args = p.parse_args(argv)
    if args.a.is_dir():
        result = compare_dirs(args.a, args.b)
    else:
        result = {args.a.name: classify(args.a.read_bytes(), args.b.read_bytes())}
    if args.json:
        args.json.write_text(json.dumps(result, indent=1) + "\n")
    for name, r in result.items():
        print(
            f"{name:14} {r['size_a']:>7} {r['size_b']:>7} runs={r['runs']:<4} "
            f"ptr={r['pointer_words']:<4} {r['pointer_deltas']} "
            f"content={r['content_words']} ins={r['inserted_words']} "
            f"del={r['deleted_words']} code={r['code_start_a']}/8 "
            f"entries={r['entries_a']}"
        )
    return 0


if __name__ == "__main__":
    sys.exit(main())
