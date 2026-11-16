# EXP-0028: Cold-Boot Check of the English Epilogue Image

Task: END-002 (the last criterion: from a cold boot)
Status: DONE
Confidence: CONFIRMED

## Observation

`EXP-0027` fixed the blank win quote (`MAIN.BIN` untouched again) and tested
the fix only by forcing from version 2's state.

## Hypothesis

From a cold boot of the `EXP-0027` image, the win quote is English, and each
of the 14 endings shows its whole English epilogue, with no RAM write.

## Procedure

Image: `build/us_en_epilogue_all/` (Track 1 `8ebc0ca3…0b67`), from
`build_en_epilogue.py --late-array1 --step 0` for rosters 1-14.

1. With the user present: `research/experiments/EXP-0018/session.sh
   local/end002/cold-session2 "build/us_en_epilogue_all/…(USA).cue"`
   (142 states, 282 screenshots). The user played Demitri and won against
   Victor.
2. From that session's bonus-screen state `f00007427` (shots `f00007367`-
   `f00007454`; before any `ST1` load), every ending forced with the stage
   byte and the character byte only:

```bash
STATE=local/end002/cold-session2/rec/states/f00007427.mcs OUT=local/end002/cold \
  research/experiments/EXP-0026/all_en.sh
./invenv.sh python research/experiments/EXP-0026/pick_text_frame.py local/end002/cold-NN
```

(`all_en.sh` now takes `STATE` and `OUT` and no longer writes the `MAIN.BIN`
literal into RAM, which `EXP-0027` made unnecessary.)

## Actual Result

- Win screen (agent-reviewed): "Your blood is even weaker than you! I will
  not let it stain my lips!" in English.
- All 14 runs reach the cast roll (frames 10,031-10,053, halted in the
  normal loop). Each key frame (agent-reviewed, tiled) shows the whole
  English paragraph, first line to last, on top of the character's art:

| Roster | Key frame | Same as `EXP-0026` |
| --- | --- | --- |
| 1 Demitri | `r004130` `d99a063c…` | yes |
| 2 Jon Talbain | `r004040` `9de3ea4e…` | different frame |
| 3 Victor | `r004040` `91d106c0…` | different frame |
| 4 Lord Raptor | `r005320` `9b75d7f2…` | different frame |
| 5 Morrigan | `r006600` `cce5a693…` | yes |
| 6 Anakaris | `r004417` `3fdb7a20…` | yes (first `EXP-0026` run) |
| 7 Felicia | `r004040` `51eefb0a…` | different frame |
| 8 Bishamon | `r004590` `1a181554…` | yes (first `EXP-0026` run) |
| 9 Rikuo | `r004049` `6c398747…` | different frame |
| 10 Sasquatch | `r004040` `a0c1e1a4…` | yes |
| 11 Huitzil | `r004034` `a1dab294…` | different frame |
| 12 Pyron | `r004046` `164c8004…` | yes |
| 13 Hsien-Ko | `r006232` `d93b497c…` | different frame |
| 14 Donovan | `r005233` `5e6ab620…` | different frame |

"Different frame" means the picker chose another moment of the art scroll
(every third shot is sampled); the text in each is whole.

## Conclusion

**CONFIRMED:** the US Enhanced epilogue image works from a cold boot: the
English win quote is kept, and all 14 characters' endings show their whole
PSP *Chronicle* English epilogue (with the logged edits) on top of the art,
then the US cast roll (D-027). `END-002` is done: M5 for `END-01`.

## Uncertainty and Alternatives

- The endings were forced from a state after one won match, not reached by
  beating the whole arcade mode; the fights before the ending were Demitri
  vs. Victor.
- Main endings and their timing were not compared with the Japanese release
  (`END-003`).
- Hardware (a real Saturn) not tried.
