"""Build the Deluxe title overlay with a one-shot Training request for VS."""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

EXPERIMENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(EXPERIMENTS / name) for name in ("EXP-0052", "EXP-0038")]
import build_edition  # noqa: E402
import build_tag  # noqa: E402

from tools.sh2.asm import Assembler  # noqa: E402

TITLE_BASE = 0x06001000
OVERLAY_END = 0x06010000
WRAPPER = 0x0600EA00
TASK_HEADER = 0x18
EDITION_TASK = 0x06009568
START_GAME = 0x06004234
START_GAME_RESUME = 0x06004240
MENU_START_RETURN = 0x060051A0
MENU_CURSOR = 0x06080868
TRAINING_REQUEST = WRAPPER  # byte in TITLE.O, zero at each overlay load

# (address, stock bytes, Training bytes). The strike variant preserves the
# two-word vitality difference needed by reaction setup (EXP-0060).
COMBAT = (
    (
        0x0602299A,
        bytes.fromhex("901504EEE075044C2448"),
        bytes.fromhex("0EB5E048E202A0260E25"),
    ),
    (0x0602B726, bytes.fromhex("64E34F26"), bytes.fromhex("A0460EB5")),
    (0x0602B8E4, bytes.fromhex("4F2664E3"), bytes.fromhex("A0140CB5")),
)


def jump(a: Assembler, label: str) -> None:
    a.mov_l_label(label, 3)
    a.op(0x432B)  # jmp @r3
    a.nop()


def combat_writes(a: Assembler, column: int) -> None:
    for index, (_, stock, training) in enumerate(COMBAT):
        code = stock if column == 1 else training
        a.mov_l_label(f"combat_{index}", 1)
        for offset in range(0, len(code), 2):
            a.mov_w_label(f"bytes_{column}_{index}_{offset}", 2)
            a.mov_w_store(2, 1)
            if offset + 2 < len(code):
                a.add_imm(2, 1)


def overlay() -> tuple[bytes, dict[str, int]]:
    a = Assembler(WRAPPER)
    a.label("training_request")
    a.data(bytes(4))
    a.label("title_task")
    a.mov_l_label("initialized_addr", 1)
    a.mov_b_load(1, 0)
    a.tst(0, 0)
    a.branch("bf", "edition")
    a.mov_imm(1, 0)
    a.mov_b_store(0, 1)
    combat_writes(a, 1)
    a.label("edition")
    jump(a, "edition_task")

    a.label("start_game")
    a.op(0x2FD6)  # mov.l r13,@-r15, original prologue
    a.push_pr()
    a.op(0x002A)  # sts pr,r0
    a.mov_l_label("menu_start_return", 1)
    a.cmp_eq(1, 0)
    a.branch("bf", "stock_start")
    a.mov_l_label("menu_cursor", 1)
    a.mov_w_load(1, 0)
    a.op(0x8801)  # cmp/eq #1,r0 (VS)
    a.branch("bf", "stock_start")
    a.mov_l_label("request_addr", 1)
    a.mov_b_load(1, 0)
    a.op(0x8801)  # cmp/eq #1,r0 (Training requested)
    a.branch("bf", "stock_start")
    a.mov_imm(0, 0)
    a.mov_b_store(0, 1)
    combat_writes(a, 2)
    a.label("stock_start")
    a.mov_l_label("first_call", 3)
    a.jsr(3)
    a.mov_imm(5, 4)  # original first call's delay slot
    a.mov_l_label("second_call", 2)
    jump(a, "resume")

    build_tag.literal_table(
        a,
        {
            "initialized_addr": "initialized",
            "edition_task": EDITION_TASK,
            "menu_start_return": MENU_START_RETURN,
            "menu_cursor": MENU_CURSOR,
            "request_addr": "training_request",
            "first_call": 0x06036950,
            "second_call": 0x06037DC2,
            "resume": START_GAME_RESUME,
            **{f"combat_{i}": row[0] for i, row in enumerate(COMBAT)},
        },
    )
    for column in (1, 2):
        for index, (_, stock, training) in enumerate(COMBAT):
            code = stock if column == 1 else training
            for offset in range(0, len(code), 2):
                a.label(f"bytes_{column}_{index}_{offset}")
                a.data(code[offset : offset + 2])
    a.label("initialized")
    a.data(bytes(2))
    return a.assemble(), a.labels


def patch_title(title: bytes) -> tuple[bytes, dict[str, object]]:
    extra, labels = overlay()
    start = WRAPPER - TITLE_BASE
    if len(title) > start or WRAPPER + len(extra) > OVERLAY_END:
        raise ValueError("Training wrapper overlaps title data or its RAM limit")
    title = title.ljust(start, b"\0") + extra
    data = bytearray(title)
    hook = Assembler(START_GAME)
    jump(hook, "target")
    build_tag.literal_table(hook, {"target": labels["start_game"]})
    patches = (
        (
            TASK_HEADER + 4,
            (EDITION_TASK - TITLE_BASE).to_bytes(4, "big"),
            (labels["title_task"] - TITLE_BASE).to_bytes(4, "big"),
        ),
        (
            START_GAME - TITLE_BASE,
            bytes.fromhex("2FD64F22D347430BE405D247"),
            hook.assemble(),
        ),
    )
    entries: list[dict[str, object]] = []
    for offset, old, new in patches:
        if len(old) != len(new) or data[offset : offset + len(old)] != old:
            raise ValueError(f"unexpected TITLE.O bytes at {offset:#x}")
        data[offset : offset + len(new)] = new
        entries.append({"offset": offset, "before": old.hex(), "after": new.hex()})
    return bytes(data), {
        "title_patches": entries,
        "wrapper_address": WRAPPER,
        "wrapper_size": len(extra),
        "wrapper_sha256": hashlib.sha256(extra).hexdigest(),
        "addresses": labels,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    files = build_edition.files()
    files["TITLE.O"], report = patch_title(build_tag.patch_title(files["TITLE.O"]))
    main = build_tag.patch_main((build_edition.EXTRACTED / "MAIN.BIN").read_bytes())
    for address, stock, training in COMBAT:
        offset = address - build_tag.MAIN_BASE
        if len(stock) != len(training) or main[offset : offset + len(stock)] != stock:
            raise ValueError(f"unexpected MAIN.BIN bytes at {address:#x}")
    files["MAIN.BIN"] = main
    result = int(build_edition.build(str(args.out), files))
    if result == 0:
        (args.out / "training_manifest.json").write_text(
            json.dumps(report, indent=2) + "\n"
        )
    return result


if __name__ == "__main__":
    raise SystemExit(main())
