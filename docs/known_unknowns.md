# Known Unknowns

Open questions about Vampire Hunter, each with its current evidence and the
smallest experiment that would answer it. Close an entry by linking the task or
experiment that answered it. Questions about a single regional difference
belong in `docs/difference_register.md` instead.

| Question | Current evidence | Smallest discriminating experiment | Task |
| --- | --- | --- | --- |
| Are these images verified Redump dumps, and what do the Japanese labels 1M, 2M/4M and 3M distinguish? | The three Japanese track 1s are byte-identical; track 2 differs only by a 1-4 sample offset (`references/saturn_jp/README.md`). | Compare each track's size, CRC-32, MD5 and SHA-1 with the Redump entries for both titles. | `ENV-007` |
| Which cartridge setting does each release need? | Both headers' peripheral field reads `J`; no cart evidence yet. | Cold boots with `ss.cart` `none`, `backup`, `extram1`, `extram4` per release. | `EMU-004` |
| Does Mednafen boot each release with the BIOS of its region, and does the base-image choice depend on it? | JP area `JT`, US area `U`; both BIOS files are available from the siblings. | Boot each image and read the BIOS line in the log. | `EMU-002`, `EMU-003` |
| Where and how does each release store its text? | No plain Shift-JIS kana runs in the program files checked; `ST?JPN`, `ST?USA`, `ST?HIS` files present on both discs; `MOJI.CHR`/`MOJI.TBL` by name a font (static, `SESSION-0001`). | Relative search of US files for known English; a RAM search at a text screen. | `DIFF-002`, `DBG-004` |
| What do the byte changes in the 52 differing files do? | Sizes and differing-byte counts only (`references/saturn_us/README.md`). | Classify each run as relocation or content; disassemble the code files' entry points. | `DIFF-001` |
| Why are `PL*.O` and `PL*.O2` different files that differ between regions in the same places? | Checked for `PL01` and `PL05` (`SESSION-0001`). | Compare all 14 pairs; find which is loaded when (CD command log). | `DIFF-001` |
| What is on the Japanese track 2? | About 18 s of audio; the US track 2 is silence. | Listen to it (play it as audio). | `DIFF-001` |
