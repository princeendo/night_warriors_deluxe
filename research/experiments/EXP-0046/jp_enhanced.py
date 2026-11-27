"""Build the END-005 Japanese pages and the JP Enhanced main-ending scripts.

The four additions are new Japanese translations of the US Saturn dialogue.
The original Japanese records are retained. Only JP Enhanced scripts use
the new page IDs. The script bank lives over the US scripts only in that
edition, since the two script tables are selected by the existing region flag.
"""

from __future__ import annotations

import struct
from pathlib import Path

EXTRACTED = Path("local/extracted/saturn_us")
MAIN_BASE = 0x06012000
JP_TABLE = 0x0605B1C0
JP_TABLE_LITERAL = 0x06036840
SCRIPT_BANK = 0x0605B1F8
US_TABLE = 0x0605B730
# Verified against the glyphs in the identical retail MOJI.TBL/CHR pair.
GLYPHS = {
    "あ": 0x160,
    "い": 0x170,
    "う": 0x180,
    "か": 0x161,
    "き": 0x171,
    "く": 0x181,
    "こ": 0x1A1,
    "し": 0x172,
    "す": 0x182,
    "せ": 0x192,
    "た": 0x163,
    "ち": 0x173,
    "っ": 0x189,
    "て": 0x193,
    "と": 0x1A3,
    "な": 0x164,
    "に": 0x174,
    "の": 0x1A4,
    "は": 0x165,
    "ま": 0x166,
    "み": 0x176,
    "も": 0x1A6,
    "よ": 0x1A7,
    "ら": 0x168,
    "り": 0x178,
    "る": 0x188,
    "れ": 0x198,
    "を": 0x199,
    "ん": 0x1A9,
    "ょ": 0x179,
    "が": 0x340,
    "ぎ": 0x341,
    "ご": 0x344,
    "じ": 0x346,
    "ず": 0x347,
    "だ": 0x34A,
    "ど": 0x34E,
    "ぱ": 0x354,
    "エ": 0x383,
    "オ": 0x384,
    "ガ": 0x359,
    "キ": 0x386,
    "ク": 0x387,
    "グ": 0x35B,
    "シ": 0x38B,
    "ジ": 0x35F,
    "ス": 0x38C,
    "セ": 0x38D,
    "タ": 0x38F,
    "イ": 0x381,
    "ド": 0x367,
    "ニ": 0x395,
    "ノ": 0x398,  # noqa: RUF001
    "ハ": 0x399,
    "ブ": 0x36A,
    "メ": 0x3A3,
    "モ": 0x3A4,
    "ラ": 0x3AB,
    "リ": 0x3AC,
    "ル": 0x3AD,
    "ヲ": 0x3B1,
    "ン": 0x3B2,
    "ー": 0x17C,
    "「": 0x19C,
    "」": 0x19D,
    "、": 0x18C,
    "。": 0x17D,
    " ": 0x020,
    "主": 0x5AC,
    "人": 0x4AA,
    "様": 0x5AD,
    "私": 0x4FC,
    "王": 0x506,
    "国": 0x4A1,
    "者": 0x4CA,
    "地": 0x4EE,
    "全": 0x4E8,
    "機": 0x4B1,
    "終": 0x597,
    "了": 0x54A,
    "作": 0x521,
    "動": 0x4F2,
    "開": 0x553,
    "始": 0x589,
    "ぬ": 0x184,
    "ュ": 0x3A8,
    "ョ": 0x3AA,
    "ナ": 0x394,
    "ボ": 0x36C,
    "ウ": 0x382,
    "ツ": 0x391,
    "ゃ": 0x177,
}
# Shown dialogue provenance: US Saturn ST2USA pages 35, 4F, 54/56, 64/65.
NEW_PAGES = {
    0xA1: ("「しんぱいしすぎよ。ご主人様の", " ことは私にまかせてちょうだい。」"),
    0xA2: ("「これからもずっといっしょじゃ。」",),
    0xA3: ("「王も国もなく、あすをうしなった", " 者たちが、まだいるかもしれぬ。」"),
    0xA4: ("「この地にみながもどり、", " ともにあすをきずくのだ。」"),
    0xA5: (
        "「ブンセキ終了。ナンボクノタイリクニ",
        " ガイライシュ、タスウ。」",
    ),
    0xA6: (
        "「オメガボウエイモード作動。全機ニツグ。",
        " ガイライシュノハイジョヲ開始スル。」",
    ),
}


def words(*values: int) -> bytes:
    return struct.pack(f">{len(values)}H", *values)


