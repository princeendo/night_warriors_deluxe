# Confirmed Discoveries

Only durable `CONFIRMED` findings about Vampire Hunter (either release) belong
here, each with an ID (`D-NNN`), its evidence (experiment, task), the
release(s) it holds for, and reproduction instructions. Hypotheses and failures
go in `research_log.md`; open questions go in `docs/known_unknowns.md`; the
regional difference inventory is `docs/difference_register.md`.

MSHvSF, XvSF and Cyberbots findings are never recorded here. A sibling finding
enters this file only after a Vampire Hunter experiment confirms the Vampire
Hunter equivalent. A finding confirmed on one release is not a finding about
the other until tested there.

## D-001: Stock Mednafen cold-boots both releases to their title screens (`EMU-003`, `EXP-0001`)

Holds for: Japanese 1M image and US image.

Stock Mednafen 1.32.1 (`de542817…582a`) with the silent home
`local/mednafen_quiet/` cold-boots each untouched image with no input. The
Japanese log reports `SGID: T-1202G`, `SGAREA: JT`, `Region: 0x1`; the US log
`SGID: T-1208H`, `SGAREA: U`, `Region: 0x4`; both `Cart: Backup Memory`
(`ss.cart auto`, no database entry). From Mednafen's BIOS selection and its
sanity check, the Japanese release boots with `sega_101.bin` and the US
release with `mpr-17933.bin`. The titles `VAMPIRE HUNTER` and `NIGHT
WARRIORS` show from about 63 s after launch. Three boots per release gave
byte-identical frames at one-second sampling (119 of 119); Japanese title
frame 065 hashes `216118a8…58a3`, US `d6617a89…177a`. Source hashes were
unchanged.

Reproduce: `research/experiments/EXP-0001/README.md`, "Procedure".

## D-002: Neither release needs an extended-RAM cart for boot and attract (`EMU-004`, `EXP-0002`)

Holds for: Japanese 1M image and US image; boot and attract mode only.

With `ss.cart` `none`, `extram1` or `extram4`, each release boots to the same
screens as with the backup-memory cart of D-001, with no warning; the three
settings give byte-identical frames, and the backup cart shifts timing by a
fraction of a second. The project keeps `ss.cart auto` (backup memory).

Reproduce: `research/experiments/EXP-0002/README.md`, "Procedure".

## D-003: Hotkey screenshots and save/load states work in both releases (`EMU-006`, `EXP-0003`)

Holds for: Japanese 1M image and US image.

With stock Mednafen and the quiet home, F9 writes a 352x240 screenshot
(330x240 during the BIOS phase) to `snaps/`, F5 saves a state of about 1.6 MB
to `mcs/`, and F7 restores it in the same session and in a fresh cold boot. A
reloaded title state reproduces the title screenshot byte for byte (Japanese
`a166ccb4…f0fd`, same session; US `025b8fd8…2209`, fresh boot). Loading does
not change the state file. Keys are not fully reliable: one post-load F9 and
one F12 were lost.

Reproduce: `research/experiments/EXP-0003/README.md`, "Procedure".

## D-004: The stock debugger dumps work RAM, writes memory and halts on writes in both releases (`EMU-007`, `EXP-0004`)

Holds for: Japanese 1M image and US image.

With emulation frozen on the title (`option+a`), the stock debugger's memory
editor dumps WRAM-L (`0x00200000-0x002FFFFF`) and WRAM-H
(`0x06000000-0x060FFFFF`) as 1 MiB files, identical when repeated; a 16-byte
`l` load into WRAM-H reads back, and loading the saved original restores it;
a WRAM-H write breakpoint (`shift+w`) halts the CPU on a store into that range.
A state saved at the same frozen instant accompanies each release's dumps
(Japanese `f945cb51…91a0`, US `2eb7dbd0…49db`).

Reproduce: `research/experiments/EXP-0004/README.md`, "Procedure".

## D-005: The agent interface works on both releases (`EMU-021`, `EXP-0005`)

Holds for: Japanese 1M image and US image.

The sibling patch (`c30146ef…5244`) applies unchanged to Mednafen 1.32.1 and
builds `vendor/mednafen/build-agent/src/mednafen` (`7826b9b9…f887`). Without
`MEDNAFEN_AGENT_DIR` it gives the same 119 per-second boot frames as stock.
With it: agent reads of WRAM-L, WRAM-H, VDP1 VRAM and VDP2 VRAM equal
`mcs_extract` of a state saved in the same poll; writes round-trip; `pause`,
`step`, `run` and `frames N` work, and `savestate` is refused while halted;
write breakpoints log and continue (`bpmode log`) or halt (`bpmode halt`),
with every register in `events.log`. Agent output may be used as evidence.

Reproduce: `research/experiments/EXP-0005/README.md`, "Procedure".

## D-006: The save-state extractor matches stock debugger dumps on both releases (`DBG-001`, `EXP-0006`)

Holds for: Japanese 1M image and US image; WRAM-L, WRAM-H, VDP1 VRAM, VDP2
VRAM.

`tools/memory/mcs_extract.py` with its default `saturn` byte order (each
stored 16-bit element swapped) reproduces stock debugger dumps of the same
paused instant byte for byte: WRAM-L and WRAM-H at two instants, VDP1 and
VDP2 VRAM at one, in each release. Without the swap (`--byte-order state`)
every region differs. These four regions extracted from states may be used
as evidence. Cart RAM and sound RAM are not covered.

Reproduce: `research/experiments/EXP-0006/README.md`, "Procedure".

