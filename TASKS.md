# Dependency-Controlled Research Plan

This is an evidence gate, not a generic backlog. `AGENTS.md` is authoritative.
Statuses are `BACKLOG`, `BLOCKED`, `READY`, `IN_PROGRESS`, `DONE`, and `REJECTED`.
At most one reverse-engineering experiment may be `IN_PROGRESS`.

The task order follows the "Verify on X" checklist in
`docs/playbook_from_mshvsf.md`, corrected by `docs/lessons_from_xvsf.md` and
`docs/lessons_from_cyberbots.md`. Task IDs are this project's own; where a
task repeats a sibling task, the note names it for its method only.

## Current State

- **2026-11-13: repository set up** (`SESSION-0001`). Phase A is done except
  the database check (`ENV-007`): Python project, rules, ignore list, the
  game-independent sibling tools with provenance, the three sibling method
  documents, and the identity of all four supplied images
  (`references/saturn_jp/README.md`, `references/saturn_us/README.md`).
- A first static comparison of the two data tracks is in those READMEs and
  in `docs/difference_register.md` (rows `FILE-01` to `FILE-10`). The most
  important observations: the three Japanese pressings share one
  byte-identical data track; both regions have the same 415 files, 363 of
  them byte-identical, **including every sound file**; 52 files differ,
  mostly program overlays (`MAIN.BIN`, `ENDING.O`, `PL01`-`PL14`,
  `SOBJ01`-`SOBJ12`). What any difference does is **UNKNOWN**.
- **2026-11-13: first decisions** (`SESSION-0002`, `DOC-002`,
  `docs/localization_policy.md`). The image will offer **JP original**, **US
  original** and **US Enhanced** (US plus the Japanese-only content), and **JP
  Enhanced** if the US release has content the Japanese one lacks
  (`EDITION-001`). Work from the Japanese 1M image only. First
  investigations: Morrigan's voices on the US disc (`AUD-001`) and the
  per-character epilogue screens (`END-001`).
- Static leads for both (`SESSION-0002`): Morrigan's files and every sound
  file are byte-identical on both discs; so are the 14 `END*.BG` files and
  `ENDDATA.BIN`, while `ENDING.O` differs. Track 1 has only 150 free sectors
  (0.3 MiB) against about 2.1 MB for one region's copy of the 52 differing
  files: switching editions will need a larger track 1 or smaller patches.
- **2026-11-13/14: the emulator chain works on both releases** (`EMU-001` to
  `EMU-007`, `EMU-020`, `EMU-021`; `EXP-0001` to `EXP-0005`; D-001 to
  D-005): stock Mednafen 1.32.1 and the patched agent build, each release on
  its own BIOS, no extended-RAM cart needed for boot and attract, the user's
  pad, hotkey screenshots and states, stock debugger dumps, and the agent
  interface (V1-V4).
- A new regional difference turned up in the intro (`INT-01`).
- Reverse-engineering experiments in progress: none; `AUD-001` is
  `IN_PROGRESS` (`EXP-0007` captured the sessions).
- **2026-11-14: save-state extractor validated** (`DBG-001`, `EXP-0006`,
  D-006). The tools for both investigations are ready.
- Next unblocked tasks: `AUD-001` (Morrigan's voices) and `END-001` (the
  epilogue screens), the user's first investigations. Offline meanwhile: `DIFF-001` (classify the 52
  differing files), `ENV-007` (database check), `DOC-003` (reference
  catalog).
- Confirmed about Vampire Hunter so far: only how it boots and runs in the
  emulator and the tools (D-001 to D-006); nothing about its internals.

## Milestones

This project merges two releases rather than translating one, so the sibling
milestones are re-anchored on **regional differences**: the rows of
`docs/difference_register.md`. A "difference class" is one kind of row
(epilogue text, victory quotes, voice samples, names, ...). The first class and
item are chosen by `DIFF-003` from evidence and the user's priorities.

