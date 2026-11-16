# EXP-0036: The Settings Block and Its Spare Bytes (EDITION-002, criterion 1)

Task: EDITION-002
Status: IN_PROGRESS (save block and spare bytes found; the options screen
not yet located)
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
- **Options screen.** Not located: the settings variables are referenced
  only in `MAIN.BIN` (and `0x0608089E` in `TITLE.O`). A session in which
  the user changes one option, with a write watch on `0x0608089F`, finds
  the screen's code.

## Uncertainty

- The spare bytes were not watched while saving or in the options screen.
- JP saves have the same layout here, but only the US code is used
  (`EDITION-001`).
