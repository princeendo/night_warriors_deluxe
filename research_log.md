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