| ID | Required outcome |
| --- | --- |
| M0 | Mednafen runs both releases; pad, screenshots, save states, debugger, agent interface, validated extraction, documentation, and Python tooling work. |
| M1 | One regional difference (the `DIFF-003` item) is switched in live RAM of the US release: it shows the Japanese release's content for that item (the first US Enhanced change). |
| M2 | The same change is reproduced from an untouched US image. |
| M3 | That difference is handled programmatically for every instance of one character (or the item's natural unit). |
| M4 | A second character works through the same generalized mechanism. |
| M5 | The whole roster is handled for that difference class. |
| M6 | The next difference class, in the user's order, repeats M1-M5 under its own tasks; one class at a time (`AGENTS.md` rule 23). |
| M7 | The edition switch: JP original, US original, US Enhanced (and JP Enhanced if needed) in one image (`EDITION-001`). |
| M8 | Combined image: every register row resolved; coverage register closed. |
| M9 | Special cases (unused assets, hidden content, debug features), each with an explicit task. |

Two gates control the work (`docs/lessons_from_xvsf.md`, lesson 11):
`GATE-M0` (technical prerequisites for the first live RAM mutation) and
`GATE-TRANSLATION` (English sources and policy before any English text that
is not already on the base disc goes on disc).

## Phase A: Repository And Environment

### ENV-001 - Create Python uv project

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** None.
- **Blockers:** None.
- **Objective:** Define an installable Python 3.12+ project managed by uv.
- **Acceptance criteria:** `pyproject.toml` declares the project, Python floor, build backend, and development dependency group; `uv.lock` is committed after synchronization.
- **Notes:** Done 2026-11-13, adapted from the Cyberbots `pyproject.toml` (`bac6fde`, renamed). uv 0.11.7; zero runtime dependencies.

### ENV-002 - Implement setup_venv.sh and invenv.sh

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** ENV-001.
- **Blockers:** None.
- **Objective:** One command creates the environment; one wrapper runs tools in it.
- **Acceptance criteria:** `./setup_venv.sh` syncs all groups; `./invenv.sh CMD` runs `CMD` in the project environment without an activated shell.
- **Notes:** Copied unchanged from Cyberbots (`bac6fde`). Both worked on 2026-11-13 (the build needs `README.md` to exist).

### ENV-003 - Add linting, formatting, typing, tests, and the game-independent tools

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** ENV-002.
- **Blockers:** None.
- **Objective:** Make `pytest`, `ruff check`, `ruff format --check`, and strict `mypy` pass from the first commit, with the sibling tools that hold no game facts.
- **Acceptance criteria:** All four commands pass through `./invenv.sh`; every copied file carries a provenance note (source repository, path, commit).
- **Notes:** 2026-11-13: copied from Cyberbots `bac6fde` (unchanged there since its own copy from XvSF `a1c82ba`): `tools/disc/{hash_source,iso9660,sector,patch_image}`, `tools/mednafen/{agent,session_recorder,replay_state,home,hotkeys,cold_boot,frame_capture,backup_ram}`, `tools/memory/{mcs_extract,diff,vdp1_sprites,vdp2_plane}`, `tools/sh2/{asm,disasm}`, `tools/text/{search,pattern_search,code_search}`, `tools/reference/{mame_audit,listxml_match,*.lua}`, and their tests. Left for later: the release tools Cyberbots improved (`make_patch`, `make_ssp`, `add_files`, `make_zips`, `check_zips`; `REL-001`) and the experiment scripts worth promoting (`docs/lessons_from_cyberbots.md`, section 5). 119 tests passed; ruff and mypy clean. **Copied is not validated:** each tool is re-validated on Vampire Hunter by the first task that uses its output as evidence (`AGENTS.md` rule 26).

### ENV-004 - Create repository documentation skeleton

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** None.
- **Blockers:** None.
- **Objective:** Rules, protocol, task list, log, discoveries, unknowns, difference register, and experiment template exist.
- **Acceptance criteria:** `AGENTS.md`, `README.md`, `TASKS.md`, `research_log.md`, `docs/research_protocol.md`, `docs/discoveries.md`, `docs/known_unknowns.md`, `docs/difference_register.md`, `research/README.md`, and `research/experiments/README.md` exist and are non-empty.

### ENV-005 - Create .gitignore and local guidance

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** None.
- **Blockers:** None.
- **Objective:** Keep game data, evidence, and machine-local guidance out of git.
- **Acceptance criteria:** `git check-ignore` reports `local/`, disc formats, archives, states, and `local_agent_guidance.md` as ignored.
- **Notes:** The ignore list is Cyberbots'. `local_agent_guidance.md` carries the user preferences from all three siblings (Cyberbots' file, retargeted), each still to be confirmed for this project in `DOC-002`.

### ENV-006 - Record immutable source identity

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** ENV-002.
- **Blockers:** None.
- **Objective:** Record filename, size, SHA-256, and release description of every Saturn source component, for both regions.
- **Acceptance criteria:** Every component is hashed with `tools/disc/hash_source.py` and recorded with a release description.
- **Notes:** 2026-11-13: three Japanese images (T-1202G V1.000 19960128, labelled 1M, 2M/4M and 3M) in `references/saturn_jp/README.md`; one US image (T-1208H V1.001 19960228) in `references/saturn_us/README.md`. The supplied archives are hashed too. Identity is **SUPPORTED**, not database-verified (`ENV-007`).

### ENV-007 - Verify the source images against a database

- **Status:** `READY`
- **Milestone:** M0 (do early; XvSF did this the day before release)
- **Dependencies:** ENV-006.
- **Blockers:** None. Cyberbots' first try (`WebFetch` of redump.org) was refused; it succeeded later in the built-in browser.
- **Objective:** Raise the identity of the two working images (Japanese 1M, US) from **SUPPORTED** to **CONFIRMED**, and learn what the Japanese labels (1M, 2M/4M, 3M) distinguish.
- **Acceptance criteria:** Each working image's track hashes match a named database entry (size, CRC-32, MD5, SHA-1 per track), or a mismatch is recorded with its consequence; every Redump entry for both titles is listed.
- **Notes:** Static evidence so far: the Japanese track 1 is identical in all three; their track 2 differs only by a 1-4 sample offset (`references/saturn_jp/README.md`). A release must name the exact image(s) it applies to either way (`AGENTS.md` rule 31).

