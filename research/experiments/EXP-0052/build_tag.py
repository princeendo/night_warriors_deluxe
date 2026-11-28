"""Build the experimental edition-aware title screen from the US retail image."""

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
FINALIZER_POINTER = 0x06013D0C
FINALIZER = 0x0601AFDC
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
LOGO = 0x06084CA8
US_LOGO_END = LOGO + 28 * 32
TAIL_LENGTH = 0x0600DFE0
TAIL_SCRATCH = 0x0600E000
TAIL_LIMIT = 0x800
STAGE_LIMIT = 0x06087108
TEXTURE_OFFSET = 0x3000
VDP1_VRAM = 0x25C00000
DRAW_SPRITES = 0x0601B7A2
# The retail JP title passes sprite ID and origin to the same renderer.
JP_WORDMARK = (
    (0x0080381E, 0xE0, 0x80),
    (0x0080380E, 0xA0, 0x58),
    (0x00803825, 0x30, 0),
)


def literal_table(assembler: Assembler, entries: dict[str, int | str]) -> None:
    assembler.align4()
    for label, value in entries.items():
        assembler.label(label)
        assembler.long(value)


def dispatcher() -> bytes:
    """Call title-only code when the experimental title overlay is resident."""
    a = Assembler(DISPATCHER)
    for address, expected in (("header", "title_header"), ("marker", "magic")):
        a.mov_l_label(address, 0)
        a.mov_l_load(0, 2)
        a.mov_l_label(expected, 3)
        a.cmp_eq(3, 2)
        a.branch("bf", "stock")
    a.push_pr()
    a.mov_l_label("render", 0)
    a.jsr(0)
    a.nop()
    a.pop_pr()
    a.label("stock")
    a.mov_l_label("finalize", 0)
    a.op(0x402B)  # jmp @r0
    a.nop()
    literal_table(
        a,
        {
            "header": TITLE_BASE,
            "title_header": 0x4D4,
            "marker": TITLE_MARKER,
            "magic": MARKER,
            "render": RENDER,
            "finalize": FINALIZER,
        },
    )
    return a.assemble()


def draw_jp_wordmark(a: Assembler) -> None:
    """Replace the US commands and preserve the subtitle/menu commands after them."""
    a.label("swap_logo")
    a.push_pr()
    a.mov_l_label("cursor", 6)
    a.mov_l_load(6, 3)
    a.mov_l_label("us_logo_end", 2)
    a.op(0x3328)  # sub r2,r3
    a.op(0x4309)  # shlr2 r3, tail length in longwords
    a.mov_l_label("tail_length", 0)
    a.mov_l_store(3, 0)
    a.mov_l_label("tail_scratch", 4)
    a.tst(3, 3)
    a.branch("bt", "reset_cursor")
    a.label("save_tail")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 4)
    a.dt(3)
    a.branch("bf/s", "save_tail")
    a.add_imm(4, 4)
    a.label("reset_cursor")
    a.mov_l_label("logo_cursor", 0)
    a.mov_l_store(0, 6)

    def draw(part: int) -> None:
        a.mov_l_label(f"jp_id{part}", 4)
        a.mov_w_label(f"jp_x{part}", 5)
        a.mov_w_label(f"jp_y{part}", 6)
        a.mov_imm(0, 7)
        a.op(0x2F76)  # fifth argument: mov.l r7,@-r15
        a.mov_l_label("sprite_writer", 0)
        a.jsr(0)
        a.nop()
        a.add_imm(4, 15)

    draw(0)
    draw(1)
    a.mov_l_label("tail_length", 0)
    a.mov_l_load(0, 3)
    a.mov_l_label("cursor", 6)
    a.mov_l_load(6, 4)
    a.mov_l_label("tail_scratch", 2)
    a.tst(3, 3)
    a.branch("bt", "jp_underline")
    a.label("restore_tail")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 4)
    a.dt(3)
    a.branch("bf/s", "restore_tail")
    a.add_imm(4, 4)
    a.mov_l_store(4, 6)
    a.label("jp_underline")
    draw(2)
    a.pop_pr()
    a.rts()
    a.nop()