## D-007: Morrigan's bat-seat win line is on the US disc but not played (`AUD-001`, `EXP-0008`)

Holds for: Japanese 1M image (plays it) and US image (does not).

Both releases load `MORRIGA.BIN` into sound RAM at `0x3B2C0`. In the
Japanese release, Morrigan's bat-seat win pose plays the 8-bit sample at
sound RAM `0x56D60` (loop end `0x215F`; `MORRIGA.BIN` offset `0x1BAA0`) on an
SCSP slot. In the US release the same pose plays no sample from Morrigan's
region, although those 8,544 bytes are identical in its sound RAM. Change
type: conditionally suppressed. What selects the sample is not known.

Reproduce: `research/experiments/EXP-0008/README.md`, "Reproduction".

## D-008: Morrigan's normal-throw voice is on the US disc but not played (`AUD-001`, `EXP-0009`)

Holds for: Japanese 1M image (plays it) and US image (does not).

At Morrigan's normal throw, the Japanese release plays the 8-bit sample at
sound RAM `0x50C2C` (`MORRIGA.BIN` offset `0x1596C`, 3,477 samples, played at
13,168 Hz). A waveform search of a 400-second play recording finds it at
every Japanese throw and nowhere in the US recording, which includes an
observed US throw; a control sample both releases play is found in both.
The sample is on both discs (identical files) and loaded at the same address
(D-007). Change type: conditionally suppressed.

Reproduce: `research/experiments/EXP-0009/README.md`, "Procedure".

## D-009: The stage byte, and forcing an ending (`END-001`, `EXP-0010`)

Holds for: Japanese 1M image (`0x0608097B`) and US image (`0x0608092B`).

During arcade mode, WRAM-H `0x0608097B` (Japanese) / `0x0608092B` (US) holds
the 0-based stage number (0 at the first opponent, 1 at the second). Writing
9 into it just after a won KO makes the game play the player character's
ending instead of another fight. The work variables around it are laid out
alike in both releases, `0x50` lower in the US release.

Reproduce: `research/experiments/EXP-0010/README.md`, "Procedure", step 3.

## D-010: Morrigan's epilogue text is shown in the Japanese release only (`END-001`, `EXP-0010`)

Holds for: Japanese 1M image and US image; Morrigan's ending.

After the main ending and an emblem card, both releases scroll Morrigan's
full-length artwork up the screen at the same time. The Japanese release
shows a paragraph of Japanese epilogue text over it; the US release shows
the artwork with no text. Change type: omitted (presentation). Whether the
text is on the US disc is not yet known.

Reproduce: `research/experiments/EXP-0010/README.md`, "Procedure", step 3.

## D-011: The Japanese epilogue text is on the US disc in `ST1JPN.BIN` and is never loaded there (`END-001`, `EXP-0011`)

Holds for: Japanese 1M image and US image; traced for Morrigan's epilogue.

The epilogue paragraph is stored in `ST1JPN.BIN` as big-endian 16-bit
character codes listed in `MOJI.TBL`, and drawn as 16x16 VDP1 sprites from
the 1,026-glyph font `MOJI.CHR` (loaded at VDP1 VRAM `0x24B98`). The
Japanese release loads `ST1JPN.BIN` into WRAM-H at `0x060C9C00` (with
`ST2JPN.BIN`) for the ending. The US release loads `MOJI.CHR` and `MOJI.TBL`
too but, at the ending, only `ST2USA.BIN` (its English main-ending text) and
no `ST1` file. `ST1JPN.BIN`, `MOJI.CHR` and `MOJI.TBL` are byte-identical on
both discs. Change type: conditionally suppressed (asset present).

Reproduce: `research/experiments/EXP-0011/README.md`.

## D-012: The epilogue is switched off in the US release by two data bytes (`END-001`, `EXP-0012`)

Holds for: Japanese 1M image and US image; tested on Morrigan's ending.

Both releases run the same ending code (addresses differ). At the start of
an ending, if the byte at `0x060808EA` (Japanese; US `0x0608089A`) is 0, the
game loads an `ST1` epilogue file whose name is chosen by the language byte
at `0x060808D2` (Japanese; US `0x06080882`): 0 `ST1JPN.BIN`, 1 `ST1USA.BIN`,
2 `ST1HIS.BIN`. The same language byte chooses `ST2JPN`/`ST2USA` for the main
ending and how its text and the epilogue text are drawn. The Japanese
release has flag 0 and language 0; the US release has flag 2 and language
1, so it never loads an epilogue file. In US RAM, clearing the flag, pointing
the ST1 name array's USA entry (`0x0606BEBC`) at `ST1JPN.BIN`, and setting
the language to 0 only after the main ending shows the English main ending
followed by the Japanese epilogue. With the flag cleared and nothing else,
the US release loads `ST1USA.BIN`, which draws as rows of "A" (a
placeholder).

Reproduce: `research/experiments/EXP-0012/README.md`, "Reproduction".

## D-013: The US start-up code sets the epilogue flag and language byte; the Japanese release never writes them (`DISC-001`, `EXP-0013`)

Holds for: Japanese 1M image and US image, from power-on to the end of
start-up (frame 1,800).

The US `MAIN.BIN` start-up routine (`0x06012070`) writes the epilogue flag
`0x0608089A` = 2 (`mov #2,r2` at file offset `0x11A`, stored at
`0x06012128`) and the language byte `0x06080882` = 1 (`mov #1,r4` at
`0x11E`, stored at `0x0601212E`; the same register also sets `0x060808A8` =
1), once, right after `MAIN.BIN` clears its work area. A write watch from
power-on shows no other writer after that clear, and no program file on
either disc has another store to them. The Japanese release has no such
code; both bytes stay at the 0 its clear leaves.

