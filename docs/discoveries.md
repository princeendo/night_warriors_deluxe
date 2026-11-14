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
