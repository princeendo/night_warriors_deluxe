# EXP-0047: Identify the Saturn text containers and menu labels

Task: DIFF-002

Status: DONE

Confidence: CONFIRMED for the file identities, English-format quote record
comparison, ASCII locations, and previously observed renderer routes.
SUPPORTED for the purpose of the dormant Spanish files.

## Observation

The ending investigations identified ST1 and ST2 records as well as
`MOJI.CHR`/`MOJI.TBL`. The difference register still described the English
quote file as having unknown contents. The title and fight display also
use some text drawn as nameplates and graphics.

## Hypothesis and prediction

Ordinary text uses more than one storage format. A relative search for
visible UI labels should identify some inline strings in the program.
The ST containers should have the header slots and relative offsets
previously observed in memory.

## Controlled change

None. Scan and compare extracted files. Use the existing matched disc
captures and traces to distinguish displayed text from data present on disc.

## Inputs and procedure

- US T-1208H V1.001, Redump 5836, Track 1 `d0960087…70da`.
- Japanese T-1202G 1M V1.000, Redump 3677, Track 1 `73cc150b…4c39`.
- Python 3.13.13 and the existing glyph renderer evidence in D-011, D-015,
  D-021, D-028 and D-029. The script reports offsets, counts and hashes.
- Run `./invenv.sh python research/experiments/EXP-0047/text_scan.py` from
  the repository root with the two extracted trees, then compare the
  output to the result below. For each English label, the search tries every
  constant byte shift that keeps the entire pattern in the byte range.

## Actual result

| File | Loader slot | US bytes | Changed bytes | Evidenced content |
| --- | --- | ---: | ---: | --- |
| `ST1JPN.BIN` | `0x1BA` | 29,324 | 0 | 371 pointers, 340 distinct destinations. Epilogues at entries 0–13, Japanese quote records in the same table (D-011, EXP-0018). |
| `ST1USA.BIN` | `0x1BC` | 8,382 | 116 | 128 pointers, 57 distinct destinations. Retail US victory quotes plus an epilogue placeholder. |
| `ST1HIS.BIN` | `0x1BE` | 2,738 | 0 | 128 pointers, 15 distinct destinations. Spanish-format quote records, including accented characters encoded with control words. |
| `ST2JPN.BIN` | `0x1BB` | 8,100 | 0 | Japanese main endings, 272 pointers and 113 distinct destinations (EXP-0029). |
| `ST2USA.BIN` | `0x1BD` | 14,323 | 8,073 | English main endings, in both Latin glyph records and byte-level ASCII records (EXP-0029, EXP-0030). |
| `ST2HIS.BIN` | `0x1BF` | 12,572 | 0 | Spanish main-ending dialogue at corresponding ST2 entries, including Demitri and Victor. |

All 116 changed bytes in `ST1USA.BIN` are low bytes of line Y positions.
Against the Japanese disc's dormant copy, the US disc moves 57 lines up
four units, 49 up eight units, and 12 up twelve units. All 128 table offsets
and every parsed X, mode and glyph word match exactly. This compares the
English-format files. Each stock disc loads its own language's quote file.

The MOJI files are identical across both discs. D-011 identifies the
table's 1,026 codes and 16×16 font glyphs in RAM and on screen. The English
main endings and win quotes use the separate Latin codes in D-021.
D-015 traces the fight-name tiles and selects the nameplate and MODE SELECT
graphics by ID. The relative search does not find a byte string for
MODE SELECT in the four program files and six text files searched.

| Label | US file offsets at shift zero |
| --- | --- |
| CONFIGURATION | `MAIN.BIN:0x422F0`, `TITLE.O:0xBC4` |
| SOUND MODE | `TITLE.O:0xB78` |
| PRESS START TO EXIT | `MAIN.BIN:0x42354`, `TITLE.O:0xBF8` |
| NOW LOADING | `MAIN.BIN:0x409F0` |
| CONTINUE | `MAIN.BIN:0x42A68` |

No matches at a nonzero shift for these labels. The scan establishes the
storage of representative labels. The surface inventory tracks what each
release actually displays.

## Conclusion and uncertainty

The six ST files, the font pair, inline labels and regional name graphics
account for the identified text paths. The Spanish data is present on both
discs. Neither stock start-up path selects its language value, and no
stock menu path to Spanish has been observed. The different ST1 inventories
and runtime quote selection are tracked in QUO-001.