Reproduce: `research/experiments/EXP-0013/README.md`, "Reproduction".

## D-014: The same flag silences Morrigan's bat-seat win line in the US release (`AUD-001`, `EXP-0014`)

Holds for: US image; Morrigan's win over Victor from state `f00011016`.

Writing 0 to the US epilogue flag (`0x0608089A`, D-012, D-013) just after
Morrigan's winning KO makes the US release play her bat-seat line (sample
`56D60`, `MORRIGA.BIN` `0x1BAA0`, D-007) at the bat-seat pose; with no write,
the same replay plays no such line. Morrigan's code (`PL05.O`, at
`0x06001000` in her fights) has four places that call `0x0603A4D6` only
when the flag is 0. The flag is therefore not only the epilogue switch.

Reproduce: `research/experiments/EXP-0014/README.md`, "Procedure" step 3.

## D-015: The flag is a region switch; it also selects the characters' names (`DISC-002`, `EXP-0015`)

Holds for: US image; Morrigan's ending from state `f00011016`; static tables
in both `MAIN.BIN` files.

With the flag `0x0608089A` cleared at Morrigan's winning KO and the language
byte left at English, the US cast roll names the second character GALLON;
the unpatched US release names it JON TALBAIN. Both `MAIN.BIN` files hold
two 14-entry name-graphic tables (Japanese `0x3829`-`0x3836`; US the same
except `0x3837`-`0x383B` for characters 2, 4, 9, 11, 13), two sets of name
positions, and two sets of fight-display name tiles, each chosen by this
flag; the flag also selects the MODE SELECT graphics and text spacing rules
(code reading, `EXP-0015`). Clearing it therefore turns the US release's
names back to the Japanese ones.

Reproduce: `research/experiments/EXP-0015/README.md`, "Procedure" step 4.

## D-016: The US release pauses when a controller is missing; the region flag decides it (`DISC-002`, `EXP-0016`)

Holds for: Japanese 1M image and US image; a Morrigan-vs-Victor fight state
of each, port 1 set to no device at start-up.

With no device in port 1, the US release shows PAUSE within a frame of
loading the fight state and stays paused; with the region flag
(`0x0608089A`) written to 0 it plays on. The Japanese release plays on with
port 1 empty. The check is in the fight-frame routine at US `0x0601D474`: a
human player's missing pad (its bit clear in `0x06076ABE`, rebuilt each frame
by `0x06013C20`) toggles pause only when the flag is non-zero.

Reproduce: `research/experiments/EXP-0016/README.md`, "Procedure".

## D-017: A 15-byte patch of the US image shows the Japanese epilogue and keeps the US release (`DISC-002`, `EXP-0018`)

Holds for: the US image (Track 1 `d0960087…70da`) patched by
`research/experiments/EXP-0018/build_epilogue.py` (Track 1 `93ca264c…39ab`);
Morrigan's ending.

Fifteen bytes in three files: in `MAIN.BIN` the ending's `ST1` call
(`0x0603B902`-`0x0603B90E`) loads `ST1JPN.BIN` by name through the file
loader `0x06013DF8` instead of taking the name from the language-indexed
array `0x0606BEB8`, with no flag test; `ST1JPN.BIN` declares the US text slot
`0x1BC` (header byte 3, `BA` → `BC`); `ENDING.O` takes the flag-0 branches at
`0x0600CFCC` and `0x0600D0D0` (card sequence, epilogue length `0x564`). The
region flag stays 2 and the language 1. From a cold boot and a won match the
win quote is English; the ending forced with the stage byte alone shows the
English main ending, then the Japanese epilogue, then a cast roll with the US
names. The unpatched image shows the art with no text. The array must stay
unchanged: the win screens load `ST1USA.BIN` through it (changing its US
entry turned the win quote Japanese).

Reproduce: `research/experiments/EXP-0018/README.md`, steps 6-9.

## D-018: The US ending's character is `0x06080980`; the D-017 patch shows all 14 Japanese epilogues (`END-001`, `EXP-0019`)

Holds for: the US image (Track 1 `d0960087…70da`) and the D-017 image (Track
1 `93ca264c…39ab`).

`0x06080980` is player 1's character, 1-based: 1 Demitri, 2 Jon Talbain,
3 Victor, 4 Lord Raptor, 5 Morrigan, 6 Anakaris, 7 Felicia, 8 Bishamon,
9 Rikuo, 10 Sasquatch, 11 Huitzil, 12 Pyron, 13 Hsien-Ko, 14 Donovan. After
a won KO it is copied to `0x0608096E` (at `0x0601DC7A`), from which the
ending builds its script struct at `0x0609159C` (character at +5). Writing
N there together with the stage byte (`0x0608092B` = 9, D-009) at a
Morrigan won-KO state plays character N's ending. On the D-017 image every
character's English ending is followed by that character's Japanese
epilogue and the US cast roll; the unpatched image shows the art without
text for all 14.

Reproduce: `research/experiments/EXP-0019/README.md` (`all_endings.sh`).

## D-019: The US PSP *Chronicle* holds an English epilogue for each of the 14 characters, drawn into its ending movies (`REF-002`, `EXP-0020`)

Holds for: `Darkstalkers Chronicle - The Chaos Tower (USA).iso` (ULUS-10005,
SHA-256 `c465f42d…49ac`).

