"""Build the experimental regional Deluxe title screen from the US retail image."""

from __future__ import annotations

import argparse
import struct
import sys
from importlib import import_module
from pathlib import Path

from chiseled_silver import command, texture

sys.path.insert(0, str(Path.cwd()))
sys.path.insert(0, "research/experiments/EXP-0038")
from tools.sh2.asm import Assembler

MAIN_BASE = 0x06012000
TITLE_BASE = 0x06001000
SPRITE_POINTER = 0x0601C184
DISPATCHER = 0x06045638
DISPATCHER_LIMIT = 0x060456B8
TITLE_MARKER = 0x0600B000
RENDER = TITLE_MARKER + 4
SAVE_OPTIONS = 0x0600DC00
PACK_POINTER = 0x060052F8
PACK_SETTINGS = 0x060148C4
LOAD_SETTINGS = 0x06014588
WRITE_SETTINGS = 0x060143B4
SETTINGS = 0x060830B4
SETTINGS_SIZE = 0x104
LANGUAGE = 0x06080882
BACKUP_DEVICE = 0x0606D780
SAVE_SCRATCH = 0x0600E800
MARKER = 0x444C5831  # DLX1
EDITION = 0x060830C5
TITLE_MODE = 0x06080864
CURSOR = 0x0608C188
STAGE_LIMIT = 0x06087108
TEXTURE_OFFSET = 0x3000
VDP1_VRAM = 0x25C00000
DRAW_SPRITES = 0x0601B7A2
# Native sprite writer inputs from the two retail title traces.
US_WORDMARK = (0x00803806, 0x00803805)
JP_WORDMARK = (0x0080381E, 0x0080380E, 0x00803825)


def literal_table(assembler: Assembler, entries: dict[str, int | str]) -> None:
    assembler.align4()
    for label, value in entries.items():
        assembler.label(label)
        assembler.long(value)


def dispatcher() -> bytes:
    """Route only the original title wordmark calls to the title overlay."""
    a = Assembler(DISPATCHER)
    a.mov_l_label("us_first", 1)
    a.cmp_eq(1, 4)
    a.branch("bt", "check_title")
    a.mov_l_label("us_second", 1)
    a.cmp_eq(1, 4)
    a.branch("bf", "stock")
    a.label("check_title")
    for address, expected in (("header", "title_header"), ("marker", "magic")):
        a.mov_l_label(address, 0)
        a.mov_l_load(0, 2)
        a.mov_l_label(expected, 3)
        a.cmp_eq(3, 2)
        a.branch("bf", "stock")
    a.mov_l_label("route", 0)
    a.op(0x402B)  # jmp @r0, forward the original fifth argument on the stack
    a.nop()
    a.label("stock")
    a.mov_l_label("sprite_writer", 0)
    a.op(0x402B)  # jmp @r0
    a.nop()
    literal_table(
        a,
        {
            "us_first": US_WORDMARK[0],
            "us_second": US_WORDMARK[1],
            "header": TITLE_BASE,
            "title_header": 0x4D4,
            "marker": TITLE_MARKER,
            "magic": MARKER,
            "route": RENDER,
            "sprite_writer": DRAW_SPRITES,
        },
    )
    return a.assemble()


def draw_sprite(a: Assembler) -> None:
    # The caller's fifth argument stays in r10 across both stock calls.
    a.op(0x2FA6)  # mov.l r10,@-r15
    a.mov_l_label("sprite_writer", 0)
    a.jsr(0)
    a.nop()
    a.add_imm(4, 15)


