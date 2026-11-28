"""Cold-boot the experimental title image and switch editions through Options."""

from __future__ import annotations

import argparse
import sys
from hashlib import sha256
from pathlib import Path

from build_tag import EDITION, SETTINGS, SETTINGS_SIZE, TEXTURE_OFFSET
from chiseled_silver import texture

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, "research/experiments/EXP-0042")
sys.path.insert(0, "research/experiments/EXP-0046")
from check_endings import quiet_home  # type: ignore[import-not-found]
from drive import PADS, WRITERS, launch, run_steps, start, stop  # type: ignore[import-not-found]

from tools.mednafen.agent import Agent
from tools.mednafen.backup_ram import BLOCK, BLOCKS, HEADER, RESERVED
from tools.memory.vdp1_sprites import sprites

START, DOWN, UP, RIGHT = "0800", "2000", "1000", "8000"
OPTION_CURSOR = 0x0608086C
LOGO_COMMAND = 0x0BA0
LOGO_SHAPE = {"us": (160, 48, 208, 80), "jp": (32, 48, 352, 64)}


def run(agent: Agent, out: Path, *steps: str) -> None:
    run_steps(agent, steps, out, PADS["us"], WRITERS["us"])


def press(agent: Agent, out: Path, key: str, frames: int = 10) -> None:
    run(agent, out, f"press:{key}", str(frames))


def capture(
    agent: Agent, out: Path, name: str, edition: int, *, options: bool = False
) -> None:
    assert agent.bus_read(EDITION, 1) == bytes([edition]), name
    vram = agent.read("vdp1vram", 0, 0x80000)
    commands = sprites(vram)
    tag = [sprite for sprite in commands if sprite.source == TEXTURE_OFFSET]
    region = "jp" if edition >= 2 else "us"
    path = out / f"{name}.png"
    agent.screenshot(path)
    digest = sha256(path.read_bytes()).hexdigest()
    print(name, "edition", edition, "tag commands", len(tag), digest)
    visible = not options and edition in (0, 3)
    assert len(tag) == int(visible), name
    if not options:
        first = next(
            (sprite for sprite in commands if sprite.command_address == LOGO_COMMAND),
            None,
        )
        assert first is not None, name
        assert (first.width, first.height, first.x, first.y) == LOGO_SHAPE[region], name
    if visible:
        data = texture(region)
        assert vram[TEXTURE_OFFSET : TEXTURE_OFFSET + len(data)] == data, name


def to_menu(agent: Agent, out: Path) -> None:
    press(agent, out, START, 120)
    press(agent, out, START, 30)
    assert agent.bus_read(0x06080864, 2) == b"\0\x02"


def to_edition(agent: Agent, out: Path) -> None:
    press(agent, out, DOWN)
    press(agent, out, DOWN)
    press(agent, out, START, 90)
    assert agent.bus_read(0x06080864, 2) == b"\0\x03"
    for _ in range(3):
        if int.from_bytes(agent.bus_read(OPTION_CURSOR, 2), "big") == 10:
            return
        press(agent, out, UP)
    raise RuntimeError("could not select EDITION")


def backup_record(agent: Agent, name: bytes) -> bytes | None:
    """Read a settings record from the test's internal backup memory."""
    backup = agent.read("backup", 0, BLOCK * BLOCKS)
    for offset in range(RESERVED * BLOCK, len(backup), BLOCK):
        if backup[offset] == 0x80 and backup[offset + 4 : offset + 15] == name:
            break
    else:
        return None

    first = backup[offset : offset + BLOCK]
    size = int.from_bytes(first[30:34], "big")
    assert size == 512, (name, size)
    cursor = HEADER
    others = []
    while (block := int.from_bytes(first[cursor : cursor + 2], "big")) != 0:
        assert RESERVED <= block < BLOCKS
        others.append(block)
        cursor += 2
        assert cursor < BLOCK - 1
    continuation = b"".join(
        backup[block * BLOCK + 4 : (block + 1) * BLOCK] for block in others
    )
    return (first[cursor + 2 :] + continuation)[:SETTINGS_SIZE]


def boot_and_switch(cue: Path, out: Path, home: Path, edition: int) -> None:
    process, agent = launch(cue, out, home, "backup")
    try:
        start(agent, None)
        run(agent, out, "3900")
        capture(agent, out, "opening", edition)
        to_menu(agent, out)
        capture(agent, out, "title-menu", edition)
        to_edition(agent, out)
        capture(agent, out, "options", edition, options=True)
        old_us = backup_record(agent, b"N_WARRIORS_")
        old_jp = backup_record(agent, b"V_HUNTER_01")
        press(agent, out, RIGHT)
        press(agent, out, START, 120)
        selected = (edition + 1) % 4
        capture(agent, out, "after-switch", selected)
        new_us = backup_record(agent, b"N_WARRIORS_")
        new_jp = backup_record(agent, b"V_HUNTER_01")
        offset = EDITION - SETTINGS
        assert new_us is not None and new_us[offset] == selected, "US startup save"
        if selected >= 2:
            assert new_jp is not None and new_jp[offset] == selected, "JP settings save"
            assert old_us is not None
            assert old_us[:offset] == new_us[:offset]
            assert old_us[offset + 1 :] == new_us[offset + 1 :]
        else:
            assert old_jp == new_jp, "US settings save changed the prior JP record"
        print("Saved edition", selected, "with existing regional settings preserved")
    finally:
        stop(process)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("cue", type=Path)
    parser.add_argument("out", type=Path)
    args = parser.parse_args()
    out = args.out.resolve()
    home = quiet_home(out)
    for number, edition in enumerate((0, 1, 2, 3, 0)):
        captures = out / f"boot-{number}-edition-{edition}"
        captures.mkdir()
        boot_and_switch(args.cue, captures, home, edition)


if __name__ == "__main__":
    main()
