# EXP-0026: All 14 English Epilogues in One Image

Task: END-002 (criterion 4, the roster)
Status: DONE
Confidence: CONFIRMED (forced from a state; cold boot not yet run)

## Observation

`EXP-0025`: with array 1 redrawn after the art, Morrigan's and Anakaris's
English epilogues showed whole, each from its own build.

## Hypothesis

One image holding all 14 English epilogues (`build_en_epilogue.py
--late-array1 --step 0`, spacing 13 px up to 16 lines, else 12 px) shows
each character's whole paragraph after the English ending.

## First Build: Three Crashes

Built with the routine address fixed at `0x060CB408` + offset (Track 1
`8e63dad2…`). Forced as in `EXP-0019` (`all_en.sh`): eleven endings ran to
the cast roll; Demitri, Rikuo and Pyron went black after the emblem card and
halted at `0x000000F2`-`F6`. Tests on Pyron:

| Run | Result |
| --- | --- |
| write log on the loaded file's area | only the file load itself (frames 1,060-1,063) writes there: nothing overwrites the routine (hypothesis DISPROVEN) |
| Pyron-only build, routine | crashes; so the all-14 layout is not the cause |
| Pyron-only build, array-2 layout (no routine) | runs to the cast roll |
| `--log-pc 060379BC`, array-2 build | the table is at `0x060C7C20`: Pyron's `ST1JPN.BIN` loads at `0x060C7C14`, Morrigan's at `0x060CB408` |

The loader (`0x06013D94`, mode 0) allocates from a heap, so the address
depends on the character's ending. For each header pair (slot, offset) it
stores base + offset at `0x06091758` + 4 × slot; slot `0x1BC` is at
`0x06091E48`.

## Fix

`r12` is computed when the epilogue starts, in the three instructions the
`EXP-0018` patch left unused (the flag read and test before the `nop` at
`0x0600CFCC`):

| File | Offset | Original → modified | Address | Purpose |
| --- | --- | --- | --- | --- |
| `ENDING.O` | `0xC0B0` | `06020766` → `06091E48` | `0x0600D0B0` | `r12` literal: the slot-`0x1BC` table pointer |
| `ENDING.O` | `0xBFC6` | `D33C 6030 2008` → `6CC2 D33B 3C3C` | `0x0600CFC6` | `mov.l @r12,r12`; `mov.l @(0x0600D0B8),r3`; `add r3,r12` |
| `ENDING.O` | `0xC0B8` | `0608089A` → `2000 0000` + (routine − `0x0C`) | `0x0600D0B8` | offset from the table to the routine, through the cache-through mirror |

The literal at `0x0600D0B8` is also read at `0x0600D04E`, into a test whose
branch the `EXP-0018` patch already made a `nop`; that read now touches the
BIOS ROM mirror, harmlessly. Disassembly of the built `ENDING.O` checked.

## Procedure

```bash
./invenv.sh python research/experiments/EXP-0023/build_en_epilogue.py \
  --late-array1 --step 0 --out build/us_en_epilogue_all 1 2 3 4 5 6 7 8 9 10 11 12 13 14
research/experiments/EXP-0026/all_en.sh          # 14 runs, 330 steps each
research/experiments/EXP-0019/sheet.sh local/end002/all-NN OUT.png 6
./invenv.sh python research/experiments/EXP-0026/pick_text_frame.py local/end002/all-NN
```

Build: Track 1 `21fb1c79681b67bf94ce81bca65b10b8f45004862a1054b8f707f49ae4019b87`.
The records end at `ST1JPN.BIN` `0x5368` (the file is `0x728C`).

## Actual Result

Every run ends in the cast roll (frames 10,032-10,053, halted in the normal
loop). Each contact sheet (agent-reviewed) shows: the English main ending,
the emblem card, the English epilogue rising on black, the art scrolling in
under it, NOW LOADING, the cast roll with US names. Key frames (the shot with
most text in each run's last 60 %), each showing the whole paragraph:

| Roster | Lines / px | Logged edits | Key frame |
| --- | --- | --- | --- |
| 1 Demitri | 17 / 12 | — | `r004133` `d99a063c…` |
| 2 Jon Talbain | 17 / 12 | — | `r004049` `b0ba4e3a…` |
| 3 Victor | 16 / 13 | — | `r004034` `74beb46d…` |
| 4 Lord Raptor | 16 / 13 | Rapter → Raptor | `r005320` `96be4bb6…` |
| 5 Morrigan | 16 / 13 | — | `r006588` `cce5a693…` |
| 6 Anakaris | 18 / 12 | exaulted → exalted | `r004408` `8b2c1bc0…` |
| 7 Felicia | 16 / 13 | — | `r004040` `443100d1…` |
| 8 Bishamon | 15 / 13 | "more a" → "more than a" | `r004593` `708ed96b…` |
| 9 Rikuo | 17 / 12 | kindom's → kingdom's | `r004046` `746d4067…` |
| 10 Sasquatch | 16 / 13 | — | `r004034` `a0c1e1a4…` |
| 11 Huitzil | 16 / 13 | — | `r004043` `e470ab87…` |
| 12 Pyron | 14 / 13 | — | `r004043` `164c8004…` |
| 13 Hsien-Ko | 17 / 12 | "new … speakig" → "knew … speaking"; "lie" → "lies" | `r006322` `8b0cf55c…` |
| 14 Donovan | 14 / 13 | — | `r005224` `632d217a…` |

## Conclusion

**CONFIRMED (forced):** one patched US image shows each of the 14 English
epilogues whole, on top of the character's art, after the English ending,
with the US cast roll (D-025). Every English line is the PSP *Chronicle*
text with only the logged edits (user decisions of 2026-11-15).

## Uncertainty and Alternatives

- Not yet from a cold boot of the built image, and not compared side by side
  with the Japanese epilogue's timing per character.
- Reviewed from contact sheets (every 6th shot) and one key frame each; the
  transcription itself still has had no second reading.
- "Le marta" (Raptor's) and other names the US Saturn lacks are as the PSP
  has them.