def render() -> bytes:
    """Use stock wordmarks and append the tag only on the two Enhanced titles."""
    tiles = {region: texture(region) for region in ("us", "jp")}
    a = Assembler(RENDER)
    a.mov_l_label("edition", 0)
    a.mov_b_load(0, 0)
    a.op(0x8801)  # cmp/eq #1,r0, US Original needs no changes
    a.branch("bt", "done")
    a.mov_l_label("mode", 0)
    a.mov_w_load(0, 0)
    a.op(0x8802)  # cmp/eq #2,r0, title menu
    a.branch("bt", "logo_frame")
    a.op(0x880A)  # cmp/eq #10,r0, opening title
    a.branch("bf", "done")
    a.label("logo_frame")
    a.mov_l_label("cursor", 6)
    a.mov_l_load(6, 3)
    a.mov_l_label("minimum", 0)
    a.cmp_hs(0, 3)
    a.branch("bf", "done")
    a.mov_l_label("limit", 0)
    a.cmp_hs(0, 3)
    a.branch("bt", "done")

    a.mov_l_label("logo_words", 2)
    a.mov_l_load(2, 0, post=True)
    a.mov_l_label("logo_mode", 1)
    a.cmp_eq(1, 0)
    a.branch("bf", "done")
    a.mov_w_r0_disp(2, 2)  # CMDSIZE at LOGO+10
    a.mov_w_label("logo_size", 1)
    a.cmp_eq(1, 0)
    a.branch("bf", "done")
    a.add_imm(4, 2)
    a.mov_l_load(2, 0)
    a.mov_l_label("logo_xy", 1)
    a.cmp_eq(1, 0)
    a.branch("bf", "done")

    a.mov_l_label("edition", 0)
    a.mov_b_load(0, 0)
    a.tst(0, 0)
    a.branch("bt", "select_us_tag")
    a.op(0x8802)  # cmp/eq #2,r0, JP Original
    a.branch("bt", "jp_logo")
    a.op(0x8803)  # cmp/eq #3,r0, JP Enhanced
    a.branch("bf", "done")
    a.label("jp_logo")
    a.push_pr()
    a.mov_l_label("jp_swap", 0)
    a.jsr(0)
    a.nop()
    a.pop_pr()
    a.mov_l_label("edition", 0)
    a.mov_b_load(0, 0)
    a.op(0x8803)  # cmp/eq #3,r0
    a.branch("bf", "done")
    a.mov_l_label("cursor", 6)
    a.mov_l_load(6, 3)
    a.mov_l_label("jp_tag", 2)
    a.mov_l_label("jp_tile", 5)
    a.branch("bra", "tag_ready")
    a.nop()
    a.label("select_us_tag")
    a.mov_l_label("us_tag", 2)
    a.mov_l_label("us_tile", 5)
    a.label("tag_ready")
    a.mov_imm(8, 1)
    a.label("send_command")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 3)
    a.dt(1)
    a.branch("bf/s", "send_command")
    a.add_imm(4, 3)
    a.mov_l_store(3, 6)

    a.mov(5, 2)
    a.mov_l_label("vram", 3)
    a.mov_w_label("tile_words", 1)
    a.label("send_texture")
    a.mov_l_load(2, 0, post=True)
    a.mov_l_store(0, 3)
    a.dt(1)
    a.branch("bf/s", "send_texture")
    a.add_imm(4, 3)
    a.label("done")
    a.rts()
    a.nop()
    draw_jp_wordmark(a)
    a.label("tile_words")
    a.word(len(tiles["us"]) // 4)
    a.label("logo_size")
    a.word(0x1430)
    for i, (_, x, y) in enumerate(JP_WORDMARK):
        a.label(f"jp_x{i}")
        a.word(x)
        a.label(f"jp_y{i}")
        a.word(y)
    literal_table(
        a,
        {
            "edition": EDITION,
            "mode": TITLE_MODE,
            "cursor": CURSOR,
            "minimum": US_LOGO_END,
            "limit": US_LOGO_END + TAIL_LIMIT,
            "logo_words": LOGO + 4,
            "logo_mode": 0x00807080,
            "logo_xy": 0x00D00050,
            "us_tag": "us_tag_data",
            "us_tile": "us_tile_data",
            "jp_tag": "jp_tag_data",
            "jp_tile": "jp_tile_data",
            "jp_swap": "swap_logo",
            "logo_cursor": LOGO,
            "us_logo_end": US_LOGO_END,
            "tail_scratch": TAIL_SCRATCH,
            "tail_length": TAIL_LENGTH,
            "sprite_writer": DRAW_SPRITES,
            "vram": VDP1_VRAM + TEXTURE_OFFSET,
            **{f"jp_id{i}": part[0] for i, part in enumerate(JP_WORDMARK)},
        },
    )
    assert US_LOGO_END + TAIL_LIMIT + (85 - 28 + 1) * 32 < STAGE_LIMIT
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
        and SAVE_OPTIONS + len(save) <= TAIL_LENGTH
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
    entry = FINALIZER_POINTER - MAIN_BASE
    start = DISPATCHER - MAIN_BASE
    code = dispatcher()
    assert data[entry : entry + 4] == struct.pack(">I", FINALIZER)
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
