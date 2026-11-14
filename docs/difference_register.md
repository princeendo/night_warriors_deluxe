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
| NAM-01 | Title | Vampire Hunter becomes Night Warriors; subtitle kept. | Header title `VAMPIRE HUNTER` | Header title `NIGHT WARRIORS`; ISO volume ID still `VAMPIRE_HUNTER` | renamed (header only so far) | — | UNKNOWN on screen | `REF-004` |
| NAM-02 | Fighter names | Gallon/Jon Talbain, Zabel Zarock/Lord Raptor, Aulbath/Rikuo, Phobos/Huitzil, Lei-Lei/Hsien-Ko. | — | File names keep the JP names on both discs | — | — | UNKNOWN | `REF-004`, `LOC-001` |
| NAM-03 | Supporting name | Anita is Amanda in the Western localization. | — | — | — | — | UNKNOWN | `REF-004` |
| NAM-04 | Supporting name | Lin-Lin/Mei-Ling: only a lead for later games. | — | — | — | — | UNKNOWN | `REF-004` |
| END-01 | Post-ending epilogue | JP epilogue text over the scrolling character art is absent from export; the art scroll remains. | The user: post-ending artwork with scrolling Japanese text, per character (2026-11-13) | 14 `END*.BG` and `ENDDATA.BIN` byte-identical on both discs; `ENDING.O` differs in 1,668 bytes (static) | — | PSP gallery (to verify) | UNKNOWN | `END-001` |
| END-02 | Main endings | Rewritten, different page counts (arcade lead). | — | — | — | — | UNKNOWN | `END-001` |
| END-03 | Pyron's ending | English: consuming Earth; JP: collecting planets (reported). | — | — | — | — | UNKNOWN | `END-001` |
| QUO-01 | Victory quotes | Inventories and selection differ (arcade lead; English has health and mirror conditions). | — | — | — | — | UNKNOWN | `QUO-001` |
| AUD-01 | Morrigan normal throw | Extra JP voice sample (Saturn report, from memory). | — (report from memory) | Sound files, `MORRIGA.BIN` and `MORRIGA*.SEQ` byte-identical on both discs (static) | — | — | UNKNOWN | `AUD-001` |
| AUD-02 | Morrigan command throw | Extra JP voice sample (same report). | — (report from memory) | Sound files, `MORRIGA.BIN` and `MORRIGA*.SEQ` byte-identical on both discs (static) | — | — | UNKNOWN | `AUD-001` |
| AUD-03 | Morrigan bat-seat win pose | Full JP spoken line (same report). | — (report from memory) | Sound files, `MORRIGA.BIN` and `MORRIGA*.SEQ` byte-identical on both discs (static) | — | — | UNKNOWN | `AUD-001` |
| AUD-04 | Donovan victory audio | Extra JP victory sounds (arcade lead). | — | as AUD-01 | — | — | UNKNOWN | `AUD-001` |
| ANI-01 | Sasquatch victories | JP pose/sound differences (arcade lead); a US Saturn guide documents a hidden pose. | — | — | — | — | UNKNOWN | `AUD-001` |
| BIO-01 | Manual biographies | US manual has character stories; JP/US booklet comparison outstanding. | — | — | — | — | UNKNOWN (off-disc) | `REF-003` |
| SYS-01 | Appendix/settings | Present under both titles; not a JP-only feature (reported). | — | — | — | — | UNKNOWN | `REF-004` |
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
| FILE-08 | `ST1USA.BIN`, `ST2USA.BIN` | same sizes; 116 and 8,073 bytes differ; their `JPN` and `HIS` siblings are identical | UNKNOWN | UNKNOWN | `DIFF-001`, `DIFF-002` |
| FILE-09 | `VH_ABS.TXT`, `VH_BIB.TXT`, `VH_CPY.TXT` | emptied on the US disc | ISO descriptive files, presumably never shown in game | UNKNOWN | `DIFF-001` |
| FILE-10 | Track 2 | JP: about 18 s of audio; US: silence | UNKNOWN (probably the CD-player warning) | UNKNOWN | `DIFF-001` |
