"""EXP-0005: validate the patched agent interface on both releases (V1 smoke, V2-V4).

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0005/validate.py {jp,us} OUT_DIR

Launches the patched build in the silent home with a fresh agent directory,
runs the checks, writes ``OUT_DIR/result.json``, and stops Mednafen with
SIGTERM. Outputs (dumps, state, screenshot, log) stay under the ignored
OUT_DIR. V1's stock-equivalence half is a separate `cold_boot` run.

Copied from the Cyberbots repository,
``research/experiments/EXP-0006/validate.py`` at commit ``bac6fde`` (itself
from XvSF). Changed: the release is an argument; the title frame; the V4
ranges are chosen at run time (the first 16-byte WRAM-H block below the stack
area that changes between the V2 read and a read 30 frames later, with its
cache-through mirror) instead of Cyberbots addresses; V4 runs 600 frames.
"""

from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
from tools.mednafen.agent import Agent, AgentError, parse_pairs

BINARY = Path("vendor/mednafen/build-agent/src/mednafen")
HOME = Path("local/mednafen_quiet")
IMAGES = {
    "jp": Path(
        "local/disc_images/vh_saturn_jp_1m/"
        "Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
    ),
    "us": Path(
        "local/disc_images/nw_saturn_us/"
        "Night Warriors - Darkstalkers' Revenge (USA).cue"
    ),
}
TITLE_FRAME = 3900  # about 65 s: the title (EXP-0001 frames 063-070)
WRITE_OFFSET = 0xF0000  # WRAM-H offset used by EXP-0004's write test
PATTERN = b"EMU-021 WRITE OK"
SEARCH_END = 0xF0000  # look for a changing block below the stack area
V4_FRAMES = 600
WRAMH_RANGES = ("06000000-060FFFFF", "26000000-260FFFFF")


def connect(agent: Agent, timeout: float = 30.0) -> None:
    deadline = time.monotonic() + timeout
    while True:
        try:
            agent.status()
            return
        except AgentError:
            if time.monotonic() > deadline:
                raise
            time.sleep(0.5)


def first_changed_block(a: bytes, b: bytes, end: int) -> int:
    for offset in range(0, end, 16):
        if a[offset : offset + 16] != b[offset : offset + 16]:
            return offset
    raise ValueError("no WRAM-H block changed")


def main(release: str, out: Path) -> int:
    image = IMAGES[release]
    out.mkdir(parents=True, exist_ok=False)
    agent_dir = (out / "agent").resolve()
    env = {
        **os.environ,
        "MEDNAFEN_HOME": str(HOME.resolve()),
        "MEDNAFEN_AGENT_DIR": str(agent_dir),
    }
    for stale in (HOME / "sav").glob("*"):
        stale.unlink()
    result: dict[str, object] = {"release": release, "image": str(image)}
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            [str(BINARY), str(image)], env=env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            agent = Agent(agent_dir, timeout=20.0)
            connect(agent)
            # V1 smoke.
            result["v1"] = {
                "status": agent.status(),
                "spaces": agent.spaces(),
                "regs": {k: f"{v:08X}" for k, v in agent.regs().items()},
            }
            # Run to the title by frame count.
            frame0 = int(agent.status()["frame"])
            agent.frames(TITLE_FRAME - frame0)
            halted = agent.wait_halted(120.0)
            agent.run()
            # V2: reads, state and screenshot in one poll (one instant).
            names = {"workraml": "wram_l", "workramh": "wram_h"}
            names |= {"vdp1vram": "vdp1_vram", "vdp2vram": "vdp2_vram"}
            spaces = set(result["v1"]["spaces"])  # type: ignore[index]
            reads = [
                f"read {space} 0 {0x100000 if space.startswith('work') else 0x80000}"
                f" {(out / (name + '.bin')).resolve()}"
                for space, name in names.items()
                if space in spaces
            ]
            replies = agent.command(
                *reads,
                f"savestate {(out / 'v2.mc0').resolve()}",
                f"screenshot {(out / 'v2.png').resolve()}",
                "status",
            )
            result["v2"] = {"halted_at": halted, "replies": replies}
            # V3: paused write round trip and halt control.
            agent.pause()
            before = agent.read("workramh", WRITE_OFFSET, len(PATTERN))
            agent.write("workramh", WRITE_OFFSET, PATTERN)
            written = agent.read("workramh", WRITE_OFFSET, len(PATTERN))
            agent.write("workramh", WRITE_OFFSET, before)
            restored = agent.read("workramh", WRITE_OFFSET, len(PATTERN))
            paused = agent.status()
            agent.step()
            stepped = agent.status()
            agent.run()
            running = agent.status()
            start = int(agent.status()["frame"])
            agent.frames(30)
            after = agent.wait_halted(30.0)
            try:
                agent.savestate(out / "refused.mc0")
                refused = "accepted"
            except AgentError as error:
                refused = str(error)
            result["v3"] = {
                "before": before.hex(),
                "written": written.hex(),
                "restored": restored.hex(),
                "round_trip": written == PATTERN and restored == before,
                "paused": paused,
                "stepped": stepped,
                "running": running,
                "frames_start": start,
                "frames_halted": after,
                "savestate_while_halted": refused,
            }
            # V4: breakpoint log, continuing, on a block that changes by itself.
            later = agent.read("workramh", 0, 0x100000)
            v2_wramh = (out / "wram_h.bin").read_bytes()
            block = first_changed_block(v2_wramh, later, SEARCH_END)
            lo, hi = 0x06000000 + block, 0x06000000 + block + 15
            ranges = (
                f"{lo:08X}-{hi:08X}",
                f"{lo + 0x20000000:08X}-{hi + 0x20000000:08X}",
            )
            agent.clear_events()
            agent.bpmode("log")
            agent.breakpoints("write", ranges)
            agent.run()
            agent.frames(V4_FRAMES)
            agent.wait_halted(60.0)
            agent.breakpoints("write")
            agent.bpmode("halt")
            hits = [line for line in agent.events() if line.startswith("hit")]
            frames = sorted({int(parse_pairs(h).get("frame", "0")) for h in hits})
            result["v4"] = {
                "ranges": ranges,
                "hits": len(hits),
                "hit_frames_first_last": [frames[0], frames[-1]] if frames else [],
                "first_hits": hits[:5],
                "last_hits": hits[-3:],
                "pcs": sorted({parse_pairs(h).get("PC", "") for h in hits}),
            }
            # V4b: halt mode on all of WRAM-H, as EXP-0004 run F did by hand.
            agent.clear_events()
            agent.breakpoints("write", WRAMH_RANGES)
            agent.run()
            stop = agent.wait_halted(30.0)
            regs = agent.regs()
            agent.breakpoints("write")
            result["v4b"] = {
                "ranges": WRAMH_RANGES,
                "status": stop,
                "events": agent.events()[:3],
                "regs": {k: f"{v:08X}" for k, v in regs.items()},
            }
        finally:
            process.send_signal(signal.SIGTERM)
            result["exit_code"] = process.wait(timeout=30)
    (out / "result.json").write_text(json.dumps(result, indent=1) + "\n")
    print(json.dumps(result, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1], Path(sys.argv[2])))
