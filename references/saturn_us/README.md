# Night Warriors Saturn US: Source Image

The US release, *Night Warriors: Darkstalkers' Revenge* (Capcom, 1996,
T-1208H). Permitted provenance and factual metadata only; never commit the
image or anything extracted from it. Which release is the modification base
is a user decision (`DOC-002`).

## Local Source Image (`ENV-006`, 2026-11-13)

The user supplied a Redump-style 7z in `~/Downloads/vh_nw_saturn/`
(`Night Warriors - Darkstalkers' Revenge (USA).7z`, SHA-256
`b7ddc8a916526e3aba5f14378935cc925154451698a2b9d94e02a1e13324126b`). It was
extracted unchanged with macOS `tar -xf` (libarchive) into the ignored,
previously empty folder `local/disc_images/nw_saturn_us/`. Treat these files
as immutable.

Release description: `Night Warriors: Darkstalkers' Revenge (USA), Sega Saturn
T-1208H V1.001 19960228; Redump disc 5836 (http://redump.org/disc/5836/)`.

**Database match: CONFIRMED (`ENV-007`, 2026-11-25).** Both tracks match Redump
disc `5836` (`Night Warriors: Darkstalkers' Revenge`, USA, `T-1208H`, V1.001,
1996-02-28, ring codes `SATURNT1208H P2H` / `P3H`, volume label
`VAMPIRE_HUNTER`) across size, CRC-32, MD5, and SHA-1. Redump also catalogs one
European PAL release (disc `4675`, `T-7009H-50`, V1.001).

| Filename | Size (bytes) | CRC-32 | MD5 | SHA-1 | SHA-256 |
| --- | ---: | --- | --- | --- | --- |
| `Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin` | 493741248 | `91921ea9` | `d284efa04e4bccd1a0f859feae7830e5` | `c1c01169d0e4d0acd7e4bfe768eae67c6b90fb1d` | `d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da` |
| `Night Warriors - Darkstalkers' Revenge (USA) (Track 2).bin` | 1766352 | `e75e991c` | `3b0c741e4fd1e326f4b3a69ecf401090` | `ac745b711b27c2488ee26410dadb7da29fd946d5` | `271844bfb734ab4fd322bc753bfad63b8a6e31d7d24272d52b5d10989065cdbb` |
| `Night Warriors - Darkstalkers' Revenge (USA).cue` | 281 | `eeefc0e2` | `a49df201359ee2a43cf5d1fd13d77d17` | `df0ebbe7119acd59298da7bc0559b85f788a71e1` | `203a53dff34c4adea6a709c822fa485d4325a4bd63aa6b0ea03f1ed7a141fbb2` |

RetroAchievements disc header MD5 (first 512 bytes of Track 1 sector 0 user
data): `8c7156c2e38f75a9ec54016427967e9e`.

Produced with `tools.disc.hash_source --json` (ignored
`local/logs/env006-hashes-nw_saturn_us.json`), agreeing with `shasum -a 256`.

## Observations (2026-11-13, static, no emulator)

- **Layout.** Track 1 `MODE1/2352`, 209,924 sectors (FAD 150-210,073), the
  same size as the Japanese track 1. Track 2 `AUDIO`, 751 sectors with a
  2-second pregap; **every byte is zero** (about 8 seconds of silence), where
  the Japanese track 2 holds about 18 seconds of sound.
- **System area.** `SEGA SEGASATURN`, maker `SEGA TP T-12`, product
  `T-1208H`, version `V1.001`, date `19960228` (one month after the Japanese
  `19960128`), `CD-1/1`, area `U`, peripherals `J`, title `NIGHT WARRIORS`.
- **ISO 9660.** Clean (`--check`: 0 bad sync, 0 non-Mode-1, 0 address
  mismatches). Volume ID `VAMPIRE_HUNTER` (unchanged from Japan); root at LSN
  20, 20,480 bytes; 415 files, no subdirectories; volume space 210,674 blocks
  = track 1 plus track 2. Extracted to the ignored `local/extracted/saturn_us/`.
  `iso_listing.json` holds name, LSN, size and SHA-256 of each file.

## JP/US File Comparison (2026-11-13, static)

From the two `iso_listing.json` files and a byte comparison of the extracted
files. Plain observation; what any difference *does* is **UNKNOWN**.

- **Same file set.** Both discs have the same 415 names; no file is
  region-only. File names use the Japanese character names on both discs
  (`AULBATH.BIN`, `GALLON.BIN`, `LEILEI.BIN`, `PHOBOS.BIN`, `ZABEL.BIN`).
- **363 files are byte-identical**, including every sound file
  (`SOUND.HED`, `SOUND.MP`, `SOUND.TBL`, `SDDRVS*.TSK`, all 30 `*.SEQ`), the
  per-character `*.BIN` files, all `END*.BG` ending backgrounds, and
  `ST1JPN.BIN`, `ST2JPN.BIN`, `ST1HIS.BIN`, `ST2HIS.BIN`. **HYPOTHESIS**: the
  Japanese-only voice samples reported by the web research (AUD-01 to AUD-03)
  are present on the US disc and are not selected, rather than absent.
- **52 files differ.** The three ISO abstract/bibliography/copyright files
  (`VH_ABS.TXT`, `VH_BIB.TXT`, `VH_CPY.TXT`) are empty on the US disc, which
  moves the 44 files that start before JP LSN 3,238 back by up to three
  sectors; every later file keeps its LSN.

| Files | JP size → US size | Bytes that differ |
| --- | --- | --- |
| `0.BIN` | 279,124 → 279,580 (+456) | size differs |
| `MAIN.BIN` | 368,048 → 374,544 (+6,496) | size differs |
| `TITLE.O` | 33,760 → 34,076 (+316) | size differs |
| `P03_.SPR` | 599,444 → 599,732 (+288) | size differs |
| `ENDING.O` | 64,080 (same) | 1,668 (`0x5506`-`0xFA4F`) |
| `P00.BIN` | 16,714 (same) | 1,179 |
| `P03_.BIN` | 84,894 (same) | 46 |
| `PL01.O`-`PL14.O` and `PL01.O2`-`PL14.O2` | same size except `PL08` (-60) and `PL09` (+16) | 291-659 each; a `.O` and its `.O2` are different files but differ between regions in the same number of bytes (at the same offsets, checked for `PL01` and `PL05`) |
| `SOBJ01.O3`-`SOBJ12.O3` | same | 55-215 each |
| `ST1USA.BIN` | 8,382 (same) | 116 |
| `ST2USA.BIN` | 14,323 (same) | 8,073 |
| `VH_ABS.TXT`, `VH_BIB.TXT`, `VH_CPY.TXT` | 431, 40, 59 → 0 | emptied |

- **Text.** A scan for runs of Shift-JIS kana found none in `0.BIN`,
  `MAIN.BIN`, `ENDING.O`, `TITLE.O`, `PL01.O`, `SOBJ01.O3` or `ST1USA.BIN`
  in either region, and English-looking ASCII runs occur equally in both
  regions' graphics files (noise). Where either region keeps its text, and in
  what encoding, is **UNKNOWN** (`DIFF-002`).
- The `ST?JPN`, `ST?USA` and `ST?HIS` files start with what look like offset
  tables; the names suggest per-region data present on both discs
  (**HYPOTHESIS**; `DIFF-002`).
