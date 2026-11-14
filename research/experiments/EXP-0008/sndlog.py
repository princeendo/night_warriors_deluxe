"""EXP-0008: replay a state and log sound-RAM changes frame by frame.

Run from the repository root:

    ./invenv.sh python research/experiments/EXP-0008/sndlog.py \
        {jp,us} STATE FRAMES OUT_DIR

Launches the patched Mednafen (agent interface, D-005) in the quiet home with
``-soundrecord OUT_DIR/sound.wav``, loads STATE, then advances one frame at a
time for FRAMES frames. After each frame it reads sound RAM
(``scspram`` 0x0000-0xFFFF, i.e. ``0x25A00000``-``0x25A0FFFF``) and appends to
``OUT_DIR/changes.jsonl`` one line per frame: the frame number and every run
of changed bytes (offset, old hex, new hex) against the previous frame. A
screenshot is taken every 10 frames. No input is sent. Outputs stay under the
ignored OUT_DIR.
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
from tools.mednafen.agent import Agent, AgentError

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
SPAN = 0x10000
SCSP_SLOTS = 0x25B00000


def runs(old: bytes, new: bytes) -> list[list[object]]:
    """Runs of differing bytes as [offset, old_hex, new_hex]."""
    out: list[list[object]] = []
    i, n = 0, len(new)
    while i < n:
        if old[i] == new[i]:
            i += 1
            continue
        j = i
        while j < n and old[j] != new[j]:
            j += 1
        out.append([i, old[i:j].hex(), new[i:j].hex()])
        i = j
    return out


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


def main(release: str, state: Path, frames: int, out: Path) -> int:
    out.mkdir(parents=True, exist_ok=False)
    agent_dir = (out / "agent").resolve()
    env = {
        **os.environ,
        "MEDNAFEN_HOME": str(HOME.resolve()),
        "MEDNAFEN_AGENT_DIR": str(agent_dir),
    }
    for stale in (HOME / "sav").glob("*"):
        stale.unlink()
    shots = out / "shots"
    shots.mkdir()
    command = [
        str(BINARY),
        "-soundrecord",
        str((out / "sound.wav").resolve()),
        str(IMAGES[release]),
    ]
    summary: dict[str, object] = {"release": release, "state": str(state)}
    with (out / "mednafen.log").open("wb") as log:
        process = subprocess.Popen(
            command, env=env, stdout=log, stderr=subprocess.STDOUT
        )
        try:
            agent = Agent(agent_dir, timeout=20.0)
            connect(agent)
            agent.loadstate(state)
            agent.frames(1)
            start = agent.wait_halted(30.0)
            summary["start"] = start
            previous = agent.read("scspram", 0, SPAN)
            (out / "scspram-start.bin").write_bytes(previous)
            # All 512 KiB of sound RAM once, to check where samples sit.
            (out / "scspram-full-start.bin").write_bytes(
                agent.read("scspram", 0, 0x80000)
            )
            with (
                (out / "changes.jsonl").open("w") as changes,
                (out / "slots.bin").open("wb") as slots,
            ):
                for k in range(frames):
                    agent.frames(1)
                    status = agent.wait_halted(10.0)
                    current = agent.read("scspram", 0, SPAN)
                    frame = int(status["frame"])
                    # SCSP slot registers (32 slots x 0x20 bytes), one record
                    # per frame: 4-byte frame number, then 0x400 bytes.
                    slots.write(frame.to_bytes(4, "big"))
                    slots.write(agent.read("physical", SCSP_SLOTS, 0x400))
                    changes.write(
                        json.dumps({"frame": frame, "runs": runs(previous, current)})
                        + "\n"
                    )
                    previous = current
                    if k % 10 == 0:
                        agent.screenshot(shots / f"f{frame:08d}.png")
            (out / "scspram-end.bin").write_bytes(previous)
            summary["end"] = agent.status()
        finally:
            process.send_signal(signal.SIGTERM)
            summary["exit_code"] = process.wait(timeout=30)
    (out / "summary.json").write_text(json.dumps(summary, indent=1) + "\n")
    print(json.dumps(summary, indent=1))
    return 0


if __name__ == "__main__":
    assert runs(b"abcd", b"aXYd") == [[1, "6263", "5859"]]
    assert runs(b"ab", b"ab") == []
    raise SystemExit(
        main(sys.argv[1], Path(sys.argv[2]), int(sys.argv[3]), Path(sys.argv[4]))
    )
