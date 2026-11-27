"""Compile one new translation per fighter and stock quote condition.

Source is the Japanese Saturn ST1JPN record given with each new translation.
The stock English ST1USA records are retained and used in English editions.
Only US Enhanced uses the random selector and the mixed table.
"""

from __future__ import annotations

import struct
import textwrap
from collections.abc import Callable
from pathlib import Path

EXTRACTED = Path("local/extracted/saturn_us")
MAIN_BASE = 0x06012000
JP_ROWS = 0x06054394
JP_TABLE = 0x06054714
US_TABLE = 0x060547BC
SELECTOR_TEST = 0x0601E020
NEW_RECORD = 0x80
# Roster order, then mirror, high, mid and low vitality.
TRANSLATIONS = (
    (  # Demitri
        (0x070, "A fool. You won't get away with posing as me."),
        (0x07E, "Do you still not grasp my absolute power?"),
        (0x07C, "Nothing stirs me like a game with lives at stake."),
        (0x017, "Heh. That was entertaining. A little danger now and then suits me."),
    ),
    (  # Jon Talbain
        (0x081, "Are those fangs just for show? Pathetic!"),
        (0x08D, "You really don't know the meaning of fear, do you?"),
        (0x08C, "Any wall in my way, I'll tear down with these claws."),
        (0x01E, "The world's a big place. You actually made me fight for real."),
    ),
    (  # Victor
        (0x093, "I'm you and you're me... I don't get it."),
        (0x09A, "Huh... You stopped moving. Oh well."),
        (0x095, "The doctor made me strong. That's why I win."),
        (0x09C, "Doctor... When are you going to wake up?"),
    ),
    (  # Lord Raptor
        (0x0AA, "Beat it, you rotten corpse! Oh, that goes for me too! Ha!"),
        (0x028, "Lost your voice because I'm so cool? No autographs!"),
        (0x0A7, "What's that? You think I've got no rhythm? Ha ha ha!"),
        (0x0AF, "The real fight starts when you're dead!"),
    ),
    (  # Morrigan
        (0x0B1, "You're an illusion, a false power born of darkness."),
        (0x031, "You're cute when you get all worked up."),
        (0x0B5, "Give me more thrills. I want this to be a night to remember."),
        (0x0B3, "What a thrill. A narrow victory goes straight to my head."),
    ),
    (  # Anakaris
        (0x0C2, "Mock me not... not... not. There is only one king!"),
        (0x03B, "Sing my praises aloud, aloud, aloud!"),
        (0x0CF, "Five thousand years... years... years. Only a nap to me."),
        (0x0CE, "Do not lament, lament, lament. This is fate, fate, fate."),
    ),
    (  # Felicia
        (0x0D0, "You look just like me. How weird!"),
        (0x167, "I'm not all alone anymore!"),
        (0x0D8, "Get a little stronger, then come be my friend, okay?"),
        (0x0DE, "That outfit... Aren't you embarrassed?"),
    ),
    (  # Bishamon
        (0x0E1, "I've read your every stroke. What a dull blade!"),
        (0x0ED, "What a scream! A finer feast I could not ask for!"),
        (0x0E7, "You cannot resist my curse! This man is mine for life!"),
        (0x04D, "Stubborn wretch! Hold still and rust on my blade!"),
    ),
    (  # Rikuo
        (0x0F7, "Water has a life of its own. Ignore that and it will take yours."),
        (0x053, "Hopeless. A minnow can't beat a shark."),
        (0x0FB, "Your life has dried up completely."),
        (0x0FD, "Until I reclaim my home, I must go on through this waterless land."),
    ),
    (  # Sasquatch
        (0x101, "Protecting the village is my job. You ain't up to it!"),
        (0x10A, "Hurts, huh? Bet it does! Now quit making trouble!"),
        (0x108, "Well, time to eat."),
        (0x10C, "Ow, ow, ow! I'm too hungry to put any strength into it!"),
    ),
    (  # Huitzil
        (0x112, "Speed and power are equal. My superior programming wins."),
        (0x060, "Target repelled at fifty percent power."),
        (0x11F, "Unidentified life signs approaching. Prepare to attack."),
        (0x065, "Power dropping. Power dropping. Switching to backup battery."),
    ),
    (  # Pyron
        (0x122, "So be it. I'll grant your wish. Become dust in the cosmos!"),
        (0x069, "To all living things: cease your futile struggling at once."),
        (
            0x06E,
            "The best in the world or the best in the universe. Which is stronger?",
        ),
        (0x12A, "This planet is beautiful. So why are you all so ugly?"),
    ),
    (  # Hsien-Ko
        (0x138, "It's an old line, but I've got to say it. I'm the real one!"),
        (0x137, "You didn't close it out. You've got to be sharper!"),
        (0x13B, "I fought seriously. What's the point if you lose?"),
        (0x131, "You're good! You had me worried there, yeah."),
    ),
    (  # Donovan
        (0x15A, "You will not deceive me."),
        (0x154, "Know what defeat means. I won't leave you a way to survive."),
        (0x160, "Yes... I have no hesitation about destroying your kind."),
        (0x153, "Abominable... It is all abominable!"),
    ),
)


