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
