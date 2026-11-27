"""Verify edition isolation and English quote selection on the rebuilt disc."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0048"))
from check_names import RIGHT, START, UP, option, press  # type: ignore[import-not-found]
from retail_run import (
    ADDRESS,
    frames,
    launch,
    quiet_home,
    read,
    run_steps,
    save,
    start,
    stop,
    until,
)
from us_enhanced_quotes import EXTRACTED, NEW_RECORD, SELECTOR_TEST, US_TABLE

from tools.mednafen.agent import Agent

# Inputs exactly on the four branch boundaries, with the winner side fixed.
BRANCHES = (("mirror", 115), ("high", 115), ("mid", 114), ("low", 30))


def cold_win(agent: Agent, out: Path) -> Path:
    def run(*steps: str) -> None:
        run_steps(agent, steps, out, 0x06076AB6, 0x06013C74)

    run(*option(), *press(UP), *press(UP))
    for position, edition in enumerate((0, 1, 2, 3, 0)):
        assert read(agent, 0x060830C5, 1) == edition
        expected = 0x0018 if edition == 0 else 0x2008
        assert read(agent, SELECTOR_TEST, 2) == expected
        if position < 4:
            run(*press(RIGHT))
    run(*press(START, 120), *press(UP), *press(UP), *press(START, 300))
    run(*press("0400", 60), *press("0400", 60), *press("0400", 60), "1500")
    run("write:0607706B:0101", "write:06080977:01", "1020")
    checkpoint = out / "before-last-round.mc0"
    save(agent, checkpoint)
    return checkpoint


def choices(agent: Agent, checkpoint: Path, out: Path, all_conditions: bool) -> None:
    selector, dispatch, renderer, p1, winner_side = ADDRESS["us"]
    base = 0x06012000
    main = (EXTRACTED / "MAIN.BIN").read_bytes()
    p2 = p1 + 0x404
    cases = [(13, 1, 0)]  # natural roster, original high-vitality quote
    cases += [
        (fighter, cond, 1)
        for fighter in range(1, 15)
        for cond in (range(4) if all_conditions else ((fighter - 1) % 4,))
    ]
    selected = []
    for roster, group, alternate in cases:
        start(agent, checkpoint)
        agent.bus_write(0x0607706B, bytes.fromhex("0101"))
        agent.bus_write(0x06080977, b"\x01")
        until(agent, selector, 1600)
        assert read(agent, winner_side, 1) == 0
        actors = [read(agent, o + 0x3B7, 1) for o in (p1, p2)]
        condition, vitality = BRANCHES[group]
        opponent = roster if condition == "mirror" else roster % 14 + 1
        agent.bus_write(p1 + 0x3B7, bytes([roster]))
        agent.bus_write(p2 + 0x3B7, bytes([opponent]))
        agent.bus_write(p1 + 0x3C0, vitality.to_bytes(2, "big"))
        until(agent, 0x0601E05A, 180)  # JSR of the JP branch's random-byte function
        # With high byte zero these seeds return 0 or 2. The stock & 0x0E
        # contributes zero or two bytes to the word offset within the group.
        agent.bus_write(0x0608087C, (alternate * 2).to_bytes(2, "big"))
        registers = until(agent, dispatch, 180)
        record = registers["R5"] & 0xFFFF
        ptr = int.from_bytes(main[US_TABLE - base + (roster - 1) * 4 :][:4], "big")
        expected = (
            NEW_RECORD + 4 * (roster - 1) + group
            if alternate
            else int.from_bytes(main[ptr - base + 2 * group :][:2], "big")
        )
        assert record == expected, (roster, condition, record, expected)
        for obj, actor in zip((p1, p2), actors, strict=True):
            agent.bus_write(obj + 0x3B7, bytes([actor]))
        until(agent, renderer, 1000)
        frames(agent, 140)
        target = f"{roster:02d}-{condition}-{record:03x}.png"
        agent.screenshot(out / target)
        selected.append({"fighter": roster, "condition": condition, "record": record})
        print(target, flush=True)
    (out / "quote-selection.json").write_text(json.dumps(selected, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--checkpoint", type=Path)
    args = parser.parse_args()
    process, agent = launch(args.cue, args.out, quiet_home(args.out), "none", False)
    try:
        start(agent, args.checkpoint)
        checkpoint = args.checkpoint or cold_win(agent, args.out)
        choices(agent, checkpoint, args.out, args.all)
    finally:
        stop(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
