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

## 2026-11-13 — SESSION-0003: stock Mednafen (EMU-001)

Task: EMU-001

User request (2026-11-13): "Yes, start EMU-001".

Action: copied `mednafen-1.32.1.tar.xz` (`cp -c`) from Cyberbots'
`local/downloads/`; size 3,571,236 and SHA-256 `de7eb94a…3832` equal the
siblings'. Extracted with `bsdtar` to `vendor/mednafen/src/`; configured and
built in `vendor/mednafen/build/` with the siblings' flags (`docs/mednafen.md`).
`configure` 30 s, `make -j12` 2 min 31 s, both exit 0. Ran `-help` with
`MEDNAFEN_HOME=local/mednafen`.

Result: binary `vendor/mednafen/build/src/mednafen`, 21,318,680 bytes, SHA-256
`de542817…582a` (differs from Cyberbots' build on macOS 26.7.2, as
expected). Banner: Mednafen 1.32.1 with the `ss` module; exit 255 for
`-help`, as in every sibling. `grep` of `src/ss/` finds no database entry for
`T-1202G` or `T-1208H`.

Conclusion: `EMU-001` done. Nothing was downloaded or installed.

Next action: `EMU-002` (homes; both BIOS files from Cyberbots), then
`EMU-003` cold boots with the user present.

## 2026-11-13 — SESSION-0004: project-local Mednafen homes (EMU-002)

Task: EMU-002

User request (2026-11-13): "Yes, start EMU-002".

Action: copied `sega_101.bin` and `mpr-17933.bin` (`cp -p`) from Cyberbots'
ignored `local/mednafen/firmware/`; `cmp` clean; SHA-256 `dcfef4b9…deac` and
`96e106f7…266f`, both equal to Mednafen 1.32.1's `Documentation/ss.html`. Ran
`./invenv.sh python -m tools.mednafen.home` twice (first: quiet home created,
three quiet settings set; second: no change). Ran `-help` with each home.

Result: each home loads 7,904 settings, 0 unknown. `mednafen.cfg` hashes
`48a7cf6b…28fc` (interactive) and `ef89728…5019` (quiet) equal Cyberbots' and
XvSF's; the diff is the three quiet settings. Details and launch commands for
both releases in `docs/mednafen.md`.

Open: whether a volume-0 home still records sound (matters for `AUD-001`);
which BIOS each release boots with (`EMU-003`).

Next action: `EMU-003`, cold boots of both releases with the user present.

## 2026-11-13 — EXP-0001: cold boots of both releases (EMU-003)

Task: EMU-003

User request (2026-11-13): "Yes, boot them now".

Hypothesis: stock Mednafen with the silent home cold-boots each untouched
image to its title with no input, on its own region's BIOS, the same way each
time.

Action: three 120 s no-input boots per release with
`tools.mednafen.cold_boot`, `sav/` emptied before each, source manifests
before and after (`research/experiments/EXP-0001/README.md`).

Result: all six exit 0; logs show `T-1202G`/`JT`/`0x1` and
`T-1208H`/`U`/`0x4`, both `Cart: Backup Memory`; frames byte-identical within
each release; titles from about 63 s; sources unchanged. Mednafen's code
(`ss.cpp` BIOS selection and sanity check) ties region `0x1` to
`sega_101.bin` and `0x4` to `mpr-17933.bin`. The intro differs at second 39
(a red `DARKSTALKERS` card in the US release, a white screen with a dark mark
in the Japanese one): new register row `INT-01`.

Conclusion: CONFIRMED (D-001). `cold_boot.py` re-validated on Vampire Hunter.

Next action: `EMU-004` (cart settings), `EMU-005` (pad), `EMU-006`
(screenshots and states), with the user present.

## 2026-11-13 — EXP-0002: cart settings on boot and attract (EMU-004)

Task: EMU-004

User request (2026-11-13): "Yes, start EMU-004".

Hypothesis: neither release needs an extended-RAM cart for boot and attract.

Action: one 120 s no-input boot per release with `ss.cart` `none`,
`extram1`, `extram4` (`EXP-0001` stands for `backup`, which `auto` chose);
pinned config restored after each; source manifests before and after.

Result: the three settings give byte-identical frames within each release
and differ from `EXP-0001` only by sub-second timing (agent-reviewed); no
warning; sources unchanged. Bonus: Japanese frame 038 shows a red logo
starting "VAM" where the US shows `DARKSTALKERS`, refining `INT-01`.

Conclusion: CONFIRMED for boot and attract (D-002). `ss.cart auto` kept.

Next action: `EMU-005` (pad) and `EMU-006` (screenshots and states).

## 2026-11-14 — SESSION-0005: pad bindings (EMU-005)

Task: EMU-005

User request: "Yes, start EMU-005".

