# EXP-0035: How the 52 Differing Files Differ (DIFF-001)

Task: DIFF-001 (input to `EDITION-001`)
Status: DONE
Confidence: CONFIRMED (static, reproducible); what each content change does
is UNKNOWN unless a cited experiment says so

## Observation

`references/saturn_us/README.md`: 52 files differ between the Japanese 1M
and US data tracks. `EDITION-001` needs to know how, to price each way of
putting both releases on one disc.

## Method

`tools/disc/diff_files.py` (unit test `tests/unit/test_diff_files.py`)
aligns the two versions on 32-bit words (as is when the sizes match,
`difflib` when not) and classifies each differing word pair: **pointer**
(both words point into WRAM-L or WRAM-H; the delta is counted) or
**content**; inserted and deleted words are counted. Code is identified by
decoding the first instructions (`0.BIN`, `MAIN.BIN` start with code) and,
for files that start with a (slot, offset) table ended by `FFFFFFFF` (the
`ST` file format, D-021), by how many entries point at a function prologue.

```bash
./invenv.sh python -m tools.disc.diff_files local/extracted/saturn_jp local/extracted/saturn_us \
  --json research/experiments/EXP-0035/diff_jp_us.json > research/experiments/EXP-0035/summary.txt
./invenv.sh python -m tools.disc.diff_files local/extracted/saturn_us/PL10.O local/extracted/saturn_us/PL10.O2
```

`diff_jp_us.json` holds, per file, sizes, SHA-256s, every run (offsets and
word counts), pointer deltas and counts: no file bytes. Run time about 2.5
min (`difflib` on `MAIN.BIN`, `0.BIN`, `P03_.SPR`).

## Result

| Group | Files | JP bytes (sectors) | What differs |
| --- | --- | --- | --- |
| Boot and main program | `0.BIN`, `MAIN.BIN`, `TITLE.O` | 680,932 (334) | code: 6,688 content words, 20,655 words inserted or deleted, plus pointers |
| Overlays | `PL01`-`PL14` `.O`/`.O2`, `SOBJ01`-`SOBJ12.O3`, `ENDING.O` | 756,944 (385) | almost only pointers: 1,307 content words over 41 files |
| Data | `P00.BIN`, `P03_.BIN`, `P03_.SPR` | 701,052 (344) | content only (no pointers); `P03_.SPR` +288 bytes |
| Text | `ST1USA.BIN`, `ST2USA.BIN` | 22,705 (12) | content (D-021, `EXP-0030`) |
| ISO notes | `VH_ABS/BIB/CPY.TXT` | 530 | emptied in US |
| **All** | 52 | **2,161,633 (1,075)** | |

1. **The overlays are code relinked, not rewritten.** Every overlay starts
   with an entry table whose entries mostly point at SH-2 prologues
   (`PL10.O`: 37 entries, 28 at a `push`/`sts.l pr`; `ENDING.O` 52, 49).
   Their differing words are almost all pointers with a few repeated
   deltas (JP → US): `-0x50` (the variables block, as the flag `0x060808EA`
   → `0x0608089A`) and `-0x858`, `-0x86C`, `-0x8C4` (routines in the main
   program, whose JP load base is `0x06013A00` and US `0x06012000`,
   `EXP-0015`). Content words: 0-40 per file (`PL10` 40, `PL14` 29), more in
   `PL08` (400, and 60 bytes shorter) and `PL09` (107, 16 longer). So an
   overlay works only with its own region's `MAIN.BIN`.
2. **`PL*.O` vs `PL*.O2` (open since `SESSION-0001`): the same code linked
   for the other player slot.** In both regions, 13 of the 14 pairs differ
   only by pointers, all `+0x8000` (`0x06001000` → `0x06009000`); `PL10`
   adds one content word, `PL08` seven and six inserted words.
3. **The main program changed for real** (insertions and thousands of
   content words), as `EXP-0015`-`EXP-0017` found in part (the region-flag
   tables, the pause check, the title's Start test).
4. **`P00.BIN`, `P03_.BIN`, `P03_.SPR` are data** (their entry tables do
   not point at code; no pointer changes). What they hold is UNKNOWN.

## Conclusion

A region's code is one linked set: `0.BIN`, `MAIN.BIN`, `TITLE.O` and the
41 overlays must come from the same region. Byte-identical originals for
both regions on one disc mean carrying both sets (1,063 sectors for the
Japanese copy of the 49 code and data files, beyond the 150 free).

## Uncertainty

- A "pointer" is any word into work RAM; a constant that happens to fall
  there is miscounted (rare: the deltas cluster on four values).
- `difflib` alignment of the size-changed files is one valid alignment, not
  necessarily the editor's.
