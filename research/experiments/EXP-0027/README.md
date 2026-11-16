# EXP-0027: The Blank Win Quote After a Cold Boot, and Its Fix

Task: END-002 (cold-boot check)
Status: DONE
Confidence: CONFIRMED (fix tested by forcing; the second cold boot is next)

## Observation

Cold boot of the `EXP-0026` image (Track 1 `21fb1c79…`) with the user
present (`EXP-0018/session.sh local/end002/cold-session CUE`, which now
takes the image as a second argument; 174 states, 343 screenshots). The user
won Demitri vs. Victor; the win screen showed Demitri's portrait with **no
quote** (the user: "The win quote was blank"; agent-reviewed screenshots
from `f00008395` on). Version 2 (`EXP-0018`) showed the English quote there.

## Hypothesis

The win screens build their quote with the same text builder, from the same
`MAIN.BIN` literal (`0x06037A98`) that `EXP-0025` changed on disc; their
glyphs now go to array 1 slots, which the win screen does not show.

## Change and Test 1: no `MAIN.BIN` patch; the routine swaps the literal

`MAIN.BIN` unpatched. The 56-byte routine set the literal to `0x060833CC`
before its call to `0x06020766` and restored `0x060839D4` after. Tested from
version 2's bonus-screen state (its RAM holds an unpatched `MAIN.BIN`, now
identical to the image's), Track 1 `feab7710…`:

| Run | Result |
| --- | --- |
| win screen (`--steps 40 --step-frames 15`) | English quote again: "By the abyss! You offer no challenge to me!" |
| Pyron, Anakaris, Morrigan endings | cut at 238 characters ("…Unfortunate", "…Aensl") |

So the hypothesis about the win quote holds, but the epilogue text is not
built inside `0x06020766`.

## Order of Events (PC log, `local/end002/order`)

`--log-pc 0600CFE2 --log-pc 0600D014 --log-pc 0600D018 --log-pc 060379E0`:
frame 6,140: the per-character set-up (`0x0600CFE2`), then `jsr @r13`, then
`jsr @r12` (the routine); frame 6,141: the builder's literal load
(`0x060379E0`, called from `0x06037CFE`), then the next `r13` and `r12`. The
builder runs once, between the routine's first and second calls.

## Change and Test 2: set on the first call, restore after

The routine (68 bytes, `LATE_ROUTINE` in `build_en_epilogue.py`) keeps a
flag word in its own data in the loaded `ST1JPN.BIN` (0 in the file, so
fresh in every ending). First call: flag = 1, literal = `0x060833CC`. Every
later call: literal = `0x060839D4`. Then, as before, `jsr 0x06020766` and the
late array-1 draw. Disassembly checked. Track 1
`8ebc0ca3d6eeb224f117ed3e4c584f3309f34819f18b38ac12c29553ec160b67`.

| Run | Result |
| --- | --- |
| win screen (`fix-winquote`) | English quote (`r000460` `adb72551…`) |
| Pyron (`fix-end-12`) | whole paragraph (`r004040` `164c8004…`, the same frame as `EXP-0026`), cast roll |
| Anakaris (`fix-end-06`) | whole 345 characters (`r004402` `e9c43d9d…`), cast roll |
| Morrigan (`fix-end-05`) | whole paragraph (`r006603` `cce5a693…`, the same frame as `EXP-0026`), cast roll |
| WRAM-H at the run's last state (`r010036`) | literal `0x06037A98` = `0x060839D4` again |

## Conclusion

**CONFIRMED:** the `EXP-0025` change to `MAIN.BIN` blanked the win quotes,
because they share the epilogue's text builder and literal. With `MAIN.BIN`
untouched and the literal set by the ending-only routine just for the one
epilogue build, the win quote is English and the epilogues are whole
(D-026). Every image change is now in files loaded for the ending
(`ENDING.O`, `ST1JPN.BIN`) plus the `EXP-0018` `MAIN.BIN` bytes.

## Uncertainty and Alternatives

- If an ending ended after the routine's first call but before its second,
  the literal would stay changed until the next ending; no way to skip there
  was seen (the text-intro loop reads no input), not tested.
- Not yet from a second cold boot.
- Lesson: `EXP-0024`/`EXP-0025` tested only the ending; any change to a file
  loaded at boot needs the other screens that use the same code checked
  (here the win screen).
