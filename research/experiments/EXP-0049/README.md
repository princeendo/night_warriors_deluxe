# EXP-0049: Victory quote selection and US Enhanced translations

Task: QUO-001

Status: DONE

Confidence: CONFIRMED for both tables, the condition checks and the rendered
US Enhanced additions.

## Retail inventory and control

The title's JP and US language settings select different quote tables.
The US T-1208H V1.001 program starts choosing the winner's quote at
`0x0601DFE4`. The same routine is at `0x0601E850` on the Japanese
T-1202G V1.000 1M disc. Both programs contain both selector tables,
and their per-fighter record IDs match across discs for a given language.

| Branch | Code condition | JP word choices | US word choices |
| --- | --- | ---: | ---: |
| Mirror | Winner and opponent roster IDs match | 8 | 1 |
| High | Non-mirror, winner vitality field greater than 114 | 8 | 1 |
| Mid | Non-mirror, vitality field 31–114 | 8 | 1 |
| Low | Non-mirror, vitality field 30 or below | 8 | 1 |

The winner object is selected at `0x0601DFEE` in US and
`0x0601E85A` in JP. Both use fighter ID at object offset `0x3B7`
and the signed word at `0x3C0`. The mirror branch takes precedence.
The Japanese branch reads `RNG & 0x0E` as a byte offset within the
eight-word group. Duplicate IDs give some records more than one slot.
There are 323 unique selectable Japanese record destinations and 56
unique English destinations. The Japanese table pointers are at
`0x06054714` (US program) and `0x060547F4` (JP program). The English
pointers are at `0x060547BC` and `0x0605489C` respectively. This counts
records by destination, rather than comparing text for semantic duplicates.

`quote_inventory.py` compares all 14 tables for each language and writes
record IDs and file offsets, with no source dialogue in the output.
The stock images were both cold-booted through an Arcade loss, a continue,
a rematch with Victor, and the next fight against Bishamon. From each
reference's own saved round, only the winner's vitality field and, for the
mirror case, the opponent ID were forced before selection. The five
observations from each version were:

| Case, fighter 13 (Hsien-Ko / Lei-Lei) | US record | JP record |
| --- | --- | --- |
| Low, 30 | `0x072` | `0x131` |
| Mid, 31 | `0x071` | `0x130` |
| Mid, 114 | `0x071` | `0x130` |
| High, 115 | `0x070` | `0x133` |
| Mirror, 115 | `0x073` | `0x138` |

The observations, screenshots and fresh-source identifiers are saved under
`local/exp0049/live-us` and `local/exp0049/live-jp`. The numerical ranges
are engine field values, with no conversion to displayed percentages.

## US Enhanced

The user selected "Add translated Japanese variants to US Enhanced"
on 2026-11-27. One new translation from the Japanese Saturn record is
included for each character and each condition. The 56 source IDs and
new English lines are paired in `us_enhanced_quotes.py`. The Japanese
records were inspected from the game font and glyph codes, using local
renders for reading. Fixed language text follows its edition. The existing
official US record and new translation each occupy four of the eight
selector slots within their condition.

### Controlled changes and predictions

- US Enhanced changes the word at `0x0601E020` from `2008` (TST) to
  `0018` (SETT). This selects the stock eight-way branch with the
  actual English language byte unchanged. The renderer still loads the
  English table.
- The 896-byte JP selector bank in RAM at `0x06054394` is populated
  with the mixed English record IDs when E=0. Original SHA-256
  `f1f2404fe37ee4240064fd5b4ab1ca97ebdfddad998f89a997330ce1fe03d082`,
  replacement
  `8d45e15d1cf157d7533d9af224ff4291750880a2ee8f31816aecec509c47a0d2`.
  The title wrapper reverts both locations for E=1, E=2 and E=3.
- The expanded `ST1USA.BIN` grows from 8,382 to 15,038 bytes and keeps
  slot `0x1BC`. The table grows by 224 bytes at file offset `0x20C`.
  Each original pointer gains 224 so it refers to the same unchanged
  record. The new records use `0x80`–`0xB7`, with each offset derived by
  `english_file()`. The replacement SHA-256 is
  `593540d0b48fdd076013cbb3884bd218369a4bea6723aaad80bab4250de5e7b6`.
  US Original retains its original branch and record IDs. JP editions
  retain their stock Japanese file and selector bank.
- The new glyph records use the existing Latin encoding, with up to
  four lines of 24 glyphs and reflow at whole words. New records contain
  newly translated English from the cited Japanese donor IDs.

### Runtime check

`check_enhanced.py` boots the combined candidate and cycles all four
editions through OPTION MODE, checking that only the US Enhanced switch
applies the extra selector. It reaches a real Arcade match via pad input.
From that match's checkpoint, the same stock condition and renderer path
are exercised. The test sets the RNG seed at the stock random getter,
and validates the index received by the quote constructor. For the new
records it forces each roster and condition at the selector, restores the
fight's real roster IDs immediately afterward, and captures the rendered
English text on the same winner art. It also captures a stock line with
the initial roster and stock RNG choice.

The candidate builds from the untouched US Redump 5836 image. Track 1
SHA-256 `d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d`.
Mednafen 1.32.1 agent build (0001 and 0002), Python 3.13.13, isolated
quiet home. The stock-source run and the candidate probe are separate
cold boots.

The complete check selected and rendered all 56 translated records
`0x80`–`0xB7` plus a stock quote (`0x070`). All captions were visually
reviewed for missing glyphs and line clipping. The result metadata is
`local/exp0049/enhanced/quote-selection.json`, SHA-256
`02f9fa1ff5e7d4e5cb616a5ee9bb66ddb98dd2ccfc809371ec78eb1e4fb8c482`.
The 57 screenshots use the filename form fighter-condition-record.
The exact build also passed the names preference reboot and HUD
regression (`local/exp0049/combined-names`). The full Mode 1 sector
check reported 209,924 sectors and zero invalid sectors.

## Reproduction

```sh
./invenv.sh python research/experiments/EXP-0049/quote_inventory.py local/exp0049/quote-inventory.json
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/next_release_candidate
./invenv.sh python research/experiments/EXP-0049/check_enhanced.py \
  "build/next_release_candidate/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  local/exp0049/recheck --all
```

The separate retail runs and reviewed surface captures are described in
[EXP-0050](../EXP-0050/README.md).
