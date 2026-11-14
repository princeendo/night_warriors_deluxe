# Research Log

This chronological journal preserves both successful and failed work. Durable,
confirmed findings are separately summarized in `docs/discoveries.md`.

## Entry Template

```markdown
## YYYY-MM-DD HH:MM TZ — EXP-NNNN or SESSION-NNNN

Task: TASK-ID

Goal:

Observation:

Hypothesis:

Action:

Result:

Conclusion:

Next action:
```

## 2026-11-13 — SESSION-0001: repository set up

Task: ENV-001 to ENV-006, DOC-001

Goal: create the repository from the three sibling projects' method (MSHvSF,
XvSF and Cyberbots, each released), and record every supplied source image
before any research.

User request (2026-11-13, verbatim excerpt): "The purpose of this repository
is to create an "Ultimate" edition of Vampire Hunter / Night Warriors which
synthesizes the Japanese and US versions into a single image. ... Please set
up this repository in the same vein as `cyberbots_saturn_en_translation`,
`msh_vs_sf_saturn_en_translation`, and `xmen_vs_sf_saturn_en_translation`".

Action:

- Rules: `AGENTS.md` adapted from Cyberbots (`bac6fde`). Rule 13 names all
  three siblings; rule 14 adds that the two Saturn releases share nothing
  beyond what a comparison shows; rule 16 makes patch reuse wait for
  `DOC-002`; rule 21's release-asset exception is to be confirmed; rules 23
  and 24 re-anchor on difference classes; new rules 27-31 cover merging two
  releases (what establishes a difference, change types, English provenance,
  keeping US wording, naming the image).
