"""Capture a matched retail Arcade run and exercise the quote selector."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0042"))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "EXP-0046"))
from check_endings import quiet_home, read  # type: ignore[import-not-found]
from drive import (  # type: ignore[import-not-found]
    PADS,
    WRITERS,
    launch,
    run_steps,
    start,
    stop,
)
from quote_inventory import EXTRACTED, RELEASES, groups

from tools.mednafen.agent import Agent

ADDRESS = {
    "us": (0x0601DFE4, 0x06037D46, 0x0603798E, 0x06076C20, 0x0608096D),
    "jp": (0x0601E850, 0x0603859E, 0x060381E6, 0x06076C70, 0x060809BD),
}
CASES = (("low", 30), ("mid-lo", 31), ("mid-hi", 114), ("high", 115), ("mirror", 115))
TITLE_INPUTS = ("3900", "shot:title", "press:0800", "120", "press:0800", "30")


def frames(agent: Agent, count: int) -> None:
    agent.frames(count)
    agent.wait_halted(200)


def until(agent: Agent, pc: int, limit: int) -> dict[str, int]:
    agent.bpmode("halt")
    agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}"])
    agent.frames(limit)
    status = agent.wait_halted(240)
    agent.breakpoints("pc")
    if int(status["pc"], 16) != pc:
        raise RuntimeError(f"did not reach {pc:#x}: {status}")
    return agent.regs()


def save(agent: Agent, checkpoint: Path) -> None:
    agent.run()
    agent.savestate(checkpoint)
    agent.pause()
    agent.wait_halted()
    if not checkpoint.exists():
        raise RuntimeError(f"checkpoint missing at {checkpoint}")


def arcade(agent: Agent, out: Path, region: str) -> Path:
    offset = 0x50 if region == "jp" else 0

    def run(*steps: str) -> None:
        run_steps(agent, steps, out, PADS[region], WRITERS[region])

    def pick(prefix: str = "") -> None:
        run(
            f"shot:{prefix}select",
            "press:0400",
            "60",
            f"shot:{prefix}speed",
            "press:0400",
            "60",
            f"shot:{prefix}mode",
            "press:0400",
            "250",
            f"shot:{prefix}load",
            "1250",
        )

    def time_over(winner: int) -> None:
        loser_vitality = (0x0607706B if winner == 1 else 0x06076C67) + offset
        run(f"write:{loser_vitality:08X}:0101", f"write:{0x06080977 + offset:08X}:01")

    run(*TITLE_INPUTS, "shot:title-menu", "press:0800", "300")
    pick()
    run("shot:first-fight", "300")
    time_over(2)
    run("1020")
    time_over(2)
    run("720", "shot:continue", "press:0800", "900", "shot:reselect")
    pick("re-")
    run("shot:rematch", "300")
    time_over(1)
    run("1020")
    checkpoint = out / "before-last-round.mc0"
    save(agent, checkpoint)
    time_over(1)
    _, _, renderer, _, _ = ADDRESS[region]
    until(agent, renderer, 1600)
    frames(agent, 110)
    agent.screenshot(out / "quote.png")
    frames(agent, 2200)
    agent.screenshot(out / "second-fight.png")
    return checkpoint


def quotes(agent: Agent, checkpoint: Path, out: Path, region: str) -> None:
    selector, dispatch, renderer, p1, winner_side = ADDRESS[region]
    base, japanese, english = RELEASES[region]
    main = (EXTRACTED / f"saturn_{region}" / "MAIN.BIN").read_bytes()
    variations = 8 if region == "jp" else 1
    expected = groups(main, base, japanese if region == "jp" else english, variations)
    shift = 0x50 if region == "jp" else 0
    observations = []
    for condition, health in CASES:
        start(agent, checkpoint)
        agent.bus_write(0x0607706B + shift, bytes.fromhex("0101"))
        agent.bus_write(0x06080977 + shift, b"\x01")
        until(agent, selector, 1600)
        side = read(agent, winner_side, 1)
        assert side == 0
        p2 = p1 + 0x404
        winner = read(agent, p1 + 0x3B7, 1)
        loser = read(agent, p2 + 0x3B7, 1)
        changed_loser = winner if condition == "mirror" else loser
        if condition != "mirror" and loser == winner:
            changed_loser = winner % 14 + 1
        agent.bus_write(p1 + 0x3C0, health.to_bytes(2, "big"))
        agent.bus_write(p2 + 0x3B7, bytes([changed_loser]))
        registers = until(agent, dispatch, 180)
        record = registers["R5"] & 0xFFFF
        idx = {"mirror": 0, "high": 1, "mid-lo": 2, "mid-hi": 2, "low": 3}[condition]
        candidates = expected[winner - 1][idx * variations : (idx + 1) * variations]
        assert record in candidates, (region, condition, record, candidates)
        agent.bus_write(p2 + 0x3B7, bytes([loser]))
        until(agent, renderer, 1000)
        frames(agent, 110)
        agent.screenshot(out / f"quote-{condition}.png")
        observations.append(
            {
                "condition": condition,
                "health_field": health,
                "winner": winner,
                "opponent": changed_loser,
                "record": record,
            }
        )
    (out / "quote-selection.json").write_text(json.dumps(observations, indent=2) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("region", choices=ADDRESS)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    process, agent = launch(args.cue, args.out, quiet_home(args.out), "none", False)
    try:
        start(agent, None)
        checkpoint = arcade(agent, args.out, args.region)
        quotes(agent, checkpoint, args.out, args.region)
    finally:
        stop(process)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
