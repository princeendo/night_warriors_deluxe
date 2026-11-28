"""Encode the original Design F tag as a transparent Saturn RGB sprite."""

from __future__ import annotations

import math
import struct

GLYPHS = {
    "D": (
        "011111100",
        "011111110",
        "011100111",
        "011000011",
        "011000011",
        "011000111",
        "011000111",
        "011001110",
        "011111100",
        "111111000",
    ),
    "E": (
        "001111111",
        "011111110",
        "011100000",
        "011100000",
        "011111100",
        "011111000",
        "011100000",
        "011100000",
        "011111110",
        "111111100",
    ),
    "L": (
        "001110000",
        "011100000",
        "011100000",
        "011100000",
        "011100000",
        "011100000",
        "011100000",
        "011100000",
        "011111110",
        "111111100",
    ),
    "U": (
        "011100011",
        "011100111",
        "011100111",
        "011100111",
        "011100111",
        "011100111",
        "011100111",
        "011111110",
        "011111110",
        "001111100",
    ),
    "X": (
        "111100011",
        "011100111",
        "001111110",
        "000111100",
        "000111000",
        "000111000",
        "001111100",
        "011101110",
        "111000111",
        "110000011",
    ),
}

SOURCE_WIDTH = 84
SOURCE_HEIGHT = 17
WIDTH = 88
HEIGHT = 28
SLOPE = {"us": -0.111611, "jp": -0.128092}


def rgb555(color: str) -> int:
    """Saturn direct-color pixels use the MSB and place red in the low bits."""
    red, green, blue = bytes.fromhex(color)
    return 0x8000 | (red >> 3) | ((green >> 3) << 5) | ((blue >> 3) << 10)


def unrotated() -> list[list[int]]:
    """Convert Design F to native pixels with softer in-game highlights."""
    pixels = [[0] * SOURCE_WIDTH for _ in range(SOURCE_HEIGHT)]
    layers = (
        (-1, 3, ("172038",)),
        (0, 2, ("49659a", "394875")),
        (0, 1, ("b2c6da", "7f9eba", "a9becf")),
    )
    for inset, size, colors in layers:
        for index, letter in enumerate("DELUXE"):
            for line, row in enumerate(GLYPHS[letter]):
                color = rgb555(colors[line * len(colors) // len(GLYPHS[letter])])
                rake = (9 - line) * 34 // 100
                for column, ink in enumerate(row):
                    if ink == "1":
                        x = 5 + 11 * index + column + rake + inset
                        y = 3 + line + inset
                        for dy in range(size):
                            pixels[y + dy][x : x + size] = [color] * size

    blue = rgb555("4b78a8")
    pale = rgb555("a6b7c9")
    pixels[7][73:80] = [blue] * 7
    for line in range(5, 10):
        pixels[line][76] = blue
    pixels[7][75:78] = [pale] * 3
    for line in range(6, 9):
        pixels[line][76] = pale
    return pixels


def texture(region: str) -> bytes:
    """Bake the fitted regional rotation into a normal sprite, without filtering."""
    angle = math.atan(SLOPE[region])
    sine, cosine = math.sin(angle), math.cos(angle)
    source = unrotated()
    result = bytearray()
    for y in range(HEIGHT):
        for x in range(WIDTH):
            dx, dy = x + 0.5 - WIDTH / 2, y + 0.5 - HEIGHT / 2
            sx = math.floor(dx * cosine + dy * sine + SOURCE_WIDTH / 2)
            sy = math.floor(-dx * sine + dy * cosine + SOURCE_HEIGHT / 2)
            inside = 0 <= sx < SOURCE_WIDTH and 0 <= sy < SOURCE_HEIGHT
            color = source[sy][sx] if inside else 0
            result.extend(struct.pack(">H", color))
    return bytes(result)


def command(region: str, texture_offset: int) -> bytes:
    """One normal direct-color sprite command in native VDP1 byte order."""
    if texture_offset % 8:
        raise ValueError("VDP1 texture offset must be 8-byte aligned")
    # The 352x240 source capture begins at VDP1 x=16 and eight lines above y=0.
    x, y = 243 + 16, (124 if region == "us" else 121) - 8
    return struct.pack(
        ">16H",
        0,
        0,
        0x00A8,
        0,
        texture_offset // 8,
        (WIDTH // 8 << 8) | HEIGHT,
        x,
        y,
        *([0] * 8),
    )