`PSP_GAME/USRDIR/movie/hunend/HmovieNN_2.pmf` (NN = 01-14; a 2,048-byte PSMF
header, then an MPEG program stream, H.264 480x272) shows an English
paragraph over the character's art; frame 300 holds the whole paragraph. No
epilogue text exists as character data on the disc (the only English text
files, `mess00.bin`, hold menu labels). Order: 01 Hsien-Ko, 02 Donovan,
03 Demitri, 04 Morrigan, 05 Anakaris, 06 Victor, 07 Lord Raptor, 08 Jon
Talbain, 09 Felicia, 10 Rikuo, 11 Sasquatch, 12 Bishamon, 13 Huitzil,
14 Pyron. That each renders the Saturn Japanese epilogue of the same
character is SUPPORTED (a reading by meaning), not part of this finding.

Reproduce: `research/experiments/EXP-0020/README.md` (`frames.sh`).

## D-020: The `ENDING.O` flag-0 path at `0x0600CFCE` is the epilogue's 416-frame text introduction (`END-001`, `EXP-0021`)

Holds for: the US `ENDING.O` (loaded at `0x06001000`) on the US image and the
D-017 image; the Japanese release shows the same sequence.

With the region flag 0 (or the branch at `0x0600CFCC` made a `nop`, D-017),
`ENDING.O` runs a loop at `0x0600D008` once per frame for 416 frames
(`0x1A0`), during which the epilogue paragraph rises onto a black screen;
the art scroll starts after it. With the flag 2 the US release jumps to
`0x0600D02E` and starts the art straight after the emblem card. Logged:
version 2, `0x0600D008` x416 on frames 6,140-6,555; unpatched, 0.

Reproduce: `research/experiments/EXP-0021/README.md`.

## D-021: In English mode the epilogue renderer draws the win-quote Latin codes (`END-002`, `EXP-0022`)

Holds for: the D-017 image with `ST1JPN.BIN` lines rewritten
(`research/experiments/EXP-0022/build_en_test.py`).

Epilogue lines are records of x, y, `0001`, then 16-bit codes, ended by
`FFFF` (next line) or `0000`. With the language byte at 1, Latin codes in
those records draw in the US win-quote font: capitals and most punctuation
are ASCII + `0x80` (`A` = `00C1`, `'` = `00A7`, `!` = `00A1`, `?` = `00BF`),
lowercase `a`-`z` are `0201`-`021A`, space is `0020`, and comma and period
are `00AE` and `00AC` (the reverse of ASCII + `0x80`). They mix with `MOJI`
codes in one paragraph. Advance about 12 pixels; about 26 characters fit a
line starting at x = `0x2C`.

Reproduce: `research/experiments/EXP-0022/README.md`.

## D-022: Epilogue records are found through a self-relative table, and at most 238 characters are drawn (`END-002`, `EXP-0023`)

Holds for: the US `MAIN.BIN` (unchanged in the D-017 image) reading an `ST1`
file in English mode.

The table at file offset `0x0C` holds one 32-bit word per character, indexed
by roster number − 1 (D-018); the record starts at the word's own address
plus its value (`0x060379B2`-`0x060379C2`). The ending reads only the file
header, that word and the record. Each non-space character adds an 8-byte
entry to a list at `0x060839D4` (literal at `0x06037A98`) with no length
check; only the first 238 are drawn (an English paragraph was cut at its
238th non-space character), which is exactly the longest Japanese
epilogue's length.

Reproduce: `research/experiments/EXP-0023/README.md`.

## D-023: Moving the epilogue glyph list to sprite array 2 gives 302 characters on top of the art (`END-002`, `EXP-0024`)

Holds for: the D-017 image plus `EXP-0023/build_en_epilogue.py --move-list`
(Morrigan, forced from a state with the same literal written in RAM).

Three stubs draw fixed sprite arrays each frame through `0x060188D4(base,
count)`: `0x06083344` × 128, `0x06083744` × 128, `0x06083B44` × 192; the
art is drawn after array 1 and before arrays 2-3. Changing the epilogue
builder's literal at `0x06037A98` from `0x060839D4` to `0x06083744`, and
filling list entries 64-81 (the player sprite slots, rewritten every frame)
with an off-screen line, lets an epilogue use 302 characters drawn on top of
the art; Morrigan's whole English epilogue (278) shows. Text placed in array
1 is drawn under the art.

Reproduce: `research/experiments/EXP-0024/README.md`.

## D-024: Redrawing sprite array 1 after the art gives an epilogue 413 characters (`END-002`, `EXP-0025`)

Holds for: the D-017 image plus `EXP-0023/build_en_epilogue.py --late-array1`
(Morrigan and Anakaris, forced from a state with the `MAIN.BIN` literal
written in RAM).

Each ending frame draws array 1 (through the general per-frame routine,
before the art), then arrays 2-3 (through `ENDING.O`'s `r12` =
`0x06020766`). A 36-byte routine placed in `ST1JPN.BIN` (in RAM at
`0x060CB408` + offset) calls `0x06020766` and then the reader
`0x060188D4(0x060833CC, 111)`; pointing `ENDING.O`'s `r12` literal
(`0x0600D0B0`) at it through the cache-through mirror draws array 1 slots
17-127 again, on top. With the epilogue list starting at array 1 slot 17
(`0x06037A98` = `0x060833CC`) and the player slots covered, 413 characters
fit; Anakaris's 345-character, 18-line English epilogue shows whole at
12-pixel spacing.

Reproduce: `research/experiments/EXP-0025/README.md`.

## D-025: One patched US image shows all 14 English epilogues (`END-002`, `EXP-0026`)

