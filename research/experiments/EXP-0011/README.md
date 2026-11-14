# EXP-0011: Where the Epilogue Text Comes From, and Whether the US Disc Has It

Task: END-001
Status: DONE
Confidence: CONFIRMED

## Observation

`EXP-0010` (D-010): Morrigan's epilogue paragraph shows in the Japanese
release only; the US release scrolls the same art without text. No plain
Shift-JIS exists on either disc. The checkpoint states of `EXP-0010` cover
the epilogue in both releases (Japanese `r003646`, text on screen; US
`r003643`, the same moment, no text; Japanese `r003039` and US `r003036`,
before the epilogue).

## Hypothesis

The epilogue text is stored on disc in the game's own character codes, read
into RAM at the ending in the Japanese release only, and the same file is on
the US disc.

## Controlled Change

None. Static search of the extracted files and of memory extracted from the
`EXP-0010` states (`mcs_extract`, D-006).

## Procedure and Result

1. **Shift-JIS search** of every extracted file on both discs for
   "モリガン", "眠り" and "お嬢様": **no hits**. The text is not stored as
   Shift-JIS.
2. **The font.** `MOJI.CHR` (131,328 bytes = 1,026 glyphs x 128 bytes,
   16x16 at 4 bits per pixel; SHA-256 `eedcafb7…`) and `MOJI.TBL` (1,026
   four-byte entries: a 16-bit character code and `0x0210`; `f4922be7…`) are
   identical on both discs. At every checkpoint, both releases have
   `MOJI.TBL` in WRAM-H at `0x060F73A0` and `MOJI.CHR` in VDP1 VRAM at
   `0x24B98` (64 of 65 probes at that base): the US release loads the
   Japanese font too.
3. **What is drawn.** `tools/memory/vdp1_sprites.py` on the Japanese
   epilogue frame lists 231 sprites, **213** of them 16x16 glyphs from the
   font, in rows of up to 26 (y = 116, 132, ... 292); the US frame lists 79
   sprites and **no** font glyphs. Glyph number = (source − `0x24B98`) / 128;
   its character code is `MOJI.TBL`'s entry.
4. **Source of the text.** The first row's first eight characters as
   big-endian 16-bit `MOJI.TBL` codes (`054F 0172 034A 0191 034A 0188 0170
   056D`) occur once in Japanese WRAM-H, at `0x060CAA20`, and once on each
   disc: **`ST1JPN.BIN` offset `0xE20`**. Glyph numbers and little-endian
   forms occur nowhere.
5. **Which files each release loads** (whole-file matches in WRAM-H, before
   and during the epilogue):

| File | Japanese | US |
| --- | --- | --- |
| `ST1JPN.BIN` (29,324 bytes; identical on both discs, `33a32060…`) | at `0x060C9C00` | **not loaded** |
| `ST2JPN.BIN` | at `0x060C7C5C` | not loaded |
| `ST2USA.BIN` (English main-ending dialogue, ASCII, `/` line breaks) | not loaded | at `0x060C7C14` |
| `ST1USA.BIN`, `ST1HIS.BIN`, `ST2HIS.BIN` | not loaded | not loaded |

## Conclusion

**CONFIRMED:** the Japanese epilogue text is in `ST1JPN.BIN`, as 16-bit
`MOJI.TBL` character codes, drawn as VDP1 sprites from the `MOJI.CHR` font.
`ST1JPN.BIN`, the font and its table are byte-identical on the US disc, and
the US release even loads the font; at the ending it loads `ST2USA.BIN`
(its English main-ending text) and no `ST1` file, so no epilogue text is
drawn. The asset is present; the epilogue is **conditionally suppressed**,
not removed (D-011). `ST2JPN` / `ST2USA` are the main-ending dialogue in each
language (SUPPORTED: `ST2USA.BIN` is English ending dialogue; `ST2JPN.BIN`
is loaded during the Japanese ending).

## Uncertainty and Alternatives

- Only Morrigan's paragraph was traced. `ST1JPN.BIN` has a table of offsets
  (from `0x0C`, first target `0x5CC`) to many records; that it holds all 14
  epilogues is HYPOTHESIS until each ending is forced.
- `ST1USA.BIN` (8,382 bytes, not English text: short records of 16-bit
  values such as `000A 00B6 0001 00C1 ... FFFF`) and `ST1HIS.BIN` share
  `ST1JPN.BIN`'s header shape; their purpose, and why the US copy of
  `ST1USA.BIN` differs from the Japanese copy in 116 bytes, are **UNKNOWN**.
- Which code chooses `ST1JPN`/`ST2JPN` or `ST2USA` is **UNKNOWN**; it is what
  a US Enhanced build must change, along with an English text for the
  epilogue (`GATE-TRANSLATION`).

## Reproduction

```bash
for s in jp:local/end001/jp-ko-n9-b/states/r003646.mc0 us:local/end001/us-ko-n9-b/states/r003643.mc0; do
  ./invenv.sh python -m tools.memory.mcs_extract "${s#*:}" --region wram_h --region wram_l \
    --region vdp1_vram --region vdp2_vram --out-dir research/memory_dumps/end001/epi-${s%%:*}
done
```

Then the searches above (Python, in the experiment log). States from
`EXP-0010`; all evidence in ignored paths.
