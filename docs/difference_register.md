# Regional Difference Register

The inventory this project closes: every way the Japanese release (T-1202G)
and the US release (T-1208H) differ, with both regions' evidence. The project
is complete when every row is resolved (merged, deliberately left, or proven
not a difference) against the images named in `references/saturn_jp/` and
`references/saturn_us/`, not when a large number of items has been merged
(`AGENTS.md` rules 27-31).

## How To Use It

- **Seeded rows** come from the user's web research
  (`references/web_research/vampire-hunter-vs-night-warriors-saturn-research.md`,
  2026-11-13, SHA-256 `36f7b565…f5c2`), keeping its IDs (`NAM-01`...). Its
  labels ("Regional finding", "Saturn report", "Arcade lead") are about web
  sources; on these discs every seeded row starts **UNKNOWN**.
- **Static rows** (`FILE-nn`) come from the byte comparison of the two data
  tracks (`references/saturn_us/README.md`). A file that differs is a fact; what
  the difference does is **UNKNOWN** until traced.
- A row is resolved by a recorded comparison (`AGENTS.md` rule 27). Then fill
  in the change type (rule 28), the English donor and its provenance (rule
  29), and the decision.
- Add a row for every new difference found; never delete one. Split a row when
  one lead turns out to be several differences.

Change types: **omitted**, **rewritten**, **renamed**, **reordered**,
**retimed**, **conditionally suppressed**, **asset absent**, **not a
difference**.

## Seeded From The Web Research

| ID | Area | Lead (from the web research) | JP evidence | US evidence | Change type | English donor | Status | Task |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| NAM-01 | Title | Vampire Hunter becomes Night Warriors; subtitle kept. | Header `VAMPIRE HUNTER`; title screen `VAMPIRE HUNTER` / `Darkstalkers' Revenge` (`EXP-0001`) | Header `NIGHT WARRIORS`; title screen `NIGHT WARRIORS` / `Darkstalkers' Revenge`; ISO volume ID still `VAMPIRE_HUNTER` | renamed | — | CONFIRMED on the title screen | `REF-004` |
| NAM-02 | Fighter names | Gallon/Jon Talbain, Zabel Zarock/Lord Raptor, Aulbath/Rikuo, Phobos/Huitzil, Lei-Lei/Hsien-Ko. | Cast roll: GALLON (`EXP-0010`) | Cast roll: JON TALBAIN, HSIEN-KO (`EXP-0010`); file names keep the JP names. Both releases hold both name sets; the region flag picks one (GALLON with the flag cleared in US RAM, D-015) | renamed | — | CONFIRMED in the cast roll | `REF-004`, `LOC-001` |
| NAM-03 | Supporting name | Anita is Amanda in the Western localization. | — | — | — | — | UNKNOWN | `REF-004` |
| NAM-04 | Supporting name | Lin-Lin/Mei-Ling: only a lead for later games. | — | — | — | — | UNKNOWN | `REF-004` |
| END-01 | Post-ending epilogue | JP epilogue text over the scrolling character art is absent from export; the art scroll remains. | Morrigan: epilogue paragraph over her art (`EXP-0010`), from `ST1JPN.BIN` in `MOJI` codes (`EXP-0011`) | Morrigan: same art, no text. Same code; epilogue flag 2 (JP 0) means no `ST1` file is loaded; clearing it in RAM and loading `ST1JPN` shows the Japanese epilogue after the English ending (D-012); `ST1USA.BIN` holds the US win quotes and only placeholder epilogue records (`EXP-0018`); the flag and language are constants in the US `MAIN.BIN` start-up (D-013); a 15-byte disc patch shows the Japanese epilogue in the US release (D-017, M2) | conditionally suppressed | PSP gallery (to verify) or new translation | CONFIRMED for Morrigan (D-010, D-011, D-017); 13 characters open | `END-001` |
| END-02 | Main endings | Rewritten, different page counts (arcade lead). | — | — | — | — | UNKNOWN | `END-001` |
| END-03 | Pyron's ending | English: consuming Earth; JP: collecting planets (reported). | — | — | — | — | UNKNOWN | `END-001` |
| QUO-01 | Victory quotes | Inventories and selection differ (arcade lead; English has health and mirror conditions). | — | — | — | — | UNKNOWN | `QUO-001` |
| AUD-01 | Morrigan normal throw | Extra JP voice sample (Saturn report, from memory). | Sample `50C2C` plays at every throw (`EXP-0009`, waveform search) | Never in the whole US recording, including an observed throw; sample present; one of four flag-guarded voice calls in `PL05` (SUPPORTED, `EXP-0014`) | conditionally suppressed | — | CONFIRMED (D-008) | `AUD-001` |
| AUD-02 | Morrigan command throw | Extra JP voice sample (same report). | Sample `41220` plays as Morrigan carries the opponent up (Vector Drain) (`EXP-0008`) | Never in the whole US recording (`EXP-0009`); no US Vector Drain identified yet | conditionally suppressed (SUPPORTED) | — | SUPPORTED | `AUD-001` |
| AUD-03 | Morrigan bat-seat win pose | Full JP spoken line (same report). | Pose plays Morrigan sample `56D60` (`EXP-0008`, dense) | Pose plays none of her samples; the sample is in sound RAM, identical (`EXP-0008`); clearing the epilogue flag in US RAM makes the pose play it (D-014) | conditionally suppressed | — | CONFIRMED (D-007, D-014) | `AUD-001` |
| AUD-04 | Donovan victory audio | Extra JP victory sounds (arcade lead). | — | as AUD-01; lead: `PL14` (Donovan by roster order, HYPOTHESIS) makes two sound calls only when the region flag is 0 (`EXP-0015`) | — | — | UNKNOWN | `AUD-001` |
| ANI-01 | Sasquatch victories | JP pose/sound differences (arcade lead); a US Saturn guide documents a hidden pose. | — | — | — | — | UNKNOWN | `AUD-001` |
| BIO-01 | Manual biographies | US manual has character stories; JP/US booklet comparison outstanding. | — | — | — | — | UNKNOWN (off-disc) | `REF-003` |
| SYS-01 | Appendix/settings | Present under both titles; not a JP-only feature (reported). | — | — | — | — | UNKNOWN | `REF-004` |
| SYS-02 | Who can start a game from the title menu | Found in `EXP-0015`, not in the web research. | Code: either player's Start begins ARCADE or VS (flag 0) | Code: only player 1's Start does (region flag, `TITLE.O` `0x06005138`) | conditionally suppressed (US-only behaviour, region flag) | — | SUPPORTED (code, `EXP-0017`) | `DISC-002` |
| TTL-01 | Title copyright lines | Found in `EXP-0017`, not in the web research. | Code: two lines, "CAPCOM CO., LTD. 1994, 1995, 1996" / "ALL RIGHTS RESERVED." (drawn when the flag is 0) | Code: three lines, adding "CAPCOM U.S.A., INC. 1994, 1995, 1996" (chosen by the language byte) | rewritten | — | SUPPORTED (code, `EXP-0017`) | `DISC-002` |
| INT-01 | Intro logo card | Found in `EXP-0001`, not in the web research. | Second 38-39 of a cold boot: a red hand-drawn logo starting "VAM" being drawn on black (`EXP-0002` 038; `EXP-0001` 038 caught a white flash of it) | Second 39: a red `DARKSTALKERS` logo card | rewritten (HYPOTHESIS: the Japanese card spells the Japanese title) | — | SUPPORTED as a difference (one-second sampling) | `REF-004` |
| SYS-01 | Controller removed during a fight | Found in `EXP-0015`, not in the web research. | Plays on with port 1 empty (`EXP-0016`) | Pauses at once; plays on if the region flag is cleared in RAM (D-016) | conditionally suppressed (US-only behaviour, region flag) | — | CONFIRMED (D-016) | `DISC-002` |
| AUD-05 | Morrigan hurt voice | Found in `EXP-0008`, not in the web research. | Sample `4F10C` plays when Morrigan is hit (1 s states) | Never in the whole US recording (`EXP-0009`) | conditionally suppressed (SUPPORTED) | — | SUPPORTED | `AUD-001` |
| OTHER-01 | Everything else | Opening/attract, menus, credits, blood, presentation, music, mechanics, loading/saves, hidden content: no comparison yet. | — | — | — | — | UNKNOWN | `REF-004`, `DIFF-001` |

