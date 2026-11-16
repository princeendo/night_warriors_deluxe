# EXP-0029: Main Endings — Forcing in Japanese, and the Two Regions' Scripts

Task: END-003 (criteria 1-2, and the script part of 3)
Status: DONE (this part); the per-page content comparison continues
Confidence: CONFIRMED (Japanese forcing, scripts); SUPPORTED (Pyron's meaning)

## 1. Forcing a Japanese Ending

Hypothesis: the Japanese ending-character byte is the US `0x06080980` +
`0x50` (`0x060809D0`), as for the region flag, language and stage bytes.

- WRAM-H at the Japanese won-KO state `local/aud001/jp-session/rec/states/f00023129.mcs`
  (`mcs_extract`, D-006): `0x060809D0` = `05` (Morrigan); the US state
  `f00011016` has `05` at `0x06080980`.
- `research/experiments/EXP-0029/jp_endings.sh` forces each character
  (`0608097B` = 9, `060809D0` = N, 420 steps; `local/end003/jp-NN`). All 14
  runs reach the cast roll (frames 12,764-12,789). Pyron's run
  (agent-reviewed) shows Pyron's ending and epilogue and the Japanese cast
  names (GALLON, LEI-LEI, ZABEL, AULBATH, PHOBOS).

**CONFIRMED:** `0x060809D0` is the Japanese ending character (roster order,
D-018). The US counterparts are `EXP-0019`'s unpatched controls
(`local/disc002/end-us-NN`), forced the same way; both releases' 14 endings
are now captured (criterion 2), from different won-KO states (Japanese:
Morrigan vs. Bishamon; US: Morrigan vs. Victor).

## 2. The Ending Scripts

`MAIN.BIN` (US; the same code reads either table by the region flag at
`0x060367A4`) holds two tables of 14 script pointers: Japanese `0x0605B1C0`,
US `0x0605B730`. A script is an initial wait, then six-word groups (page id,
mode, frames shown, page id | `0x8000`, mode, wait), the group with wait 0
being last. `research/experiments/EXP-0029/scripts.py` decodes all 28:

| Roster | JP pages | US pages | Ids only in JP | Ids only in US |
| --- | --- | --- | --- | --- |
| 1 Demitri | 8 | 8 | — | — |
| 2 Jon Talbain | 6 | 4 | `1C 1D` | — |
| 3 Victor | 6 | 6 | — | — |
| 4 Lord Raptor | 8 | 9 | — | `A0` |
| 5 Morrigan | 11 | 9 | `B1 B2` | — |
| 6 Anakaris | 10 | 12 | — | `C2 C3` |
| 7 Felicia | 6 | 7 | — | `46` |
| 8 Bishamon | 7 | 8 | — | `4F` |
| 9 Rikuo | 8 | 9 | — | `F0` |
| 10 Sasquatch | 8 | 11 | — | `100 101 102` |
| 11 Huitzil | 5 | 6 | — | `65` |
| 12 Pyron | 6 | 3 | `0B 0C 0D` | — |
| 13 Hsien-Ko | 12 (`D0`-`DB`) | 9 (`00`-`08`) | all | all |
| 14 Donovan | 11 (`F0`-`FA`) | 8 (`E0`-`E7`) | all | all |

The mode is 2 or 3 in every Japanese group and 0 in every US one. The US
pages are shown longer almost everywhere (e.g. Morrigan's `34`: 300 frames
Japanese, 540 US).

## 3. Where the Text Lives

- `ST2USA.BIN` (US; slot `0x1BD`) and `ST2JPN.BIN` (both discs, identical;
  slot `0x1BB`) have the `ST1` layout: a self-relative table at `0x0C`
  (`ST2USA` 301 entries, 7 null, 138 distinct records; `ST2JPN` 272
  entries, 113 distinct records, its first 16 entries all one placeholder).
- `ST2USA` records are of two kinds: line records in the win-quote Latin
  codes (D-021; e.g. entry `0x30`, Morrigan's first line, entry `0x10`,
  Demitri's), and, at entries 0-8 and `0xD0`/`0xE0` (end of file), plain
  ASCII after a 16-bit code (Hsien-Ko's, Pyron's, Donovan's). `EXP-0011`'s
  "ASCII with `/` breaks" described only the second kind.
- A page id is not the table index for every character (Demitri's ids
  `00`-`07`, his text at entry `0x10`), and the main-ending text is not read
  by the epilogue's builder (`--log-pc 060379BC` over US Demitri's ending: 0
  hits). During that ending, Demitri's record is in RAM at `0x060C51BA` but
  the rest of the file is not, so records seem to be copied out. The
  mapping is UNKNOWN.

## 4. Pyron (`END-03`)

The Japanese closing line (`jp-12` `r001792` `7a882ca7…`) has Pyron take the
planet into his collection, to shine forever in its beauty; the US one
(`end-us-12` `r001609` `f1c45a38…`) has him consume its life force and leave
a cinder. The Japanese script has three more pages (`0B`-`0D`) and the US
three fewer. SUPPORTED (a reading by meaning, as the web research reported).

## Conclusion

**CONFIRMED:** the Japanese and US main endings run from different scripts:
page counts differ for 12 of 14 characters (only Demitri and Victor have the
same pages), the Japanese has pages the US lacks for Jon Talbain, Morrigan
and Pyron, the US has extra pages for eight characters, and Hsien-Ko's and
Donovan's use entirely different pages; nearly every US page is shown
longer (D-028). What each page says, and whether an extra page is new
content or longer English split in two, is the next step.

## Uncertainty and Alternatives

- The comparison by page id assumes an id names the same scene in both
  regions; true for Morrigan's first page, not shown in general.
- A text-band extractor over the screenshots (tried here) missed most pages
  (text heights vary; short pages are not stable for two shots) and was
  dropped.
- Per-page content needs either the id-to-record mapping or reading the
  text records directly (`ST2USA` decodes to text; `ST2JPN` can be drawn
  from `MOJI.CHR`).
