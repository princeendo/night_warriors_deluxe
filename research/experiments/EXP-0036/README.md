# EXP-0036: The Settings Block and Its Spare Bytes (EDITION-002, criterion 1)

Task: EDITION-002
Status: IN_PROGRESS (save block, spare bytes and the options screen found;
the menu entry not yet designed)
Confidence: CONFIRMED (save layout, load and save routines, from code);
SUPPORTED (spare bytes: static reading plus three replays; the save path
itself was not run)

## Observation

`EDITION-001`: the edition is an options entry saved in spare save bytes.
Where the game keeps and saves its settings was unknown.

## Save File

Both regions' backup RAM (`local/mednafen/sav/*.bkr`) hold one file, US
`N_WARRIORS_`, JP `V_HUNTER_01`, 512 bytes from block 2 (blocks 3-11
follow). Read with the layout of `tools/mednafen/backup_ram.py`. In this
machine's saves the first 0x80 bytes equal `MAIN.BIN`'s built-in defaults
at `0x06067808` (no option was ever changed) and are the same in both
regions.

## Load and Save (US `MAIN.BIN`, base `0x06012000`)

- **Live block `0x060830B4`, 0x104 bytes.** Load (`0x06014588`): read the
  file to the stack; if its first long equals the defaults' (`0x06067808`),
  copy 0x104 bytes to `0x060830B4` (`0x06047AAC`); with no valid file, copy
  the defaults (`0x06047580`). Save (`0x060144F2`-`0x06014518`): copy 0x104
  bytes from `0x060830B4` to a stack buffer and write 0x200, so file bytes
  0x104-0x1FF are stack leftovers.
- **Unpack `0x06014734`** (called after the load) copies fields to live
  variables; **pack `0x060148C4`** copies them back. Offsets used by both:
  `0x04`-`0x10` (bytes: `0x0608089F`, `0x0608089E`, `0x06080881`,
  `0x06080886`, `0x060808CE`, `0x060808CD`, `0x060808B4`, `0x06080901`, ...),
  `0x18`-`0x53` (60 bytes, `0x060809DC`: the ranking), `0x54`-`0x5D`,
  `0x5E`-`0x7D` (32 bytes, `0x06080A2C`), `0x7E`-`0xF5` (120 bytes,
  `0x06080A4C`), `0xF6`-`0xFF` (words, `0x06080AC4`-`0x06080ACC`). The word
  at `0x100` (`0x060831B4`) is read directly elsewhere (`0x06014114`,
  `0x060189A4`, `0x0601D3FC`, `0x0601D51C`). Bytes `0x00`-`0x03` are the
  version tested at load.
- **Not used by either routine: `0x11`-`0x17` (`0x060830C5`-`0x060830CB`)
  and `0x102`-`0x103`.** Zero in the defaults. No literal in any program
  file points inside the block other than `0x060830B4` and `0x060831B4`.

## Replays

`EXP-0010/force.py --log-read/--log-write 060830C5-060830CB` and
`060831B6-060831B7` on `build/us_en_sasquatch`, 60 × 30 frames, from the
cold-session states `f00000008` (power-on through boot and title),
`f00007017` (Donovan's win) and `f00017787` (Sasquatch's win): from boot,
only the start-up clears (boot code before `MAIN.BIN`, `MAIN.BIN`'s
work-area clear at `0x0601200E`) and the block copy (`0x06047AC4`); in the
fight and win replays, no access at all. The save and options paths need
input and were not run.

## Where the Edition Takes Effect

D-013: `MAIN.BIN` start-up sets the flag (`0x0608089A` = 2) and language
(`0x06080882` = 1) once, before the save is loaded; the unpack at
`0x06014734` runs after the load. So the edition byte (block `0x11`) can
set both in the unpack, and again when the options screen changes it.

## Plan for Criteria 2-4 (not done)

