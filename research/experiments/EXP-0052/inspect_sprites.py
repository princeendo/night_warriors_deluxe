"""Isolate the regional logo and common glass in validated title VRAM dumps."""

from collections import Counter
from hashlib import sha256
from pathlib import Path

from tools.memory.vdp1_sprites import pixel_bytes, render, sprites

DUMPS = Path("research/memory_dumps/dbg001")
ASSETS = Path("local/extracted")
OUTPUT = Path("local/exp0052")
LOGO_COLORS = {0x7070, 0x7080}
GLASS_COLORS = {0x7100, 0x7110}
TITLE_FILES = ("TITLE.BG", "TTLDATA.BIN", "TTL.SPR")


def main() -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    for region in ("us", "jp"):
        vram = (DUMPS / f"{region}-h-vdp1.bin").read_bytes()
        assets = ASSETS / f"saturn_{region}"
        print(f"{region.upper()} VRAM: {sha256(vram).hexdigest()}")
        for name in TITLE_FILES:
            data = (assets / name).read_bytes()
            print(f"  {name}: {len(data)} bytes, {sha256(data).hexdigest()}")
        commands = sprites(vram)
        logo = [sprite for sprite in commands if sprite.color_word in LOGO_COLORS]
        glass = [sprite for sprite in commands if sprite.color_word in GLASS_COLORS]
        for group, selected in (("logo", logo), ("glass", glass)):
            png = render(vram, selected, origin=(16, -8), size=(352, 240))
            (OUTPUT / f"{region}-{group}-commands.png").write_bytes(png)
            first = selected[0].command_address
            last = selected[-1].command_address
            print(
                f"  {group}: {len(selected)} commands, 0x{first:04X}-0x{last:04X}, "
                f"render {sha256(png).hexdigest()}"
            )

        # Search only complete, high-variety samples to avoid blank matches.
        # A miss leaves encoded or transformed copies open.
        samples: Counter[bytes] = Counter()
        for sprite in logo:
            pixels = pixel_bytes(vram, sprite)
            for start in range(0, len(pixels) - 31, 8):
                block = pixels[start : start + 32]
                if len(set(block)) >= 10:
                    samples[block] += 1
                    break

        matches: Counter[str] = Counter()
        for file in sorted(assets.iterdir()):
            if file.is_file():
                data = file.read_bytes()
                for block, count in samples.items():
                    if block in data:
                        matches[file.name] += count
        print(
            f"  {samples.total()} nontrivial logo samples, disc matches {dict(matches)}"
        )


if __name__ == "__main__":
    main()