Holds for: the US image patched by `EXP-0023/build_en_epilogue.py
--late-array1 --step 0` for rosters 1-14 (Track 1 `21fb1c79…9b87`), each
ending forced from a state with the `MAIN.BIN` literal written in RAM.

`ST1JPN.BIN` is loaded from a heap, at an address that depends on the
character (`0x060CB408` for Morrigan, `0x060C7C14` for Pyron); the loader
stores the file's table address (slot `0x1BC`) at `0x06091E48`. Computing
`ENDING.O`'s `r12` from it at the epilogue's start (`0x0600CFC2`-`0x0600CFCA`)
makes the array-1 redraw routine (D-024) work for every character. Each of
the 14 English epilogues (PSP *Chronicle* text, logged edits only) shows
whole on top of the art, and every run continues to the cast roll.

Reproduce: `research/experiments/EXP-0026/README.md`.

## D-026: The win quotes share the epilogue's text builder; the list start is switched only for the epilogue (`END-002`, `EXP-0027`)

Holds for: the US image patched by `EXP-0023/build_en_epilogue.py
--late-array1 --step 0` for rosters 1-14 (Track 1 `8ebc0ca3…0b67`).

Changing the glyph-list literal at `0x06037A98` on disc blanked the win
quote after a cold boot: the win screens use the same builder and literal.
The epilogue's text is built once, at frame 6,141 for Morrigan, between the
first and second per-frame calls of `ENDING.O`'s `r12`. The array-1 redraw
routine (D-024, D-025) therefore sets the literal to `0x060833CC` on its
first call (a flag in its own data in the freshly loaded `ST1JPN.BIN`) and
restores `0x060839D4` on every later call. `MAIN.BIN` keeps its original
literal; the win quote is English and the 14 epilogues are whole.

Reproduce: `research/experiments/EXP-0027/README.md`.

## D-027: From a cold boot, the patched US image keeps the English win quote and shows all 14 English epilogues (`END-002`, `EXP-0028`)

Holds for: the US image patched by `EXP-0023/build_en_epilogue.py
--late-array1 --step 0` for rosters 1-14 (Track 1 `8ebc0ca3…0b67`).

Cold-booted and played (Demitri beat Victor): the win quote is English. From
that session's bonus-screen state, each of the 14 endings forced with the
stage and character bytes only (no RAM write) shows the English main ending,
the emblem card, then the character's whole English epilogue (PSP *Chronicle*
text with the user's logged edits) rising on black and staying on top of the
art, then the US cast roll. This is M5 for `END-01`.

Reproduce: `research/experiments/EXP-0028/README.md`.

## D-028: The Japanese ending character is `0x060809D0`, and the two regions' main endings run from different scripts (`END-003`, `EXP-0029`)

Holds for: the Japanese 1M image and the US image.

Writing `0x060809D0` (the US `0x06080980` + `0x50`) with the stage byte
`0x0608097B` = 9 at a Japanese won-KO state plays that character's ending.
`MAIN.BIN` chooses a per-character ending script by the region flag
(`0x060367A4`): Japanese table `0x0605B1C0`, US `0x0605B730`; a script is an
initial wait then six-word page groups (id, mode, frames, id | `0x8000`,
mode, wait). The page counts differ for 12 of 14 characters: the Japanese
has extra pages for Jon Talbain (2), Morrigan (2) and Pyron (3); the US has
extra pages for Lord Raptor, Anakaris, Felicia, Bishamon, Rikuo, Sasquatch
and Huitzil (1-3 each); Hsien-Ko and Donovan use different pages
altogether; Demitri and Victor match. The US pages are mostly shown longer.

Reproduce: `research/experiments/EXP-0029/README.md`.

## D-029: The US main endings are a free rewrite of the Japanese, with few omissions (`END-003`, `EXP-0030`)

Holds for: `ST2JPN.BIN` (both discs) and the US `ST2USA.BIN`, read through
the two regions' ending scripts (D-028).

Page ids name table entries in both files (Demitri's are offset by `0x10`,
Pyron's by `0x60`). Read page by page, the US main endings re-paginate and
rewrite the Japanese: only Morrigan's loses Japanese text (two lines and a
pause page); Felicia's, Bishamon's, Huitzil's and Pyron's change in meaning
and Victor's resolution differs; Bishamon's, Rikuo's and Huitzil's add lines
or a page; Hsien-Ko's and Donovan's rename (Lei-Lei/Lin-Lin, Anita). No
Japanese scene is absent from the US. The meaning comparisons are SUPPORTED
readings, not translations.

Reproduce: `research/experiments/EXP-0030/README.md`.

## D-030: Morrigan's two missing main-ending lines restored in US Enhanced, in step with her pictures (`END-004`, `EXP-0031`)

Holds for: the US image patched by `EXP-0031/build_morrigan_main.py` (Track 1
`f4edd2a4…1091`), forced from a state and from a cold boot.

The ending's pictures run on their own timeline (her pages start at script
time + 422 frames; the butler scene ends near 3,850, the bed scene runs
3,980-4,870). New `ST2USA.BIN` records in the file's unused tail (entries
`0xB1`, `0xB2`) and a new 11-page US script (in her unread Japanese script's
134 bytes, US table entry 4 repointed), with pages 33-36 shortened, put "I'm
a little tired. / Prepare my bed." and "Certainly, mistress." (a new
translation the user approved) inside the butler scene; every later page
keeps its shipped time. Other endings and the win quote are unchanged.

Reproduce: `research/experiments/EXP-0031/README.md`.

