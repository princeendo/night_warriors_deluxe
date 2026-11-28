"""Cold-boot and compare ordinary VS with a Training request on the same image."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from build_training import COMBAT, MENU_CURSOR, TITLE_BASE, TRAINING_REQUEST, overlay

EXPERIMENTS = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(EXPERIMENTS / name) for name in ("EXP-0042", "EXP-0057")]
from drive import launch, run_steps, start, stop, wait_running  # noqa: E402
from probe import FIREBALL, P2, PAD, WRITER, trial  # noqa: E402
from vsmove import hold  # noqa: E402

from tools.mednafen.agent import Agent  # noqa: E402

CHAIN = "2040x3,2000x9,2020x3,2000x10,2010x3,0000x3"
TITLE_TASK_SLOT = TITLE_BASE + 0x18


def verify_hooks(agent: Agent, out: Path, name: str, training: bool) -> None:
    request = agent.bus_read(TRAINING_REQUEST, 1)
    code = []
    for address, stock, variant in COMBAT:
        actual = agent.bus_read(address, len(stock))
        expected = variant if training else stock
        if actual != expected:
            raise ValueError(
                f"{name}: {address:08X} = {actual.hex()}, expected {expected.hex()}"
            )
        code.append(f"{address:08X}={actual.hex()}")
    line = f"{name}: request={request.hex()} {' '.join(code)}\n"
    with (out / "hooks.txt").open("a") as report:
        report.write(line)
    print(line.strip(), flush=True)
    if request != b"\0":
        raise ValueError(f"{name}: expected a clear request byte, got {request.hex()}")


def checkpoint(agent: Agent, path: Path) -> None:
    agent.run()
    wait_running(agent)
    agent.savestate(path)
    agent.pause()
    agent.wait_halted()


def title(agent: Agent, out: Path) -> None:
    run_steps(
        agent,
        ["3600", "press:0800", "120", "press:0800", "30", "press:2000", "10"],
        out,
        PAD,
        WRITER,
    )
    if agent.bus_read(MENU_CURSOR, 2) != b"\0\x01":
        raise ValueError("expected the VS cursor on the title menu")
    verify_hooks(agent, out, "cold-title", training=False)
    agent.screenshot(out / "title.png")
    checkpoint(agent, out / "title.mc0")


def enter_vs(agent: Agent, out: Path, training: bool) -> None:
    verify_hooks(agent, out, "before-start", training=False)
    if training:
        agent.bus_write(TRAINING_REQUEST, b"\x01")
    run_steps(agent, ["press:0800", "120", "shot:selection"], out, PAD, WRITER)
    verify_hooks(agent, out, "character-select", training=training)
    picks = ["press2:0800", "60"]
    picks += ["press:0400", "60", "press2:0400", "60"] * 3
    picks += ["press:0400", "60"] * 3
    run_steps(agent, picks, out, PAD, WRITER)
    # Match the earlier Demitri/Victor fixture without altering combat code.
    agent.bus_write(0x06076FD7, b"\x01")
    agent.bus_write(0x060773DB, b"\x03")
    run_steps(agent, ["1200", "shot:checkpoint"], out, PAD, WRITER)
    checkpoint(agent, out / "vs.mc0")
    start(agent, out / "vs.mc0")
    verify_hooks(agent, out, "first-round", training=training)


def check_chain(out: Path, training: bool) -> None:
    reads = {
        line.split()[0]: line.rsplit("=", 1)[1]
        for line in (out / "reads.txt").read_text().splitlines()
    }
    events = (out / "events.log").read_text()
    if training:
        if (
            any(
                value != "0000"
                for key, value in reads.items()
                if key.endswith("-knockout")
            )
            or reads["hit2-after-180-p2"] != "0001"
            or events.count(" PC=060229A2 ") != 6
        ):
            raise ValueError(
                "expected six lethal strikes, one vitality, and clear KO bytes"
            )
    elif (
        reads["hit1-after-20-knockout"] != "01ff"
        or reads["hit2-after-180-knockout"] != "0000"
        or reads["hit2-after-180-p2"] != "0090"
        or " PC=060229A2 " in events
    ):
        raise ValueError("expected a stock KO followed by round two")


def check_exit(agent: Agent, out: Path) -> None:
    verify_hooks(agent, out, "before-reset", training=True)
    # Execute the activated common hook before testing return to the title.
    agent.bus_write(P2, b"\x00\x01")
    hold(agent, PAD, WRITER, FIREBALL, [], [])
    run_steps(agent, ["90", "shot:before-reset"], out, PAD, WRITER)
    # 06013D42 compares the raw chord; 06013D4C wants only Start newly pressed.
    watch = [
        f"{address:08X}-{address + len(stock) - 1:08X}" for address, stock, _ in COMBAT
    ]
    agent.clear_events()
    hold(agent, PAD, WRITER, "0700x4,0F00x1,0000x2", [], watch)
    _, labels = overlay()
    slot = bytes.fromhex("000004d7") + (labels["title_task"] - TITLE_BASE).to_bytes(
        4, "big"
    )
    for index in range(40):
        run_steps(agent, ["120"], out, PAD, WRITER)
        if (
            agent.bus_read(TITLE_TASK_SLOT, 8) == slot
            and agent.bus_read(labels["initialized"], 1) == b"\1"
        ):
            verify_hooks(agent, out, "title-after-reset", training=False)
            agent.screenshot(out / "after-reset.png")
            (out / "events.log").write_text("\n".join(agent.events()) + "\n")
            return
        if index in (29, 31):
            run_steps(agent, ["press:0800", "30"], out, PAD, WRITER)
    agent.screenshot(out / "reset-timeout.png")
    raise ValueError("timed out waiting for the title task after the stock reset chord")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    source = parser.add_mutually_exclusive_group()
    source.add_argument(
        "--state", type=Path, help="reuse a title checkpoint from this image"
    )
    source.add_argument(
        "--exit-state", type=Path, help="check reset from an armed VS fight"
    )
    args = parser.parse_args()
    out = args.out.resolve()
    out.mkdir(parents=True)
    process, agent = launch(args.cue, out, None, "none")
    try:
        if args.exit_state is not None:
            start(agent, args.exit_state)
            check_exit(agent, out)
            return
        title_state = args.state or (out / "title.mc0")
        if args.state is None:
            start(agent, None)
            title(agent, out)
        for training, label in ((False, "off"), (True, "on")):
            branch = out / label
            branch.mkdir()
            start(agent, title_state)
            enter_vs(agent, branch, training)
            trial(agent, branch, True, None, 1, "8000x115", CHAIN, False)
            check_chain(branch, training)
    finally:
        stop(process)


if __name__ == "__main__":
    main()