## Static Differences Between The Data Tracks

From `references/saturn_us/README.md` (2026-11-13). Both discs hold the same
415 file names; these rows are the 52 files whose bytes differ.

| ID | Files | Observation | What it does | Status | Task |
| --- | --- | --- | --- | --- | --- |
| FILE-01 | `0.BIN` | +456 bytes in US | UNKNOWN (boot program, by name) | UNKNOWN | `DIFF-001` |
| FILE-02 | `MAIN.BIN` | +6,496 bytes in US | UNKNOWN | UNKNOWN | `DIFF-001` |
| FILE-03 | `TITLE.O` | +316 bytes in US | UNKNOWN (title screen, by name) | UNKNOWN | `DIFF-001` |
| FILE-04 | `ENDING.O` | same size, 1,668 bytes differ | UNKNOWN; lead for END-01/END-02 | UNKNOWN | `DIFF-001` |
| FILE-05 | `P00.BIN`, `P03_.BIN`, `P03_.SPR` | 1,179 and 46 bytes differ; `P03_.SPR` +288 bytes | UNKNOWN | UNKNOWN | `DIFF-001` |
| FILE-06 | `PL01`-`PL14` `.O`/`.O2` | 28 files; same size except `PL08` (-60) and `PL09` (+16) | UNKNOWN; per-character by count (14) | UNKNOWN | `DIFF-001` |
| FILE-07 | `SOBJ01`-`SOBJ12.O3` | same sizes, 55-215 bytes each | UNKNOWN | UNKNOWN | `DIFF-001` |
| FILE-08 | `ST1USA.BIN`, `ST2USA.BIN` | same sizes; 116 and 8,073 bytes differ; their `JPN` and `HIS` siblings are identical | `ST1JPN.BIN`: Japanese epilogue text (D-011); `ST2JPN`/`ST2USA`: main-ending dialogue per language (`EXP-0011`); `ST1USA`/`ST1HIS`/`ST2HIS`: not loaded at the ending, purpose UNKNOWN; `ST1USA` is not English text | UNKNOWN | `DIFF-001`, `DIFF-002` |
| FILE-09 | `VH_ABS.TXT`, `VH_BIB.TXT`, `VH_CPY.TXT` | emptied on the US disc | ISO descriptive files, presumably never shown in game | UNKNOWN | `DIFF-001` |
| FILE-10 | Track 2 | JP: about 18 s of audio; US: silence | UNKNOWN (probably the CD-player warning) | UNKNOWN | `DIFF-001` |