- **Flags.** From the edition: JP original and JP Enhanced flag 0,
  language 0; US original and US Enhanced flag 2, language 1. A second
  byte C, "show the Japanese-only content": 0 in every edition but US
  original (2). The overlays' guards read the flag through literals: in
  `PL05`, `PL10`, `PL14` every flag reader is a guard (4, 6, 2), and
  `ENDING.O`'s two are the epilogue path, so their literal can point at C
  instead of the flag (a data change, no `nop`s).
- **Epilogue text.** The English epilogues now replace `ST1JPN.BIN`; they
  need their own place so the Japanese editions get it intact (a new file
  in track 1's 150 free sectors, or `ST1USA.BIN`'s placeholder records),
  and the `MAIN.BIN` `ST1` call must choose by edition.
- **Morrigan's main-ending script** now overwrites her Japanese script.
  Her US Enhanced script (134 bytes) and a table to reach it need memory
  that no edition uses: UNKNOWN where.
- **Options screen.** Found (below); the new entry's drawing and input
  are the next step.

## Options Screen (two sessions with the user)

`research/experiments/EXP-0036/options_watch.py` starts the stock US image
in the interactive home with log-mode write watches (and PC logs), and
waits for the user to close the window.

1. `local/edition002/options-session` (watch on `0x0608089F`, `0x0608089E`,
   `0x06080881`, `0x06080886`): only the boot clears and the unpack, which
   ran twice (frames 1,153 and 1,694). The setting changed was not one of
   these four.
2. `local/edition002/options-session2` (plus block bytes `0x04`-`0x10` and
   PC logs of load-and-unpack `0x06014718` and pack `0x060148C4`): load and
   unpack at frame 1,154 (called from `0x06013A76`), unpack again at 1,533
   (from `MAIN.BIN` `0x0603612E`, entering the menu), pack at 2,013 (from
   `TITLE.O` `0x060052B4`). The saved file afterwards differs from the
   earlier one in **block byte `0x08` only, 1 → 3**: the pack fills it from
   `0x060809C6`, so that is the setting changed.

`0x060809C6` is edited in `TITLE.O` (`0x06001000`) at `0x0600547C` (one
direction decrements it, `0x06005488`). The menu's cursor is
`0x0608086C`; `0x060052B8` sends each value (0, 2, 4, 6, 8, 9) to its line's
handler; Start (pad bit `0x0800`, `0x060052A4`) calls the pack
`0x060148C4` (`0x060052AE`) and leaves. So **the options screen is in
`TITLE.O`**, it edits the live variables directly, and Start saves them
through the pack. Which label the user changed is not recorded.

## How the Menu Draws Its Lines (third session)

`options_watch.py` now also takes a screenshot and a state each second.
Session `local/edition002/options-session3` (the user opened OPTION, then
CONFIGURATION, and left; the user reported "There was no appendix").

- The labels are ASCII strings in `TITLE.O` (file `0xB06`-`0xC90`, the
  title menu, OPTION MODE and APPENDIX screens). One routine,
  `0x06018A1A` (in `MAIN.BIN`), draws each: x in r4, y in r5, colour in r6
  (3 when the cursor is on the line, else 1), string in r7.
- OPTION MODE (`0x060048C0` on): title at y 8; nine lines from y 40, 16
  apart, to CONFIGURATION at y `0xA8` (cursor 8); APPENDIX at y `0xB8`
  (cursor 9) **only when `0x06080A2B` is non-zero** (`0x06004B82`); PRESS
  START TO EXIT at y `0xD0`. `0x06080A2B` is saved (block byte `0x5D`); it
  is 0 here, so the user's menu has a blank slot where APPENDIX goes. What
  sets it is UNKNOWN (an unlock).
- Room: one 16-pixel slot below APPENDIX (y `0xC8`) collides with the exit
  line at `0xD0`; a new line there means moving the exit line down (to
  `0xD8`, still on screen in a 240-line capture) or using the APPENDIX
  screen (hidden until unlocked).

## Uncertainty

- The spare bytes were not watched while saving or in the options screen.
- JP saves have the same layout here, but only the US code is used
  (`EDITION-001`).
