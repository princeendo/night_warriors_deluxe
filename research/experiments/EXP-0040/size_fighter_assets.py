"""Calculate the stock loader's fighter BIN and SPR storage requirements."""

from itertools import combinations
from pathlib import Path
from struct import unpack_from

EXTRACTED = Path("local/extracted/saturn_us")
MAIN_BASE = 0x06012000


def sprite_bytes(path: Path) -> int:
    data = path.read_bytes()
    descriptors, _, payload, count, auxiliary, _ = unpack_from(">6I", data)
    table = 24 + descriptors + auxiliary
    block_sizes = unpack_from(f">{count}I", data, table)
    if (
        table + payload != len(data)
        or not 0 <= payload - 4 * count - sum(block_sizes) <= 3
    ):
        raise ValueError(f"Unexpected sprite layout in {path}")
    return len(data) - 24


def main() -> None:
    main_bin = (EXTRACTED / "MAIN.BIN").read_bytes()
    (high_start,) = unpack_from(">I", main_bin, 0x060529DC - MAIN_BASE)
    (vram_pool,) = unpack_from(">I", main_bin, 0x06012244 - MAIN_BASE)
    wram_bound = 0x060F0000 - high_start + 0x100000
    stock_bound = wram_bound + vram_pool
    full = {}
    print("Set     FULL bytes    CUT bytes  Extra bytes")
    for index in range(1, 15):
        name = f"P{index:02}"
        bin_size = (EXTRACTED / f"{name}.BIN").stat().st_size
        bin_allocation = (bin_size + 3) & ~3
        full[name] = bin_allocation + sprite_bytes(EXTRACTED / f"{name}.SPR")
        cut_sprite = EXTRACTED / f"{name}_.SPR"
        cut = full[name]
        if cut_sprite.is_file():
            cut_bin_size = (EXTRACTED / f"{name}_.BIN").stat().st_size
            cut = ((cut_bin_size + 3) & ~3) + sprite_bytes(cut_sprite)
        print(f"{name:6}{full[name]:12,d}{cut:13,d}{full[name] - cut:13,d}")

    first, second = max(
        combinations(full, 2), key=lambda pair: full[pair[0]] + full[pair[1]]
    )
    total = full[first] + full[second]
    print(f"Largest distinct FULL pair: {first} + {second}, {total:,} bytes")
    print(f"Stock WRAM pools before other allocations: at most {wram_bound:,} bytes")
    print(f"Stock pools including VDP2 VRAM: at most {stock_bound:,} bytes")
    print(f"Minimum excess over all pools: {total - stock_bound:,} bytes")


if __name__ == "__main__":
    main()
