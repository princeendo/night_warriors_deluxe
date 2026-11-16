# EXP-0037: Where the Edition Switch's Code and Data Can Live

Task: EDITION-002
Status: IN_PROGRESS (candidates found; none yet written to or watched)
Confidence: SUPPORTED (zero in every sampled state; file room from the ISO
directory); no candidate is proven free

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

## Uncertainty and Next Step

- "Zero in every state" is not "never written": a clear of zeros, or use
  between samples, is invisible. Next: a write and read watch on
  `0x06009565`-`0x0600FFFF` from power-on through the title, the options
  screen (with a change and a save) and the start of a match.
- Whether the title is always the first thing after boot, and whether each
  return to the title reloads `TITLE.O`, is UNKNOWN.
