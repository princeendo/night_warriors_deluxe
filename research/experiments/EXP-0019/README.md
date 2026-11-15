# EXP-0019: Every Character's Ending on the Patched US Image

Task: END-001 (the per-character epilogue screens), on the DISC-002 image
Status: DONE
Confidence: CONFIRMED (forced endings; not played to the end per character)

## Observation

`EXP-0018` (D-017): the version 2 image (`build_epilogue.py`) shows Morrigan's
Japanese epilogue after her English ending. The patch loads one file,
`ST1JPN.BIN`, for every character, so the other 13 endings are expected to
work the same way. Each needs a won-KO state for that character, and only
Morrigan states exist.

## Hypothesis

The ending reads its character from a RAM byte set from the winner after the
KO. Writing that byte, with the stage byte (D-009), at Morrigan's won-KO state
plays character N's ending, and on version 2 shows character N's Japanese
epilogue.

## Finding the Byte (US image, unpatched)

The script reader at `0x060367BC` reads `@(5,r4)` with `r4 = 0x0609159C`
(`charlog`). A write log on `0x060915A1` shows it written at `0x060368F8`
with `r6 = 5` (Morrigan), from the routine `0x060368D6` called by
`0x0603686E` (`charwrite`), which passes `0x0608096E & 0xFF`. A write log on
`0x0608096E` shows it copied from `0x06080980` at `0x0601DC7A`, frame 432
after the state (`charwrite2`). `0x06080980` holds 5 at the state (player 1,
Morrigan); `0x06080981` holds the opponent. `--log-write RANGE` was added to
`EXP-0010/force.py` here for the last two runs.

```bash
F=research/experiments/EXP-0010/force.py
US=local/aud001/us-session/rec/states/f00011016.mcs
./invenv.sh python $F us $US local/disc002/charlog --write 0608092B=09 --log-pc 060367BC
./invenv.sh python $F us $US local/disc002/charwrite --write 0608092B=09 --log-write 060915A1-060915A1
./invenv.sh python $F us $US local/disc002/charwrite2 --write 0608092B=09 --log-write 0608096E-0608096E
```

(Each run halted after its first hit, at about frame 3,650.)

## Controlled Change

One byte, `0x06080980` = N (N = 1-14 but 5), written with the stage byte at
the same state. Version 2 and the unpatched image each get the same writes.

## Prediction

Version 2: character N's English main ending, then N's Japanese epilogue over
N's art, then the US cast roll. Unpatched: the same ending, the art with no
text.

## Inputs and Provenance

- Version 2: `build/us_enhanced_epilogue/…(USA).cue` (Track 1 `93ca264c…39ab`),
  state `local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs`
  (Morrigan's bonus screen, before any `ST1` load; `EXP-0018` step 9).
- Control: the untouched US image (Track 1 `d0960087…70da`), state
  `local/aud001/us-session/rec/states/f00011016.mcs` (Morrigan won-KO). A
  version 2 state cannot be the control: its RAM holds the patched `MAIN.BIN`.
- Patched Mednafen `7826b9b9…f887`, quiet home.

## Procedure

```bash
research/experiments/EXP-0019/all_endings.sh            # 26 runs, 420 steps each, ~8.5 min per pair
research/experiments/EXP-0019/sheet.sh local/disc002/end-v2-02 OUT.png   # every 7th shot, 10x6
```

Outputs: `local/disc002/end-v2-NN` and `end-us-NN` (ignored). Each sheet was
agent-reviewed; key frames were picked from the sheets and checked side by
side.

## Actual Result

Every run ran to the end: 420 screenshots; the cast roll, "Thank you for
playing", and Capcom screens.

| N | Ending (English main ending seen in both) | Version 2: epilogue key frame | Control: art without text |
| --- | --- | --- | --- |
| 1 | Demitri | `r004288` `bf10de01…` | `r004925` `6cd6470e…` |
| 2 | Jon Talbain (ガロン) | `r004285` `911160f7…` | `r004288` `b97456df…` |
| 3 | Victor | `r004288` `cd9174cf…` | `r004282` `7a7890bf…` |
| 4 | Lord Raptor (ザベル) | `r005356` `60e52855…` | `r006414` `caf6eac8…` |
| 6 | Anakaris | `r004713` `0d79e63c…` | `r005353` `365e424f…` |
| 7 | Felicia | `r004288` `c02fcd44…` | `r004504` `23425d8a…` |
| 8 | Bishamon | `r004922` `49478397…` | `r005553` `978b4d79…` |
| 9 | Rikuo | `r004297` `64065797…` | `r004495` `c5036dce…` |
| 10 | Sasquatch | `r004294` `82289216…` | `r004934` `eddf2bb6…` |
| 11 | Huitzil | `r004294` `81d9d530…` | `r004291` `424c4337…` |
| 12 | Pyron | `r004288` `4c90c2a6…` | `r004710` `48a5884d…` |
| 13 | Hsien-Ko (Lei-Lei) | `r006411` `ebf60c80…` | `r006205` `5e460440…` |
| 14 | Donovan | `r005347` `d884acd5…` | `r006202` `87718380…` |

In each version 2 run the English main ending is followed by a Japanese
paragraph over that character's art, then the cast roll with the US names
(JON TALBAIN, LORD RAPTOR, HSIEN-KO). In each control the same art scrolls
with no text. The control state is still on the win screen, which names the
forced character ("HSIEN-KO WINS" for 13): the win screen reads the same
byte, an independent check of the numbering.

The order is **not** the cast-roll order: 1 Demitri, 2 Jon Talbain,
3 Victor, 4 Lord Raptor, 5 Morrigan, 6 Anakaris, 7 Felicia, 8 Bishamon,
9 Rikuo, 10 Sasquatch, 11 Huitzil, 12 Pyron, 13 Hsien-Ko, 14 Donovan. An
earlier guess (11 Hsien-Ko, 13 Huitzil) was wrong.

## Conclusion

**CONFIRMED:** `0x06080980` (US) is player 1's character, 1-based in the
order above; written with the stage byte after a won KO, it plays that
character's ending (D-018). On the version 2 image all 14 characters' endings
show their Japanese epilogue after the English ending, with US cast names;
the unpatched image shows the art without text for all 14. The 15-byte patch
of D-017 covers every character.

## Uncertainty and Alternatives

- Forced, not played: the fight before each ending was Morrigan vs. Victor.
  An ending that branches on the opponent or the fight would not show it.
- Sampled every 7th screenshot (about every 210 frames); short screens may
  be missed, and the Japanese text was not compared line by line with the
  Japanese release's own epilogues (only Morrigan's was, `EXP-0010`).
- The Japanese address of the byte is not looked up (not needed for the US
  patch).
- The emblem card ("1ST A") shows in both runs; what the `0x0600CFCC` branch
  adds is still open.
