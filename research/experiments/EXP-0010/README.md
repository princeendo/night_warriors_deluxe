# EXP-0010: Force Morrigan's Ending in Both Releases

Task: END-001
Status: DONE (first character; text storage is the next experiment)
Confidence: CONFIRMED

## Observation

The user (2026-11-13): "Each character has a post-ending artwork accompanied
by scrolling Japanese text", reported missing from the US release (`END-01`).
The 14 `END*.BG` files and `ENDDATA.BIN` are identical on both discs;
`ENDING.O` differs. Reaching an ending by play takes a full arcade run.
`EXP-0007` holds states of both releases fighting Victor (stage 1) and then
Bishamon (stage 2).

## Hypothesis

A WRAM-H byte holds the stage number; setting it to the last stage just
after a won KO makes the game play the ending; the Japanese release then
shows the epilogue text over the art and the US release does not.

## Controlled Change

One byte written right after loading a state saved just after Morrigan's
winning KO: the stage number. No input. Each release forced the same way.

## Inputs and Provenance

- States from `EXP-0007`: Japanese `f00023129` (KO won, round 3 vs.
  Bishamon, stage 2), US `f00011016` (KO won, round 3 vs. Victor, stage 1).
- Patched Mednafen `7826b9b9…f887`, quiet home.

## Tools and Environment

[`force.py`](force.py): loads a state, pauses, writes bytes to WRAM-H, then
takes a screenshot every 30 frames (and keeps a state every 300 frames, plus
WAV with `--wav`). WRAM-H extracted from `EXP-0007` states with
`mcs_extract` (D-006).

## Procedure

1. **Stage byte.** WRAM-H of four stage-1 and four stage-2 states per
   release; bytes constant within each stage with stage 2 = stage 1 + 1.
   In upper work RAM, Japanese `0x0608097B` and US `0x0608092B` (0 → 1), at
   the same place in identical neighbourhoods `0x50` apart (the same `0x50`
   seen in many `ENDING.O` differences). `0x06080979` / `0x06080929` go
   `02` → `07` (opponent, HYPOTHESIS).
2. **Vitality** (for a forced KO; not used in the end). Values that only fall
   during the Japanese round 3 vs. Bishamon: `0x06077263`/`0x06077275` (144 →
   0 at the KO, Bishamon) and `0x06076CB7`-family (144 → 3, Morrigan).
   Attempt A: state `f00023071` (just before the KO), stage 9, `0x06077263` =
   `0x06077275` = 0: **Bishamon won** (the KO is checked when a hit lands; in
   the input-free replay Bishamon hit Morrigan, who had 3 left), then the
   continue countdown. Recorded as a dead end.
3. **Forced ending.**

```bash
./invenv.sh python research/experiments/EXP-0010/force.py jp \
  local/aud001/jp-session/rec/states/f00023129.mcs local/end001/jp-ko-n9 \
  --write 0608097B=09 --steps 100
./invenv.sh python research/experiments/EXP-0010/force.py jp \
  local/end001/jp-ko-n9/states/r003045.mc0 local/end001/jp-ko-n9-b --steps 240 --wav
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/aud001/us-session/rec/states/f00011016.mcs local/end001/us-ko-n9 \
  --write 0608092B=09 --steps 100
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/end001/us-ko-n9/states/r003036.mc0 local/end001/us-ko-n9-b --steps 240 --wav
```

## Actual Result

All runs exit 0. Agent-reviewed screenshots (one every 30 frames):

| Part | Japanese | US |
| --- | --- | --- |
| After the KO | win pose, bonus, then the ending (no further fight) | same |
| Main ending | framed scenes (Pyron, the castle, Morrigan's servant, Morrigan on roses) with Japanese dialogue boxes | the same scenes and timing with English dialogue |
| Card | a gold bat emblem with roses, `1ST A` | same |
| **Epilogue** | a paragraph of Japanese text (about ten lines, shown line by line), then Morrigan's full-length artwork scrolling up **behind the text** | **the same artwork scrolling up at the same time, with no text** |
| Credits | `NOW LOADING`, `CAST` roll: DEMITRI, GALLON, ... | `CAST` roll: DEMITRI, JON TALBAIN, VICTOR, HSIEN-KO, ... |

Full-size pair at the same point (frame 4,405 of the continuation):
Japanese `jp-ko-n9-b/shots/r004405.png` (`c8c9890c…`, text over the art), US
`us-ko-n9-b/shots/r004405.png` (`25bc3f8e…`, art only). Earlier, Japanese
`r003616` (`d13ac16b…`) shows the text alone; US `r003613` (`2a8f42ea…`)
shows the art beginning to scroll in. The epilogue's content agrees with the
web research's summary for Morrigan (her father's death makes her head of the
family); no game text is committed.

## Conclusion

**CONFIRMED (Morrigan):** writing the stage byte to 9 just after a won KO
plays the ending (D-009). In the Japanese release Morrigan's ending is
followed by an epilogue paragraph over her scrolling artwork; the US release
scrolls the same artwork at the same time with no text (D-010, `END-01`:
**omitted** text, art kept). The cast roll uses each release's names
(`NAM-02`: GALLON / JON TALBAIN).

## Uncertainty and Alternatives

- One character. The other 13 endings are reachable the same way (a won KO
  state for that character is needed; the `EXP-0007` states are Morrigan's).
- Whether the US disc still holds the epilogue text (as data the code skips)
  is **UNKNOWN**; the next experiment finds where the Japanese text comes
  from (RAM at the epilogue, then its file) and looks for it on the US disc.
- Stage 9 was the first value tried; that 9 is the last stage is SUPPORTED
  (Pyron appears in the ending), not traced.

## Reproduction

The commands above, from the repository root. Screenshots and checkpoint
states stay in the ignored `local/end001/`.