- Scaffolding copied from Cyberbots `bac6fde`: `pyproject.toml` (renamed),
  `setup_venv.sh`, `invenv.sh`, `.gitignore`, `LICENSE`,
  `docs/research_protocol.md`, `research/README.md`,
  `research/experiments/README.md`, `research/artifact_manifest.schema.json`
  (schema ID renamed), and the agent-interface patch (SHA-256
  `c30146ef…5244`, identical to all three siblings').
- Method documents: `docs/playbook_from_mshvsf.md` is MSHvSF
  `docs/playbook_cross_game.md` at `447e573` with a header note (byte-equal
  below it; checked with `diff`). `docs/lessons_from_xvsf.md` is Cyberbots'
  copy with a header note. `docs/lessons_from_cyberbots.md` is new: a
  read-only subagent read Cyberbots' task list, log, discoveries, unknowns,
  policy, release docs, tools and history at `bac6fde` and digested what
  transferred, what did not, process, emulator and release lessons, tools,
  decisions to re-ask, and what matters for merging two releases.
- `references/web_research/`: the user's web research
  (`vampire-hunter-vs-night-warriors-saturn-research.md`, SHA-256
  `36f7b565…f5c2`), copied unchanged. `docs/difference_register.md` seeds one
  row per item of its difference register, each **UNKNOWN** on these discs.
- `local_agent_guidance.md` (ignored): Cyberbots' file retargeted to this
  repository, each preference marked as carried, to confirm in `DOC-002`.
- Tools (`ENV-003`): the game-independent tools and their tests, copied from
  Cyberbots `bac6fde` with a provenance note appended to each docstring
  (`TASKS.md` `ENV-003` lists them). Cyberbots never changed them after its
  own copy from XvSF. A first provenance note longer than 88 columns failed
  `ruff check` (32 E501); the note was rewrapped and the files re-copied.
- Checks: `./setup_venv.sh` (uv 0.11.7) first failed because `README.md`
  did not exist yet (hatchling validates the `readme` field); with a README
  it synced. `./invenv.sh pytest -q` 119 passed; `ruff check .` and
  `ruff format --check .` clean; `mypy` (strict) no issues in 49 files.

Source images (`ENV-006`):

- `~/Downloads/vh_nw_saturn/` holds three Japanese zips (1M, 2M/4M, 3M), one
  US 7z, and the research document. The zips were unzipped and the 7z
  extracted with macOS `tar -xf` (no 7-Zip is installed) into four new
  ignored folders under `local/disc_images/`. Archives and every component
  hashed (`tools.disc.hash_source --json`, logs ignored
  `local/logs/env006-hashes-*.json`); CUE and track 1 rechecked with
  `shasum -a 256`. Tables in `references/saturn_jp/README.md` and
  `references/saturn_us/README.md`.

First look at the discs (static, no emulator; every item an observation or
**HYPOTHESIS**):

- **Headers.** JP `T-1202G V1.000 19960128`, area `JT`, peripherals `J`,
  title `VAMPIRE HUNTER`. US `T-1208H V1.001 19960228`, area `U`,
  peripherals `J`, title `NIGHT WARRIORS`.
- **The Japanese pressings are one release.** Track 1 is byte-identical in
  all three (`73cc150b…4c39`). Track 2's audio is identical once aligned; the
  pressings differ by a write offset of +1 and -4 samples against 1M. The
  research's warning that the labels "alone do not establish a gameplay or
  script difference" is therefore answered for the data track. What the
  labels distinguish is left to `ENV-007`.
- **ISO 9660.** Both tracks are clean (`tools.disc.iso9660 --check`) and
  hold the same 415 files, no directories; volume ID `VAMPIRE_HUNTER` on
  both. Each was extracted to an ignored `local/extracted/saturn_*` folder.
  Listings with per-file SHA-256 are in `references/*/iso_listing.json`.
- **Comparison.** 363 files are byte-identical, including every sound file
  and sequence, the per-character data files named with the Japanese
  character names (`AULBATH.BIN`, `GALLON.BIN`, `LEILEI.BIN`, `PHOBOS.BIN`,
  `ZABEL.BIN`), the ending backgrounds, and `ST?JPN.BIN`/`ST?HIS.BIN`. 52
  differ: `0.BIN`, `MAIN.BIN`, `TITLE.O` and `P03_.SPR` change size; the
  others (`ENDING.O`, `P00.BIN`, `P03_.BIN`, 28 `PL*` overlays, 12 `SOBJ*`
  overlays, `ST1USA.BIN`, `ST2USA.BIN`) keep their size with 46 to 8,073
  bytes changed; the three ISO descriptive files are empty on the US disc.
  The US track 2 is all zeros.
- **Text.** A scan for runs of Shift-JIS kana found none in the program
  files checked; an ASCII scan for English-like runs found equal counts in
  both regions, in graphics files (noise). Where either release keeps its
  text is open (`DIFF-002`).

Hypotheses this raises (to test, not to assume):

1. The Japanese-only voices reported for Morrigan (AUD-01 to AUD-03) are on
   the US disc and not selected, since every sound file is byte-identical.
   Alternatives: the voices are not in the sound files at all (e.g. carried
   by a differing program overlay), or the report is mistaken. Test by
   tracing the sound call at the event in both releases (`AUD-001`).
2. The regional differences live mostly in program overlays (`MAIN.BIN`,
   `ENDING.O`, `PL*`, `SOBJ*`), so a merged image may need mostly code and
   table changes, not new assets. `DIFF-001` classifies the byte changes
   first.
3. `ST?USA.BIN`, `ST?JPN.BIN` and `ST?HIS.BIN` are per-language data present
   on both discs, and the US release may select the `USA` files where the
   Japanese one selects `JPN` (or they may be unrelated to language).
   `DIFF-002`.
4. The ending art (`END*.BG`) is shared; whether the US release still holds
   the epilogue text (END-01) is open. `ENDING.O` differs in 1,668 bytes of
   the same size, a lead for `END-001`.

Conclusion: Phase A is done except `ENV-007`. Nothing about Vampire Hunter's
internals is confirmed.

Next action: `DOC-002` (the base release and the sibling decisions),
`EMU-001` (Mednafen 1.32.1 from the sibling archive after a hash check),
`DIFF-001` (classify the differing files), `ENV-007`.

## 2026-11-13 — SESSION-0002: first decisions and static leads

Task: DOC-002, AUD-001, END-001, EDITION-001 (write-ups only)

Goal: record the user's first decisions and turn their two investigation
requests into tasks, with whatever a static look can add.

User decisions (2026-11-13, verbatim):

- "If we don't need all the separate JP releases, we can keep just one and
  work from that."
- "I definitely want to check the US disc for whether the Morrigan info is
  present."
- "Apparently, there are individual character story epilogue screens in the
  JP version that don't exist in the US version. We should investigate."
- "Each character has a post-ending artwork accompanied by scrolling Japanese
  text."
- "For this release, my goal is to have the "Ultimate" edition have the
  option for the user to switch between the JP original, the US original,
  and the US "Enhanced" which incorporates the missing JP pieces. If there
  are pieces in the US version which don't exist in the JP version, we can
  also create an "Enhanced" version for JP."

Action:

- Kept the Japanese 1M image; deleted `local/disc_images/vh_saturn_jp_2m4m/`
  and `local/disc_images/vh_saturn_jp_3m/` (identical data track,
  `SESSION-0001`; archives remain in `~/Downloads/vh_nw_saturn/`).
- Wrote `docs/localization_policy.md` (decisions, and what is deferred to
  which task); `DOC-002` closed with every other decision deferred by name.
- Static look (from `references/*/iso_listing.json`):
  - `MORRIGA.BIN`, `MORRIGA1.SEQ`, `MORRIGA2.SEQ` and every sound file are
    byte-identical on both discs.
  - The 14 `END*.BG` files (`END00`-`END0D`, 53,156 to 502,752 bytes) and
    `ENDDATA.BIN` (7,821 bytes) are byte-identical; `ENDING.O` is not
    (`FILE-04`).
  - Track 1's last used sector is 209,774 of 209,924 in both releases: 150
    free sectors (0.3 MiB). The 52 differing files total 2,162,163 bytes
    (JP) and 2,169,101 bytes (US).
- Wrote up `AUD-001`, `END-001` (both blocked on the M0 chain) and
  `EDITION-001` (backlog) in `TASKS.md`.

Hypotheses (to test, not to assume):

1. Morrigan's Japanese-only voices are on the US disc and the US code does
   not call them (`AUD-001`). Static evidence only shows the sound files are
   the same.
2. The `END*.BG` files are the 14 characters' post-ending artwork, present on
   both discs, and the US `ENDING.O` leaves out the scrolling text
   (`END-001`). Two of them (`END0C`, `END0D`) have the same size, so the
   count may not map one file per character.
3. An image holding both regions' editions needs more than track 1's free
   tail (`EDITION-001`).

Conclusion: both investigations need a running emulator; nothing static
settles them.

Next action: `EMU-001` (pinned Mednafen) to start the M0 chain; offline
meanwhile, `DIFF-001`.