def render() -> bytes:
    """Draw the active wordmark and insert DELUXE before the stock foreground."""
    tiles = {region: texture(region) for region in ("us", "jp")}
    a = Assembler(RENDER)
    a.mov_l_label("edition", 0)
    a.mov_b_load(0, 0)
    a.mov_imm(2, 1)
    a.cmp_hs(1, 0)
    a.branch("bf", "us_edition")
    a.mov_imm(4, 2)
    a.cmp_hs(2, 0)
    a.branch("bf", "test_sprite")
    a.label("us_edition")
    a.mov_imm(0, 0)
    a.label("test_sprite")
    a.mov_l_label("us_first", 1)
    a.cmp_eq(1, 4)
    a.branch("bf", "draw_second")

    a.tst(0, 0)
    a.branch("bt", "draw_first")
    a.mov_l_label("jp_first", 4)
    a.add_imm(0x20, 5)
    a.add_imm(0x30, 6)
    a.label("draw_first")
    a.mov_l_label("sprite_writer", 0)
    a.op(0x402B)  # jmp @r0, preserve all stock call arguments
    a.nop()

    a.label("draw_second")
    # Keep the native origin, flags, and fifth argument over the sprite calls.
    a.mov_l_load(15, 1)
    a.push_pr()
    for register in (8, 9, 10, 11, 12, 13):
        a.op(0x2F06 | (register << 4))  # mov.l Rm,@-r15
    a.mov(5, 8)
    a.mov(6, 9)
    a.mov(1, 10)
    a.mov(0, 11)
    a.mov(7, 13)
    a.tst(11, 11)
    a.branch("bt", "stock_second")
    a.mov_l_label("jp_second", 4)
    a.add_imm(-0x20, 5)
    a.add_imm(8, 6)
    a.label("stock_second")
    draw_sprite(a)
    a.mov(0, 12)  # return value of the primary call
    a.tst(11, 11)
    a.branch("bt", "select_us_tag")
    a.mov_l_label("jp_third", 4)
    a.mov(8, 5)
    a.add_imm(-0x80, 5)
    a.add_imm(-0x10, 5)
    a.mov(9, 6)
    a.add_imm(-0x50, 6)
    a.mov(13, 7)
    draw_sprite(a)
    a.mov_l_label("jp_tag", 2)
    a.mov_l_label("jp_tile", 5)
    a.add_imm(0x21, 9)
    a.branch("bra", "tag_ready")
    a.nop()
    a.label("select_us_tag")
    a.mov_l_label("us_tag", 2)
    a.mov_l_label("us_tile", 5)
    a.add_imm(0x24, 9)

    a.label("tag_ready")
    a.mov_l_label("cursor", 6)
    a.mov_l_load(6, 3)
    a.mov_l_label("stage_limit", 0)
    a.cmp_hs(0, 3)
    a.branch("bt", "done")
    a.mov_imm(8, 1)
    a.label("send_command")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 3)
    a.dt(1)
    a.branch("bf/s", "send_command")
    a.add_imm(4, 3)
    a.mov_l_store(3, 6)
    a.add_imm(-20, 3)  # return to CMDXA and finish the per-frame origin
    a.add_imm(0x43, 8)
    a.mov_w_store(8, 3)
    a.add_imm(2, 3)
    a.mov_w_store(9, 3)

    a.mov(5, 2)
    a.mov_l_label("vram", 3)
    a.mov_w_label("tile_words", 1)
    a.mov_l_label("mode", 0)
    a.mov_w_load(0, 0)
    a.op(0x8803)  # cmp/eq #3,r0, OPTION MODE
    a.branch("bt", "dim")
    a.label("send_texture")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 3)
    a.dt(1)
    a.branch("bf/s", "send_texture")
    a.add_imm(4, 3)
    a.branch("bra", "done")
    a.nop()

    a.label("dim")
    a.mov_l_label("rgb_mask", 4)
    a.mov_l_label("opaque_mask", 5)
    a.label("send_dim_texture")
    a.mov_l_load(2, 0, post=True)
    a.mov(0, 6)
    a.op(0x2049)  # and r4,r0, isolate the upper bits of each RGB555 channel
    a.op(0x4009)  # shlr2 r0, quarter the intensity of each channel
    a.op(0x2659)  # and r5,r6, retain opacity of both pixels
    a.or_(6, 0)
    a.mov_l_store(0, 3)
    a.dt(1)
    a.branch("bf/s", "send_dim_texture")
    a.add_imm(4, 3)
    a.label("done")
    a.mov(12, 0)
    for register in (13, 12, 11, 10, 9, 8):
        a.mov_l_load(15, register, post=True)
    a.pop_pr()
    a.rts()
    a.nop()

    a.label("tile_words")
    a.word(len(tiles["us"]) // 4)
    literal_table(
        a,
        {
            "edition": EDITION,
            "mode": TITLE_MODE,
            "cursor": CURSOR,
            "stage_limit": STAGE_LIMIT - 32,
            "us_first": US_WORDMARK[0],
            "jp_first": JP_WORDMARK[0],
            "jp_second": JP_WORDMARK[1],
            "jp_third": JP_WORDMARK[2],
            "us_tag": "us_tag_data",
            "us_tile": "us_tile_data",
            "jp_tag": "jp_tag_data",
            "jp_tile": "jp_tile_data",
            "sprite_writer": DRAW_SPRITES,
            "vram": VDP1_VRAM + TEXTURE_OFFSET,
            "rgb_mask": 0x739C739C,
            "opaque_mask": 0x80008000,
        },
    )
    for region, tile in tiles.items():
        a.label(f"{region}_tag_data")
        a.data(command(region, TEXTURE_OFFSET))
        a.label(f"{region}_tile_data")
        a.data(tile)
    return a.assemble()


def patch_title(stock: bytes) -> bytes:
    start = TITLE_MARKER - TITLE_BASE
    code = struct.pack(">I", MARKER) + render()
    save = save_options()
    if not (
        len(stock) <= start
        and TITLE_MARKER + len(code) <= SAVE_OPTIONS
        and SAVE_OPTIONS + len(save) <= SAVE_SCRATCH
    ):
        raise ValueError("title tag exceeds title-time free RAM")
    output = bytearray(stock.ljust(start, b"\0") + code)
    output = output.ljust(SAVE_OPTIONS - TITLE_BASE, b"\0") + save
    pack_offset = PACK_POINTER - TITLE_BASE
    assert output[pack_offset : pack_offset + 4] == struct.pack(">I", PACK_SETTINGS)
    output[pack_offset : pack_offset + 4] = struct.pack(">I", SAVE_OPTIONS)
    return bytes(output)


def save_options() -> bytes:
    """Keep the stock regional save and mirror its edition to the startup file."""
    a = Assembler(SAVE_OPTIONS)
    a.push_pr()
    a.mov_l_label("pack", 0)
    a.jsr(0)
    a.nop()
    a.mov_l_label("language", 1)
    a.mov_b_load(1, 0)
    a.tst(0, 0)
    a.branch("bf", "saved")  # The US path already writes the startup file.

    a.mov_l_label("device", 1)
    a.mov_l_load(1, 0)
    a.op(0x2F06)  # mov.l r0,@-r15, regional backup device
    a.mov_l_label("live", 0)
    a.mov_l_label("scratch", 1)
    a.mov_imm(SETTINGS_SIZE // 4, 2)
    a.label("copy_words")
    a.mov_l_load(0, 3, post=True)
    a.mov_l_store(3, 1)
    a.dt(2)
    a.branch("bf/s", "copy_words")
    a.add_imm(4, 1)
    a.mov_l_label("language", 1)
    a.mov_imm(1, 0)
    a.mov_b_store(0, 1)
    a.mov_l_label("load", 0)
    a.jsr(0)
    a.nop()
    a.mov_l_label("device", 1)
    a.mov_l_load(1, 4)
    a.mov_imm(2, 0)
    a.cmp_hs(0, 4)
    a.branch("bt", "restore_live")
    a.mov_l_label("scratch_edition", 1)
    a.mov_b_load(1, 0)
    a.mov_l_label("edition", 1)
    a.mov_b_store(0, 1)
    a.mov_l_label("write", 0)
    a.jsr(0)
    a.nop()

    a.label("restore_live")
    a.mov_l_label("scratch", 0)
    a.mov_l_label("live", 1)
    a.mov_imm(SETTINGS_SIZE // 4, 2)
    a.label("restore_words")
    a.mov_l_load(0, 3, post=True)
    a.mov_l_store(3, 1)
    a.dt(2)
    a.branch("bf/s", "restore_words")
    a.add_imm(4, 1)
    a.mov_l_label("device", 1)
    a.mov_l_load(15, 0, post=True)
    a.mov_l_store(0, 1)
    a.mov_l_label("language", 1)
    a.mov_imm(0, 0)
    a.mov_b_store(0, 1)
    a.label("saved")
    a.pop_pr()
    a.rts()
    a.nop()
    literal_table(
        a,
        {
            "pack": PACK_SETTINGS,
            "load": LOAD_SETTINGS,
            "write": WRITE_SETTINGS,
            "language": LANGUAGE,
            "device": BACKUP_DEVICE,
            "live": SETTINGS,
            "edition": EDITION,
            "scratch": SAVE_SCRATCH,
            "scratch_edition": SAVE_SCRATCH + EDITION - SETTINGS,
        },
    )
    return a.assemble()


def patch_main(stock: bytes) -> bytes:
    data = bytearray(stock)
    entry = SPRITE_POINTER - MAIN_BASE
    start = DISPATCHER - MAIN_BASE
    code = dispatcher()
    assert data[entry : entry + 4] == struct.pack(">I", DRAW_SPRITES)
    assert DISPATCHER + len(code) <= DISPATCHER_LIMIT
    assert not any(data[start : start + len(code)])
    data[entry : entry + 4] = struct.pack(">I", DISPATCHER)
    data[start : start + len(code)] = code
    return bytes(data)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("out")
    args = parser.parse_args()
    edition = import_module("build_edition")
    files = edition.files()
    files["TITLE.O"] = patch_title(files["TITLE.O"])
    files["MAIN.BIN"] = patch_main((edition.EXTRACTED / "MAIN.BIN").read_bytes())
    return int(edition.build(args.out, files))


if __name__ == "__main__":
    raise SystemExit(main())
