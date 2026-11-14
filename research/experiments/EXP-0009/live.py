"""EXP-0009: log the SCSP slots densely while the user plays.

Run from the repository root (``session.sh`` does this):

    ./invenv.sh python research/experiments/EXP-0009/live.py AGENT_DIR OUT_DIR

Attaches to a running patched Mednafen (D-005). Until Mednafen stops
answering, it repeatedly saves a state to a scratch file, reads its active
SCSP slots with ``EXP-0008/slots.py``, and appends ``{"frame", "slots"}`` to
``OUT_DIR/slots.jsonl``; every half second it also saves a screenshot to
``OUT_DIR/shots/f<frame>.png``. While the game is paused by the debugger no
state can be saved, so those moments are skipped. States are not kept.
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, str(Path(__file__).parents[1] / "EXP-0008"))
from slots import active_slots

from tools.mednafen.agent import Agent, AgentError


def frame_of(reply: str) -> int:
    return int(reply.split("frame=")[1].split()[0])


def main(agent_dir: Path, out: Path) -> int:
    shots = out / "shots"
    shots.mkdir(parents=True, exist_ok=True)
    tmp = (out / "tmp.mc0").resolve()
    agent = Agent(agent_dir.resolve(), 10.0)
    next_shot = 0.0
    with (out / "slots.jsonl").open("a") as rows:
        while True:
            try:
                status = agent.command("status")[-1]
                frame = frame_of(status)
                if time.monotonic() >= next_shot:
                    agent.screenshot(shots / f"f{frame:08d}.png")
                    next_shot = time.monotonic() + 0.5
                if "halted=1" in status:
                    time.sleep(0.05)
                    continue
                replies = agent.command(f"savestate {tmp}", "status")
                rows.write(
                    json.dumps(
                        {
                            "frame": frame_of(replies[-1]),
                            "slots": active_slots(tmp.read_bytes()),
                        }
                    )
                    + "\n"
                )
                rows.flush()
            except AgentError as error:
                print(f"stopped: {error}")
                break
    tmp.unlink(missing_ok=True)
    return 0


if __name__ == "__main__":
    assert frame_of("ok halted=0 frame=1234 hits=0") == 1234
    raise SystemExit(main(Path(sys.argv[1]), Path(sys.argv[2])))
