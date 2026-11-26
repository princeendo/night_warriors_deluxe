"""AUD-004: a VS match with forced fighters and scripted motions, in stereo.

Cold boot (no cart), title -> VS, P2 joins, both take the default pick and
confirm speed, mode, handicap and stage. ``--watch`` then logs every write
to the fighter ID bytes until the fight is loaded (to find the writer).
``--ids`` writes both one-based IDs after the picks, before the fight loads.

Once the fight runs, ``--moves`` plays motion scripts on a pad. Each script
is a comma list of ``RAWWORDxFRAMES`` items, held frame by frame: the raw
pad word is written each frame after the game stores it, and the pressed
word gets the newly set bits. ``wait:N`` items run N frames without input.
Sound is recorded to ``sound.wav``. With ``--slot-frames``, the SCSP slots
are sampled from save states (``slots2.py``) after each script.
Sound RAM is dumped to ``scspram.bin`` at the end.
"""

from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "EXP-0042"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from drive import (  # type: ignore[import-not-found]
    PADS,
    WRITERS,
    launch,
    run_steps,
    start,
    stop,
)
from slots2 import active_slots

from tools.mednafen.agent import Agent

IDS = {"us": (0x06076FD7, 0x060773DB), "jp": (0x06077027, 0x0607742B)}


def hold(
    agent: Agent,
    pad_words: int,
    writer: int,
    script: str,
    log: list[object],
    watch: list[str],
) -> None:
    prev = 0
    for item in script.split(","):
        if item.startswith("wait:"):
            agent.frames(int(item[5:]))
            agent.wait_halted(timeout=600)
            prev = 0
            continue
        word_text, count = item.split("x")
        word = int(word_text, 16)
        for _ in range(int(count)):
            pressed = word & ~prev
            pad_range = f"{pad_words + 2:08X}-{pad_words + 3:08X}"
            agent.breakpoints("write", [pad_range, *watch])
            data = word.to_bytes(2, "big") + pressed.to_bytes(2, "big")
            agent.onhit_write(writer, pad_words, data)
            agent.frames(1)
            agent.wait_halted()
            agent.onhit_clear()
            agent.breakpoints("write", watch)
            frame = int(agent.status()["frame"])
            log.append(
                {"frame": frame, "raw": f"{word:04X}", "pressed": f"{pressed:04X}"}
            )
            prev = word


def sample_slots(agent: Agent, out: Path, frames: int, records: list[object]) -> None:
    """Save a state every 2 frames for FRAMES frames and parse its slots."""
    tmp = out / "tmp.mc0"
    for _ in range(frames // 2):
        agent.frames(2)
        agent.wait_halted()
        frame = int(agent.status()["frame"])
        agent.run()
        agent.savestate(tmp)
        agent.pause()
        agent.wait_halted()
        deadline = time.monotonic() + 5
        while not tmp.exists() and time.monotonic() < deadline:
            time.sleep(0.02)
        records.append({"frame": frame, "slots": active_slots(tmp.read_bytes())})
        tmp.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path, help="new directory")
    parser.add_argument("--ids", type=int, nargs=2)
    parser.add_argument("--watch", action="store_true")
    parser.add_argument("--select-wait", type=int, default=120)
    parser.add_argument("--fight-wait", type=int, default=1500)
    parser.add_argument("--moves", nargs="*", default=[], help="PAD:SCRIPT, PAD 1 or 2")
    parser.add_argument("--slot-frames", type=int, default=0)
    parser.add_argument("--region", choices=IDS, default="us")
    parser.add_argument(
        "--arcade", action="store_true", help="ARCADE instead of VS (P2 is the CPU)"
    )
    parser.add_argument(
        "--patch",
        nargs="*",
        default=[],
        help="ADDR:HEX writes made once the title is reached (RAM only)",
    )
    parser.add_argument(
        "--trace",
        type=lambda text: int(text, 16),
        nargs="*",
        default=[],
        help="PCs logged during moves",
    )
    parser.add_argument(
        "--watch-sound",
        action="store_true",
        help="log SH-2 writes to the sound driver command area during moves",
    )
    args = parser.parse_args()

    out = args.out.resolve()
    out.mkdir(parents=True)
    process, agent = launch(args.cue, out, None, "none", wav=True)
    pad, writer = PADS[args.region], WRITERS[args.region]
    p1_id, p2_id = IDS[args.region]
    log: list[object] = []
    try:
        start(agent, None)
        title = ["3600", "press:0800", "120", "press:0800", "30"]
        if args.arcade:  # ARCADE, default pick, speed and mode
            title += ["press:0800", "300", "press:0400", "60"]
            title += ["press:0400", "60", "press:0400", "60"]
        else:  # VS, P2 joins, both take the default pick
            title += ["press:2000", "10", "press:0800", str(args.select_wait)]
            title += ["press2:0800", "60", "press:0400", "60", "press2:0400", "60"]
        title += ["shot:select"]
        run_steps(agent, title[:1], out, pad, writer)
        for patch in args.patch:
            address, _, hex_bytes = patch.partition(":")
            agent.bus_write(int(address, 16), bytes.fromhex(hex_bytes))
        run_steps(agent, title[1:], out, pad, writer)
        confirm = ["press:0400", "60", "press2:0400", "60"] * 2 + [
            "press:0400",
            "60",
        ] * 3
        if args.arcade:
            confirm = []
        if args.ids:
            # Nothing writes the ID bytes between the picks and the load
            # (``--watch`` runs), so the forced IDs reach every loader.
            run_steps(agent, confirm, out, pad, writer)
            for value, address in zip(args.ids, (p1_id, p2_id), strict=True):
                if value:  # 0 keeps the game's pick (the CPU opponent in Arcade)
                    agent.bus_write(address, bytes([value]))
        else:
            run_steps(agent, confirm, out, pad, writer)
            if args.watch:
                agent.bpmode("log")
                agent.breakpoints(
                    "write", [f"{p1_id:08X}-{p1_id:08X}", f"{p2_id:08X}-{p2_id:08X}"]
                )
        agent.frames(args.fight_wait)
        agent.wait_halted(timeout=300)
        ids = agent.bus_read(p1_id, 1)[0], agent.bus_read(p2_id, 1)[0]
        log.append({"ids": ids})
        agent.screenshot(out / "fight.png")
        records: list[object] = []
        watch = ["25A00700-25A007FF"] if args.watch_sound else []
        agent.bpmode("log")
        agent.clear_events()
        agent.breakpoints("write", watch)
        agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}" for pc in args.trace])
        for index, move in enumerate(args.moves):
            pad_no, _, script = move.partition(":")
            words = pad + (4 if pad_no == "2" else 0)
            log.append({"move": move, "start": agent.status()["frame"]})
            hold(agent, words, writer, script, log, watch)
            agent.screenshot(out / f"move{index}.png")
            if args.slot_frames:
                sample_slots(agent, out, args.slot_frames, records)
        if records:
            (out / "slots.jsonl").write_text(
                "".join(json.dumps(r) + "\n" for r in records)
            )
        (out / "scspram.bin").write_bytes(agent.read("scspram", 0, 0x80000))
        (out / "events.log").write_text("\n".join(agent.events()) + "\n")
        (out / "log.json").write_text(json.dumps(log, indent=1, default=str))
        print(json.dumps(log[-1] if log else {}, default=str))
    finally:
        stop(process)


if __name__ == "__main__":
    main()