Action: copied the 13 port 1 gamepad bindings from Cyberbots' interactive
config (equal to XvSF's) into both homes with `tools.mednafen.home
--bindings-from`; second run `no change`; both configs now byte-identical to
the siblings' (`docs/mednafen.md`). Opened Night Warriors (US) in the
interactive home; the log found the bound controller (`0xecccd365…0000`,
"PS4 Controller"). The user tried each button in the game's options.

Result (the user, 2026-11-14): "Everything but L/R worked, but that's
expected. You can anticipate the emulator is working just fine." L and R stay
on Mednafen's keyboard default. The config was unchanged after the run.

Conclusion: `EMU-005` done. The user's second sentence is recorded as a
working preference in `local_agent_guidance.md` ("Emulator Trust").

Next action: `EMU-006` (screenshots and save/load states).

## 2026-11-14 — EXP-0003: screenshots and states by hotkey (EMU-006)

Task: EMU-006

User request: "Yes, start EMU-006".

Hypothesis: F9, F5 and F7 work in both releases, and a reloaded title state
reproduces the title screenshot.

Action: per release, a cold boot with `--keep-focus` (F9 title, F5, F9
attract, F7, F9, F9) and a fresh boot loading that state (F9, F7, F9, F9).

Result: states of about 1.6 MB, unchanged by loading. Japanese post-load
screenshot equals the title shot in the same session; US post-load
screenshot in a fresh boot equals the US title shot. One post-load F9 in
jp-b was lost; in us-b the F12 was not acted on within 30 s and the tool
stopped Mednafen with SIGTERM (no leftover process, no timing record). The
`NOW LOADING` screen after the title is byte-identical in both releases.

Conclusion: CONFIRMED (D-003). `hotkeys.py` re-validated, with the siblings'
known key losses.

Next action: `EMU-007` (stock debugger dumps), kept minimal before
`EMU-020`/`EMU-021`.

## 2026-11-14 — EXP-0004: stock debugger (EMU-007)

Task: EMU-007

User request: "Yes, start EMU-007".

Hypothesis: in each release the stock debugger dumps both work-RAM banks
repeatably, writes and restores memory, and halts on a WRAM-H write.

Action: Cyberbots' `EXP-0004` step files (same actions; freeze at 65 s) per
release: run A (two dumps per bank, write test, state) and run F (write
breakpoint over WRAM-H, window captures).

First attempt (01:19): the user used the computer meanwhile ("I'm pretty sure
I messed you up, sorry"); the Japanese run A wrote no dumps and its F12 timed
out. Stopped all runs (no process left; settings and sources unchanged),
moved the output to `local/emu007/disturbed/`. The user: "Yes, rerun now".

Result (rerun, 01:22-01:29): all four runs exit 0; per release, identical
1 MiB dump pairs for each bank, the write test reads back pattern then
original, and the breakpoint halts on a stack store into WRAM-H (Japanese PC
`0605186C`, US PC `06000864` in an `INT47` handler). Same-instant states kept
for `DBG-001`.

Conclusion: CONFIRMED (D-004). Hotkey runs need the user hands-off.

Next action: `EMU-020` (put the agent-patch reuse question to the user);
`DBG-001` can run offline meanwhile.

## 2026-11-14 — SESSION-0006: why stock is not enough (EMU-020)

Task: EMU-020

Question to the user: "Reuse the siblings' Mednafen agent-interface patch
here (EMU-020)?" Answer (2026-11-14): "Yes, reuse it".

Action: wrote `docs/mednafen_agent_interface.md`: the siblings' evidence
(MSHvSF `EMU-012`/`EMU-020`, XvSF and Cyberbots `EMU-020`), this project's
own (`EXP-0003`: a lost F9, an F12 ignored for 30 s; `EXP-0004`: a disturbed
run that wrote no dumps, registers read by eye), and why `AUD-001` and
`END-001` need machine-readable reads, writes, breakpoints and registers.
The MSHvSF protocol reference is copied below it (via Cyberbots `bac6fde`).
Recorded the decision in `docs/localization_policy.md`.

Conclusion: `EMU-020` done.

Next action: `EMU-021`: build the patch on a copy of the stock source and
run V1-V4 on both releases.

## 2026-11-14 — EXP-0005: agent interface built and validated (EMU-021)

Task: EMU-021

User request: "Yes, start EMU-021".

Action: patched a copy of the stock source (`src-agent/`), built it in
`build-agent/` (31 s + 2 min 17 s, exit 0, no warnings from patched files);
V1 equivalence boots without the agent directory; `EXP-0005/validate.py`
(adapted from Cyberbots `EXP-0006`) per release; `mcs_extract` of each V2
state.

Result: binary `7826b9b9…f887`. Both releases: 119/119 boot frames equal
stock; four agent reads equal the extractor's output of the same-poll state;
write round trip exact; halt control as designed; log mode 462/517 hits;
halt mode stops with registers. Both WRAM-L reads also equal `EXP-0004`'s
stock WRAM-L dumps. The V4 code addresses differ between releases by a
constant `0x70` (HYPOTHESIS: shifted code, for `DIFF-001`).

Conclusion: CONFIRMED (D-005). Agent output may be used as evidence.

Next action: `DBG-001` (extractor against stock dumps of the same instant,
offline).

## 2026-11-14 — EXP-0006: extractor against stock dumps (DBG-001)

Task: DBG-001

User requests: "Yes, start DBG-001"; then, for the video-RAM run, "Yes, run
it now".

Action: extracted WRAM-L/H from `EXP-0004`'s same-instant states (both byte
orders) and compared with its stock dumps; one key-driven run per release
(Cyberbots' run-H steps, freeze at 65 s) dumped all four regions with a
same-instant state; compared both byte orders.

Result: with the `saturn` order every region equals its stock dump at every
instant in both releases; the unswapped order differs everywhere.

Mistake, corrected: the first unswapped comparison named `<region>.bin`
instead of `<region>.state-order.bin` (missing files read as "differs"), and
a zsh loop did not split its pairs. Redone in Python; the corrected result is
in the experiment.

Conclusion: CONFIRMED (D-006). M0's tool checks are done; `AUD-001` and
`END-001` are ready.

Next action: `AUD-001` or `END-001`, in the user's order.

## 2026-11-14 — EXP-0007: recorded Morrigan sessions (AUD-001)

Task: AUD-001

User request: "Morrigan voices first". The user asked how to do the command
throw; looked up (StrategyWiki, Night Warriors moves): Vector Drain is a
half-circle back + medium or heavy punch, close.

Action: `EXP-0007/session.sh` ran the patched Mednafen with `-soundrecord`
and the session recorder (a state every second, a screenshot every half
second) for each release in turn; the user played Morrigan.

Result: about 7 minutes per release (Japanese: Victor and Bishamon beaten;
US: Victor beaten, Bishamon unfinished after the controller disconnected).
The bat-seat win pose appears in both releases. The user: "Morrigan seemed
to have some more dialogue in the JP version." The sound driver is Sega's
standard `SDDRVS` Ver1.33b; `MORRIGA1.SEQ` looks like a 23-sequence bank
(HYPOTHESIS).

Mistakes: the first contact sheets used ffmpeg `drawtext`, which this build
lacks; rebuilt without labels.

Next action: replay states before the bat-seat pose (then the throws) in
each release with sound-command logging.

## 2026-11-14 — EXP-0008: which Morrigan samples each release plays (AUD-001)

Task: AUD-001

User request: "Yes, run it" (replay the saved moments and log the sounds).

Action and dead ends: sound-RAM logging per frame (`sndlog.py`) found a
busy area at `0x700`-`0x7BF` (not decoded). Reading the SCSP slot registers
through the agent's `physical` space at `0x25B00000` returned only zeros:
the debugger does not map them. Save states hold them (`[SCSP] SlotRegs`),
so `slots.py` reads active slots from states and `dense.py` saves a state
every ~4 frames while a replay runs.

Result: both releases load `MORRIGA.BIN` at sound RAM `0x3B2C0`. The Japanese
bat-seat pose plays Morrigan sample `0x56D60`; the US pose plays none of her
samples, though the bytes are identical in its RAM (D-007). Over the whole
sessions (1 s states), Morrigan samples `50C2C` (close grab), `41220` (air
carry, Vector Drain) and `4F10C` (being hit) appear only in the Japanese
session.

Mistake, corrected before commit: the experiment record first said the pose
frames in the replays came from reviewed screenshots; `dense.py` takes none.
The timing now cites the session screenshots.

Next action: locate US throws (session screenshots) and replay matched
Japanese and US throws densely; then trace what selects each sample.

## 2026-11-14 — EXP-0009: Morrigan's samples in the recordings (AUD-001)

Task: AUD-001

User request: "Yes, confirm throws".

First attempt: a live slot logger saving a state every 4 frames during play
(`live.py`). The user: "I already did this. Why are we doing it again?" and
"It's going to be hard to do this. The game is very obviously stuttering
from what you're doing." Stopped it (no process left; settings unchanged).
Lesson: no frequent state saves during user play.

Action: matched-filter search (`wavsearch.py`, ffmpeg `afir`) of the
`EXP-0007` WAV recordings for each Morrigan sample at the pitch read from its
slot registers, with a control sample both releases play.

Result: the four Japanese-only samples occur in the Japanese recording (the
throw voice five times, two more than the states showed) and never in the US
recording; the control occurs in both. A US throw is visible at frames
4,263-4,313 with no throw voice. Normal-throw voice CONFIRMED suppressed
(D-008); Vector Drain and hurt voices SUPPORTED.

Next action: find what selects each sample, or switch to `END-001` as the
user prefers.

## 2026-11-14 — EXP-0010: forcing Morrigan's ending (END-001)

Task: END-001

User request: "Switch to epilogues".

Static first: the `ENDING.O` differences are 1-2 byte changes with
recurring deltas (−0x50 and others): relocated addresses, not new content
(HYPOTHESIS). `ENDDATA.BIN` starts with an ID/offset table.

Action: found the stage byte by comparing WRAM-H of stage-1 and stage-2
states (`0x0608097B` JP, `0x0608092B` US; the same layout `0x50` apart).
Found the fighters' vitality (max 144). Dead end: zeroing the opponent's
vitality before the KO does not KO him (a KO is checked on a hit), and the
input-free replay let Bishamon win. Working method: from the state just
after the won KO, write 9 to the stage byte; the ending plays (D-009).

Result: Morrigan's ending in both releases, frame-matched. The Japanese
release shows an epilogue paragraph over her scrolling artwork; the US
release scrolls the same artwork with no text (D-010). The cast roll uses
each release's names.

Next action: find where the Japanese epilogue text comes from and whether
the US disc holds it.

## 2026-11-14 — EXP-0011: the epilogue text's source (END-001)

Task: END-001

User request: "Yes, check the disc".

Action and dead ends: no Shift-JIS on either disc. Diffing VDP1/VDP2 VRAM
between the releases was too noisy (art at different positions). Searching
for runs of font codes matched graphics everywhere (codes are small
numbers). What worked: `MOJI.CHR` (a 1,026-glyph 16x16 font) sits in VDP1
VRAM in both releases; the Japanese epilogue frame draws 213 glyph sprites,
the US one none; the first row's codes, looked up in `MOJI.TBL`, occur once
in Japanese RAM and once on each disc, in `ST1JPN.BIN` at `0xE20`.

Result: `ST1JPN.BIN` (identical on both discs) is loaded only by the Japanese
release at the ending; the US release loads `ST2USA.BIN` (English ending
dialogue) and no `ST1` file. The epilogue text is on the US disc (D-011).
`ST1USA.BIN` is not English text; its purpose is open.

Next action: the other 13 endings, then the code that chooses the text
files.

## 2026-11-14 — EXP-0012: the epilogue switch (END-001)

Task: END-001

User request: "Find the switch".

Action: found the `ST1`/`ST2` name tables and pointer arrays in `MAIN.BIN`,
the ST1 loader (language byte × 4 into the array) and, with a PC breakpoint
in a forced Japanese ending, its caller: it skips the loader when a flag
byte is non-zero. Read both bytes in every state: Japanese 0/0, US 1
(language) and 2 (flag).

Tests in US RAM, one change at a time: language 0 mid-ending stalls the
English dialogue (dead end); language 0 at the emblem does nothing (no file
loaded); language 0 from the KO gives the Japanese main ending but still no
epilogue; flag 0 loads `ST1USA.BIN`, drawn as rows of "A" (placeholder);
flag 0 plus the USA array entry pointed at `ST1JPN` loads it but draws no
text in English mode; then language 0 from the emblem card shows the
Japanese epilogue after the English main ending (D-012).

Note: this is the M1 outcome reached inside `END-001` before the formal
`GATE-M0` GO; flagged to the user.

Next action: where the bytes are set; other endings; English epilogue format.

## 2026-11-14 — GATE-M0 GO and M1

User request: asked "Count this as M1 reached, with your GO recorded now?",
the user answered "Yes, record GO".

Action: recorded the GO in `TASKS.md` (`GATE-M0` DONE; `DIFF-003` and
`DBG-002` to `DBG-004` closed for `END-01` Morrigan with their evidence from
`EXP-0010` to `EXP-0012`; `RE-001` done) and in
`docs/localization_policy.md`. Deviation recorded: the GO followed the first
RAM change instead of preceding it, and `REF-004` was not done.

Next action: write up the M2 tasks (`DISC-001`: where the epilogue flag and
language byte are set; `DISC-002`: the same result from a rebuilt US image).

## 2026-11-14 — EXP-0013: where the two bytes are set (DISC-001)

Task: DISC-001

User request: "Yes, trace them" (start M2 by tracing where the epilogue flag
and language byte are set).

Action: wrote up `DISC-001` and `DISC-002`. Static cross-reference
(`EXP-0013/xref.py`) of every program file: the only stores are in the US
`MAIN.BIN` start-up routine (`mov #2` / `mov #1` constants). Boot write
watches (`EXP-0013/boot_watch.py`, 1,800 frames, exact one-byte ranges) on
both releases: after `MAIN.BIN` clears its work area, US writes flag 2 and
language 1 once (PC `0x06012128`, `0x0601212E`); Japanese writes neither.
A first US run with 4-byte windows also caught a settings copy writing the
neighbouring bytes; superseded by the exact runs (D-013).

Commands: `ruff check` and `ruff format --check` on `EXP-0013/` pass;
`xref.py` self-check passes.

Lead: the flag is read by `TITLE.O`, `SOBJ08.O3` and `PL05`/`PL10`/`PL14`,
so clearing it from boot may change more than the epilogue (known unknowns).

Next action: `DISC-002`, the epilogue from a patched US image.

## 2026-11-14 — EXP-0014: the flag's other readers (DISC-002, AUD-001)

User request: "Check other readers".

Action: matched `PL05.O` to Morrigan's code (player-1 slot in her Victor
fights, both releases). Listed every flag reader (`EXP-0014/readers.py`):
four in `PL05` and two in `PL14` skip a sound call when the flag is
non-zero; `PL10`, `TITLE.O`, `SOBJ08.O3` (tests 4) and about 20 `MAIN.BIN`
readers (mostly a choice between two tables) not yet explained. Controlled
run from US `f00011016`: flag 0 vs no write, WAV search for the bat-seat
sample: present at 5.02 s (0.73) with the flag cleared, absent in the
control; same pose in both (D-014).