def patches(main: bytes) -> list[tuple[int, bytes]]:
    """Use the stock eight-way selector with English records in US Enhanced."""
    test = SELECTOR_TEST - MAIN_BASE
    if main[test : test + 2] != bytes.fromhex("2008"):
        raise ValueError("unexpected victory quote language test")
    jp_rows = struct.unpack_from(">14I", main, JP_TABLE - MAIN_BASE)
    us_rows = struct.unpack_from(">14I", main, US_TABLE - MAIN_BASE)
    mixed = bytearray()
    for roster, (jp, us, row) in enumerate(
        zip(jp_rows, us_rows, TRANSLATIONS, strict=True)
    ):
        if jp != JP_ROWS + 64 * roster:
            raise ValueError("unexpected Japanese quote bank layout")
        for group, (source, _) in enumerate(row):
            jp_ids = struct.unpack_from(">8H", main, jp - MAIN_BASE + 16 * group)
            if source not in jp_ids:
                raise ValueError(f"Japanese quote {source:#x} is outside its group")
            (stock,) = struct.unpack_from(">H", main, us - MAIN_BASE + 2 * group)
            translated = NEW_RECORD + 4 * roster + group
            mixed += struct.pack(">8H", *([stock, translated] * 4))
    # SETT enters the eight-way branch with r0 still containing language 1.
    return [(SELECTOR_TEST, bytes.fromhex("0018")), (JP_ROWS, bytes(mixed))]


def record(text: str, encode: Callable[[str], list[int]]) -> bytes:
    lines = textwrap.wrap(
        text, width=24, break_long_words=False, break_on_hyphens=False
    )
    if not 1 <= len(lines) <= 4 or any(len(line) > 24 for line in lines):
        raise ValueError(f"quote does not fit: {text!r}")
    words = []
    y = 0xB0 if len(lines) == 4 else 0xB8
    for index, line in enumerate(lines):
        words.extend((0x38, y + index * 12, 1, *encode(line)))
        words.append(0 if index == len(lines) - 1 else 0xFFFF)
    return struct.pack(f">{len(words)}H", *words)


def english_file(encode: Callable[[str], list[int]]) -> bytes:
    source = (EXTRACTED / "ST1USA.BIN").read_bytes()
    header = 12
    old_end = header + NEW_RECORD * 4
    if header + struct.unpack_from(">I", source, header)[0] != old_end:
        raise ValueError("unexpected English quote table")
    records = [record(text, encode) for row in TRANSLATIONS for _, text in row]
    ptrs = bytearray()
    for at in range(header, old_end, 4):
        (offset,) = struct.unpack_from(">I", source, at)
        if not old_end <= at + offset < len(source):
            raise ValueError("English quote offset outside the file")
        ptrs += struct.pack(">I", offset + 4 * len(records))
    body = bytearray(source[old_end:])
    for encoded in records:
        # Each new table word sits immediately before the remaining table.
        at = header + len(ptrs)
        target = old_end + 4 * len(records) + len(body)
        ptrs += struct.pack(">I", target - at)
        body += encoded
    return source[:header] + ptrs + body
