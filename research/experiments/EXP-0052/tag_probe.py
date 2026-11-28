"""Draw Design F in a replayed retail title frame via the live VDP1 list."""

from __future__ import annotations

import argparse
import json
import sys
from hashlib import sha256
from pathlib import Path

from chiseled_silver import command, texture

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, "research/experiments/EXP-0042")
sys.path.insert(0, "research/experiments/EXP-0046")
from check_endings import quiet_home  # type: ignore[import-not-found]
from drive import launch, start, stop  # type: ignore[import-not-found]

from tools.mednafen.agent import Agent
from tools.memory.vdp1_sprites import sprites, walk

FINALIZE = 0x0601AFDC
COPY_DONE = 0x0601B004
CURSOR = 0x0608C188
TEXTURE_OFFSET = 0x3000
END = bytes.fromhex("8000")


def at_pc(agent: Agent, pc: int) -> None:
    agent.breakpoints("pc", [f"{pc:08X}-{pc:08X}"])
    agent.bpmode("halt")
    agent.frames(5)
    if int(agent.wait_halted()["pc"], 16) != pc:
        raise RuntimeError(f"did not hit {pc:#x}")
    agent.breakpoints("pc")


def inject(agent: Agent, tile: bytes, cursor: int) -> None:
    vram = agent.read("vdp1vram", 0, 0x80000)
    limit = TEXTURE_OFFSET + len(tile)
    assert all(
        item.address + 32 <= TEXTURE_OFFSET or item.address >= limit
        for item in walk(vram)
    )
    assert all(sprite.source >= limit for sprite in sprites(vram))
    commands = []
    for offset in range(0, len(tile), 256):
        chunk = tile[offset : offset + 256]
        commands.append(f"write vdp1vram {TEXTURE_OFFSET + offset:X} {chunk.hex()}")
    agent.command(*commands)
    assert agent.read("vdp1vram", TEXTURE_OFFSET, len(tile)) == tile
    agent.bus_write(cursor, command("us", TEXTURE_OFFSET))
    agent.bus_write(CURSOR, (cursor + 32).to_bytes(4, "big"))


def trial(agent: Agent, state: Path, out: Path, *, tag: bool) -> dict[str, object]:
    start(agent, state)
    tile = texture("us")
    at_pc(agent, FINALIZE)
    cursor = int.from_bytes(agent.bus_read(CURSOR, 4), "big")
    baseline = agent.bus_read(cursor, 32)
    if tag:
        inject(agent, tile, cursor)
    at_pc(agent, COPY_DONE)
    vdp_cursor = cursor - 0x06084108
    actual = agent.read("vdp1vram", vdp_cursor, 34)
    expected = command("us", TEXTURE_OFFSET) + END if tag else END
    if not actual.startswith(expected):
        raise RuntimeError(f"unexpected VDP1 list end: {actual.hex()}")
    captures = {}
    for frame in range(1, 5):
        at_pc(agent, FINALIZE)
        path = out / f"{'tag' if tag else 'control'}-{frame}.png"
        agent.screenshot(path)
        captures[path.name] = sha256(path.read_bytes()).hexdigest()
        if tag:
            # The added command from the preceding frame already names this tile.
            cursor = int.from_bytes(agent.bus_read(CURSOR, 4), "big")
            assert agent.read("vdp1vram", TEXTURE_OFFSET, len(tile)) == tile
            agent.bus_write(cursor, command("us", TEXTURE_OFFSET))
            agent.bus_write(CURSOR, (cursor + 32).to_bytes(4, "big"))
        at_pc(agent, COPY_DONE)
    return {
        "cursor": hex(cursor),
        "previous": baseline.hex(),
        "vdp_list_tail": actual.hex(),
        "texture_sha256": sha256(tile).hexdigest(),
        "screenshots": captures,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("state", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    process, agent = launch(args.cue, out, quiet_home(out), "backup")
    try:
        results = {
            "control": trial(agent, args.state, out, tag=False),
            "tag": trial(agent, args.state, out, tag=True),
        }
        (out / "result.json").write_text(json.dumps(results, indent=2) + "\n")
    finally:
        stop(process)


if __name__ == "__main__":
    main()