Commands: `ruff check`/`format` on `EXP-0014/` pass.

Not explained: the portrait-frame colour and confetti differ between the two
runs (not tested whether random).

Next action: decide with the user whether to map the `MAIN.BIN` table
readers before the one-byte patch, or patch first and compare screens.

## 2026-11-14 — EXP-0015: mapping the region flag's readers (DISC-002)

User request: "Map them first".

Action: PC census (`EXP-0015/pc_census.py`) of the 21 US `MAIN.BIN`
readers from power-on (7,200 frames) and over the 411 US session states (60
frames each, 7 min 42 s); named each screen from the session screenshots.
Read every reader and compared its table pair: name graphics, name
positions, fight-display name tiles (US entries differ for characters 2, 4,
9, 11, 13: the renamed five), MODE SELECT graphics, Japanese punctuation
spacing, US glyph substitutions, ending script tables, a pause check, three
readers that act only on value 4. All checked tables are also in the
Japanese `MAIN.BIN`. Continued the `EXP-0012` flag-cleared ending to the
credits: the cast roll shows GALLON where the unpatched US run shows JON
TALBAIN (D-015).

Commands: `ruff check`/`format` on `EXP-0015/` pass.

Not tested: the win, loading, fight and MODE SELECT screens with the flag
cleared (no renamed character in the session); the pause check; `PL10`.

Next action: `DISC-002`, a patch that opens only the Japanese-only branches.

## 2026-11-14 — EXP-0016: the region flag's pause check (DISC-002)

User request: "Check pause first".

Action: read the fight-frame routine `0x0601D474` and the pad routine
`0x06013C20`. First test, `--onhit` writing `0x06076ABE` = 0 before the
read: no effect; a trace showed the routine still read 3 (HYPOTHESIS: the
SH-2 data cache hides agent writes; recorded in known unknowns). Second
test, port 1 set to no device (`-ss.input.port1 none`): US pauses at once
(logged: pad missing, flag 2, pause toggled); US with the flag cleared plays
on (flag-0 branch, neither PC reached); Japanese plays on (D-016). New
register row `SYS-01`.

Tools: `EXP-0010/force.py` gained `--onhit`, `--log-pc` and `--setting`;
`ruff check`/`format` pass.

Mistake: the Japanese run logged a US address; its log is not used.

Next action: `DISC-002`, opening only the Japanese-only branches.

## 2026-11-14 — EXP-0017: the region flag's title check (DISC-002)

User request: "Check title test first".

Action: found `TITLE.O` loaded at `0x06001000` in the title-menu WRAM-H
(US state `f00001903`), and read the flag readers of both `TITLE.O` files.
US: with the flag set, only player 1's Start begins ARCADE or VS. Japanese:
the flag selects whether two copyright lines are drawn; the US file picks
two or three lines (adding CAPCOM U.S.A.) by the language byte. Register
rows `SYS-02`, `TTL-01` (SUPPORTED).

Not run: the input test needs a player-2 Start press, which the agent cannot
send without a new mapping and a focus-taking key press. Read
`src-agent/src/ss/debug.inc`: the agent's write bypasses the emulated SH-2
cache, which explains `EXP-0016`'s failed write.

Next action: `DISC-002`.

## 2026-11-14 — EXP-0018: the epilogue from a patched US image (DISC-002)

User request: "Yes, build it".

Scope: the epilogue only (`END-01`, the first difference class); Morrigan's
voices are a second class (`AGENTS.md` rule 23) and wait for their own task.

Action: found why D-012 needed the language switch: text files declare their
own slot; `ST1JPN.BIN` declares the JP slot while the English-mode epilogue
routine (shared with win quotes) reads the US slot. Read the two `ENDING.O`
flag tests (card sequence; epilogue length `0x564` vs `0x384`). Built
`build/us_enhanced_epilogue/` with five byte changes
(`EXP-0018/build_epilogue.py`); verified only those bytes differ and all
209,924 sectors pass EDC/ECC. Rehearsal (old state + two RAM writes for the
`MAIN.BIN` changes): English ending, then the Japanese epilogue, then the
credits, language byte 1 throughout.

Fault found: Mednafen persisted `ss.input.port1 none` from `EXP-0016` into the
quiet config; the first rehearsal paused and the `EXP-0016` Japanese pad
control had no pad. Restored the config; `force.py` now restores it after each
run; reran the Japanese control (identical to the port-1-empty run);
corrected `EXP-0016`.

Next action: the user plays one match as Morrigan on the patched image
(`EXP-0018/session.sh`); then force the ending and compare with the
unpatched image.

## 2026-11-14 — EXP-0018: cold boot of version 1 fails; version 2 (DISC-002)

User request: "Yes, start it" (one match as Morrigan on the patched image).

Result: the user won 2-0 vs. Sasquatch from power-on; the win-quote screen
showed Morrigan's **Japanese** win quote. DISPROVEN: "`ST1USA.BIN` is only a
placeholder and the `ST1` name array is used only by the ending" (EXP-0012,
EXP-0018 version 1). The array is read by the `ST1` loader `0x0603790E`,
which `MAIN.BIN` also calls from `0x06014208` and `0x0601E16C` with no flag
test; `ST1USA.BIN` is the US win-quote file (SUPPORTED).

Action: version 2 leaves the array alone and makes the ending's call load
`ST1JPN.BIN` directly (two single-use literals and two instructions at
`0x0603B902`-`0x0603B9E8`; see EXP-0018). Rebuilt (Track 1 `93ca264c…`), 15
bytes differ, sectors valid. Rehearsed from the session's bonus-screen state
with version 2's code in RAM: English win quote; forced ending shows the
English ending, then the Japanese epilogue, then CAST.

Next action: a cold boot of version 2 with one match won as Morrigan
(`EXP-0018/session.sh`, same path), then the forcing and the unpatched
control.

## 2026-11-14 — EXP-0018: cold boot of version 2, M2 reached (DISC-002)

User request: "Yes, start it" (one match as Morrigan on version 2).

Result: the user won 2-0 vs. Victor from power-on; the win quote is English.
From the bonus-screen state `f00007741`, the ending forced with the stage
byte only (`--steps 420`) shows the English main ending, the emblem card,
the Japanese epilogue, the art, and the cast roll with US names. Control
(unpatched image, unpatched won-KO state `f00011016`, same forcing): the
same ending and cast roll, the art with no text. CONFIRMED (D-017);
`DISC-002` DONE, M2 for `END-01` (Morrigan).

Not checked: the other 13 endings; what the `ENDING.O` card branch
(`0x0600CFCC`) adds (the card shows in the control too); the screens served
by the other two `ST1` load sites.

Next action: the other 13 endings under `END-01`.

## 2026-11-14 — EXP-0019: every character's ending (END-001)

User request: "Yes, do the endings" (the other 13 endings on version 2).

Found: the ending reads its character from `0x0608096E`, copied from
`0x06080980` (player 1's character) at `0x0601DC7A` after the KO (write logs;
`force.py --log-write` added). Writing `0x06080980` = N with the stage byte
at Morrigan's won-KO state plays character N's ending.

Result: `all_endings.sh` ran 26 runs (version 2 and the unpatched control for
N = 1-14 but 5, 420 steps each). Every version 2 run shows N's English
ending, N's Japanese epilogue over N's art, and the US cast roll; every
control shows the art without text. CONFIRMED (D-018).

DISPROVEN: the roster order I assumed (11 Hsien-Ko, 13 Huitzil); the endings
and the control win screens give 11 Huitzil, 13 Hsien-Ko.

