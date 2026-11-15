# EXP-0021: What the `ENDING.O` Branch at `0x0600CFCC` Adds

Task: END-001 (leftovers listed after `EXP-0018`)
Status: DONE
Confidence: CONFIRMED

## Observation

The DISC-002 version 2 patch turns the region-flag branch at `0x0600CFCC`
(US `ENDING.O`, file offset `0xBFCC`) into a `nop`, so the flag-0 path runs.
`EXP-0018` called it "the card sequence" but saw the emblem card in the
control too, so what the path adds was not isolated.

## Static Reading (US `ENDING.O`, loaded at `0x06001000`)

`tools/sh2/disasm.py --base 0x06001000 --start 0x0600CFA0 --end 0x0600D040`:
with the flag (`0x0608089A`) non-zero, `bf 0x0600D02E` skips to code shared
by both paths, which sets `0x060916A0` = 16. With the flag 0, the path at
`0x0600CFCE` sets `0x060916A0` = `0xFF40` (−192) and `@r9` = `0xFE80`, calls
`0x06037D46` with `r4 = 0x3C00` and `r5` = the ending character − 1
(`0x0608096E`), calls `0x06017244` and `0x06016F44` twice, then loops
`0x1A0` (416) times at `0x0600D008`: `@r9` + 1, `0x060916A0` = `@r9` / 2,
then the frame calls `0x06043ECC`, `0x06020766` and `0x06007BBC(1)`.

## Hypothesis

The flag-0 path is a 416-frame sequence shown between the emblem card and
the art scroll, one loop pass per frame; the US release skips it.

## Controlled Change

The image only (version 2 vs. unpatched), under the same forcing as
`EXP-0018` step 9, with PC logging at the path's first instruction, the loop
and the join.

## Prediction

Version 2: `0x0600CFCE` once, `0x0600D008` 416 times on consecutive frames,
then `0x0600D02E` once; the screens show something new in those frames.
Unpatched: only `0x0600D02E`.

## Procedure

```bash
F=research/experiments/EXP-0010/force.py
C="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
L="--log-pc 0600CFCE --log-pc 0600D008 --log-pc 0600D02E"
./invenv.sh python $F us local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs \
  local/end001/card-v2 --image "$C" --write 0608092B=09 ${=L} --steps 260
./invenv.sh python $F us local/aud001/us-session/rec/states/f00011016.mcs \
  local/end001/card-us --write 0608092B=09 ${=L} --steps 260
```

The Japanese reference is the `EXP-0010` run `local/end001/jp-ko-n9-b`.

## Actual Result

| Run | `0x0600CFCE` | `0x0600D008` | `0x0600D02E` | Screens after the card (agent-reviewed) |
| --- | --- | --- | --- | --- |
| Version 2 | 1 | 416, frames 6,140-6,555 | 1, frame 6,556 | black, then the Japanese paragraph rises onto the black screen (`r006184`-`r006549`); then the art scrolls in under it |
| Unpatched | 0 | 0 | 1, frame 6,470 | the art (Morrigan's wing) scrolls in straight after the card |
| Japanese release (`EXP-0010`) | — | — | — | card, black, the paragraph rises onto black, then the art scrolls in under it |

## Conclusion

**CONFIRMED:** the flag-0 path at `0x0600CFCE` is the epilogue's text
introduction: for 416 frames (about 6.9 seconds) the paragraph rises onto a
black screen before the art scroll starts, as in the Japanese release. The
US release skips it and starts the art straight after the card. The card
itself is common to both paths. The version 2 patch at `0x0600CFCC` is
needed for the Japanese presentation (D-020).

## The Glyph Strip (closed without an experiment)

`EXP-0012` saw a strip of filler glyphs across the top of the emblem card
when the region flag was cleared in US RAM. It is absent from both releases'
cards (`EXP-0010`) and from the version 2 build (`EXP-0018`, `EXP-0019`): it
is a by-product of clearing the flag in RAM, which the build does not do.
Its cause stays UNKNOWN; it is not pursued.

## Uncertainty and Alternatives

- What `0x06037D46`, `0x06017244` and `0x06016F44` each do (the per-character
  call is likely the text set-up) is not traced.
- Morrigan only; the loop count does not depend on the character in the
  code read here.