## D-031: Four `nop`s in Morrigan's code restore her Japanese-only voices in US Enhanced (`AUD-002`, `EXP-0032`)

Holds for: the US image patched by `EXP-0032/build_voices.py` (Track 1
`2985ff73…1ae8`), from a cold boot and play.

Her code (`PL05.O`, and `PL05.O2` for player 2, same offsets) skips four
voice calls when the region flag is non-zero. Making each guard's `bf` a
`nop` (file `0x1490` win line, `0x1A1E` Vector Drain, `0x3342` hurt,
`0x5280` normal throw; the hurt one by elimination) plays all four samples
at their events, with the flag kept at 2; the win quote is unchanged.

Reproduce: `research/experiments/EXP-0032/README.md`.

## D-032: Opening Donovan's first guard plays his Japanese-only win sample in US Enhanced (`AUD-003`, `EXP-0033`)

Holds for: the US image patched by `EXP-0033/build_donovan.py` (Track 1
`64344d58…984e`), replayed from post-KO states of play sessions, including a cold boot
(`EXP-0034`'s session). The call follows only his pose 0, a win after the
first round.

Donovan's code (`PL14.O`, player 1) skips a sound call (code `0x1B4`, `bf` at
file `0x111C`) when the region flag is non-zero. At his win the Japanese
release starts sample `0x5687A` (8-bit, `0x2475` bytes) 8 frames after the
looping `0x1B4B2` both regions play. From the same US state, the patched
image starts `0x5687A` 12 frames after `0x1B4B2`; with the guard bytes
restored in RAM it never does, and no other sample differs. The sample's
bytes are at the same sound-RAM address in both regions.

Reproduce: `research/experiments/EXP-0033/README.md`.

## D-033: Sasquatch's Japanese win-pose creatures and pose restored by six `nop`s (`AUD-003`, `EXP-0034`)

Holds for: the US image patched by `EXP-0034/build_sasquatch.py` (Track 1
`e6e81ccc…dc99`), shown by forced replays from play sessions of both
releases with the same `nop`s written in RAM, and from a cold boot.

Sasquatch's code (`PL10.O`, player 1; `PL10.O2` same offsets) chooses his
win pose in one state machine (`0x060044FC`): Up + A + B + C held gives pose
4 (pad word `0x0708`, confirmed in both releases), otherwise a random pose 0
or 1. With the region flag non-zero, poses 0, 1 and 4 skip spawning small
snow creatures and their sample `0x53116`, and pose 5 (a roar) replaces pose
1 (a shy pose). Making the six guards `nop` (file `0x32D0`, `0x3354`,
`0x33C2`, `0x3460`, `0x34CA`, `0x35B8`) gives the Japanese poses, creatures
and sample with the flag at 2. The steam of pose 4 is in both releases.

Reproduce: `research/experiments/EXP-0034/README.md`.

## D-034: One US image switches between US Enhanced, US original and JP original from OPTION (`EDITION-002`, `EXP-0035`-`EXP-0038`)

Holds for: `build/us_edition` (`EXP-0038/build_edition.py`, Track 1
`25e05ec1…f1be`), from a cold boot with the user, Morrigan.

An EDITION line in OPTION MODE (in APPENDIX's blank slot) stores the
edition in the settings block's spare byte `0x11` (saved with the other
settings; 0 = US Enhanced, the default). Code added to a relocated
`TITLE.O`, run before the title task each frame, applies it: region flag,
language, a "Japanese content" byte C (block byte `0x12`) and, for US
Enhanced only, `MAIN.BIN`'s epilogue-file call and Morrigan's script. The
character guards and the ending read C. The English epilogues are in
`ST2HIS.BIN`'s place (language 2, never selected), `ST1JPN.BIN` stays
stock. Each edition gives its own voices, endings and names.

Reproduce: `research/experiments/EXP-0038/README.md`.

## D-035: Donovan's second region guard holds back a sound for punch + kick with his sword planted (`EXP-0039`)

Holds for: the Japanese 1M image (live session and replays); the US
release by identical code.

`PL14`'s guard at file `0x23C4` skips sample `0x4F2EA` (8-bit, `0xD00`
bytes, code `0x1B2`) that the Japanese release plays when, with Donovan's
sword stuck in the floor (object byte `+0x228` = 1), a punch and the kick
of the same strength are pressed together. Writing the flag to 2 in the
Japanese release removes only that sample. The code path is the same in
both releases' `PL14.O` apart from relocated literals.

Reproduce: `research/experiments/EXP-0039/README.md`.

## D-036: `FULL` still loads reduced sets for the mixed attract matchup (`ANI-002`, `EXP-0040`)

Holds for: the stock US T-1208H and Japanese 1M T-1202G images, from the
retail title checkpoints into the Anakaris vs. Rikuo/Aulbath attract fight.

Replaying each checkpoint with the animation byte set to 0 (`CUT`) and 1
(`FULL`) verified both values at the CPU read. `FULL` reached the fighter
equality check, then both settings selected the same `P06_` and `P09_`
resource sets and produced the same fight frame within each release. The
equality checks are at US `0x06021928` and JP `0x06022194`.

Reproduce: `research/experiments/EXP-0040/README.md`.

## D-037: `FULL` fits one full set, not two: a mirror loads `P06`, the forced Anakaris vs. Huitzil pair runs out of memory (`ANI-002`, `EXP-0041`)

Holds for: the stock US T-1208H image (Track 1 `d0960087…70da`), from the
retail title checkpoint with the attract fighters forced in RAM (IDs written
at `0x06035908` to `0x06076FD7` and `0x060773DB`).

