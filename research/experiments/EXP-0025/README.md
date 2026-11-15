# EXP-0025: Drawing Array 1 Again After the Art (Room for All 14)

Task: END-002 (criteria 2-3: Morrigan, then a second character)
Status: DONE
Confidence: CONFIRMED (forced from a state; cold boot not yet run)

## Observation

`EXP-0024`: on-top room is 302 characters, because sprite array 1 is drawn
before the art. A PC log during the epilogue (`--log-pc 0601899C --log-pc
060189C2 --log-pc 060188D4`, `local/end002/stubs2`, frames 6,500 and 6,800)
shows the order every frame: array 1 through `0x06020282` (the general
per-frame routine, reached through `ENDING.O`'s `r13` = `0x06043ECC`), then
arrays 2 and 3 through `ENDING.O`'s `r12` = `0x06020766` (return address in
`ENDING.O`, `0x0600D01C` in the text intro, `0x0600D0E4` in the art phase).

## Hypothesis

If, in the ending only, array 1's slots are drawn once more after
`0x06020766` returns, text placed there shows on top of the art, giving the
list array 1 slot 17 to the end of array 3: 431 slots (413 after the 18
player slots).

## Controlled Change

Three additions to the `EXP-0024` build (`build_en_epilogue.py
--late-array1`):

| File | Offset | Original → modified | Address | Purpose |
| --- | --- | --- | --- | --- |
| `MAIN.BIN` | `0x25A98` | `060839D4` → `060833CC` | `0x06037A98` | glyph list starts at array 1 slot 17 (the first slot the epilogue clears) |
| `ST1JPN.BIN` | after the records, 4-aligned | JP win-quote data → 36-byte routine | `0x060CB408` + offset | `sts.l pr`; `jsr 0x06020766`; `jsr 0x060188D4` with `r4` = `0x060833CC`, `r5` = 111; `lds.l pr`; `rts` |
| `ENDING.O` | `0xC0B0` | `06020766` → `2…` (routine, cache-through) | `0x0600D0B0` | `r12` literal: the ending calls the routine each frame |

The routine runs from the `ST1JPN.BIN` image in RAM (loaded at `0x060CB408`
before `r12` is set), through the cache-through mirror so no stale
instruction cache line can be used. The filler line now covers list entries
175-192. Forced tests write the `MAIN.BIN` literal in RAM too (`EXP-0024`).

## Procedure

```bash
B=research/experiments/EXP-0023/build_en_epilogue.py
F=research/experiments/EXP-0010/force.py
S=local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs
C="build/us_en_epilogue_late/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python $B --late-array1 --out build/us_en_epilogue_late 5
./invenv.sh python $F us $S local/end002/en-morrigan-late --image "$C" \
  --write 0608092B=09 --write 06037A98=060833CC --steps 330
./invenv.sh python $B --late-array1 --step 12 --out build/us_en_epilogue_late 6
./invenv.sh python $F us $S local/end002/en-anakaris-late --image "$C" \
  --write 0608092B=09 --write 06080980=06 --write 06037A98=060833CC --steps 330
```

## Actual Result

| Run | Characters / lines | Result |
| --- | --- | --- |
| Morrigan (`en-morrigan-late`) | 278 / 16 at 13 px | the whole paragraph on top of the art (`r007646`), the same picture as `EXP-0024`; the run continues through the cast roll |
| Anakaris (`en-anakaris-late`, Track 1 `42f17862…d88b`) | 345 / 18 at 12 px | the whole paragraph, including "5,000", on top of his art (`r005685` `803f714d…`); the last line, "desert sands.", on screen; logged edit "exaulted" → "exalted" applied; the run continues through the cast roll |

The disassembly of the routine bytes matches the listing above; the
`--move-list` build still reproduces `EXP-0024`'s Track 1 (`6ec651e6…`).

## Conclusion

**CONFIRMED:** redrawing array 1 slots 17-127 after `0x06020766`, from a
routine in the loaded `ST1JPN.BIN` reached through `ENDING.O`'s `r12`, puts
them on top of the art; with the list starting at array 1 slot 17 there is
room for 413 characters, more than the longest English epilogue (345), in up
to 18 lines at 12-pixel spacing (D-024). Nothing changes outside the ending
except one `MAIN.BIN` literal used only by the epilogue builder.

## Uncertainty and Alternatives

- Not yet from a cold boot of a built image (to run with the user).
- Array 1 slots 17-127 are drawn twice in the ending (once under the art,
  once on top); no visible effect, but VDP1 draws up to 111 more sprites a
  frame.
- The routine lives in `ST1JPN.BIN`'s RAM image; nothing overwrote it before
  the cast roll in these runs, but later reloads of that area while `r12`
  still points there were not traced beyond the cast roll.
- 12-pixel spacing is tight (descenders touch the next line); a per-character
  choice (13 where 16 lines or fewer) is open.
- The `ST1JPN.BIN` English layout serves the US Enhanced build only; the
  Japanese editions need the file intact (`EDITION-001`).