Not checked: endings after a real fight as each character; the Japanese text
line by line against the Japanese release (only Morrigan's was); the card
branch `0x0600CFCC`.

Next action: decide what remains of `END-001` before a second difference
class (rule 23).

## 2026-11-14 — EXP-0020: the PSP Chronicle's English epilogues (REF-002)

User request: try the PSP *Chronicle* image before a new translation. The
ISO was not in `~/Downloads/vh_nw_saturn` but in the repository root
(ignored); moved unchanged into `local/disc_images/psp_chronicle_us/`
(SHA-256 `c465f42d…` before and after), identity SUPPORTED (ULUS-10005).

Tried and failed: a search for character names in plain and shifted 8/16-bit
encodings over every file found only the menu text in `mess00.bin`; the
epilogue text is not character data.

Result: `movie/hunend/HmovieNN_2.pmf` shows an English epilogue drawn into
the video for all 14 characters (D-019). Read against the Saturn Japanese
epilogues (EXP-0019 frames), each tells the same story, mostly shortened;
Lord Raptor's and Sasquatch's change the meaning, Bishamon's and Rikuo's
change details (SUPPORTED, a reading by meaning). Agent transcription kept
locally (`local/ref002/psp_epilogues/transcript.md`, not committed).

Not checked: the `_1` movies (main endings) and `hun2end`; whether the PSP
English was made from the Saturn or the arcade Japanese; a second reading of
the transcription.

Next action: `GATE-TRANSLATION` needs the user's GO on the PSP text and its
policy (typos, changed meanings); meanwhile the `END-001` leftovers.

## 2026-11-14 — EXP-0021: the `0x0600CFCC` branch and the glyph strip (END-001)

Static reading of the US `ENDING.O` flag-0 path (`0x0600CFCE`-`0x0600D02C`):
a scroll set-up, a per-character call (`0x06037D46`) and a 416-pass loop.
Logged PCs, version 2 vs. unpatched under the `EXP-0018` forcing: version 2
runs the loop 416 times on consecutive frames (6,140-6,555); unpatched never
enters it. On screen, version 2 and the Japanese release (`EXP-0010`) show
the paragraph rising onto black before the art; unpatched starts the art
straight after the card. CONFIRMED (D-020). The "card sequence" label in
`EXP-0018` was wrong and is corrected (the patch bytes are unchanged).

The emblem-card glyph strip from `EXP-0012` is absent from both releases and
from the build; closed without an experiment, cause UNKNOWN.

Next action: review `END-001` against its acceptance criteria (`END-02`,
`END-03` rows).

## 2026-11-15 — GATE-TRANSLATION: the user's decisions for the epilogue English

User request: "Discuss the PSP GO". Four questions asked; answers (all the
recommended option): the PSP English for all 14 epilogues; spelling and
missing-word slips fixed and logged; names as the US Saturn spells them;
line breaks free, any cut or rewording asked first. Recorded in
`docs/localization_policy.md` and the `GATE-TRANSLATION` block. The gate
stays `BLOCKED` on `DOC-003` alone.

Next action: `DOC-003` (reference catalogue).

## 2026-11-15 — DOC-003 done; GATE-TRANSLATION open for the epilogues

User request: "Yes, do DOC-003". Wrote `docs/references.md`: platform
sections copied from Cyberbots `cf9f6d0` (`diff` shows them identical), the
MAME 0.289 CPS-II sets of this game (read from the sibling's pinned
`cps2.cpp`, SHA-256 `a8c09ef8…`, which matches the MSHvSF record), the web
research's 23 sources with permitted and forbidden uses, and the sources by
kind. No source was re-read or downloaded. With `DOC-003` done,
`GATE-TRANSLATION` is open for the `END-01` epilogue scope only.

Next action: `END-002` (the US English-mode epilogue text format, then one
character's PSP English).

## 2026-11-15 — END-001 closed, END-002 started; EXP-0022 Latin text in the epilogue

User request: "Yes, start END-002". `END-002` needed `END-001` done; asked,
the user chose "Split END-02/03 out": `END-001` closed for the epilogues,
rows `END-02`/`END-03` moved to a new `END-003` after `END-01` reaches M5.
`END-002` written as a full task.

Static: `ST1USA.BIN` holds English win quotes in a Latin set (capitals ASCII
+ `0x80`, lowercase `0201`-`021A`) that `MOJI.TBL` partly lacks; the
epilogue records are x, y, `0001`, codes, `FFFF`/`0000`.

EXP-0022: three lines of Morrigan's record replaced in place by PSP English
on the version 2 image. They show in English, in the win-quote font, over
her art (CONFIRMED, D-021). First run had comma and period swapped: the
right codes are comma `00AE`, period `00AC` (checked in `ST1USA.BIN`);
script fixed and rerun.

Tried and rejected: assuming ASCII + `0x80` for every mark (comma and period
differ). Not found: how the game picks a character's record (the table at
`0x0C` does not point at line starts).

Next action: a read trace of the record lookup; then Morrigan's whole
paragraph.

## 2026-11-15 — EXP-0023: record lookup and the 238-glyph limit (END-002)

`force.py --log-read` added. Read trace: the epilogue record is found
through a self-relative table at `ST1JPN.BIN` `0x0C` (index = roster − 1);
the ending reads only the header, that entry and the record (D-022).

Built Morrigan's whole PSP paragraph as a new record in the unread part of
`ST1JPN.BIN` (`EXP-0023/build_en_epilogue.py`, text read from the local
transcript). It shows in English but stops at the 238th non-space
character, the length of the longest Japanese epilogue. The glyph list at
`0x060839D4` (8 bytes a glyph, no bound) runs into an area that a VDP1
command builder rewrites every frame (write log). All 14 English epilogues
are 263-345 glyphs.

Correction: the `EXP-0022` script had three PSP lines hard-coded, against
rule 21 (pushed in `e5f37e0`); they now live in an ignored local file and
the rebuild is byte-identical. The pushed history keeps those three lines.

Next action: find RAM unused during the ending (write log over a candidate
area) and move the list there; no text cut without the user.

## 2026-11-15 — EXP-0024: room for an English epilogue

User request: "Yes, move the list". The 238 limit is the slot count of
fixed sprite arrays drawn each frame (`0x06083344` × 128, `0x06083744` ×
128, `0x06083B44` × 192); the epilogue list started at array 2 slot 82.
Logs and a WRAM-H dump showed arrays 1-2 empty during the epilogue except 18
player sprite slots (blank, off screen, rewritten every frame).

Tried and failed: (1) a forced test without writing the code change into RAM
(`MAIN.BIN` is loaded at boot; a state keeps the old literal); (2) starting
the list in array 1: the whole paragraph drew, but the first 111 characters
under the art (array 1 is drawn before it).

Result: list at array 2 slot 0 with an off-screen filler line over the
player slots: Morrigan's whole English epilogue on top of her art (D-023).
302 characters of room: 4 of 14 English epilogues fit.

Next action: more room (draw order, or the player slots) before asking for
any trims; cold boot of Morrigan's build with the user present.

## 2026-11-15 — EXP-0025: array 1 redrawn on top; room for all 14

User request: "Yes, find more room". A PC log showed the per-frame order in
the ending: array 1 (general routine, before the art), then arrays 2-3
through `ENDING.O`'s `r12` (`0x06020766`). No dead space in `ENDING.O`, so a
36-byte routine goes in `ST1JPN.BIN`'s unread tail (loaded at `0x060CB408`):
it calls `0x06020766`, then the reader for array 1 slots 17-127. `r12`'s
literal points at it through the cache-through mirror.

Result: Morrigan unchanged and whole; Anakaris (345 characters, 18 lines at
12 px) whole on top of the art; both runs continue through the cast roll
(CONFIRMED, forced, D-024). Room: 413 characters.

Not checked: a cold boot; the routine's area after the cast roll; spacing
13 vs 12 per character.

Next action: all 14 in one image (criterion 4 of `END-002`).

## 2026-11-15 — EXP-0026: all 14 English epilogues in one image

User request: "Yes, build all 14". Built with per-character spacing (13 px
up to 16 lines, else 12 px). First run: Demitri, Rikuo and Pyron crashed
after the card. DISPROVEN: the routine is overwritten (a write log showed
only the file load). Found: `ST1JPN.BIN` loads at a per-character heap
address (Pyron `0x060C7C14`), so the fixed `r12` target was wrong for them.
Fix: `r12` = @`0x06091E48` (the loader's slot-`0x1BC` table pointer) + the
routine's offset, computed in the three instructions freed by `EXP-0018`.

Result: all 14 forced endings show the whole English paragraph on top of the
art and reach the cast roll (D-025). Frame picker added
(`EXP-0026/pick_text_frame.py`).

Next action: cold boot of the all-14 image with the user present.

## 2026-11-15 — EXP-0027: the cold boot showed a blank win quote

User request: "Yes, start it" (cold boot of the all-14 image). The user won
Demitri vs. Victor and reported: "The win quote was blank." Screenshots agree.

Cause (CONFIRMED): the win screens share the epilogue's text builder and the
glyph-list literal at `0x06037A98`, which `EXP-0025` changed on disc. My
`EXP-0024`-`EXP-0026` tests only covered the ending (forced from states),
so they could not see it.

Tried and failed: swapping the literal only around the routine's call to
`0x06020766` (the builder does not run there; epilogues cut at 238 again).
A PC log showed the builder runs once, between the routine's first and
second calls. Fix: set on the first call (flag in the routine's data),
restore on later calls; `MAIN.BIN` untouched. Win quote English, Pyron,
Anakaris and Morrigan whole, literal restored after the ending (D-026).

Lesson: a change to a file loaded at boot must be checked on every screen
that uses the same code, not only the one it was made for.

Next action: second cold boot with the user present.

## 2026-11-16 — EXP-0028: cold boot of the fixed image; END-002 done

User request: "Yes, start it" (second cold boot). The user beat Victor with
Demitri; the win quote is English. From the session's bonus-screen state
`f00007427`, all 14 endings forced with the stage and character bytes only:
every one shows its whole English epilogue on top of the art and reaches
the cast roll (D-027). `END-002` DONE: M5 for `END-01`.

`all_en.sh` now takes `STATE` and `OUT` and no longer writes the `MAIN.BIN`
literal (unneeded since `EXP-0027`).

Next action: the user chooses the next class (`EDITION-001`, `END-003`,
`AUD-002`).

## 2026-11-16 — EXP-0029: main endings, forcing in Japanese and the scripts

User request: "Main endings" (`END-003`, written up as a full task).

Found: the Japanese ending character is `0x060809D0` (US + `0x50`; dump,
then all 14 Japanese endings forced; Pyron's shows Pyron). `MAIN.BIN` has a
per-character ending script table per region (`0x0605B1C0` JP, `0x0605B730`
US); decoded all 28 (`EXP-0029/scripts.py`): page counts differ for 12 of
14 (D-028). Pyron's closing line differs in meaning (SUPPORTED).

Tried and failed: (1) a text-band extractor over screenshots (missed most
pages; deleted); (2) the epilogue builder's PC (`0x060379BC`) does not read
main-ending text; (3) `ST2USA.BIN` is not resident in RAM as a file during
an ending (only Demitri's record found). The page-id-to-record mapping stays
UNKNOWN.

Corrected: `EXP-0011` called `ST2USA.BIN` ASCII; most records are Latin-code
line records like `ST1USA.BIN`, a few are ASCII.

Next action: per-page content in both regions (read `ST2USA`, draw
`ST2JPN`), then classify the extra pages.

## 2026-11-16 — EXP-0030: the main endings page by page

User request: "Yes, continue". `ST2USA.BIN` decoded (both record kinds;
`EXP-0029/st2_text.py`), `ST2JPN.BIN` drawn from `MOJI` (`draw_st2jpn.py`).
Page ids map to entries directly except Demitri (+0x10) and Pyron (+0x60),
found by content. All 14 compared by meaning (D-029): a free rewrite
re-paginated for English; Morrigan's alone loses Japanese text; Felicia,
Bishamon, Huitzil, Pyron change in meaning. Japanese forced runs checked for
the right character. `END-003` DONE.

Not checked: pictures asset by asset; the PSP main-ending movies
(`HmovieNN_1`) as an English donor; the code path of the page-id offset.

Next action: the user decides what, if anything, US Enhanced restores here.

## 2026-11-16 — User decisions on the main endings

User request: "Discuss restoring some". Three questions; answers (all the
recommended option): restore only Morrigan's missing lines; English from the
PSP main-ending movies first; minimal change. Recorded in
`docs/localization_policy.md`, the `GATE-TRANSLATION` block, and a new task
`END-004`.

## 2026-11-16 — EXP-0031: Morrigan's missing main-ending lines

User request: "Yes, start END-004". PSP `Hmovie04_1` read: it reuses the US
English, no lines to borrow. The user chose a new translation for both lines.

Space: `ST2USA.BIN` tail `0x418`-`0x4BD` free (unused table entries and an
unreferenced "A" record). DISPROVEN as free: `MAIN.BIN` zero run at
`0x0606CA5D` (an ending buffer). Used: her Japanese script slot (134 bytes,
unread with flag 2) for the new US script.

First build: pages after the insert ran late, the last one over the emblem
card (pictures keep their own timeline). Measured the scene windows in the
control and shortened pages 33-36 so both new lines sit in the butler scene
and later pages keep their times. Forced: in step (D-030). Win quote, Pyron,
Anakaris unchanged (text-page timings; shots differ by animation phase only).

Next action: cold boot with the user.

## 2026-11-16 — EXP-0031 cold boot; END-004 done

User request: "Yes, start it". The user played Morrigan and beat Victor;
English win quote. From the bonus-screen state `f00007111`, her ending
(stage byte only) shows the two restored lines in the butler scene and the
rest as shipped; Pyron's epilogue unchanged. `END-004` DONE.

Next action: the user chooses `EDITION-001` or `AUD-002`.

## 2026-11-16 — EXP-0032: Morrigan's voices (AUD-002)

User request: "Morrigan's voices". `AUD-002` written as a full task. The
four guards in `PL05.O` (and `PL05.O2`, same offsets): `bf` at `0x1490`,
`0x1A1E`, `0x3342`, `0x5280`. With all four made `nop` in RAM and the flag
left at 2, the bat-seat line plays at her win (5.021 s, score 0.734, as
`EXP-0014`); one at a time, only `0x06002490` does it. Built the image
(`EXP-0032/build_voices.py`). US/JP `PL05.O` differ only in address
literals.

Next action: cold-boot play session (throws, Vector Drain, hurt, win).

## 2026-11-16 — EXP-0032: Morrigan's voices from a cold boot; AUD-002 done

User played the voices image (Morrigan vs. Jon Talbain) after I explained
the inputs (my first request listed the moves without saying how; the user
pointed this out). All four voices found at their events in the recording
(throw 174.4 s 0.405, hurt 204.4 s 0.586, Vector Drain 249.2 s 0.661, win
261.0 s 0.731). Offline replays tie throw, Vector Drain and win to their
guards; the hurt replay did not repeat the hit (no inputs), so it is by
elimination. Win quote English. `session.sh` now records sound.

Next action: the user chooses (`EDITION-001`, or the rest of the roster's
voices and poses).

## 2026-11-16 — AUD-003 started: Donovan and Sasquatch

User request: "Other characters' voices". Only `PL05`, `PL10`, `PL14` and
`SOBJ08.O3` read the region flag. `PL14` (Donovan by roster order,
HYPOTHESIS): two guarded sound calls like Morrigan's; opened in
`EXP-0033/build_donovan.py` (Track 1 `64344d58…`). `PL10` (Sasquatch,
HYPOTHESIS): six readers choosing routines and object settings, not sounds
alone; not patched yet.

Next action: play sessions (Japanese reference and patched US) as Donovan.

## 2026-11-16 — EXP-0033: Donovan sessions

Two sessions with the user (Japanese, patched US), Donovan beating Victor.
`PL14` is Donovan's code. The Japanese replay runs the guarded sound block
at his win (frame 180); the US replay never enters it (flag 2 or cleared),
and opening the guards changes no sample. DISPROVEN for this match: that the
guards alone hold back his win sound. Open: why the block is not entered in
the US match (pose or state; the tested variable is `00` US / `01` JP).
`dense.py` gained an image argument and RAM writes.

Next action: more US wins as Donovan, or trace what enters the block.

## 2026-11-16 — EXP-0033: offline trace, Donovan's guarded sound found

User request: "Trace it offline first". The earlier entry's DISPROVEN was
wrong: the US state `f00007677` is about 80 frames before the KO and a
replay sends no input, so the replayed round never ended (shots: timer
58 → 38, Victor standing). Corrected.

From post-KO US states `f00007737`, `f00007794`, `f00007851` (patched image,
`force.py --log-pc 06002088 --log-pc 0600211E --log-pc 060033C6`, 60 × 15
frames): each runs the state routine 8 times and the first guarded call
once, as the Japanese replay did; the second guarded call never.
`dense.py us f00007737 400`, patched vs guards restored in RAM: identical
samples except `0x5687A` (patched frame 189, restored never); the Japanese
run plays the same `0x5687A` (frame 177) after the shared `0x1B4B2`. Its
bytes are at the same sound-RAM address in both regions. D-032.

Slip: running two `dense.py` at once fails (the second left an empty
folder); run them one after the other.

Next action: a cold boot of `build/us_en_donovan` with the user, playing
Donovan to a win; then Sasquatch (`PL10`).

## 2026-11-16 — EXP-0034: Sasquatch's win-pose chooser (static)

User choice: "Sasquatch first" (before Donovan's cold boot). The six `PL10`
flag readers are one state machine (`0x060044FC`) choosing a win pose: in
US, poses 0 and 4 skip spawning effect objects and pose 1 becomes pose 5.
Pose 4 needs the pad word `0x0708` at the choice; the button table
`0x0606792C` reads it as Up + A + B + C (bit order HYPOTHESIS). Not run.

Next action: Sasquatch sessions with the user, Japanese 1M and US original.

## 2026-11-16 — EXP-0034: Sasquatch sessions, replays and build

Sessions with the user (`local/aud004/jp-session`, `us-session`, stock
images): Sasquatch beat Victor 2-0 in each, holding Up + A + B + C; the pad
word read `0x0708` and both releases took pose 4 every round. Forced poses
(RAM writes to the chooser) from `us f00007802` and `jp f00007249`: US flag
2 lacks the snow creatures and sample `0x53116` in poses 0, 1, 4 and plays
pose 5 for 1; flag 0, or the six `nop`s alone, match the Japanese. Build
`build/us_en_sasquatch` (Track 1 `e6e81ccc…`), checked loaded from disc from
`us f00003511`. D-033. The lead's "steam" pose is not region-gated.

Commands: `EXP-0034/README.md`. Tests: `pytest` and `ruff` pass.

Next action: one cold boot of `build/us_en_sasquatch` with the user, a win
as Donovan and a win as Sasquatch (`AUD-003` criterion 3).

## 2026-11-16 — AUD-003 cold boot: Donovan and Sasquatch confirmed

Session with the user on `build/us_en_sasquatch` (`local/aud004/cold-session`):
Donovan beat Victor 2-0, lost to Bishamon, continued as Sasquatch, beat
Bishamon 2-0. In live RAM all eight guards (`PL14` two, `PL10` six) read
`0009`. Sasquatch round 1 (random pose 1): the shy pose and snow creatures
on screen; replay from `f00017787` plays `0x53116`. Donovan: the first
post-KO replay (`f00005029`) never reached the guarded call. Reading the
chooser: the call follows only pose 0, a win after the first round (round
counter `0x0608096A`); round 2 from `f00007017` plays `0x5687A` 8 frames
after `0x1B4B2`, and not with the guards restored. AUD-003 DONE.

Tests: `pytest` 119 passed; `ruff` clean.

Next action: the user chooses (`EDITION-001`, or Donovan's second guard).

## 2026-11-16 — EXP-0035 / DIFF-001: how the 52 files differ

User request: "Edition switch design". `EDITION-001` depends on `DIFF-001`
(READY), so that ran first. `tools/disc/diff_files.py` (new, 4 unit tests):
overlays relinked against their region's `MAIN.BIN` (four repeated pointer
deltas, few content words); `.O2` = `.O` relinked `+0x8000`; boot, main and
title changed as code; `P00`/`P03_` data. JP copies of all 52: 1,075
sectors against 150 free. Slips: the empty `VH_*.TXT` broke the decoder; an
entry-table check stopped on out-of-range offsets in `PL08`/`PL10`/`PL11`
(now counted, not decoded).

Next action: `EDITION-001` options to the user.

## 2026-11-16 — EDITION-001 decided

Options put to the user (`AskUserQuestion`) with `EXP-0035`'s costs: both
code sets (+1,075 sectors, boot-time choice, loader UNKNOWN) or one code set
switched at run time (US code in Japanese mode; US code changes stay;
`P00`/`P03_` maybe needed); chooser at boot, boot menu, or saved options;
JP Enhanced or not. Answers: "No, one code set"; "Options menu, saved";
"Yes". Recorded verbatim in `EDITION-001` and the edition policy.
`EDITION-002` (implementation) and `EDITION-003` (JP Enhanced scope)
added as BACKLOG.

Next action: the user chooses between `EDITION-002` and `EDITION-003`.

## 2026-11-16 — EDITION-003 decided: what JP Enhanced adds

From the register, the US-only candidates put to the user: the US main
endings' added lines and pages (`EXP-0030`), the pause on a missing pad
(D-016), win-quote differences (not yet compared, `QUO-001`). Answers:
"US-only ending lines"; "Hide until it differs (Recommended)". `END-005`
added (BACKLOG; needs a `GATE-TRANSLATION` decision for new Japanese text).

Next action: the user chooses (`EDITION-002`, or `END-005`).

## 2026-11-16 — EDITION-002 started (EXP-0036): settings block

User request: "Yes, start EDITION-002". The save (`N_WARRIORS_`, 512 bytes)
is the 0x104-byte block at `0x060830B4` plus stack leftovers; load, unpack,
pack and save routines read from `MAIN.BIN`. Bytes `0x11`-`0x17` are not
used by unpack or pack; replays from power-on, a fight and a win show only
boot clears and the block copy there. Plan for the run-time edition in
`EXP-0036`. Slip: two `force.py` runs printed "no such file" because
`events.log` is only written on a hit (no hits = no access).

Next action: a session where the user opens the options screen and changes
one setting (write watch on `0x0608089F`), to find the screen's code.

## 2026-11-16 — EXP-0036: the options screen found

Two sessions with the user (`options_watch.py`, write watches in the live
game). First: the watched four variables never changed outside the unpack
(the change was elsewhere). Second, with the block and the routines logged:
unpack on entering the menu (`0x0603612E`), pack on Start from `TITLE.O`
(`0x060052B4`); the save differed only in block byte `0x08` (1 → 3), filled
from `0x060809C6`, which `TITLE.O` edits at `0x0600547C`. The options
screen is in `TITLE.O`, cursor `0x0608086C`, handlers from `0x060052B8`.

Next action: how the menu draws its lines (to add an EDITION line).

## 2026-11-16 — EXP-0036: how the options lines are drawn

Third session (screenshots and states each second). Labels are ASCII in
`TITLE.O`, drawn by `0x06018A1A` (x, y, colour, string). OPTION MODE lines
16 px apart from y 40; APPENDIX (cursor 9, y `0xB8`) is drawn only when
`0x06080A2B` (saved, block `0x5D`) is non-zero: an unlock, 0 here, which is
why the user saw no APPENDIX. A new EDITION line fits only by moving the
exit line down, or on the hidden APPENDIX screen.

Next action: the user chooses where the EDITION line goes.

## 2026-11-16 — EXP-0037: room for the edition switch

Zero-run scan of 90 states (boot, matches, endings, menus): no free WRAM-L,
and in WRAM-H only the system area below `0x06001000` and the stack's
reach. Disc room after each file measured (`TITLE.O` 740 bytes,
`ENDING.O` 1,456, `MAIN.BIN` 240). The RAM after `ENDING.O` is used during
endings. While the title runs, `0x06009565`-`0x0600FFFF` stays zero (only
`0x06009564` is used after `TITLE.O`). Design: title-time code applies the
edition and patches `MAIN.BIN`'s RAM. Not proven free yet.

Next action: a write/read watch on that range across boot, title, options
(with a save) and a match start.

## 2026-11-16 — EXP-0037: title-time RAM confirmed free

Read/write watch on `0x06009565`-`0x0600FFFF` (`local/edition002/free-watch`):
BIOS clears at boot, then nothing through the title, OPTION, a change and a
save; the first access is `MAIN.BIN` `0x0604EC34` at the match start
(player 2's overlay load). EXP-0037 DONE.

Next action: the edition values and the default for saves without the
byte (user), then build the switch.

## 2026-11-16 — EXP-0038: edition switch build design

User request: "Yes, build it". Inventory of the static US Enhanced
changes and an edition-aware form for each (EXP-0038). Findings on the
way: `ENDING.O` calls `0x06007BBC(1)` twice in a row (a frame-wait loop),
so one call with 2 frees 6 bytes for an edition test plus the late-routine
pointer; header slots `0x1BE`/`0x1BF` belong only to the never-loaded HIS
files, so `ST2HIS.BIN`'s place (14,336 bytes with its room) can hold the
English epilogue file and `0x1BE` its routine pointer. Nothing built yet.

Next action: let `patch_image.py` grow a file within its room; then the
build in stages, each tested in replays.

## 2026-11-16 — EXP-0038: patcher grows files; title hook found

`patch_image.py --grow` (tested). The title and options screens draw their
text once; a boot replay runs `TITLE.O` slot `0x4D9` (`0x060032A4`) every
title frame from `MAIN.BIN`'s title-mode table, a hook point needing only
a `TITLE.O` header change. Slip: a force.py run with 34 `--log-pc` values
logged nothing; nine at a time works.

Next action: confirm slot `0x4D9` runs on the options screen and after a
game; then write the apply routine and the EDITION line.

## 2026-11-16 — EXP-0038: relocation works; the title task is the hook

`patch_image.py --relocate` (tested) moves a file into track 1's 150 free
tail sectors. With Start held by an on-hit RAM write, a relocated
`TITLE.O` (with a marker) loads like the stock one: the game follows the
directory entry. The real per-frame title hook is the title task
`0x06004FAC` (slot `0x4D7`); the earlier `0x060032A4` is attract mode.
Slips: `force.py` keeps no states to read RAM from, so RAM checks use a
small agent script; replays without input never reach the title.

Next action: write the apply routine and wrapper; test by holding Start.

## 2026-11-16 — EXP-0038: the apply routine works

`title_code.py` builds the wrapper and apply routine (568 bytes) into a
relocated `TITLE.O`. A replay holding or pulsing Start never reaches the
title menu (attract demo), so the test wrote the code and the task slot
pointer into RAM over the user's title-menu state `0026`: each edition
byte gives the expected flag, language, C, slot `0x1BE` and `MAIN.BIN`
patches. Slip: the "ST2HIS.BIN" string is at `0x0605B780` (fixed).

Next action: the EDITION line and its input, then the overlay and ending
changes and the English file.

## 2026-11-16 — EXP-0038: EDITION line written; needs a live test

Draw and input routines for the EDITION line added to `title_code.py`
(920 bytes in all). Simulated presses (on-hit pad writes) reach the task's
pad read but move no cursor, stock or patched (an input gate not traced),
so the line is tested live: `build/exp0038_menu_test` (stock US plus the
new `TITLE.O`).

Next action: a session with the user on that image (OPTION, move to
EDITION, left/right, Start).

## 2026-11-16 — EXP-0038: the EDITION line works live

Session with the user on `build/exp0038_menu_test`: the line shows in
OPTION MODE's blank slot, the cursor reaches it, left/right change E, and
the apply routine switches flag, language, C and the `MAIN.BIN` patches
at once (E 2 → JP original values; E 0 → US Enhanced); Start saves E.
Not seen: the APPENDIX-unlocked layout.

Next action: the overlay literals (C), `ENDING.O`'s edition test and frame
wait, the English file in `ST2HIS.BIN`'s place; then the full build.

## 2026-11-16 — EXP-0038: full build; endings correct per edition (forced)

`build_edition.py` builds from the stock image (`build/us_edition`). Forced
Morrigan endings with the title code's RAM writes per edition: US original
stock, JP original Japanese with its epilogue, US Enhanced with restored
lines and, once the boot-time directory cache entry for the relocated
`ST2HIS.BIN` is written too (states from stock sessions cache the old
entry, `0x060709EC`), the English epilogue on top of the art.

Next action: a cold boot of `build/us_edition` with the user: choose each
edition in OPTION and win a match; endings forced from those states.

## 2026-11-16 — EDITION-002 done: cold boot in three editions

Session with the user on `build/us_edition`: three Morrigan wins, one per
edition. The edition applies on each title load; restored voices play in
US Enhanced and JP original (wavsearch), a replay shows the US original
guard skipping the bat-seat call; forced endings from each match: English
epilogue with restored lines, stock US, Japanese with GALLON. D-034.

Next action: the user chooses (`END-005` for JP Enhanced, Donovan's second
guard, a release, or the remaining register rows).

## 2026-11-16 — EXP-0039: Donovan's second guard

User choice: "Donovan's second guard". Static: the guard ends an action
starter that needs Donovan's `+0x228` = 1 and is called after a
punch + same-strength-kick check. Live session (JP) with the call logged:
4 fires, all while his sword was planted. Replays injecting light punch +
light kick reproduce it in exactly the planted states; `dense.py` shows
the only flag-dependent sample is `0x4F2EA`. Code identical in both
releases. D-035. Tools: `options_watch.py` `pc:` arguments; `dense.py`
on-hit writes. The user asked for a move list; inputs were given as
generic motions (no verified Donovan list on hand).

Next action: the user chooses.

## 2026-11-16 — Project renamed Night Warriors Deluxe

User request: rename the project "Night Warriors Deluxe" (built on Night
Warriors; not aiming to include everything, e.g. all of the PSP release).
Changed: `AGENTS.md` goal line, README title and a sentence on the name,
the edition policy (decision row, verbatim), `pyproject.toml` name,
description and authors, `uv.lock` (`uv lock --offline`: the package entry
only), the schema `$id`. Unchanged: provenance notes naming the repository
as it was when code was copied, past log entries, the GitHub repository
and local folder names (`vampire_hunter_ultimate`). Tests: 125 passed.
Then, at the user's request ("Rename both"), the GitHub repository was
renamed `princeendo/night_warriors_deluxe` (as `princeendo`, not the work
account active in `gh`; GitHub redirects the old URL), `origin` repointed,
and the local folder moved to `/Users/colinwhite/workspace/personal/night_warriors_deluxe`
(the virtual environment re-synced there, since its scripts hold absolute
paths).

## 2026-11-18 — Local disk cleanup

User request: clean up the space (35 GB). Deleted permanently, by the
user's choice: the 16 test images in `build/` other than `us_edition`
(each rebuilt by its experiment's script), and the screenshots, states,
sound-RAM dumps and WAVs inside the 256 replay folders under `local/`
(`force.py`/`dense.py` outputs; their `run.json`, event logs and slot lists
kept). 19.2 GiB; the repository is now 16 GB. Kept: every user play
session, the source images, `local/extracted`, `local/psp_extract`,
`vendor/`, the waveform-search work files. Earlier screenshot-based
results are recorded in the experiment READMEs; to see them again, rebuild
the image and rerun the recorded command.

## 2026-11-19 — Play sessions archived on the homelab

User request: archive the play sessions on the homelab, using the
`remote_server_maintenance` repository's access method. The 24 user
play-session folders under `local/` (10,938 files, 9,363,348,412 bytes)
were copied to the homelab archive folder `NightWarriorsDeluxe-Saturn`
(same paths, SHA-256 `MANIFEST.tsv`, restore `README.md`), verified with
`sha256sum -c` on the server, and logged there (commit `5787f0d`). The Mac
copies were kept. Location and access are in `local_agent_guidance.md`.
Then the user chose "Delete Mac copies": with all 10,938 local files
confirmed in the manifest at matching sizes, the 24 folders were deleted
from `local/` (9,363,348,412 bytes; the repository is now 6.9 GB). The
homelab archive is now the only copy; restore a group folder before
replaying any of its states (archive `README.md`; maintenance repo commit
`9b75553`). Experiment READMEs still cite these sessions by their `local/`
paths, which restoring brings back.


## 2026-11-25 — Release 0.1.0 preparation (`ENV-007`, `DOC-004`, `REL-001`)

User request: check readiness for `v0.1.0` on GitHub and draft the Reddit
announcement post (using the sibling template, with screenshots).

User decisions (verbatim, multiple choice, recorded in
`docs/localization_policy.md`):
- Scope: "(Recommended) Ship v0.1.0 with what's built now (US Enhanced, US Original, JP Original) and defer END-005, QUO-001, LOC-001, and full audit to later versions"
- Format: "(Recommended) xdelta only (proven reliable in Cyberbots; build relocates TITLE.O and ST2HIS.BIN in Track 1)"
- Pre-release checks: "(Recommended) Run full pre-release prep: ENV-007 (Redump check), DOC-004 (README), REL-001 (xdelta zips + verification), and RetroAchievements hash check"
- Screenshots: "(Recommended) Capture fresh clean screenshots from build/us_edition in Mednafen (OPTION menu, English epilogues, restored Morrigan ending lines, Sasquatch pose, JP mode)"

Results:
- **`ENV-007` DONE (Redump verification):** verified in the built-in browser
  against `http://redump.org/`. Untouched US image matches Redump disc `5836`
  (`Night Warriors: Darkstalkers' Revenge`, `T-1208H`, V1.001: Track 1 CRC-32
  `91921ea9`, MD5 `d284efa0…30e5`, SHA-1 `c1c01169…fb1d`; Track 2 CRC-32
  `e75e991c`, MD5 `3b0c741e…1090`, SHA-1 `ac745b71…46d5`). Untouched JP 1M
  image matches Redump disc `3677` (`Vampire Hunter: Darkstalkers' Revenge`,
  `T-1202G`, V1.000: Track 1 CRC-32 `94c313ab`, SHA-1 `77390da7…800ed`; Track
  2 CRC-32 `9921da39`, SHA-1 `780688b0…4bb84`). All Redump entries listed
  (`5836`, PAL `4675`, JP `3677` 1M, `3681` 2M/4M, `1456` 3M, Sample `20095`);
  `1M`/`2M, 4M`/`3M` confirmed as JVC glass-mastering batch ring codes.
  Updated `references/saturn_us/README.md`, `references/saturn_jp/README.md`,
  and `docs/known_unknowns.md`.
- **RetroAchievements check:** `retroachievements.org` returned HTTP 403
  Cloudflare bot check in the browser (not bypassed); web search indicates
  there is currently no Sega Saturn set for *Night Warriors* (arcade only).
  First 512 bytes of Track 1 sector 0 user data hash to MD5
  `8c7156c2e38f75a9ec54016427967e9e` in both untouched US Track 1 and
  `build/us_edition` Track 1 (enforced by `tools.disc.make_patch`).
- **`REL-001` DONE (release tools, xdelta patch, reproducible zip):**
  - Ported `tools/disc/make_patch.py`, `tools/release/make_zips.py`,
    `tools/release/check_zips.py`, and their unit tests from Cyberbots
    (`bac6fde`) with provenance notes and Night Warriors Deluxe defaults
    (xdelta-only). Also fixed 6 pre-existing strict mypy annotations in
    `tools/disc/patch_image.py` and `tests/unit/test_diff_files.py`.
  - Built `night_warriors_deluxe.Track1.xdelta` (54,362 bytes, SHA-256
    `01f3aeabae96a25fa50905a90f1a4028382fc302c91e10872efdeb0d4d86fa82`,
    xdelta3 3.2.2) twice identically (`cmp` clean) and round-trip verified;
    committed metadata record `release/night_warriors_deluxe.json`.
  - Built `build/release/v0.1.0/night_warriors_deluxe_0.1.0_xdelta.zip`
    (49,807 bytes, SHA-256
    `92b8c26c3b9236c2294a6d169fddc6c8edcc1e31b33cb30e089e905a471330e0`) twice
    identically (`v0.1.0` and `v0.1.0-again`), verified by `check_zips`
    applying the unpacked patch to untouched US Track 1 (`d0960087…70da`) and
    producing `25e05ec14a258e7f2bea49e51023dfbf96c553aae688b67c5044728c4040f1be`.
- **`DOC-004` DONE:** updated `README.md` to the final MSHvSF/Cyberbots layout
  and wrote `release/README.md`, `release/RELEASING.md`, and
  `release/notes_v0.1.0.md`.

Checks: `./invenv.sh ruff check .` passed; `./invenv.sh ruff format --check .`
(146 files formatted); `./invenv.sh mypy` (0 issues in 57 source files);
`./invenv.sh pytest -q` (142 passed).

Next action: commit, push `main`, and push tag `v0.1.0` as `princeendo`;
capture fresh screenshots from `build/us_edition` and draft the Reddit post
under `build/reddit_0.1.0/post.md`.

## 2026-11-26 — Playtester follow-up and mixed-matchup animation

Scope from the user: investigate `FULL` with different fighters, the P1
Anakaris audio issue, Morrigan's Soul Fist trail panning, and Capcom's
Appendix code/options. The user said, “I'm totally fine with requiring a
4M cart, though it would be cool to have a cart/no-cart version.” Start
with a 4 MiB implementation if needed and verify a cart-free path. Keep
the 1 MiB question open until allocations are measured. The user approved
silent Mednafen cold boots for the animation experiment.

`ANI-002`, `EXP-0040`, D-036: with `00` and `01` written separately to the
animation byte from the same title checkpoint, both retail loaders drew
Anakaris vs. Rikuo/Aulbath with `P06_` and `P09_`. The CPU reads both values
and checks fighter equality for `FULL`. The before/after screenshots match
within each release. Failed attempts to confirm the speed selection from
the Deluxe checkpoint were dropped from the evidence. The retail title
replays give the mixed-matchup control without input.

The stock US loader's `.BIN` plus `.SPR` storage for the largest distinct
pair (Anakaris and Huitzil) is 2,256,056 bytes. Its three pools have an upper
bound of 1,578,860 bytes before other use. Both original Track 1 hashes were
rechecked against the source manifests after the runs.

Recorded `ANI-003`, `AUD-004`, `AUD-005` and `APP-001` with acceptance
criteria. Next for `ANI-002` is a mirror control and large-pair allocation
traces. The two sound reports and the Appendix unlock sequence remain
separate verification tasks. No game patch was built in this session.

Verification: `./invenv.sh ruff check .`,
`./invenv.sh ruff format --check .`, `./invenv.sh mypy`, and additional
`mypy` checks on both `EXP-0040` scripts passed. `./invenv.sh pytest -q`
passed all 142 tests. Experiment commands and evidence hashes are in
`research/experiments/EXP-0040/README.md`.

## 2026-11-26 — `ANI-002` done: mirror control and large-pair allocations (`EXP-0041`)

User request: start the new playtester follow-up tasks. `ANI-002` was the one
`IN_PROGRESS` experiment, so it went first. Muted Mednafen runs from the US
retail title checkpoint, under the consent the user gave for this experiment
earlier today. No disc bytes changed, and US Track 1 still hashes to
`d0960087…70da` after the runs.

- The attract code writes both one-based fighter IDs at `0x06035908`.
  Forcing them there (halt on the P2 write, step, overwrite, check the
  readback) gave an Anakaris mirror and Anakaris vs. Huitzil. The CPU's own
  reads in the loader confirmed the forced values.
- Mirror: `CUT` loads `P06_` once (684,404 bytes), `FULL` loads `P06` once
  (1,162,868 bytes). Both screenshots show Anakaris against Anakaris.
- The fighter pools hold 1,372,412 bytes. Anakaris vs. Huitzil `CUT` uses
  1,367,788. With the equality branch at `0x0602192A` forced in RAM
  (`890F` to `A00F`), `FULL` requests `P06` and `P11`, fails on a 112,784-byte
  request at `0x06013F68` ("Out Of Memory"), and the console resets to the BIOS
  CD player.
- Only 3 of 91 distinct pairs fit both full sets in the stock pools, each with
  Morrigan. The largest pair needs 883,644 more bytes. The largest single
  request is 112,784 bytes. Mednafen's 1 MiB cart is two 512 KiB banks.
- Process error, corrected: the first forced runs left the ID write
  breakpoint armed when the script switched to halt mode, so their "pools
  before" snapshot came from frame 321, not the loader entry. The script now
  halts, steps, verifies and clears it first. The four runs were deleted and
  rerun; loads and fighter totals were unchanged.

Not done: the JP mirror (the JP mixed path matched in `EXP-0040`), and where
the pools are reset (UNKNOWN). `ANI-003` is now `READY`; its first question
is whether fighter data works from A-bus cart RAM.

## 2026-11-26 — `APP-001` done: Appendix code, agent cache fix, default unlock (`EXP-0042`)

User choice after `ANI-002`: "APP-001 Appendix check".

- Static: the code is B, X, Down, A, Y on CONFIGURATION (each press within
  14 frames), and it is identical in US and JP `TITLE.O`. A second code on
  line 2 (X, X, Right, A, Z) sets `0x06080A2A`; what it unlocks is UNKNOWN.
  Deluxe v0.1.0 leaves the code untouched.
- Injected presses reached the logo but not the title menu, as in
  `EXP-0038`. A trace showed the cause: the agent wrote `0800` to the
  pressed word before the title task read it, yet the task read 0 from the
  emulated SH-2 cache. User decision, verbatim: "Patch agent build
  (Recommended)". Patch `0002` (20 lines, `src/ss/debug.inc`, agent tree
  only) purges the written lines on both CPUs. The rebuilt binary is
  `7040f6fe…4cdd`. `revalidate.sh` passed V1-V4 on both releases
  (09:17-09:24), and the title menu then opened from an injected Start.
  Writes in earlier experiments were judged by what the CPU read, so they
  stand.
- Live, from cold boots with an empty save: the code unlocks, APPENDIX
  opens, FULL is set and saved, and all of it persists across a reboot on US
  retail, JP retail and Deluxe v0.1.0 (no cart), and on Deluxe with a 4 MiB
  cart. Regression on Deluxe: EDITION (y `0xC8`) touches PRESS START TO EXIT
  (y `0xD0`) once unlocked.
- User decisions, verbatim: first "Should we move that edition chooser to
  the appendix instead?". Then, told that the Appendix is hidden without the
  code and that its screen is full: "Let's keep it in options and also
  unlock appendix by default."
- Correction, recorded so it is not repeated: I first told the user that the
  unlocked attract demo picks HUNTER or CLASSIC music at random, from a static
  reading. The run disproved it: the demo sets the BGM option to RANDOM and
  randomizes `0x06080962`, which is the scenery variant (alternate stage
  colours), and the two runs' audio was byte-identical. The policy note was
  corrected before commit.
- Built: `title_code.py` now writes 1 to `0x06080A2B` each title frame, and
  `0x06004C46` changes `00D0` to `00D8`. `build/us_edition` was rebuilt
  (Track 1 `a87f7f70…ab0d`, deterministic: a test build to
  `build/us_edition_app001` had the same hash and was deleted). Cold-boot
  checked with no cart and with a 4 MiB cart: unlocked with no code entered,
  everything persists, and the exit line has the usual gap.

Removed (standing permission): `build/us_edition_app001` (rebuildable by the
command above). v0.1.0's image is rebuildable from tag `v0.1.0`.

## 2026-11-26 — `ANI-003`: cart-backed `FULL` (`EXP-0043`)

User choice: "ANI-003 cart FULL". Muted Mednafen cold boots, driven by
injected presses (`EXP-0042` tooling).

- Design from the allocator: three bump pools and a baseline copied once at
  boot. P1's set fills the pools bottom-up and P2's top-down. Pointing pool 2
  at the 4 MiB cart gives both sides room with no allocator change. The cart
  ID and RAM addresses come from the XvSF lead (`CPK.EMM`) and were
  re-checked here.
- RAM prototype on the retail image: Anakaris vs. Huitzil loaded both full
  sets with no out-of-memory call. Huitzil's 1,093,188 bytes are in the cart.
- Built into the Deluxe title wrapper (`title_code.py` `cart`). First test
  failed for a dull reason: from a cold boot with no input, the title task
  never runs (the logo screen), so the routine never ran. The forced runs now
  press Start once. In play the title task always runs before a match.
- Results: 4 MiB with FULL gives full sets in both orders and for all 14
  fighters. 4 MiB with CUT, no cart, and 1 MiB load stock sets (the last two
  traces are byte-identical). Arcade (rounds by time-over: timer
  `0x06080977`, vitality P1 `0x06076C67`, P2 `0x0607706B`), opponent
  changes, continue and rematch, and VS all work. Pace is the same as a
  no-cart CUT fight.
- Slips, fixed: a zsh loop that did not split words (no run started), and a
  rematch run whose picks landed during the select screen's load.
- `build/us_edition` was rebuilt (Track 1 `8882e154…72df`, identical to the
  test build). The test build `build/exp0043_cart` was deleted (standing
  permission, rebuildable). The APP-001 cold-boot check was rerun on the
  final image.

Open: the real-Saturn check with a 4 MiB cart (the user, before release).
1 MiB is not qualified. The routine runs in every edition and changes
nothing unless `FULL` is set with a 4 MiB cart.

## 2026-11-26 — `AUD-004`: Anakaris on P1 hijacks the opponent's shared sounds (`EXP-0044`)

User choice: "AUD-004 Anakaris sound". The user supplied the playtester's
words (asked as a multiple choice, answered with the comment): several 2P
sound effects are "loaded in strangely" whenever Anakaris is played from 1P
(Demitri's dash and fireball, Pyron's fireball, Sasquatch/Donovan/Huitzil
ice), never with Anakaris on P2.

- Disproven first: P1's oversized `ANAKA1.SEQ` overrunning P2's data. Sound
  RAM is intact; the P2 sequence slot is 1,624 bytes after P1's in every run.
- Tooling: `vsmove.py` drives VS (and Arcade) with forced fighters and
  frame-held motions. P2 is driven on pad 2. Forcing IDs after the picks
  was checked against the files in sound RAM.
- Reproduced with voice sampling (SA in Anakaris's bank for Demitri's
  fireball part 2 and dash) on US and JP, then traced to the game's request:
  the shared-sound lookup `0x0603A1C8` prefers P1's character (table
  `0x0606C10C`), and Anakaris owns copies of 17 of 27 types.
- First fix attempts, recorded so they are not retried: (1) infer the
  requester from the queue's high word: it is always 0, the queue holds no
  partner ID; (2) infer it from the ID range: works for the fireball, but
  the dash uses ID `0x75` from either side; (3) a 128-byte helper carved from
  pool 0: not needed. Final: with Anakaris on P1, try P2's character first
  (78 bytes in place, US Enhanced via the edition patch list).
- Verified in VS and Arcade for Demitri, Pyron, Sasquatch, Huitzil and the
  CPU Victor. Controls are unchanged (retail plus the RAM fix only, in two
  batteries), and the original editions keep stock bytes. Donovan's motions
  produced no shared sound; his ice attack is unverified live.
- Side observation, recorded in `known_unknowns.md`: Deluxe and retail differ
  in a few bank-0 sound starts under identical inputs; not from this fix.
- `build/us_edition` was rebuilt (Track 1 `33768e29…a2a4`). The test build
  `build/exp0044_sound` was deleted (standing permission, rebuildable).