## Phase B: Documentation And Decisions

### DOC-001 - Carry over the sibling playbooks

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** None.
- **Blockers:** None.
- **Objective:** Give every session the sibling method, pitfalls, and tools list without treating any of it as Vampire Hunter fact.
- **Acceptance criteria:** `docs/playbook_from_mshvsf.md` is a copy of the current MSHvSF `docs/playbook_cross_game.md` with its source commit; `docs/lessons_from_xvsf.md` and `docs/lessons_from_cyberbots.md` digest what did and did not transfer to the second and third games.
- **Notes:** 2026-11-13: playbook from MSHvSF `447e573` (unchanged since; byte-equal below its header note); `lessons_from_xvsf.md` copied from Cyberbots `bac6fde` with a header note; `lessons_from_cyberbots.md` written new from Cyberbots `bac6fde` by a read-only subagent. The user's web research is copied unchanged to `references/web_research/` (SHA-256 `36f7b565…f5c2`). Re-copy when a source changes; record the new commit.

### DOC-002 - Put the project decisions to the user

- **Status:** `DONE`
- **Milestone:** GATE-TRANSLATION (base-release question: before `DIFF-003`)
- **Dependencies:** DOC-001.
- **Blockers:** None.
- **Objective:** Ask the user to decide, confirm, or defer the decisions this project needs, including those carried from the siblings (`docs/playbook_from_mshvsf.md` "The User's MSHvSF Localization Decisions", `docs/lessons_from_xvsf.md` "User Decisions Worth Re-asking", `docs/lessons_from_cyberbots.md` section 6).
- **Acceptance criteria:** Each decision has a recorded answer (verbatim, dated) or an explicit deferral to the task that produces its evidence, in `research_log.md` and `docs/localization_policy.md` (created by this task, on the Cyberbots file's structure: answered / deferred / per-gate tables).
- **Done 2026-11-13** (`SESSION-0002`): the user decided the editions (JP original, US original, US Enhanced, JP Enhanced if needed), the working Japanese image (1M) and the first investigations (`AUD-001`, `END-001`), unprompted; every other decision is deferred by name to the task that produces its evidence (`docs/localization_policy.md`, "Deferred To Evidence"). Those questions are asked there.
- **Notes (original scope):** Multiple-choice questions with a "(Recommended)" option. Project-specific: **which release is the base** (the US image with Japanese content restored, or the Japanese image with the US English brought in); which Japanese pressing a release names; which difference classes are in scope and in what order (epilogues, main-ending rewrites, victory quotes, voices and poses, names, other); English sources and their order (US Saturn wording kept; PSP *Darkstalkers Chronicle*; arcade *Night Warriors*; new translation marked as such; fan transcripts as locators only); names policy (US, JP, or a toggle; Amanda/Anita); whether regional variants become options. Carried: reuse of the patched Mednafen (`AGENTS.md` rule 16); release formats and timing (rule 21); push and hardware-check policy; the preferences in `local_agent_guidance.md`.

### DOC-003 - Build the reference catalog

- **Status:** `READY`
- **Milestone:** M0 (do early)
- **Dependencies:** DOC-001.
- **Blockers:** None.
- **Objective:** Reuse the sibling platform references and list Vampire Hunter-specific prior art.
- **Acceptance criteria:** `docs/references.md` lists the platform references (Saturn, SH-2, CD/ISO 9660, Mednafen, CPS-II, MAME) with their sibling source, and separately the Vampire Hunter sources: the 23 sources of the web research (with what each may and may not be used for), translation or restoration projects, text dumps, official English releases, and guides/manuals.
- **Notes:** Start from the web research's source register (section 12). Its notable leads: the Arcade Patches CPS-2 restoration (unofficial, arcade-only), the PSP *Chronicle* gallery (official, unverified coverage), the Video Game Museum arcade ending gallery, and two conflicting fan epilogue transcripts.

### DOC-004 - Start the README in its final layout

- **Status:** `BACKLOG`
- **Milestone:** before REL-001
- **Dependencies:** DOC-002.
- **Blockers:** None.
- **Objective:** Avoid XvSF's post-release README reorganization.
- **Acceptance criteria:** `README.md` follows the MSHvSF/Cyberbots README section layout, with placeholders for what is not done.

## Phase C: Emulator

### EMU-001 - Pin and build stock Mednafen

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** ENV-002.
- **Blockers:** Ask before downloading source or installing build dependencies.
- **Objective:** Have a stock Mednafen build under ignored `vendor/` with its exact version, source URL, hash, and build commands recorded.
- **Acceptance criteria:** `docs/mednafen.md` records the version, source hash, configure and build commands, and the binary's `-help` banner.
- **Notes:** All three siblings used stock 1.32.1 (`de7eb94a…3832`), so the agent patch applies unchanged. The archive is in Cyberbots' and XvSF's `local/downloads/mednafen-1.32.1/`; copy it after checking its hash instead of downloading again. Homebrew's `mednafen` is not the pinned build.
- **Done 2026-11-13** (`SESSION-0003`, `docs/mednafen.md`): archive copied from Cyberbots, hash `de7eb94a…3832` equal to the siblings'; built with the siblings' flags in 3 min; binary `de542817…582a`, 21,318,680 bytes; `-help` banner shows 1.32.1 with the `ss` module (exit 255, as the siblings'). Neither release is in Mednafen's Saturn database (for `EMU-004`). Nothing downloaded or installed.

### EMU-002 - Create the project-local Mednafen configuration

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-001.
- **Blockers:** None.
- **Objective:** Run Mednafen with a configuration and BIOS path local to this checkout, never the user's global configuration.
- **Acceptance criteria:** The launch command, base directory, BIOS identities (filename, size, SHA-256) for **both** regions, and forced settings are recorded; `tools/mednafen/home.py` pins the interactive and quiet homes.
- **Notes:** This project needs the Japanese BIOS `sega_101.bin` (`dcfef4b9…`) and the North American `mpr-17933.bin` (`96e106f7…`); both are in Cyberbots' `local/mednafen/firmware/`. Copy them and record their hashes. Check that Mednafen picks the BIOS by the disc's area code (`JT` vs `U`) and record which it used for each boot (`EMU-003`).
- **Done 2026-11-13** (`SESSION-0004`, `docs/mednafen.md`): both BIOS files copied from Cyberbots, `cmp` clean, hashes equal to Mednafen's `ss.html`; `tools.mednafen.home` created and pinned both homes (second run: no change); each home's `-help` loads 7,904 settings with 0 unknown; both `mednafen.cfg` hashes equal Cyberbots' and XvSF's. Launch commands for both releases recorded.

### EMU-003 - Boot both releases

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-002, ENV-006.
- **Blockers:** None; run with the user present.
- **Objective:** Reach the title screen from a cold boot of each untouched image.
- **Acceptance criteria:** Three cold boots of the Japanese 1M image and three of the US image reach a stable title screen; each boot log shows `T-1202G` or `T-1208H`; source hashes match before and after; screenshots kept locally.
- **Notes:** Use `tools/mednafen/cold_boot.py` and the quiet home. With the user present (`local_agent_guidance.md`, "Emulator Consent").
- **Done 2026-11-13** (`EXP-0001`, D-001): three no-input boots per release, frames identical within each release, titles at about 63 s, each release on its own BIOS, sources unchanged. `ss.cart auto` gave both a backup-memory cart. A new intro difference (`INT-01`) was seen at second 39.

### EMU-004 - Determine the cartridge requirement

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-003.
- **Blockers:** None; run with the user present.
- **Objective:** Find which cartridge setting each release needs, with controls.
- **Acceptance criteria:** Boots with `ss.cart` set to `none`, `backup`, `extram1` and `extram4` are each recorded per release (log line, what the game shows, how far it gets); the project setting is chosen from that evidence.
- **Notes:** `EXP-0001`: `ss.cart auto` gives both releases a backup-memory cart (no database entry). The peripheral field reads `J` in both headers.
- **Done 2026-11-13** (`EXP-0002`, D-002): `none`, `extram1` and `extram4` give identical boot and attract frames in both releases; the backup cart (`auto`, from `EXP-0001`) shifts timing by under a second; no warning. Project setting kept: `ss.cart auto`. Play was not tested. MSHvSF and XvSF needed the 4 MiB cart; Cyberbots needed none for boot and attract.

### EMU-005 - Configure and document the pad

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-003.
- **Blockers:** None; run with the user present.
- **Objective:** The user's controller drives every button the game uses, and Start, in game.
- **Acceptance criteria:** A mapping table is recorded and each button is observed in the game's button configuration or in play.
- **Notes:** Start from the siblings' 8BitDo M30 mapping (six buttons, like this game).
- **Done 2026-11-14** (`SESSION-0005`, `docs/mednafen.md`): sibling bindings copied into both homes; the user tried every button in the US release's options: "Everything but L/R worked, but that's expected." Configs equal Cyberbots' and XvSF's (`cb1c2d3b…a1e9`, `aad9a7ef…57cf`).

### EMU-006 - Verify screenshots and save states

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-003.
- **Blockers:** None; run with the user present.
- **Objective:** Screenshots and save/load states work and are stored under ignored paths.
- **Acceptance criteria:** A state saved and reloaded reproduces the same screen, in each release; files are ignored by git.
- **Done 2026-11-14** (`EXP-0003`, D-003): F9/F5/F7 work in both releases; a reloaded title state reproduces the title screenshot byte for byte (Japanese same session, US fresh boot); states and screenshots are ignored. One post-load F9 and one F12 were lost.

### EMU-007 - Verify debugger access and memory dumps

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-006.
- **Blockers:** None; run with the user present.
- **Objective:** Dump WRAM-L and WRAM-H at a paused instant with the stock debugger.
- **Acceptance criteria:** Dumps of `0x00200000-0x002FFFFF` and `0x06000000-0x060FFFFF` are saved with sizes and hashes recorded; a memory write and a write breakpoint are each observed once.
- **Notes:** Keep this minimal and move to `EMU-020`/`EMU-021` straight after: every sibling lost time to stock-debugger GUI automation (`docs/lessons_from_xvsf.md`, lesson 10; `docs/lessons_from_cyberbots.md`, section 3).
- **Done 2026-11-14** (`EXP-0004`, D-004): repeatable 1 MiB dumps of both banks in both releases, a write and its revert, and a write breakpoint halting on a WRAM-H store. A first attempt was disturbed by use of the computer and rerun.

### EMU-020 - Record why stock Mednafen is insufficient

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-007.
- **Blockers:** None; ask the user about reusing the patch.
- **Objective:** Satisfy `AGENTS.md` rule 16 before using the patched build.
- **Acceptance criteria:** A short record cites MSHvSF `EMU-012`/`EMU-020`, XvSF `EMU-020` and Cyberbots `EMU-020` and confirms the same limits apply here; the user is asked whether to reuse the patch (deferred here from `DOC-002`) and the answer is recorded verbatim.
- **Done 2026-11-14** (`docs/mednafen_agent_interface.md`): sibling evidence cited; this project's own limits from `EXP-0003` and `EXP-0004` (lost F9, ignored F12, a disturbed run with no dumps, registers read by eye). The user: "Yes, reuse it".

### EMU-021 - Build and validate the agent interface

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-020.
- **Blockers:** None; boots run with the user present (no key presses, so hands-off is not needed).
- **Objective:** Drive Mednafen from Python so the user only plays.
- **Acceptance criteria:** `vendor/mednafen/patches/0001-agent-interface.patch` (`c30146ef…5244`) applies to the pinned version and builds; validations V1-V4 (`docs/mednafen_agent_interface.md`) pass on Vampire Hunter states of both releases; `tools/mednafen/agent.py` tests pass.
- **Notes:** Cyberbots' agent quirks (no save while halted; one Mednafen per home unless `MEDNAFEN_ALLOWMULTI=1`; RAM-written pad input is not seen through the SH-2 cache) are in `docs/lessons_from_cyberbots.md`, section 3.
- **Done 2026-11-14** (`EXP-0005`, D-005): patch applied without fuzz; binary `7826b9b9…f887`; V1 equivalence 119/119 frames and V1-V4 pass on both releases. Agent output may now be used as evidence.

### DBG-001 - Validate the save-state extractor on Vampire Hunter

- **Status:** `DONE`
- **Milestone:** M0
- **Dependencies:** EMU-007.
- **Blockers:** None. Use `EXP-0004`'s dumps and same-instant states.
- **Objective:** Extract WRAM-L, WRAM-H, VDP1 and VDP2 VRAM from states, validated byte for byte against debugger dumps of the same instant on Vampire Hunter.
- **Acceptance criteria:** Each region matches a stock debugger dump exactly; the result goes to `docs/discoveries.md`; cart RAM and sound RAM stay `HYPOTHESIS`.
- **Notes:** Every sibling found each stored 16-bit element byte-swapped. Re-test, do not assume. `mcs_extract` expects a 4 MiB cart section (Cyberbots' gap); size it from the state if `EMU-004` picks another cart. Sound RAM (for `AUD-001`) is not yet supported by the extractor.
- **Done 2026-11-14** (`EXP-0006`, D-006): extraction with the `saturn` byte order equals stock debugger dumps for WRAM-L and WRAM-H (two instants) and VDP1/VDP2 VRAM (one instant) in both releases; the unswapped order differs. Cart RAM and sound RAM not covered.

## Phase D: References

### REF-001 - Decide and intake the arcade sets (optional)

- **Status:** `BACKLOG`
- **Milestone:** GATE-TRANSLATION
- **Dependencies:** DOC-002.
- **Blockers:** No arcade sets supplied. Ask the user when an investigation needs them (deferred from `DOC-002`).
- **Objective:** Decide whether the CPS-II *Vampire Hunter* / *Night Warriors* sets are wanted as a reference (regional branches, English ending text, quote selection), and if so hash and verify them.
- **Acceptance criteria:** Either each zip is hashed and matched to a MAME set with a pinned MAME version, or the task is `REJECTED` with the user's reason.
- **Notes:** Cyberbots found the US arcade kept both regions' assets and chose by a region byte (`docs/lessons_from_cyberbots.md`, section 7). The web research's audio and pose leads (AUD-04, ANI-01) are arcade leads.

### REF-002 - Decide and intake the PSP Darkstalkers Chronicle (optional)

- **Status:** `BACKLOG`
- **Milestone:** GATE-TRANSLATION
- **Dependencies:** DOC-002.
- **Blockers:** No PSP image supplied. Ask the user when `END-001` reaches the English source question (deferred from `DOC-002`).
- **Objective:** Decide whether the English PSP *Darkstalkers Chronicle: The Chaos Tower* is a reference for official English epilogues and revised endings, and if so record its identity.
- **Acceptance criteria:** Either every component is hashed with an identity status, or the task is `REJECTED` with the user's reason.
- **Notes:** The web research names it the most promising official English source (its sources 6 and 7) but its coverage and alignment with the Saturn text are unverified.

### REF-003 - Paired manuals (off-disc, optional)

- **Status:** `BACKLOG`
- **Milestone:** M9 or out of scope
- **Dependencies:** DOC-002.
- **Blockers:** No scans supplied; whether printed material is in scope is still to ask.
- **Objective:** Resolve `BIO-01` or reject it as outside a disc image.
- **Acceptance criteria:** A page-level JP/US comparison with provenance, or `REJECTED` with the user's reason.

### REF-004 - Inventory the text, audio and presentation surfaces of both releases

- **Status:** `BLOCKED`
- **Milestone:** M1
- **Dependencies:** EMU-021.
- **Blockers:** EMU-021.
- **Objective:** List every place either release shows text or plays a voice, and capture each in both releases under matched settings, so the register's rows can be compared.
- **Acceptance criteria:** `docs/text_surfaces.md` holds a table of surfaces (screen, when shown, sample screenshot path and hash per release, same/different) from screenshots the agent reviewed, built from several captures of each release: a cold boot left on the attract loop, title and menus (Appendix included), one arcade run through at least two fights with a continue, a win screen, one ending with its credits. Every register row it touches is updated with both regions' evidence.
- **Notes:** XvSF's single session missed five surfaces (`docs/lessons_from_xvsf.md`, lesson 6); Cyberbots' kept every state and still missed endings and versus mode (`docs/lessons_from_cyberbots.md`, lesson 3). Keep every state (`--keep-states 0`). Match the settings named by the web research before comparing (animation options, Appendix).

## Phase E: Differences, Checkpoints And Memory Analysis

### DIFF-001 - Classify the 52 differing files offline

- **Status:** `READY`
- **Milestone:** M1 (static analysis only; no image change)
- **Dependencies:** ENV-003.
- **Blockers:** None.
- **Objective:** For each `FILE-nn` row, describe how the two regions' bytes differ without assuming what the difference does.
- **Acceptance criteria:** A script (`tools/disc/`) lists, per differing file, the runs of differing bytes (offset, length) and classifies each as a likely pointer/relocation change (consistent 32-bit deltas into a load range) or a content change; the SH-2 code files are identified by disassembly of their entry points; same-size files (`ENDING.O`, `PL*`, `SOBJ*`, `P00.BIN`, `ST?USA.BIN`) are summarized first; `PL*.O` vs `PL*.O2` is explained or listed as open. Committed output: offsets, lengths, hashes and counts only, no game text or code bytes (`AGENTS.md` rule 21). Register rows updated.
- **Notes:** Which file is loaded when, and where, are runtime questions for `DBG-004`. A content change in a program overlay is a lead, not an explanation.

### DIFF-002 - Locate where each release keeps its text

- **Status:** `READY`
- **Milestone:** M1 (static analysis only)
- **Dependencies:** ENV-003.
- **Blockers:** None.
- **Objective:** Find the storage and encoding of in-game text in both releases.
- **Acceptance criteria:** Candidate containers are tested (`ST?JPN`/`ST?USA`/`ST?HIS.BIN` and their offset tables; `MOJI.CHR`/`MOJI.TBL` as a font; graphics files for text drawn as art); for each, the evidence for or against is recorded; relative search (the method that found Cyberbots' arcade English, `EXP-0008`) is run on the US files for a few English strings known from the US release.
- **Notes:** A kana-run scan found no plain Shift-JIS in the program files (`references/saturn_us/README.md`). That only excludes plain Shift-JIS in those files. Confirmation needs a RAM search at runtime (`DBG-004`).

### DIFF-003 - Choose the first difference and its milestone unit

- **Status:** `BLOCKED`
- **Milestone:** M1
- **Dependencies:** REF-004, DIFF-001, AUD-001, END-001.
- **Blockers:** REF-004.
- **Objective:** Pick one register row (and one character, where it applies) as the M1 target, and fix the milestone unit for its class.
- **Acceptance criteria:** The choice and reason are recorded; the difference is captured in both releases under the same action and settings; a checkpoint shortly before it exists in the US release.
- **Notes:** Candidates by the web research's weight: one character's epilogue (END-01), one Morrigan voice event (AUD-01 to AUD-03, whose sound files are identical on both discs), one renamed character (NAM-02). The user's priorities (2026-11-13): Morrigan's voices (`AUD-001`) and the epilogues (`END-001`); choose between them from those tasks' findings.

### DBG-002 - Observe how the chosen difference is selected

- **Status:** `BLOCKED`
- **Milestone:** M1
- **Dependencies:** EMU-021, DIFF-003.
- **Blockers:** EMU-021.
- **Objective:** Learn whether the chosen item is fixed or varies from one checkpoint, in both releases, before planning checkpoints.
- **Acceptance criteria:** Several replays of one checkpoint per release, with what is shown or played recorded.

### DBG-003 - Capture checkpoints

- **Status:** `BLOCKED`
- **Milestone:** M1
- **Dependencies:** DBG-002.
- **Blockers:** DBG-002.
- **Objective:** States and evidence before the item, during it, and after it, in both releases.
- **Acceptance criteria:** Each checkpoint is reproducible from its state and named in an experiment record.

### DBG-004 - Find the code and data behind the chosen difference

- **Status:** `BLOCKED`
- **Milestone:** M1
- **Dependencies:** DBG-001, DBG-003, DIFF-001.
- **Blockers:** DBG-003.
- **Objective:** Find what each release runs or reads at the item, and where they diverge.
- **Acceptance criteria:** The renderer or sound call is identified by a controlled change; the data in RAM is located; the divergence is tied to a `FILE-nn` row (or shown to be elsewhere); whether the other release's content is already on the base disc is recorded as tested or open.

## Phase F: The User's First Investigations

### AUD-001 - Are Morrigan's Japanese-only voices on the US disc?

- **Status:** `IN_PROGRESS`
- **Milestone:** M1 (investigation; no image change)
- **Dependencies:** EMU-021, DBG-001.
- **Blockers:** None.
- **Objective:** For each of `AUD-01` (normal throw), `AUD-02` (command throw) and `AUD-03` (bat-seat win pose), learn what each release plays, and whether the Japanese sound is on the US disc.
- **Acceptance criteria:** Each event is reproduced in both releases from matched checkpoints (same characters, settings and inputs) with sound recorded (ignored files, hashes kept); the sound command each release issues at the event is logged (sound RAM writes or the sound driver's command queue); the register rows get a change type (**conditionally suppressed**, **asset absent**, **not a difference**, or other) with that evidence; if the Japanese sample is on the US disc, where it is and what selects it are recorded.
- **Notes:** Static (`SESSION-0002`): every sound file (`SOUND.HED`, `SOUND.MP`, `SOUND.TBL`, `SDDRVS*.TSK`, all `*.SEQ`) and `MORRIGA.BIN`, `MORRIGA1.SEQ`, `MORRIGA2.SEQ` are byte-identical on both discs, so **HYPOTHESIS**: the samples are present on the US disc and the US code does not call them. The report is from memory (web research source 13); a "not a difference" outcome is possible. Method: Cyberbots `EXP-0088` (`-qtrecord`, sample-level comparison); the extractor does not yet cover sound RAM (`DBG-001`). Which `PL*` overlay is Morrigan's is unknown (`DIFF-001`).
- **Progress 2026-11-14:** `EXP-0007` recorded one Morrigan session per release (sound, a state every second, screenshots); the bat-seat pose occurs in both releases; the user heard "some more dialogue" in the Japanese one. Next: replay states before each event with sound-command logging.
- **Progress 2026-11-14 (`EXP-0008`, D-007):** the bat-seat pose line is CONFIRMED present on the US disc and not played (sample `MORRIGA.BIN` `0x1BAA0`); throw (`50C2C`), Vector Drain (`41220`) and hurt (`4F10C`) samples play only in the Japanese session (SUPPORTED, 1 s states). Remaining for `DONE`: locate US throws and replay them densely beside Japanese ones (matched evidence), then find what selects each sample.
- **Progress 2026-11-14 (`EXP-0009`, D-008):** a waveform search of the `EXP-0007` recordings confirms the normal-throw voice is never played in the US release (an observed US throw is silent); Vector Drain and hurt voices are absent from the whole US recording (SUPPORTED). Live slot logging during play was abandoned: it made the game stutter (the user's report). Remaining for `DONE`: what selects each sample (the code to change for US Enhanced); a US Vector Drain, if wanted.

### END-001 - The per-character epilogue screens

- **Status:** `READY`
- **Milestone:** M1 (investigation; no image change)
- **Dependencies:** EMU-021, DBG-001.
- **Blockers:** None.
- **Objective:** Show what follows each character's ending in each release, and find what the Japanese release uses for the post-ending artwork with scrolling text and whether the US disc still holds it.
- **Acceptance criteria:** For one character first, the whole ending sequence (main ending, artwork and text scroll, credits) is captured in both releases without skipped transitions (states kept, screenshots agent-reviewed); the epilogue's artwork and text are tied to their files and RAM; whether the US release shows the artwork, shows it without text, or skips it is recorded; whether the Japanese text (or its graphics) is on the US disc is recorded with the comparison that shows it; register rows `END-01` to `END-03` updated. A method to reach every character's ending by forcing (not playing) is recorded.
- **Notes:** The user (2026-11-13): "Each character has a post-ending artwork accompanied by scrolling Japanese text." Static (`SESSION-0002`): the 14 `END*.BG` files (`END00`-`END0D`) and `ENDDATA.BIN` are byte-identical on both discs; `ENDING.O` is the same size with 1,668 bytes changed (`0x5506`-`0xFA4F`). **HYPOTHESIS**: `END*.BG` are the artwork (14 files, 14 characters) and the US `ENDING.O` skips or cuts the text. Japanese text could also be drawn as graphics; no plain Shift-JIS was found. English for US Enhanced is a later `GATE-TRANSLATION` question (PSP *Chronicle*, `REF-002`, or a new translation). Cyberbots forced endings with four RAM writes (`docs/lessons_from_cyberbots.md`, lesson 4).

### EDITION-001 - Design the edition switch

- **Status:** `BACKLOG`
- **Milestone:** M7 (design may start once `DIFF-001` and one of `AUD-001`/`END-001` are done)
- **Dependencies:** DIFF-001.
- **Blockers:** None for the static part.
- **Objective:** Decide how one image offers JP original, US original, US Enhanced (and JP Enhanced if needed), from measured costs.
- **Acceptance criteria:** Options with costs presented to the user as a multiple-choice question: where the choice is made (boot menu, options screen, a button held at boot), where it is stored, and how each edition gets its code and data (both regions' differing files on disc and loaded by name, or one region's files plus patches applied at load); whether "original" must be byte-for-byte that release's code; the disc-space route. The answer is recorded verbatim.
- **Notes:** Static (`SESSION-0002`): track 1 has 150 free sectors (0.3 MiB) in both releases; one region's copy of the 52 differing files is about 2.1 MB; the header differs (`T-1202G` vs `T-1208H`, area `JT` vs `U`). Growing track 1 moves track 2 (a short warning or silence), changes the system area's sizes, and rules out SSP (`docs/lessons_from_cyberbots.md`, section 4). The system area also decides which BIOS region a real Saturn accepts: **UNKNOWN** how a merged image should be labelled. Cyberbots' options sub-menu and spare-save-byte pattern (D-055 to D-058) is the sibling precedent.

## Gates

### GATE-M0 - Confirm environment and checkpoint prerequisites

- **Status:** `BLOCKED`
- **Milestone:** M0
- **Dependencies:** ENV-001 to ENV-006, EMU-001 to EMU-007, EMU-020, EMU-021, DBG-001 to DBG-004, DIFF-003.
- **Blockers:** Dependencies not done.
- **Objective:** Make an explicit go/no-go decision before the first live RAM mutation.
- **Acceptance criteria:** Every dependency is `DONE`; no unresolved workflow blocker can invalidate M1 evidence; the user's GO is recorded verbatim.

### GATE-TRANSLATION - Confirm English sources and policy

- **Status:** `BLOCKED`
- **Milestone:** before any English not already on the base disc goes on disc
- **Dependencies:** DOC-002, DOC-003, and whichever of REF-001/REF-002 the user keeps.
- **Blockers:** Dependencies not done.
- **Objective:** No new or donor English text goes on disc before its sources, the pairing method, and the user's policy are settled.
- **Acceptance criteria:** Every dependency is `DONE`; the user gives a recorded GO. Each later scope extension (new class, new donor source, names) is its own dated block under this gate.

## Later Milestones (outline only)

Placeholders so the order is visible. Each becomes a full task, with its own
acceptance criteria, only when its prerequisites are done ("Write up the Mx
tasks" just in time). The method for each is in the three sibling documents.

| ID | Milestone | Outline |
| --- | --- | --- |
| RE-001 | M1 | Switch the chosen item in live RAM of the US release, with a no-write control. |
| DISC-001 | M2 | Trace the RAM data to its disc file by a write breakpoint from a pre-load checkpoint; identify the format. |
| DISC-002 | M2 | Reproduce the M1 change from a rebuilt image (same-size, in place, EDC/ECC regenerated with `tools/disc/patch_image.py`); cold-boot play check by the agent. |
| RE-002 | M3 | Selection: what picks each instance (character, opponent, health, route), and forcing it from a checkpoint. |
| RE-003 | M3 | Generator for one character; every instance verified live by forcing. |
| RE-004 | M4 | A second character through the same mechanism. |
| RE-005 | M5 | Whole roster for the class; capacity; regression references. |
| END-002 | M1-M5 for END-01/02/03 | Epilogue and ending text for US Enhanced, after `END-001`: English donor (PSP or new), timing against the art scroll, roster. |
| AUD-002 | M1-M5 for AUD/ANI | Voices and poses for US Enhanced, after `AUD-001`: the rest of the roster (Donovan, Sasquatch first). |
| QUO-001 | M1-M5 for QUO-01 | Victory quotes: inventory per release, selection conditions, donor English. |
| LOC-001 | M7 | Names in each edition (NAM-02/03; deferred from `DOC-002`); whether both releases' name art is on both discs; toggle decided early (`docs/lessons_from_xvsf.md`, lesson 9). |
| UI-001 | M8 | Title, attract, menus, credits, boot warnings: each surface the register marks different. |
| COV-001 | M8 | Coverage register: every row resolved (`docs/coverage_exceptions.md`). |
| SPECIAL-001 | M9, user approval | Unused or unreachable assets, debug features, hidden content. |
| REL-001 | after M5 | Copy Cyberbots `make_patch` (with the RetroAchievements header guard), `make_zips`/`check_zips` (and `add_files`/`make_ssp` only if needed); parameterize the source folder, manifest and author; decide formats early, since adding files rules out SSP (`docs/lessons_from_cyberbots.md`, section 4). Patches are Release assets only, never committed. |