An Anakaris mirror loads `P06_` once under `CUT` (684,404 pool bytes) and
`P06` once under `FULL` (1,162,868), and both screenshots show Anakaris
against Anakaris. Anakaris vs. Huitzil under `CUT` loads `P06_` and `P11_`
(1,367,788 bytes). The allocator's three bump pools at `0x06076AD8` (WRAM-H,
WRAM-L, VDP2 carve) give the fighter loads 1,372,412 bytes: 172,668 +
1,048,576 + 151,168. With the equality branch at `0x0602192A` forced in RAM
(`89 0F` to `A0 0F`), `FULL` requests `P06` and `P11` (2,256,056 bytes). A
112,784-byte request then fails at `0x06013F68` ("Out Of Memory", handler
`0x0601B078`), and the console resets to the Saturn BIOS CD player. Each
measured total equals the set's `.BIN` plus `.SPR` storage from `EXP-0040`.

Reproduce: `research/experiments/EXP-0041/README.md`.


## D-038: Agent writes reach the game after patch `0002` (cache-coherent writes) (`APP-001`, `EXP-0042`)

Holds for: the Mednafen 1.32.1 agent build with patches `0001` and `0002`
(binary `7040f6fe…4cdd`), on both releases.

Without `0002`, an agent write of `0800` to the US pressed-pad word
`0x06076AB8` just before the title task read it gave R0 = 0 at
`0x06004FDE`: the game read its emulated SH-2 cache. With `0002`, which
purges the written lines on both CPUs, the same trace read `0800` and the
title menu opened. V1-V4 (`EXP-0005`) pass again on both releases. V1:
119 of 119 cold-boot frames equal the `0001`-only build. V2: four regions
equal the extractor. V3 and V4 also pass.

Reproduce: `research/experiments/EXP-0042/README.md` (`revalidate.sh`).

## D-039: Capcom's Appendix code works and persists on both retail releases and Deluxe v0.1.0 (`APP-001`, `EXP-0042`)

Holds for: US T-1208H, JP 1M T-1202G and Deluxe v0.1.0 (`build/us_edition`
Track 1 `25e05ec1…f1be`), cold boots with an empty save, no cart (and a
4 MiB cart on Deluxe).

In OPTION MODE with the cursor on CONFIGURATION (line 8), B, X, Down, A, Y
(each within 14 frames) sets the unlock byte (US `0x06080A2B`, JP
`0x06080A7B`). APPENDIX then shows as line 9. A or C opens it (mode 5),
and Right on ANIMATION sets FULL. Start saves, and a second cold boot with
the same backup memory restores the unlock, FULL and, on Deluxe, the
edition. The sequence tables and menus are identical in both releases. JP
variables sit at US + `0x50`. On Deluxe v0.1.0 the unlocked menu draws
EDITION at y `0xC8` touching PRESS START TO EXIT at y `0xD0`.

Reproduce: `research/experiments/EXP-0042/README.md` (`app_check.py`).

## D-040: An unlocked Appendix changes the attract demo's BGM option and scenery (`APP-001`, `EXP-0042`)

Holds for: the US T-1208H image, from the retail title checkpoint.

The demo setup reads the unlock byte twice. At `0x060359B4` it sets the BGM
option `0x06080A26` to 2 (RANDOM) if unlocked, else 0 (HUNTER). At
`0x06035A8C` it sets the scenery variant `0x06080962` to a pseudo-random
bit if unlocked, else 0. With only the unlock byte changed, the demo read
BGM 0 / variant 0 and BGM 2 / variant 1, and variant 1 drew the stage in its
alternate colours. The two runs' sound recordings are byte-identical.

Reproduce: `research/experiments/EXP-0042/README.md` (`demo-wav-*`).

## D-041: Deluxe now starts with the Appendix unlocked and the exit line one line lower (`APP-001`, `EXP-0042`)

Holds for: `build/us_edition` Track 1 `a87f7f70…ab0d` (`TITLE.O`
`8ecf3a4b…9756`), rebuilt by `research/experiments/EXP-0038/build_edition.py`.

The title wrapper writes 1 to `0x06080A2B` each title frame, and
`0x06004C46` holds `00D8` (was `00D0`). From cold boots with an empty save
and no code entered, the unlock byte is 1 on the first OPTION MODE frame
and APPENDIX shows. The cursor reaches APPENDIX (9) and EDITION (10).
EDITION, APPENDIX and FULL work and persist across a reboot. PRESS START TO
EXIT is drawn one line below EDITION with the usual gap.

Reproduce: `research/experiments/EXP-0042/README.md`.

## D-042: With a 4 MiB cart, Deluxe gives full animation to different fighters (`ANI-003`, `EXP-0043`)

Holds for: `build/us_edition` Track 1 `8882e154…72df` (`TITLE.O`
`c3d7459c…2fb34`), in Mednafen 1.32.1, from cold boots.

Each title frame, the Deluxe wrapper checks for a 4 MiB cart: the ID
`0x24FFFFFF` reads `0x5C` four times and a non-destructive RAM test passes.
Then, once per boot, it points allocator pool 2 (live `0x06076AE8`,
baseline `0x06076AD0`) at `0x22400000`-`0x22800000` and clears the
loaded-set slots, and it sets `0x0602192A` to `A00F`. With `FULL`, every
tested mixed pair then loads two full sets (indexes 0-13) with no
out-of-memory call: Anakaris/Huitzil in both orders, and six pairs
covering the other twelve fighters. P2's set lies in cart RAM. Arcade
(round and opponent changes, continue and rematch) and VS keep full sets,
and the round timer counts down at the same rate as a no-cart CUT fight.
With no cart, a 1 MiB cart, or `CUT`, the loaded sets are stock.

