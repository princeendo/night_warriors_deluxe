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
