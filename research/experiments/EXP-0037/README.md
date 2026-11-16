# EXP-0037: Where the Edition Switch's Code and Data Can Live

Task: EDITION-002
Status: DONE
Confidence: CONFIRMED for `0x06009565`-`0x0600FFFF` while the title runs
(access watch, one session); the other candidates SUPPORTED at most

## Observation

The edition switch needs: an EDITION line in the options screen (`TITLE.O`,
EXP-0036), code that applies the edition (flag, language, a "Japanese
content" byte), Morrigan's Enhanced main-ending script (134 bytes) without
overwriting her Japanese one, and the English epilogues outside
`ST1JPN.BIN`.

## 1. RAM That Stays Zero Everywhere

`free_ram.py 256` over 90 states (every 6th of `local/aud004/cold-session`,
boot to three matches; every 3rd of the `EXP-0026` endings `all-05` and
`all-12`; every 5th of `local/edition002/options-session3`): no run in
WRAM-L; in WRAM-H only `0x06000AFF`-`0x06000BFF` (257), `0x06000E19`-
`0x06000FC1` (425), below the overlays in the system area, and
`0x060FF804`-`0x060FFCEB` (1,256), inside the stack's reach (the save load
alone takes a 25 KB frame). None is safe without more proof. At 64 bytes
nothing else appears above `0x06001000`. The `MAIN.BIN` tests for flag 4
(`0x06018032`, `0x06018E00`) guard a few instructions only: no dead code to
reuse there.

## 2. Room on the Disc After Each File

From the ISO directory (`tools/disc/iso9660.py`), bytes between a file's end
and the next file:

| File | Size | Room |
| --- | --- | --- |
| `MAIN.BIN` | 374,544 | 240 |
| `TITLE.O` | 34,076 | 740 |
| `ENDING.O` | 64,080 | 1,456 |
| `PL05.O` / `PL10.O` / `PL14.O` | | 1,132 / 1,176 / 404 |
| `ST1JPN.BIN` / `ST1USA.BIN` / `ST2USA.BIN` | | 1,396 / 1,858 / 13 |

Growing a file into its room only helps if the RAM after its load is free
while it runs.

- **`ENDING.O`** (loaded at `0x06001000`, ends `0x06010A50`): the 1,456
  bytes after it are in use in every ending state (1,272-1,291 nonzero).
  No.
- **`TITLE.O`** (ends `0x0600951C`): `usage.py` over all 50 states of
  `options-session3` (boot, title, OPTION MODE, CONFIGURATION): only
  `0x06009564` is ever nonzero (the byte the menu tests before the exit
  line); **`0x06009565`-`0x0600FFFF` (27,291 bytes) stays zero** while the
  title and its menus run (the player-2 overlay slot, unused there). So
  `TITLE.O` could grow by up to 740 bytes (to `0x06009800`), keeping
  `0x06009564` clear, or title code could load a new file into that space.

## Design This Points To (not built)

Everything the edition changes in `MAIN.BIN` can be written by title-time
code, because the edition changes only at the title: the title applies the
saved edition on entry and after the menu, and patches `MAIN.BIN`'s RAM
(Morrigan's script and table entry, the `ST1` call) from data it carries.
Room for that code and data: `TITLE.O`'s 740 bytes, or a new file (track 1
has 150 free sectors) loaded into the free title-time RAM by a short hook.
The overlays' guards point at the "Japanese content" byte instead of the
flag (a literal change on disc). The English epilogues go to a new file.

## 3. Access Watch Over the Title-Time Range

`EXP-0036/options_watch.py local/edition002/free-watch <US cue>
06009565-0600FFFF` (read and write watch, log mode, stock US image). The
user booted, opened OPTION, changed a setting, saved with Start, and
started an Arcade match. Accesses by frame:

| Frames | PC | What |
| --- | --- | --- |
| 8-11 | `0x000002B0` | BIOS start-up clear |
| 325 | `0x00002F06` | BIOS, during boot (before `TITLE.O` runs) |
| 1,206; 1,606; 1,996 | (PC log only) | load-and-unpack, unpack on entering OPTION, pack on Start: no access to the range |
| 3,471-3,476 | `0x0604EC34` (`MAIN.BIN`) | 6,782 accesses as the match loads player 2's overlay |
| 3,624 on | `0x06009xxx`-`0x0600Fxxx` | the overlay's own code and data during the fight |

**From boot to the match start, through the title, the options screen, a
change and a save, nothing reads or writes `0x06009565`-`0x0600FFFF`.** The
title-time code and data can live there.

## Uncertainty

- One session; the attract mode (title left idle) and returning to the
  title after a game were not watched.
- Whether each return to the title reloads `TITLE.O` is UNKNOWN; the edition
  code must be (re)loaded with it either way.