Reproduce: `research/experiments/EXP-0043/README.md`.

## D-043: With Anakaris on P1, the opponent's shared sound effects play his copies; Deluxe US Enhanced fixes it (`AUD-004`, `EXP-0044`)

Holds for: US T-1208H and JP 1M T-1202G (bug), and `build/us_edition` Track
1 `33768e29…a2a4` in the US Enhanced edition (fix), in Mednafen.

For a shared sound (record type `0xFE`, type g in byte 4), the US lookup at
`0x0603A1C8` checks P1's character in the table `0x0606C10C[g]` first. It
plays P1's song from bank 1 whenever P1's character has an entry, whoever
requested it. Anakaris has entries for 17 of the 27 types, all also owned by
another character. With him on P1, Demitri's P2 fireball and dash request
bank 1 songs 1 and 8 (Anakaris's samples `462CA`, `4B172`) instead of bank 2
songs 0 and 2. Pyron's fireball, Sasquatch's and Huitzil's ice sounds, and
the CPU Victor's `g=0` sound in Arcade behave the same way. JP plays the
same wrong samples. Sound RAM itself is intact. The US Enhanced edition
replaces the 78-byte lookup so that, with Anakaris on P1, P2's character is
tried first. Every tested case then plays the requester's own sound, and
the other matchups are unchanged. Since 2026-11-26 the fix applies in
every edition (user decision; `EXP-0045`).

Reproduce: `research/experiments/EXP-0044/README.md`.

## D-044: Morrigan's Soul Fist trail is pinned left by an `and` for `or`; fixed in every edition (`AUD-005`, `EXP-0045`)

Holds for: US T-1208H and JP 1M T-1202G (bug), and `build/us_edition` Track 1
`4d70df42…4451` (fix), in Mednafen.

Before queuing her trail sound (shared types `g=2`, `g=5`), Morrigan's code
combines the screen position from `0x0603AC44` with flags using `and r4,r5`.
This happens at `0x06004BE2` and `0x06004DBA` in `PL05.O`, the same offsets
in `PL05.O2`. The `and` leaves position 0, so the trail voice plays at
DIPAN `16` (far left) wherever she stands. Every other character's matching
call uses `or`. With `or r4,r5` (`254B`) in both files, the trail pans from
her side toward the target (P1 `12` → `06`, P2 `02` → `15`), plays
centered in mono, and her other sounds are unchanged. The fix is applied
in every edition (user decision).

Reproduce: `research/experiments/EXP-0045/README.md`.

## D-045: US quote line spacing differs between discs, and program files also hold ASCII UI labels

Holds for the US T-1208H V1.001 and Japanese 1M T-1202G V1.000 images.
Both have `ST1USA.BIN` with the same 128 table pointers and the same glyph
words at every destination. The 116 differing bytes are exclusively the
low bytes of line Y positions, with shifts of −4, −8 or −12 in the US
copy. These files hold the English-format inventory. The Japanese default
loads `ST1JPN.BIN` instead (D-011, EXP-0018). The program also stores
inline ASCII menu and fight labels. `TITLE.O:0xB78` holds SOUND MODE,
`MAIN.BIN:0x409F0` holds NOW LOADING, and `MAIN.BIN:0x42A68` holds
CONTINUE on the US disc. A relative byte scan finds each at shift zero.

Evidence and reproduction: [EXP-0047](../research/experiments/EXP-0047/README.md).

## D-046: JP Enhanced selects a separate script bank and six new Japanese ending pages

The US-based Deluxe build offers E=3 in OPTION MODE. With E=3 the title
wrapper selects the Japanese region and language, writes a 508-byte
table and script bank into the part of RAM used by the unused US scripts,
and points the Japanese table literal at it. Ten Japanese script
pointers retain their stock destinations. Four point to new scripts
which use previously unused entries in the enlarged `ST2JPN.BIN`.
All six pages displayed on the expected art from a cold-boot Arcade
checkpoint. The control uses the original Japanese table on the same
checkpoint. Only JP Enhanced selects the added script bank.

Evidence, inputs, byte changes, and reproduction: [EXP-0046](../research/experiments/EXP-0046/README.md).

## D-047: The name preference can switch fighter labels independently of edition

Deluxe uses settings byte `0x060830C7` and resolves a separate name-region
flag at `0x060830C8`. Japanese name tiles appeared on the US Enhanced HUD
after a cold boot with the save retained and the quote rendered in
English. Switching to US Original preserved the saved preference and
resolved the stock US name flag. JP Enhanced accepted the US name flag
while its Japanese region and language values remained zero.

Evidence and reproduction: [EXP-0048](../research/experiments/EXP-0048/README.md).

## D-048: The stock victory quote selector has four conditions and varies its Japanese decisions

Both retail programs contain the same two language-specific selector
tables. They use winner/opponent equality first, then the winner field
at offset `0x3C0` with cutoffs at 30 and 114. The Japanese selector takes
one of eight table slots via the stock random byte. The English selector
has a single slot per condition. Their reachable record counts are
323 and 56. Matched Arcade controls on both discs reproduced the
boundary and mirror branches.

US Enhanced now uses the eight-way selector with the English renderer.
It adds one translation per fighter/condition and keeps the existing US
record in each group. Every translated ID was selected and displayed in
the combined build. The other editions retain their previous selection.

Evidence and reproduction: [EXP-0049](../research/experiments/EXP-0049/README.md).