def ending_file() -> bytes:
    data = bytearray((EXTRACTED / "ST2JPN.BIN").read_bytes())
    font_codes = {
        code
        for code, _ in struct.iter_unpack(">HH", (EXTRACTED / "MOJI.TBL").read_bytes())
    }
    for page_id, lines in NEW_PAGES.items():
        entry = 0x0C + page_id * 4
        if entry + struct.unpack_from(">I", data, entry)[0] != 0x19BE:
            raise ValueError(f"unexpected Japanese record at {page_id:#x}")
        struct.pack_into(">I", data, entry, len(data) - entry)
        x = (352 - 13 * max(map(len, lines))) // 2
        for index, line in enumerate(lines):
            codes = [GLYPHS[char] for char in line]
            if len(line) > 24 or set(codes) - (font_codes | {0x20}):
                raise ValueError(f"page {page_id:#x} exceeds the font or layout")
            data += words(x, 0xBA + 0x10 * index, 1, *codes)
            data += words(0 if index == len(lines) - 1 else 0xFFFF)
    return bytes(data)


def stock_script(main: bytes, addr: int) -> tuple[int, list[tuple[int, ...]]]:
    off = addr - MAIN_BASE
    (initial_wait,) = struct.unpack_from(">H", main, off)
    pages = []
    for page in struct.iter_unpack(">6H", main[off + 2 : off + 2 + 12 * 14]):
        page_id, _, _, hide, _, wait = page
        if hide != page_id | 0x8000:
            raise ValueError(f"unexpected page at {addr:#x}: {page}")
        pages.append(page)
        if wait == 0:
            return initial_wait, pages
    raise ValueError(f"unterminated script at {addr:#x}")


def add_page(
    pages: list[tuple[int, ...]],
    after: int,
    new_id: int,
    shown: int,
    *,
    gap: int = 10,
    keep_time: bool = True,
    wait_before: int | None = None,
) -> None:
    index = next(i for i, page in enumerate(pages) if page[0] == after)
    page_id, mode, old_shown, hide, hide_mode, old_gap = pages[index]
    if keep_time:
        pool = old_shown + old_gap - gap - shown
        new_shown = min(old_shown, pool - 5)
        new_gap = pool - new_shown
        if new_shown < 80:
            raise ValueError(
                f"page {page_id:#x} does not have time for page {new_id:#x}"
            )
    else:
        new_shown = old_shown
        new_gap = wait_before if wait_before is not None else old_gap or 10
    pages[index] = (page_id, mode, new_shown, hide, hide_mode, new_gap)
    pages.insert(
        index + 1,
        (new_id, mode, shown, new_id | 0x8000, hide_mode, gap if old_gap else 0),
    )


def patches(main: bytes) -> list[tuple[int, bytes]]:
    pointers = list(struct.unpack_from(">14I", main, JP_TABLE - MAIN_BASE))
    original_scripts = [stock_script(main, addr) for addr in pointers]
    stock_pages = {page[0] for _, pages in original_scripts for page in pages}
    if NEW_PAGES.keys() & stock_pages:
        raise ValueError("JP Enhanced uses a stock Japanese ending page ID")
    bank = bytearray(4 * len(pointers))
    for roster in (5, 8, 9, 11):
        index = roster - 1
        wait, pages = original_scripts[index]
        if roster == 5:
            add_page(pages, 0x34, 0xA1, 130, gap=20)
        elif roster == 8:
            add_page(pages, 0x4E, 0xA2, 120, keep_time=False)
        elif roster == 9:
            # The short gap clipped the first seven glyphs on the next page.
            add_page(pages, 0x54, 0xA3, 105, keep_time=False, wait_before=84)
            add_page(pages, 0x55, 0xA4, 120)
        else:
            # Preserve the standby page and avoid overlapping the results card.
            add_page(pages, 0x63, 0xA6, 180, gap=35)
            add_page(pages, 0x63, 0xA5, 150, gap=25)
        pointers[index] = SCRIPT_BANK + len(bank)
        bank += words(wait)
        for page in pages:
            bank += words(*page)
    if SCRIPT_BANK + len(bank) > US_TABLE:
        raise ValueError("JP Enhanced scripts exceed the US script bank")
    struct.pack_into(">14I", bank, 0, *pointers)
    if struct.unpack_from(">I", main, JP_TABLE_LITERAL - MAIN_BASE)[0] != JP_TABLE:
        raise ValueError("Japanese ending table does not match the stock literal")
    return [
        (SCRIPT_BANK, bytes(bank)),
        (JP_TABLE_LITERAL, struct.pack(">I", SCRIPT_BANK)),
    ]
