"""EXP-0018: build a US image that shows the Japanese epilogue after the English ending.

    ./invenv.sh python research/experiments/EXP-0018/build_epilogue.py [OUT_DIR]

Reads MAIN.BIN, ENDING.O and ST1JPN.BIN from the untouched US data track,
checks the original bytes at each site, applies the changes in PATCHES
(the region flag stays 2, so names, menus and US-only behaviour are kept),
and writes the image with ``tools.disc.patch_image`` (same-size in-place
replacement, EDC/ECC regenerated). OUT_DIR defaults to
``build/us_enhanced_epilogue``.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.disc import patch_image
from tools.disc.iso9660 import Track

SOURCE = Path("local/disc_images/nw_saturn_us")
TRACK = "Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin"
MANIFEST = Path("references/saturn_us/README.md")

# (file, file offset, original, modified, RAM address, purpose)
PATCHES = [
    # The ending's ST1 call loads ST1JPN.BIN by name. The shared name array is
    # left alone: the win screens load ST1USA.BIN (English win quotes) through it.
    (
        "MAIN.BIN",
        0x29902,
        "D338",
        "D438",
        0x0603B902,
        "mov.l @(0x0603B9E4),r3 -> r4: r4 = the literal (now the ST1JPN.BIN name)",
    ),
    (
        "MAIN.BIN",
        0x29904,
        "6030",
        "0009",
        0x0603B904,
        "mov.b @r3,r0 (the flag read) -> nop",
    ),
    (
        "MAIN.BIN",
        0x29908,
        "8B02",
        "0009",
        0x0603B908,
        "ST1 gate: 'bf skip' -> nop; the ending loads an ST1 file with the flag at 2",
    ),
    (
        "MAIN.BIN",
        0x299E4,
        "0608089A",
        "0605B850",
        0x0603B9E4,
        "literal, used only at 0x0603B902: region flag address -> ST1JPN.BIN name",
    ),
    (
        "MAIN.BIN",
        0x299E8,
        "0603790E",
        "06013DF8",
        0x0603B9E8,
        "literal, used only at 0x0603B90A: language-indexed ST1 loader -> file loader",
    ),
    (
        "ST1JPN.BIN",
        0x3,
        "BA",
        "BC",
        None,
        "header slot 0x1BA (JP) -> 0x1BC (US), read by the English-mode renderer",
    ),
    (
        "ENDING.O",
        0xBFCC,
        "8B2F",
        "0009",
        0x0600CFCC,
        "epilogue: take the Japanese (flag 0) branch: card sequence before the text",
    ),
    (
        "ENDING.O",
        0xC0D0,
        "8B02",
        "0009",
        0x0600D0D0,
        "epilogue length: Japanese 0x564 frames instead of US 0x384",
    ),
]


def apply(data: bytes, patches: list[tuple]) -> bytes:
    out = bytearray(data)
    for _, offset, old, new, _, _ in patches:
        o, n = bytes.fromhex(old), bytes.fromhex(new)
        if out[offset : offset + len(o)] != o:
            raise ValueError(f"offset {offset:#x}: expected {old}")
        out[offset : offset + len(n)] = n
    return bytes(out)


def main() -> int:
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("build/us_enhanced_epilogue")
    track_path = SOURCE / TRACK
    args = ["--source-dir", str(SOURCE), "--manifest", str(MANIFEST), "--track", TRACK]
    with tempfile.TemporaryDirectory(dir="build") as tmp, track_path.open("rb") as s:
        track = Track(s, track_path.stat().st_size)
        for name in sorted({p[0] for p in PATCHES}):
            lsn, size = patch_image.find_entry(track_path, name + ";1")
            data = apply(track.read(lsn, size), [p for p in PATCHES if p[0] == name])
            (Path(tmp) / name).write_bytes(data)
            args += ["--file", name + ";1", "--data", str(Path(tmp) / name)]
        return patch_image.main([*args, "--out-dir", str(out)])


if __name__ == "__main__":
    assert apply(b"\x8b\x02", [("x", 0, "8B02", "0009", 0, "")]) == b"\x00\x09"
    raise SystemExit(main())
