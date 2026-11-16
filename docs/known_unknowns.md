# Known Unknowns

Open questions about Vampire Hunter, each with its current evidence and the
smallest experiment that would answer it. Close an entry by linking the task or
experiment that answered it. Questions about a single regional difference
belong in `docs/difference_register.md` instead.

| Question | Current evidence | Smallest discriminating experiment | Task |
| --- | --- | --- | --- |
| Does the agent's RAM `write` reach the CPU when the byte is in the SH-2 data cache? | `EXP-0016`: a write to `0x06076ABE` just before the game read it was not seen (R4 = 3); earlier writes to other bytes were. Source (`EXP-0017`): the write goes straight to the RAM array and never touches the emulated cache (SUPPORTED). | Before relying on a write, log the register the game reads it into (`--log-pc`). A fix would be a Mednafen change (rule 17), not made. | tooling |
| ~~What else does the region flag control?~~ Mapped (`EXP-0015`, D-015): Japanese-only content, US renames and menu graphics, text spacing. The pause check is answered (US pauses when a pad is missing, D-016); the `TITLE.O` check is read (US: only player 1's Start begins ARCADE/VS, SUPPORTED, `EXP-0017`). Still open: `PL10` (Sasquatch?), the ending script tables (`060367A4`), `0601F17E`, and the byte `0x060808A9` that forces the JP branch of four readers. | `EXP-0015`, `EXP-0016` | Disassemble the `TITLE.O` reader; play Sasquatch with the flag cleared. | `DISC-002` |
| What does the US-only byte `0x060808A8` (= 1, set with the language byte) do? | Written once at US start-up; no other load in `MAIN.BIN` (`EXP-0013`). | Search the overlays for the literal; clear it at boot and compare. | `DISC-002` |
| Are these images verified Redump dumps, and what do the Japanese labels 1M, 2M/4M and 3M distinguish? | The three Japanese track 1s are byte-identical; track 2 differs only by a 1-4 sample offset (`references/saturn_jp/README.md`). | Compare each track's size, CRC-32, MD5 and SHA-1 with the Redump entries for both titles. | `ENV-007` |
| ~~Which cartridge setting does each release need?~~ Answered for boot and attract (D-002): none; the project keeps `ss.cart auto` (backup memory). Still open: does play or saving check for a cart? | `EXP-0002` | Note any cart message in later play sessions. | later, only if seen |
| Does Mednafen boot each release with the BIOS of its region, and does the base-image choice depend on it? | JP area `JT`, US area `U`; both BIOS files are available from the siblings. | Boot each image and read the BIOS line in the log. | `EMU-002`, `EMU-003` |
| Where and how does each release store its text? | No plain Shift-JIS kana runs in the program files checked; `ST?JPN`, `ST?USA`, `ST?HIS` files present on both discs; `MOJI.CHR`/`MOJI.TBL` by name a font (static, `SESSION-0001`). | Relative search of US files for known English; a RAM search at a text screen. | `DIFF-002`, `DBG-004` |
| What do the byte changes in the 52 differing files do? | Sizes and differing-byte counts only (`references/saturn_us/README.md`). | Classify each run as relocation or content; disassemble the code files' entry points. | `DIFF-001` |
| Why are `PL*.O` and `PL*.O2` different files that differ between regions in the same places? | Checked for `PL01` and `PL05` (`SESSION-0001`). | Compare all 14 pairs; find which is loaded when (CD command log). | `DIFF-001` |
| What is on the Japanese track 2? | About 18 s of audio; the US track 2 is silence. | Listen to it (play it as audio). | `DIFF-001` |
| What does Donovan's second region guard play? | `PL14` `0x23C4` (P1 `0x060033C4`) skips a call with code `0x1B2` in US; opened in the build, never reached in any replay or session (`EXP-0033`). | Find what reaches the block holding `0x060033C4` (log its callers), then force it from a post-KO state. | `AUD-003` |
