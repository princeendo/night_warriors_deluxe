"""Compare the differing FILE-05 archives from the two retail extractions."""

from bisect import bisect_right
from collections import Counter
from difflib import SequenceMatcher
from hashlib import sha256
from itertools import pairwise
from pathlib import Path
from struct import unpack_from

EXTRACTED = Path("local/extracted")
JP = EXTRACTED / "saturn_jp"
US = EXTRACTED / "saturn_us"


def word(data: bytes, offset: int) -> int:
    return int(unpack_from(">I", data, offset)[0])


def slots(data: bytes) -> dict[int, int]:
    entries: dict[int, int] = {}
    for index in range(0, len(data), 8):
        slot = word(data, index)
        if slot == 0xFFFFFFFF:
            return entries
        entries[slot] = word(data, index + 4)
    raise ValueError("No slot table terminator")


def changed_slots(jp: bytes, us: bytes) -> dict[int, int]:
    directory = slots(jp)
    assert directory == slots(us)
    by_offset = {offset: slot for slot, offset in directory.items()}
    offsets = sorted(by_offset)
    changed: Counter[int] = Counter()
    for index, (a, b) in enumerate(zip(jp, us, strict=True)):
        if a != b:
            previous_offset = bisect_right(offsets, index) - 1
            assert previous_offset >= 0
            changed[by_offset[offsets[previous_offset]]] += 1
    return dict(changed)


def page_starts(data: bytes, table: int, count: int) -> list[int]:
    cells = range(table, table + 4 * count, 4)
    return [cell + word(data, cell) for cell in cells]


def ending_pages(data: bytes, slot: int, next_slot: int, count: int) -> list[bytes]:
    directory = slots(data)
    end = page_starts(data, directory[next_slot], 1)[0]
    bounds = [*page_starts(data, directory[slot], count), end]
    assert bounds == sorted(bounds)
    return [data[a:b] for a, b in pairwise(bounds)]


def verify_st2(pages: list[bytes], st2: bytes, aliases: list[int]) -> None:
    st2_starts = page_starts(st2, 0x0C, max(aliases) + 1)
    for page, alias in zip(pages, aliases, strict=True):
        start = st2_starts[alias]
        assert st2[start : start + len(page)] == page


def sprite_blocks(data: bytes) -> list[bytes]:
    descriptors, _, payload, count, auxiliary, _ = unpack_from(">6I", data)
    table = 24 + descriptors + auxiliary
    sizes = unpack_from(f">{count}I", data, table)
    cursor = table + 4 * count
    hashes = []
    for size in sizes:
        hashes.append(sha256(data[cursor : cursor + size]).digest())
        cursor += size
    assert table + payload == len(data) and 0 <= len(data) - cursor <= 3
    return hashes


def main() -> None:
    for name in ("P00.BIN", "P03_.BIN"):
        a, b = ((root / name).read_bytes() for root in (JP, US))
        print(name, {hex(slot): count for slot, count in changed_slots(a, b).items()})

    jp, us = ((root / "P00.BIN").read_bytes() for root in (JP, US))
    jp_pages = ending_pages(jp, 0x1E6, 0x1E7, 11)
    us_pages = ending_pages(us, 0x1E6, 0x1E7, 11)
    changed = [
        i for i, (a, b) in enumerate(zip(jp_pages, us_pages, strict=True)) if a != b
    ]
    print("Changed P00 English page IDs:", changed)
    verify_st2(
        us_pages,
        (US / "ST2USA.BIN").read_bytes(),
        [*range(0x10, 0x18), *range(0x68, 0x6B)],
    )
    print("US P00 English page bodies match ST2USA entries 10-17 and 68-6A")

    japanese_pages = ending_pages(jp, 0x1E5, 0x1E6, 14)
    assert ending_pages(us, 0x1E5, 0x1E6, 14) == japanese_pages
    verify_st2(
        japanese_pages,
        (JP / "ST2JPN.BIN").read_bytes(),
        [*range(0x10, 0x18), *range(0x68, 0x6E)],
    )
    spanish_start = page_starts(jp, slots(jp)[0x1E7], 1)[0]
    assert page_starts(us, slots(us)[0x1E7], 1)[0] == spanish_start
    assert jp[spanish_start:] == us[spanish_start:]
    print("P00 Japanese and Spanish pages match across regions")

    for name in ("P00.SPR", "P03.BIN", "P03.SPR"):
        assert (JP / name).read_bytes() == (US / name).read_bytes()
    print("P00.SPR and Victor's full P03.BIN and P03.SPR are byte-identical")

    archives = [sprite_blocks((root / "P03_.SPR").read_bytes()) for root in (JP, US)]
    jp_blocks, us_blocks = archives
    align = SequenceMatcher(None, jp_blocks, us_blocks, autojunk=False)
    print("Reduced sprite blocks JP/US:", len(jp_blocks), len(us_blocks))
    print("Matching blocks:", sum(block.size for block in align.get_matching_blocks()))
    for tag, jp_start, jp_end, us_start, us_end in align.get_opcodes():
        if tag != "equal":
            print(tag, (jp_start, jp_end), (us_start, us_end))


if __name__ == "__main__":
    main()
