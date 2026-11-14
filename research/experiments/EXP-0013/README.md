# EXP-0013: Where the Epilogue Flag and Language Byte Are Set

Task: DISC-001
Status: DONE
Confidence: CONFIRMED (who writes the two bytes, from power-on to the end of
start-up); HYPOTHESIS (what else the flag controls)

## Observation

`EXP-0012` (D-012): the US release has the epilogue flag at 2 and the
language byte at 1 (Japanese release: 0 and 0) in every state examined, from
the first fight to the ending. Where they are set decides how a disc patch
(M2) or an edition switch (M7) sets them.

## Hypothesis

The US `MAIN.BIN` writes both bytes as constants once at start-up, and no
other code writes them; the Japanese release never writes them, so they
keep the 0 its start-up clear leaves.

## Controlled Change

None to the games. Static cross-reference of every program file on both
discs, then a write watch on each byte from power-on, with no input.

## Prediction

Statically, each US byte has exactly one store, in `MAIN.BIN` start-up code,
and the Japanese bytes have none. In the watch, after `MAIN.BIN` clears its
work area, the US bytes are written once each (2, 1) and the Japanese bytes
not at all.

## Inputs and Provenance

- `MAIN.BIN`: US `b4a3c192…16e8` (loaded at `0x06012000`), Japanese
  `08e042ad…5f21` (`0x06013A00`); every other extracted file of both discs
  (`local/extracted/`).
- Patched Mednafen `7826b9b9…f887`, quiet home, each release on its own BIOS
  (D-005), cold boot with no state loaded.

## Tools and Environment

- [`xref.py`](xref.py): lists each `mov.l @(disp,PC),Rn` whose literal is a
  given value, with the instructions around it (`tools/sh2/disasm.py`).
  Literals reached another way (GBR, a base register plus offset) are missed;
  the watch covers that gap for start-up.
- [`boot_watch.py`](boot_watch.py): boots a release, pauses at the agent's
  first answer (frame 1), arms write breakpoints in log mode, runs N frames,
  and keeps `events.log`, a screenshot and WRAM-H.

## Procedure

1. Search every extracted file of both discs for the four addresses as
   big-endian longs.
2. `xref.py` on both `MAIN.BIN` files and on every `*.O*` overlay (base 0,
   which keeps the literal alignment), checking the 12 instructions after each
   load for a store through the loaded register.
3. Boot watches, 1,800 frames each:

```bash
./invenv.sh python research/experiments/EXP-0013/boot_watch.py us local/disc001/us-boot1 \
  0608089A-0608089A 06080882-06080882 --frames 1800
./invenv.sh python research/experiments/EXP-0013/boot_watch.py jp local/disc001/jp-boot1 \
  060808EA-060808EA 060808D2-060808D2 --frames 1800
```

A first US run with 4-byte windows (`local/disc001/us-boot`) also caught a
settings copy at `0x06014746`/`0x060147AC` (frame 1628), which writes the
neighbours `0x06080881` and `0x06080898`, not the two bytes. The exact
one-byte runs above replaced it.

## Actual Result

**Static.** The only store to either byte in any file is in the US
`MAIN.BIN` start-up routine (`0x06012070`, called from `0x06013A0E` while
`0x0606D774` is 0):

```text
0601211A  mov   #2,r2
0601211C  mov.l @(..),r1   ; 0x0608089A  epilogue flag
0601211E  mov   #1,r4
...
06012128  mov.b r2,@r1     ; flag     = 2
0601212A  mov.l @(..),r3   ; 0x06080882  language
0601212C  mov.l @(..),r2   ; 0x060808A8
0601212E  mov.b r4,@r3     ; language = 1
06012130  mov.l @(..),r1   ; 0x06013BBA
06012132  jsr   @r1
06012134  mov.b r4,@r2     ; 0x060808A8 = 1 (delay slot, same register)
```

These are `MAIN.BIN` file offsets `0x11A` (`E202`) and `0x11E` (`E401`). The
Japanese `MAIN.BIN` has no such routine: its start-up (`0x06013A70`) writes
neither byte. All other loads of the four addresses (20 in the Japanese
`MAIN.BIN`, 21 in the US one; `ENDING.O`, `TITLE.O`, `SOBJ08.O3`, and
`PL05`, `PL10`, `PL14` `.O`/`.O2` in both) are followed by a read.

**Watch** (`events.log`: US `8844b7f7…8254`, Japanese `16ffed8d…8805`):

| PC (US / Japanese) | Frames | Hits | What it is |
| --- | --- | --- | --- |
| `000002B0` / `000002B0` | 9-554 | 4 / 4 | BIOS, before the game's program loads |
| `06012EA4`, `060136DA`, `06011930` / `06012E9C`, `060136BA`, `06011880` | 78-348 | 163 / 191 | a boot program that runs before `MAIN.BIN` is loaded over the same area |
| `0601200E` / `06013A0E` | 1466 / 1448 | 2 / 2 | `MAIN.BIN` clearing its work area (zero) |
| **`06012128`** / none | 1469 | 1 | US flag ← 2 |
| **`0601212E`** / none | 1469 | 1 | US language ← 1 |

At frame 1,800 (both on "NOW LOADING", screenshots identical, `4660da9f…`)
WRAM-H holds US flag 2, language 1, `0x060808A8` = 1; Japanese 0, 0, and 0 at
the matching `0x060808F8`.

## Conclusion

**CONFIRMED:** the US release sets the epilogue flag to 2 and the language
byte to 1 with two immediate constants in its `MAIN.BIN` start-up routine,
once, just after its work area is cleared; nothing else writes them. The
Japanese release never writes them, so they stay 0 (D-013). A disc patch of
`MAIN.BIN` offset `0x11B` (`02` → `00`) is therefore the candidate for
clearing the flag from boot (`DISC-002`). The language byte cannot be changed
there alone: the same register also sets `0x060808A8`, and D-012 shows that
Japanese language in the main ending gives a Japanese main ending.

## Uncertainty and Alternatives

- The watch ends at the start of the game proper (frame 1,800). Writes later
  (attract, menus, fights, ending) are excluded only by the static search,
  which cannot see a write through a computed address, and by the constant
  values in every `EXP-0007`/`EXP-0010` state.
- **The flag is read far beyond the ending** (HYPOTHESIS: it is a general
  export switch): `TITLE.O`, `SOBJ08.O3`, three character overlays (`PL05`,
  `PL10`, `PL14`) and MAIN code that also tests for the value 4. Clearing it
  from boot may change more than the epilogue; what each reader does is
  **UNKNOWN** (known unknowns).
- What `0x060808A8` (US only, 1) does is **UNKNOWN**; MAIN.BIN has no other
  load of it.

## Reproduction

The `boot_watch.py` commands above, then group `events.log` by `PC=`.
Static: `./invenv.sh python research/experiments/EXP-0013/xref.py
local/extracted/saturn_us/MAIN.BIN 06012000 0608089A` (and `06080882`; the
Japanese file at `06013A00` with `060808EA`, `060808D2`). Outputs stay in the
ignored `local/disc001/`.
