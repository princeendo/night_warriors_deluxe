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
- Reverse-engineering experiments in progress: none. `AUD-001` (Morrigan's
  voices: D-007, D-008) and `END-001` (Morrigan's epilogue: D-010) are
  `IN_PROGRESS`.
- **2026-11-14: save-state extractor validated** (`DBG-001`, `EXP-0006`,
  D-006). The tools for both investigations are ready.
- Next unblocked tasks: `AUD-001` (Morrigan's voices) and `END-001` (the
  epilogue screens), the user's first investigations. Offline meanwhile: `DIFF-001` (classify the 52
  differing files), `ENV-007` (database check), `DOC-003` (reference
  catalog).
- **2026-11-14: M1 reached, GATE-M0 GO recorded** (`EXP-0012`, D-012).
  The first difference is `END-01`, Morrigan's epilogue: in US RAM, clearing
  the epilogue flag, pointing the US `ST1` slot at `ST1JPN.BIN` and setting
  the language byte to Japanese after the main ending shows the Japanese
  epilogue after the English ending. The user (2026-11-14), asked "Count
  this as M1 reached, with your GO recorded now?": "Yes, record GO". M1 was
  reached inside `END-001` before the gate; the user accepted it as is.
- **2026-11-14: `DISC-001` done** (`EXP-0013`, D-013): the US start-up code
  sets flag 2 and language 1 as two constants in `MAIN.BIN`; the Japanese
  release never writes them. The flag is also read by the title, a sprite
  overlay and three character overlays (what for: UNKNOWN).
- **2026-11-14: the flag is a region switch** (`EXP-0014`, `EXP-0015`,
  D-014, D-015). Clearing it in US RAM brings back Morrigan's bat-seat line
  and the epilogue, but also the Japanese names (cast roll: GALLON for JON
  TALBAIN). Both releases hold both regions' tables; the flag picks. The
  Japanese-only items (epilogue gate, Morrigan's four voice calls, two
  `PL14` sound calls) are separate branches that a patch can open alone.
- **2026-11-14:** the flag's pause check is a US-only auto-pause when a
  controller is missing (`EXP-0016`, D-016).
- **2026-11-14:** the flag's title check makes only player 1's Start begin
  ARCADE/VS in the US release (SUPPORTED by code, `EXP-0017`). Every reader
  of the flag is now classified; the agent's RAM writes bypass the emulated
  SH-2 cache (check that a write was read before trusting it).
- **2026-11-14 (`DISC-002`, `EXP-0018`):** the first patched image's cold
  boot turned the win quote Japanese (the `ST1` name array is shared with the
  win screens). Version 2 loads `ST1JPN.BIN` only from the ending's own
  call; rehearsed correctly, its cold boot is next.
- **2026-11-14: M2 reached** (`DISC-002` done, `EXP-0018`, D-017): the
  version 2 image, cold-booted and played, keeps the English win quote and
  shows Morrigan's Japanese epilogue after the English ending, with US cast
  names; the unpatched control shows none.
- **2026-11-14: all 14 endings** (`EXP-0019`, D-018): the ending's character
  is `0x06080980`; forced with it, every character's Japanese epilogue shows
  on the version 2 image after the English ending, and none on the unpatched
  image.
- **2026-11-14: PSP intake** (`REF-002` done, `EXP-0020`, D-019): the US
  *Chronicle* image holds an English epilogue for all 14 characters, drawn
  into its ending movies; each tells the same story as the Saturn Japanese
  epilogue, mostly shortened (Lord Raptor's and Sasquatch's change the
  meaning).
- **2026-11-14: `END-001` leftovers** (`EXP-0021`, D-020): the `0x0600CFCC`
  branch is the Japanese 416-frame text introduction on black, not part of
  the card; the glyph strip is a by-product of clearing the flag in RAM,
  absent from both releases and the build (closed).
- **2026-11-15: epilogue English decided** (`GATE-TRANSLATION` block): the
  PSP text for all 14, spelling fixes logged, US Saturn names, rewrap then
  ask. The gate opens once `DOC-003` is done.
- **2026-11-15: `GATE-TRANSLATION` open for the `END-01` epilogues**
  (`DOC-003` done, `docs/references.md`).
- **2026-11-15: English in the epilogue** (`END-002`, `EXP-0022`, D-021):
  three PSP lines drawn in Morrigan's epilogue in the US win-quote font; the
  encoding is known. `END-001` closed; `END-02`/`END-03` moved to `END-003`.
- **2026-11-15: record lookup and the 238-glyph limit** (`EXP-0023`,
  D-022): Morrigan's whole English paragraph shows but stops at 238
  characters; every English epilogue is longer (263-345).
- **2026-11-15: Morrigan's whole English epilogue** (`EXP-0024`, D-023),
  forced, on top of the art; 302 characters of room, enough for 4 of 14.
- **2026-11-15: room for all 14** (`EXP-0025`, D-024): array 1 redrawn on
  top in the ending; Anakaris's 345-character English epilogue shows whole.
- **2026-11-15: all 14 English epilogues in one image** (`EXP-0026`,
  D-025), each forced and reviewed.
- **2026-11-15: blank win quote found and fixed** (`EXP-0027`, D-026): the
  first cold boot showed no win quote; `MAIN.BIN` is now untouched and the
  epilogue's list start is switched only inside the ending.
- **2026-11-16: M5 for `END-01`** (`END-002` done, `EXP-0028`, D-027): from
  a cold boot, the English win quote is kept and all 14 English epilogues
  show whole.
- **2026-11-16: main endings started** (`END-003`, user: "Main endings";
  `EXP-0029`, D-028): Japanese endings forced; the two regions' ending scripts
  differ in page count for 12 of 14 characters; Pyron's meaning differs.
- **2026-11-16: main endings compared** (`END-003` done, `EXP-0030`,
  D-029): the US main endings are a free rewrite; only Morrigan's loses
  Japanese text; four change in meaning.
- **2026-11-16: main-ending scope decided:** US Enhanced restores only
  Morrigan's missing lines (`END-004`), English from the PSP first, all else
  as shipped.
- **2026-11-16: Morrigan's main-ending lines restored** (`END-004` done,
  `EXP-0031`, D-030), confirmed from a cold boot.
- **2026-11-16: Morrigan's voices** (`AUD-002`, user choice; `EXP-0032`):
  the four region-flag guards in her code opened; the win line plays (forced).
- **2026-11-16: Morrigan's voices restored** (`AUD-002` and `AUD-001`
  done, `EXP-0032`, D-031): all four play in US Enhanced from a cold boot.
- **2026-11-16: Donovan and Sasquatch** (`AUD-003`, user choice): opening
  Donovan's first guard plays his Japanese-only win sample in US
  (`EXP-0033`, D-032); six `nop`s give Sasquatch his Japanese win poses,
  creatures and sample (`EXP-0034`, D-033), in `build/us_en_sasquatch`;
  both confirmed from a cold boot. `AUD-003` done. Every region-flag reader
  in the character code is now handled except Donovan's unreached second
  guard.
- **2026-11-16: edition switch decided** (`DIFF-001` done first, `EXP-0035`;
  `EDITION-001` done): one code set (the US release's) switched at run time
  from an options entry saved in spare save bytes; four editions, JP
  Enhanced included.
- **2026-11-16: edition switch built** (`EDITION-002` done, `EXP-0036`-
  `EXP-0038`, D-034): `build/us_edition` offers US Enhanced (default), US
  original and JP original from OPTION, confirmed from a cold boot. `EDITION-003`
  done: JP Enhanced adds the US main endings' extra content in new Japanese
  (`END-005`), hidden in the menu until it exists.
- **2026-11-25: v0.1.0 release prepared** (`ENV-007`, `DOC-004`, `REL-001`
  done): US (`T-1208H`, Redump `5836`) and JP 1M (`T-1202G`, Redump `3677`)
  source identities CONFIRMED against Redump; `make_patch`, `make_zips`, and
  `check_zips` ported from Cyberbots (`bac6fde`) with unit tests; xdelta-only
  release zip `night_warriors_deluxe_0.1.0_xdelta.zip` (49,807 bytes, SHA-256
  `92b8c26c…30e0`) built twice identically and round-trip verified to Track 1
  `25e05ec1…f1be` (RA header MD5 `8c7156c2…7e9e` unchanged). `END-005`,
  `QUO-001`, `LOC-001`, `REF-004`/`UI-001`/`COV-001`, `DIFF-002`, `REF-001`,
  and `REF-003` explicitly deferred by the user to post-0.1.0. Ready for tag
  `v0.1.0` and publication on github.com by `princeendo`.
- **2026-11-26: playtester follow-up.** Mixed-matchup `FULL`, the P1
  Anakaris audio report, Morrigan's Soul Fist trail panning, and Appendix
  access are in scope. A 4 MiB requirement is acceptable for full animation.
  A cart-free configuration is preferred if feasible. The first experiment
  confirmed that `CUT` and `FULL` load the same reduced sets in the first
  mixed attract fight on both retail discs (`ANI-002`, `EXP-0040`, D-036).
- **2026-11-26: `ANI-002` done** (`EXP-0041`, D-037): `FULL` fits one full
  set in the 1,372,412-byte fighter pools, so it works only in mirrors. A
  forced Anakaris vs. Huitzil `FULL` pair needs 883,644 more bytes and resets
  the console. `ANI-003` (cart-backed `FULL`), `AUD-004`, `AUD-005` and
  `APP-001` are `READY`.
- **2026-11-26: `APP-001` done** (`EXP-0042`, D-038 to D-041): Capcom's
  Appendix code works and persists on both retail releases and Deluxe. Deluxe
  now starts with the Appendix unlocked, and PRESS START TO EXIT sits one line
  lower (user decision). The agent build gained patch `0002` (cache-coherent
  writes), so injected pad presses now reach menus. V1-V4 pass again.
- **2026-11-26: `ANI-003` built and checked in Mednafen** (`EXP-0043`,
  D-042): with a 4 MiB cart, `FULL` now gives full animation to different
  fighters in Arcade and VS. Without one it behaves as shipped. Only the
  real-Saturn check remains. `AUD-004` and `AUD-005` are `READY`.
- **2026-11-26: `AUD-004` fixed** (`EXP-0044`, D-043): with Anakaris on P1,
  P2's shared sound effects played his copies (a stock bug in both
  releases). US Enhanced now plays each opponent's own sounds. Only a live
  check of Donovan's ice attack remains.
- **2026-11-26: `AUD-005` done** (`EXP-0045`, D-044): Morrigan's Soul Fist
  trail was pinned far left by an `and` for `or` in her code. It now follows
  the fireball. By user decision both sound fixes apply in every edition
  (`build/us_edition` Track 1 `4d70df42…4451`).
- **2026-11-27: the next-release scope now includes JP Enhanced, victory
  quotes, the names toggle, and the text and UI audits.** The user will
  verify the combined build on a physical Saturn after those changes are
  incorporated. `DIFF-002` identified the six ST text containers, the font
  and representative UI strings (`EXP-0047`, D-045).
- **2026-11-27: JP Enhanced is playable in Mednafen.** `END-005` adds
  six Japanese pages across Morrigan, Bishamon, Rikuo and Huitzil and
  exposes the fourth edition in OPTION MODE (`EXP-0046`, D-046).
- **2026-11-27: the Enhanced editions have a saved NAMES preference.**
  `LOC-001` confirmed both preference directions in OPTION MODE and a
  saved Japanese HUD label with an English victory quote in US Enhanced
  (`EXP-0048`, D-047).
- **2026-11-27: US Enhanced adds victory-quote variants for all 14
  fighters.** `QUO-001` found 323 selectable Japanese records and 56
  English. The user approved translations for more variety. The build
  adds 56, one per fighter and mirror/vitality condition alongside the
  existing US record. Verified the selectors and rendered all 56 in
  Mednafen (`EXP-0049`, D-048).

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

- **Status:** `DONE` (2026-11-25)
- **Milestone:** M0 (do early; XvSF did this the day before release)
- **Dependencies:** ENV-006.
- **Blockers:** None.
- **Objective:** Raise the identity of the two working images (Japanese 1M, US) from **SUPPORTED** to **CONFIRMED**, and learn what the Japanese labels (1M, 2M/4M, 3M) distinguish.
- **Acceptance criteria:** Each working image's track hashes match a named database entry (size, CRC-32, MD5, SHA-1 per track), or a mismatch is recorded with its consequence; every Redump entry for both titles is listed.
- **Done 2026-11-25:** Verified in the built-in browser against `http://redump.org/`. Both working images match Redump across size, CRC-32, MD5, and SHA-1 for every track: US `Night Warriors: Darkstalkers' Revenge` = Redump disc `5836` (`T-1208H`, V1.001); JP 1M `Vampire Hunter: Darkstalkers' Revenge` = Redump disc `3677` (`T-1202G`, V1.000). All Redump entries listed (`5836`, PAL `4675`, JP `3677` 1M, `3681` 2M/4M, `1456` 3M, Sample `20095`); `1M`/`2M, 4M`/`3M` confirmed as JVC glass-mastering batch ring codes (`T-1202GP-00715 <batch> C 62`). Recorded in `references/saturn_us/README.md` and `references/saturn_jp/README.md`.

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

- **Status:** `DONE`
- **Milestone:** M0 (do early)
- **Dependencies:** DOC-001.
- **Blockers:** None.
- **Objective:** Reuse the sibling platform references and list Vampire Hunter-specific prior art.
- **Acceptance criteria:** `docs/references.md` lists the platform references (Saturn, SH-2, CD/ISO 9660, Mednafen, CPS-II, MAME) with their sibling source, and separately the Vampire Hunter sources: the 23 sources of the web research (with what each may and may not be used for), translation or restoration projects, text dumps, official English releases, and guides/manuals.
- **Notes:** Start from the web research's source register (section 12). Its notable leads: the Arcade Patches CPS-2 restoration (unofficial, arcade-only), the PSP *Chronicle* gallery (official, unverified coverage), the Video Game Museum arcade ending gallery, and two conflicting fan epilogue transcripts.
- **Done 2026-11-15:** `docs/references.md`: the platform sections copied unchanged from Cyberbots (`cf9f6d0`; byte-identical, checked with `diff`); the CPS-II sets of this game in MAME 0.289 `cps2.cpp` (SHA-256 `a8c09ef8…`, matching the MSHvSF pin); the web research's 23 sources with what each may and may not be used for; official English releases, restoration projects, text dumps and guides by kind; this project's evidence records. Sources were not re-read; nothing was downloaded.

### DOC-004 - Start the README in its final layout

- **Status:** `DONE` (2026-11-25)
- **Milestone:** before REL-001
- **Dependencies:** DOC-002.
- **Blockers:** None.
- **Objective:** Avoid XvSF's post-release README reorganization.
- **Acceptance criteria:** `README.md` follows the MSHvSF/Cyberbots README section layout, with placeholders for what is not done.
- **Done 2026-11-25:** Rewrote `README.md` in the MSHvSF/Cyberbots layout (`Download`, `What's Changed`, `Patch Files` + `Applying a Patch`, `Build the Patch`, `Development`), linking `v0.1.0`, `release/README.md`, `release/notes_v0.1.0.md`, and Redump disc `5836`.

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

- **Status:** `DONE`
- **Milestone:** GATE-TRANSLATION
- **Dependencies:** DOC-002.
- **Blockers:** None.
- **Objective:** Decide whether the English PSP *Darkstalkers Chronicle: The Chaos Tower* is a reference for official English epilogues and revised endings, and if so record its identity.
- **Acceptance criteria:** Either every component is hashed with an identity status, or the task is `REJECTED` with the user's reason.
- **Notes:** The web research names it the most promising official English source (its sources 6 and 7) but its coverage and alignment with the Saturn text are unverified.
- **Done 2026-11-14 (`EXP-0020`, D-019):** the user supplied the US ISO and asked to try it before a new translation (kept as a reference). Hashed with identity SUPPORTED (`references/psp_chronicle_us/README.md`). English epilogues for all 14 characters are text drawn into `movie/hunend/HmovieNN_2.pmf`; frames, hashes and the per-character comparison with the Saturn Japanese are in `EXP-0020`. Whether to use this text, and how to treat its typos and changed meanings, is `GATE-TRANSLATION`.

### REF-003 - Paired manuals (off-disc, optional)

- **Status:** `BACKLOG`
- **Milestone:** M9 or out of scope
- **Dependencies:** DOC-002.
- **Blockers:** No scans supplied; whether printed material is in scope is still to ask.
- **Objective:** Resolve `BIO-01` or reject it as outside a disc image.
- **Acceptance criteria:** A page-level JP/US comparison with provenance, or `REJECTED` with the user's reason.

### REF-004 - Inventory the text, audio and presentation surfaces of both releases

- **Status:** `READY`
- **Milestone:** M1
- **Dependencies:** EMU-021 (done).
- **Blockers:** None.
- **Objective:** List every place either release shows text or plays a voice, and capture each in both releases under matched settings, so the register's rows can be compared.
- **Acceptance criteria:** `docs/text_surfaces.md` holds a table of surfaces (screen, when shown, sample screenshot path and hash per release, same/different) from screenshots the agent reviewed, built from several captures of each release: a cold boot left on the attract loop, title and menus (Appendix included), one arcade run through at least two fights with a continue, a win screen, one ending with its credits. Every register row it touches is updated with both regions' evidence.
- **Notes:** XvSF's single session missed five surfaces (`docs/lessons_from_xvsf.md`, lesson 6); Cyberbots' kept every state and still missed endings and versus mode (`docs/lessons_from_cyberbots.md`, lesson 3). Keep every state (`--keep-states 0`). Match the settings named by the web research before comparing (animation options, Appendix).

## Phase E: Differences, Checkpoints And Memory Analysis

### DIFF-001 - Classify the 52 differing files offline

- **Status:** `DONE` (2026-11-16)
- **Milestone:** M1 (static analysis only; no image change)
- **Dependencies:** ENV-003.
- **Blockers:** None.
- **Objective:** For each `FILE-nn` row, describe how the two regions' bytes differ without assuming what the difference does.
- **Acceptance criteria:** A script (`tools/disc/`) lists, per differing file, the runs of differing bytes (offset, length) and classifies each as a likely pointer/relocation change (consistent 32-bit deltas into a load range) or a content change; the SH-2 code files are identified by disassembly of their entry points; same-size files (`ENDING.O`, `PL*`, `SOBJ*`, `P00.BIN`, `ST?USA.BIN`) are summarized first; `PL*.O` vs `PL*.O2` is explained or listed as open. Committed output: offsets, lengths, hashes and counts only, no game text or code bytes (`AGENTS.md` rule 21). Register rows updated.
- **Notes:** Which file is loaded when, and where, are runtime questions for `DBG-004`. A content change in a program overlay is a lead, not an explanation.
- **Done 2026-11-16 (`EXP-0035`):** `tools/disc/diff_files.py` (tested) classifies every differing word as pointer or content and finds code by entry tables. The 41 overlays are relinked, not rewritten (pointers `-0x50`, `-0x858`, `-0x86C`, `-0x8C4`; 0-40 content words each); `.O2` is `.O` relinked `+0x8000` for player 2; `0.BIN`, `MAIN.BIN`, `TITLE.O` changed as code; `P00`/`P03_` are data. A region's code is one linked set. Register rows `FILE-01`-`FILE-07` updated.

### DIFF-002 - Locate where each release keeps its text

- **Status:** `DONE`
- **Milestone:** M1 (static analysis only)
- **Dependencies:** ENV-003.
- **Blockers:** None.
- **Objective:** Find the storage and encoding of in-game text in both releases.
- **Acceptance criteria:** Candidate containers are tested (`ST?JPN`/`ST?USA`/`ST?HIS.BIN` and their offset tables; `MOJI.CHR`/`MOJI.TBL` as a font; graphics files for text drawn as art); for each, the evidence for or against is recorded; relative search (the method that found Cyberbots' arcade English, `EXP-0008`) is run on the US files for a few English strings known from the US release.
- **Notes:** A kana-run scan found no plain Shift-JIS in the program files (`references/saturn_us/README.md`). That excludes plain Shift-JIS for the strings searched. D-011 and D-021 identify the engine's Japanese and Latin codes.
- **Done (2026-11-27, `EXP-0047`, D-045):** documented the observed text routes, headers, hashes, MOJI, and image-based labels. The US relative scan finds representative menu and HUD strings at shift zero. The two English-format quote files contain the same text and pointers, with only 116 changed Y bytes. Spanish dialogue exists in both regions; normal use of it has not been observed.

### DIFF-003 - Choose the first difference and its milestone unit

- **Status:** `DONE` (2026-11-14, by the user's `GATE-M0` GO)
- **Milestone:** M1
- **Dependencies:** REF-004, DIFF-001, AUD-001, END-001.
- **Blockers:** REF-004.
- **Objective:** Pick one register row (and one character, where it applies) as the M1 target, and fix the milestone unit for its class.
- **Acceptance criteria:** The choice and reason are recorded; the difference is captured in both releases under the same action and settings; a checkpoint shortly before it exists in the US release.
- **Result:** `END-01`, Morrigan's epilogue; milestone unit: one character's ending. Captured in both releases under the same forcing (`EXP-0010`); US checkpoint before it: `local/aud001/us-session/rec/states/f00011016.mcs` (won KO) and `local/end001/us-enhanced-test/states/r006089.mc0` (emblem card). Reason: the user's priorities and the first item reached (`EXP-0012`). `REF-004` (its blocker) was not done; the user's GO accepted the choice without it.
- **Notes:** Candidates by the web research's weight: one character's epilogue (END-01), one Morrigan voice event (AUD-01 to AUD-03, whose sound files are identical on both discs), one renamed character (NAM-02). The user's priorities (2026-11-13): Morrigan's voices (`AUD-001`) and the epilogues (`END-001`); choose between them from those tasks' findings.

### DBG-002 - Observe how the chosen difference is selected

- **Status:** `DONE` (2026-11-14, for `END-01` Morrigan, by the user's `GATE-M0` GO)
- **Milestone:** M1
- **Dependencies:** EMU-021, DIFF-003.
- **Blockers:** EMU-021.
- **Objective:** Learn whether the chosen item is fixed or varies from one checkpoint, in both releases, before planning checkpoints.
- **Acceptance criteria:** Several replays of one checkpoint per release, with what is shown or played recorded.
- **Result:** the ending sequence is fixed for one character: the US release forced four times from `f00011016` (`EXP-0010`, `EXP-0012`) and the Japanese twice from the `f00023129` line gave the same main ending each time.

### DBG-003 - Capture checkpoints

- **Status:** `DONE` (2026-11-14, for `END-01` Morrigan, by the user's `GATE-M0` GO)
- **Milestone:** M1
- **Dependencies:** DBG-002.
- **Blockers:** DBG-002.
- **Objective:** States and evidence before the item, during it, and after it, in both releases.
- **Acceptance criteria:** Each checkpoint is reproducible from its state and named in an experiment record.
- **Result:** checkpoints before (won KO), during (main ending, emblem card) and after (epilogue) the item in both releases, kept every 300 frames under `local/end001/` and named in `EXP-0010` and `EXP-0012`.

### DBG-004 - Find the code and data behind the chosen difference

- **Status:** `DONE` (2026-11-14, for `END-01` Morrigan, by the user's `GATE-M0` GO)
- **Milestone:** M1
- **Dependencies:** DBG-001, DBG-003, DIFF-001.
- **Blockers:** DBG-003.
- **Objective:** Find what each release runs or reads at the item, and where they diverge.
- **Acceptance criteria:** The renderer or sound call is identified by a controlled change; the data in RAM is located; the divergence is tied to a `FILE-nn` row (or shown to be elsewhere); whether the other release's content is already on the base disc is recorded as tested or open.
- **Result:** the ST1 loader and its gate found by a PC breakpoint and confirmed by controlled writes (`EXP-0012`); the text located in RAM and on both discs (`ST1JPN.BIN`, `EXP-0011`); the divergence is not in a `FILE-nn` row's code but in two WRAM-H data bytes (D-012); the Japanese content is on the US disc (D-011). Where the bytes are set is `DISC-001`.

## Phase F: The User's First Investigations

### AUD-001 - Are Morrigan's Japanese-only voices on the US disc?

- **Status:** `DONE`
- **Milestone:** M1 (investigation; no image change)
- **Dependencies:** EMU-021, DBG-001.
- **Blockers:** None.
- **Objective:** For each of `AUD-01` (normal throw), `AUD-02` (command throw) and `AUD-03` (bat-seat win pose), learn what each release plays, and whether the Japanese sound is on the US disc.
- **Acceptance criteria:** Each event is reproduced in both releases from matched checkpoints (same characters, settings and inputs) with sound recorded (ignored files, hashes kept); the sound command each release issues at the event is logged (sound RAM writes or the sound driver's command queue); the register rows get a change type (**conditionally suppressed**, **asset absent**, **not a difference**, or other) with that evidence; if the Japanese sample is on the US disc, where it is and what selects it are recorded.
- **Notes:** Static (`SESSION-0002`): every sound file (`SOUND.HED`, `SOUND.MP`, `SOUND.TBL`, `SDDRVS*.TSK`, all `*.SEQ`) and `MORRIGA.BIN`, `MORRIGA1.SEQ`, `MORRIGA2.SEQ` are byte-identical on both discs, so **HYPOTHESIS**: the samples are present on the US disc and the US code does not call them. The report is from memory (web research source 13); a "not a difference" outcome is possible. Method: Cyberbots `EXP-0088` (`-qtrecord`, sample-level comparison); the extractor does not yet cover sound RAM (`DBG-001`). Which `PL*` overlay is Morrigan's is unknown (`DIFF-001`).
- **Progress 2026-11-14:** `EXP-0007` recorded one Morrigan session per release (sound, a state every second, screenshots); the bat-seat pose occurs in both releases; the user heard "some more dialogue" in the Japanese one. Next: replay states before each event with sound-command logging.
- **Progress 2026-11-14 (`EXP-0008`, D-007):** the bat-seat pose line is CONFIRMED present on the US disc and not played (sample `MORRIGA.BIN` `0x1BAA0`); throw (`50C2C`), Vector Drain (`41220`) and hurt (`4F10C`) samples play only in the Japanese session (SUPPORTED, 1 s states). Remaining for `DONE`: locate US throws and replay them densely beside Japanese ones (matched evidence), then find what selects each sample.
- **Progress 2026-11-14 (`EXP-0009`, D-008):** a waveform search of the `EXP-0007` recordings confirms the normal-throw voice is never played in the US release (an observed US throw is silent); Vector Drain and hurt voices are absent from the whole US recording (SUPPORTED). Live slot logging during play was abandoned: it made the game stutter (the user's report). Remaining for `DONE`: what selects each sample (the code to change for US Enhanced); a US Vector Drain, if wanted.
- **Progress 2026-11-14 (`EXP-0014`, D-014):** the epilogue flag also gates Morrigan's voices: clearing it in US RAM after her winning KO makes the bat-seat line play at the same pose (control: no line). Her code (`PL05`) skips four voice calls when the flag is non-zero. Next: the throw and Vector Drain with the flag cleared (needs play), and what `PL14` (two guarded sound calls) is.
- **Done 2026-11-16 (via `AUD-002`, D-031):** what selects each sample is the four guarded calls in `PL05` (codes `0x134`-`0x139`); opening them plays the Japanese samples in the US release. The register rows have their change type (conditionally suppressed).

### END-001 - The per-character epilogue screens

- **Status:** `DONE`
- **Milestone:** M1 (investigation; no image change)
- **Dependencies:** EMU-021, DBG-001.
- **Blockers:** None.
- **Objective:** Show what follows each character's ending in each release, and find what the Japanese release uses for the post-ending artwork with scrolling text and whether the US disc still holds it.
- **Acceptance criteria:** For one character first, the whole ending sequence (main ending, artwork and text scroll, credits) is captured in both releases without skipped transitions (states kept, screenshots agent-reviewed); the epilogue's artwork and text are tied to their files and RAM; whether the US release shows the artwork, shows it without text, or skips it is recorded; whether the Japanese text (or its graphics) is on the US disc is recorded with the comparison that shows it; register rows `END-01` to `END-03` updated. A method to reach every character's ending by forcing (not playing) is recorded.
- **Notes:** The user (2026-11-13): "Each character has a post-ending artwork accompanied by scrolling Japanese text." Static (`SESSION-0002`): the 14 `END*.BG` files (`END00`-`END0D`) and `ENDDATA.BIN` are byte-identical on both discs; `ENDING.O` is the same size with 1,668 bytes changed (`0x5506`-`0xFA4F`). **HYPOTHESIS**: `END*.BG` are the artwork (14 files, 14 characters) and the US `ENDING.O` skips or cuts the text. Japanese text could also be drawn as graphics; no plain Shift-JIS was found. English for US Enhanced is a later `GATE-TRANSLATION` question (PSP *Chronicle*, `REF-002`, or a new translation). Cyberbots forced endings with four RAM writes (`docs/lessons_from_cyberbots.md`, lesson 4).
- **Progress 2026-11-14 (`EXP-0010`, D-009, D-010):** endings are forced by writing 9 to the stage byte (`0x0608097B` JP, `0x0608092B` US) right after a won KO. Morrigan's ending: the Japanese release shows an epilogue paragraph over her scrolling art; the US release scrolls the same art with no text. Next: where the Japanese text comes from (RAM, then file) and whether the US disc holds it; then the other 13 characters (each needs a won-KO state for that character).
- **Progress 2026-11-14 (`EXP-0011`, D-011):** the Japanese epilogue text is `ST1JPN.BIN` (16-bit `MOJI.TBL` codes, drawn as VDP1 sprites from `MOJI.CHR`); all three files are identical on the US disc, which loads the font but no `ST1` file at the ending. Next: the other 13 endings (a won-KO state per character), then the code that picks `ST1JPN`/`ST2JPN` vs `ST2USA` (what US Enhanced must change).
- **Progress 2026-11-14 (`EXP-0012`, D-012):** the switch is data, not code: an epilogue flag (`0x060808EA` JP 0 / `0x0608089A` US 2) gates loading an `ST1` file, and the language byte (`0x060808D2` JP 0 / `0x06080882` US 1) picks the file and how text is drawn. In US RAM, the English main ending followed by the Japanese epilogue was shown (the M1 outcome, reached here before the formal `GATE-M0` GO). `ST1USA.BIN` is a placeholder (rows of "A"). Next: where the two bytes are set; the other 13 endings; an English epilogue format (`GATE-TRANSLATION`).
- **Done 2026-11-15 (user decision):** closed for `END-01` (the epilogues), whose criteria are met: captured in both releases (`EXP-0010`), tied to `ST1JPN.BIN`/`MOJI` and RAM (D-011, D-012), the US shows the art without text (D-010), the text is on the US disc (D-011), and every character is reached by forcing (D-009, D-018). Rows `END-02` and `END-03` moved to `END-003` (user: "Split END-02/03 out"), which waits for `END-01` to reach M5 (rule 23).

### END-002 - English epilogues for US Enhanced (`END-01`, M3-M5)

- **Status:** `DONE`
- **Milestone:** M3-M5 for `END-01`
- **Dependencies:** END-001, DISC-002, GATE-TRANSLATION (epilogue scope, 2026-11-15).
- **Blockers:** None.
- **Objective:** Show each character's epilogue in English (the PSP *Chronicle* text under the user's 2026-11-15 decisions) after the English ending on a patched US image, where the Japanese epilogue shows now.
- **Acceptance criteria:** (1) The format the epilogue renderer reads (file header, records, character codes, line and length limits) is recorded with evidence. (2) One character's English epilogue shows on a patched image, with before/after screenshots, a control, and every line's provenance and each logged edit (M3). (3) A second character through the same tool (M4). (4) All 14, each forced and reviewed, with the edits log and any fit question put to the user (M5).
- **Notes:** Known: the epilogue renderer draws `MOJI` codes from the file in the slot it reads (D-011, D-017); `ST1USA.BIN` holds the US win quotes and placeholder epilogue records drawn as rows of "A" (`EXP-0012`, `EXP-0018`). Whether the font (`MOJI.CHR`) has Latin glyphs, and in what codes, is UNKNOWN.
- **Progress 2026-11-15 (`EXP-0022`, D-021):** in English mode the epilogue renderer draws the win-quote Latin codes (ASCII + `0x80` capitals and punctuation, `0201`-`021A` lowercase, `0020` space, comma `00AE`, period `00AC`) in the US win-quote font, about 12 px per character (about 26 per line). Three PSP lines in Morrigan's record showed in English over her art. Open for criterion 1: how a character's record is found (the offset table at `0x0C`), how many lines fit, and the line spacing.
- **Progress 2026-11-15 (`EXP-0023`, D-022):** records are found through a self-relative table at `0x0C` (index = roster − 1), and the ending reads nothing else in the file, so English records can sit anywhere in it. Morrigan's whole PSP paragraph (16 lines) showed in English but was cut at its 238th character: the glyph list at `0x060839D4` has room for 238 entries. All 14 English epilogues need 263-345. Next: find RAM unused during the ending and move the list there (no text cut), then test 14-18 lines.
- **Progress 2026-11-15 (`EXP-0024`, D-023):** the glyph list moved to sprite array 2 (one literal, `0x06037A98`) with an off-screen filler line over the player sprite slots: Morrigan's whole English epilogue shows on top of her art (forced; cold boot pending). Room: 302 characters; Morrigan, Bishamon, Pyron and Donovan fit, the other ten are 5-43 over. Array 1 is drawn under the art.
- **Progress 2026-11-15 (`EXP-0025`, D-024):** array 1 is drawn again after the art by a 36-byte routine in `ST1JPN.BIN` reached through `ENDING.O`'s `r12`; with the list from array 1 slot 17 there is room for 413 characters. Morrigan (16 lines) and Anakaris (345 characters, 18 lines at 12 px, the longest) show whole on top of their art (forced). Criteria 2-3 met except the cold boot. Next: all 14 in one image (criterion 4), then a cold boot with the user.
- **Progress 2026-11-15 (`EXP-0026`, D-025):** one image with all 14 English epilogues (Track 1 `21fb1c79…`); a fixed routine address crashed Demitri, Rikuo and Pyron (the file loads at a per-character address), fixed by computing `r12` from the loader's slot table. All 14 forced endings show the whole English paragraph on top of the art and reach the cast roll. Criteria 1-4 met by forcing; a cold boot of this image with the user remains before `END-002` is done.
- **Progress 2026-11-15 (`EXP-0027`, D-026):** cold boot of the `EXP-0026` image with the user: the win quote was blank (the user's report), because the win screens share the epilogue's text builder and the on-disc `MAIN.BIN` literal change. Fixed: `MAIN.BIN` untouched; the ending-only routine sets the literal on its first call and restores it after. Win quote English again; Pyron, Anakaris and Morrigan whole (forced). Next: a second cold boot with the user.
- **Done 2026-11-16 (`EXP-0028`, D-027):** cold boot with the user (Demitri beat Victor): English win quote; from that session's bonus-screen state, all 14 endings (stage and character bytes only) show the whole English epilogue on top of the art and reach the cast roll. Image: `build_en_epilogue.py --late-array1 --step 0` 1-14, Track 1 `8ebc0ca3…0b67`. Open for later tasks: the Japanese editions need `ST1JPN.BIN` intact (`EDITION-001`); the transcription's second reading; real hardware.

### END-003 - The main endings in each release (`END-02`, `END-03`)

- **Status:** `DONE`
- **Milestone:** M1 (investigation; no image change)
- **Dependencies:** END-002 (`END-01` through M5, rule 23; the user chose this class on 2026-11-16: "Main endings").
- **Blockers:** None.
- **Objective:** For each character, show what the main ending (the scenes before the epilogue) is in each release, and classify every difference: text rewritten, page or scene omitted, added, reordered, retimed, or asset absent.
- **Acceptance criteria:** (1) A method to force each character's ending in the Japanese release, with its character byte confirmed. (2) All 14 main endings captured in both releases under the same forcing (states kept, screenshots agent-reviewed). (3) The text of each tied to its file (`ST2JPN.BIN`, `ST2USA.BIN`) and record, with a per-character inventory of scenes and pages in each release. (4) Every difference recorded in `docs/difference_register.md` with both regions' evidence and its change type; Pyron's (`END-03`) compared by meaning. English for any restored Japanese-only text is a later `GATE-TRANSLATION` scope.
- **Notes:** Leads only: the web research (section 5.3) reports rewritten English for Pyron, Huitzil and Bishamon and "different page counts" (arcade). Known on these discs: the US main-ending text is `ST2USA.BIN` (ASCII, `/` line breaks; `EXP-0011`), the Japanese is `ST2JPN.BIN`; US endings are forced with `0x0608092B` = 9 and `0x06080980` = roster number (D-009, D-018).
- **Progress 2026-11-16 (`EXP-0029`, D-028):** the Japanese ending character is `0x060809D0`; all 14 Japanese endings captured (`local/end003/jp-NN`), the US ones are `EXP-0019`'s controls. The two regions' per-character ending scripts are decoded: page counts differ for 12 of 14 (details in D-028); Pyron's closing line differs in meaning (`END-03`, SUPPORTED). Open: what each page says (the page-id-to-record mapping is UNKNOWN; text can be read from `ST2USA.BIN` and drawn from `ST2JPN.BIN`), so which extra pages are new content.
- **Done 2026-11-16 (`EXP-0030`, D-029):** all 14 main endings compared page by page from the files (US decoded, Japanese drawn from `MOJI`), through the two scripts; the Japanese forced runs checked for the right character. Result: a free rewrite re-paginated for English; Japanese text missing from the US only in Morrigan's (two lines and a pause page); meaning changes in Felicia, Bishamon, Huitzil, Pyron (and Victor's resolution); added US lines in Bishamon, Rikuo, Huitzil; renames in Hsien-Ko's and Donovan's. Readings are SUPPORTED. Whether any of this goes into US Enhanced is a user decision (rule 30 keeps the US wording by default) and a later task.

### END-004 - Restore Morrigan's missing main-ending lines (US Enhanced)

- **Status:** `DONE`
- **Milestone:** M3 for `END-02` (Morrigan only, user decision 2026-11-16)
- **Dependencies:** END-003, END-002 (the build it extends), GATE-TRANSLATION (`END-02` Morrigan block, 2026-11-16).
- **Blockers:** None.
- **Objective:** In US Enhanced, Morrigan's main ending shows the Japanese-only pages the US drops (her request for bed, the butler's reply, the pause page; Japanese `ST2JPN` `36`, `37`, `B1`), in English, with every other US line unchanged.
- **Acceptance criteria:** (1) The PSP *Chronicle* Morrigan main-ending movie (`Hmovie04_1`) read for these lines, with frames and hashes; a new translation only after the user's yes. (2) The US script (`0x0605B730` entry 4) and `ST2USA.BIN` changed to show the restored pages in the Japanese order, from a cold boot, with before/after screenshots and the unpatched control. (3) The other 13 main endings and the win quotes unchanged (checked).
- **Notes:** The scripts live in `MAIN.BIN` (loaded at boot; the US table is read only by the ending, but check every screen that shares code, `EXP-0027`). Page timing and order: Japanese `34`-`B2` (D-028).
- **Progress 2026-11-16 (`EXP-0031`, D-030):** the PSP has no English for the lines (its main ending reuses the US text); the user approved a new translation ("I'm a little tired. / Prepare my bed.", "Certainly, mistress."). New records in `ST2USA.BIN`'s unused tail, a new 11-page script over her Japanese script, pages 33-36 shortened so both lines sit in the butler scene. Forced: in step, card clean; win quote, Pyron and Anakaris unchanged. Next: cold boot with the user.
- **Done 2026-11-16 (`EXP-0031`):** cold boot with the user (Morrigan beat Victor): English win quote; her ending forced from that session's state shows both restored lines in the butler scene and the rest as shipped; Pyron's epilogue unchanged. Debt for `EDITION-001`: her Japanese script slot now holds the new US script.

### AUD-002 - Morrigan's Japanese-only voices in US Enhanced

- **Status:** `DONE`
- **Milestone:** M2-M3 for `AUD-01`, `AUD-02`, `AUD-03`, `AUD-05` (user choice 2026-11-16: "Morrigan's voices")
- **Dependencies:** AUD-001 (D-007, D-008, D-014), END-004 (the build it extends).
- **Blockers:** None.
- **Objective:** US Enhanced plays Morrigan's four Japanese-only voices (normal throw, Vector Drain, bat-seat win line, hurt) with the region flag kept at 2, by opening the four flag-guarded calls in her code (`PL05.O` and its player-2 copy `PL05.O2`).
- **Acceptance criteria:** (1) Each of the four guards tied to its event. (2) A patched image plays each voice where the Japanese release does, shown by recorded sound (sample search) from a cold boot and play, with an unpatched control. (3) Nothing else about her or the opponent changes (no other `PL05` difference; win quotes and endings unchanged).
- **Notes:** Guards (US `PL05.O`, base `0x06001000`, same offsets in `PL05.O2`): `bf` at file `0x1490` (codes `0x137`/`0x136`), `0x1A1E` (`0x134`/`0x136`, through `0x0603A76E`), `0x3342` (`0x139`), `0x5280` (`0x135`). The US and Japanese `PL05.O` differ only in 465 address bytes (relocation, `MAIN.BIN` addresses). Sound is identical on both discs (`AUD-001`).
- **Progress 2026-11-16 (`EXP-0032`):** with the four guards made `nop` in RAM (flag 2), the bat-seat line plays at her win; one at a time, only the guard at `0x06002490` does it. Image built (`build_voices.py`, Track 1 `2985ff73…`). Next: a cold-boot play session (throws, Vector Drain, hurt, a win).
- **Done 2026-11-16 (`EXP-0032`, D-031):** cold boot and play with the user (Morrigan vs. Jon Talbain): throw, hurt, Vector Drain and win voices all found in the recording at their events; three guards tied by PC log, hurt by elimination; win quote English. The rest of the roster (Donovan `AUD-04`, Sasquatch `ANI-01`) is a later task.

### AUD-003 - Donovan's and Sasquatch's Japanese-only behaviour (`AUD-04`, `ANI-01`)

- **Status:** `DONE` (2026-11-16)
- **Milestone:** M1-M3 (user choice 2026-11-16: "Other characters' voices")
- **Dependencies:** AUD-002 (the method and the build it extends).
- **Blockers:** None.
- **Objective:** Find what the Japanese release plays or shows for Donovan and Sasquatch that the US release does not, and restore it in US Enhanced as for Morrigan.
- **Acceptance criteria:** (1) `PL14`/`PL10` tied to Donovan/Sasquatch by a fight. (2) Each guarded difference reproduced in both releases from play (sound recorded, samples identified with `EXP-0008/dense.py`). (3) A patched image plays or shows the Japanese behaviour from a cold boot, with the win quote and other characters unchanged.
- **Notes:** Only `PL05`, `PL10`, `PL14` (and `SOBJ08.O3`) read the region flag. `PL14.O`: two guarded sound calls (`bf` at file `0x111C`, codes `0x1B4`; `0x23C4`, `0x1B2`), opened in `EXP-0033/build_donovan.py`. `PL10.O`: six readers that pick routines and object settings (calls to `0x06030ABA`, states 64/48, routine 1 vs 5), likely pose logic; not patched yet.
- **Progress 2026-11-16 (`EXP-0033`):** sessions with the user as Donovan in both releases. `PL14` is Donovan's code (CONFIRMED). The Japanese release makes the first guarded call at his win (frame 180 of the replay; a looping sample `0x1B4B2` starts then); the first US replay never reached the KO (a replay has no input), which is why it never entered that code. From three post-KO US states the patched image runs it like the Japanese one, and the only sample that changes is `0x5687A`: the Japanese release and the patched US play it after the shared `0x1B4B2`; with the guard restored the US does not (D-032). Criterion 2 met for Donovan's first guard; the second (`0x23C4`) was not reached. Next: a cold boot of `build/us_en_donovan` with the user (criterion 3), then Sasquatch.
- **Progress 2026-11-16 (`EXP-0034`, static):** all six `PL10` readers sit in one win-pose chooser. With the flag non-zero, poses 0 and 4 (4 = Up + A + B + C held, by the pad table) spawn no effect objects and random pose 1 becomes pose 5 (SUPPORTED, from the code). Sessions with the user in both releases confirmed Up + A + B + C (`0x0708`) gives pose 4. Forced replays: the US skips the small snow creatures and sample `0x53116` in poses 0, 1 and 4 and plays pose 5 for pose 1; the flag cleared, or only the six guards `nop`, give the Japanese result (D-033). `EXP-0034/build_sasquatch.py` (Track 1 `e6e81ccc…`) loads them from disc. Criterion 2 met for both characters. 
- **Done 2026-11-16 (cold boot, `local/aud004/cold-session`):** the user won as Donovan and as Sasquatch on `build/us_en_sasquatch` (Track 1 `e6e81ccc…`). All eight guards read `0009` from the disc; Sasquatch's shy pose and snow creatures show live and `0x53116` plays; Donovan's `0x5687A` plays after his round-2 win (pose 0 only; round 1 takes pose 1, which has no call in either region). Win quotes unchanged. All criteria met. Left open: Donovan's second guard (`0x23C4`, code `0x1B2`) was never reached.

### EDITION-001 - Design the edition switch

- **Status:** `DONE` (2026-11-16)
- **Milestone:** M7 (design may start once `DIFF-001` and one of `AUD-001`/`END-001` are done)
- **Dependencies:** DIFF-001.
- **Blockers:** None for the static part.
- **Objective:** Decide how one image offers JP original, US original, US Enhanced (and JP Enhanced if needed), from measured costs.
- **Acceptance criteria:** Options with costs presented to the user as a multiple-choice question: where the choice is made (boot menu, options screen, a button held at boot), where it is stored, and how each edition gets its code and data (both regions' differing files on disc and loaded by name, or one region's files plus patches applied at load); whether "original" must be byte-for-byte that release's code; the disc-space route. The answer is recorded verbatim.
- **Notes:** Static (`SESSION-0002`): track 1 has 150 free sectors (0.3 MiB) in both releases; one region's copy of the 52 differing files is about 2.1 MB; the header differs (`T-1202G` vs `T-1208H`, area `JT` vs `U`). Growing track 1 moves track 2 (a short warning or silence), changes the system area's sizes, and rules out SSP (`docs/lessons_from_cyberbots.md`, section 4). The system area also decides which BIOS region a real Saturn accepts: **UNKNOWN** how a merged image should be labelled. Cyberbots' options sub-menu and spare-save-byte pattern (D-055 to D-058) is the sibling precedent.
- **Decision 2026-11-16 (verbatim, multiple choice; options and costs in `EXP-0035` and `research_log.md`):**
  - "Edition switch: must 'JP original' and 'US original' each run that release's own code, byte for byte? (Each region's code is one linked set — boot, main program and 41 overlays — so the regions can't be mixed file by file.)" → "No, one code set"
  - "Where should the player choose the edition?" → "Options menu, saved"
  - "Is a JP Enhanced edition needed (Japanese text and voices, plus fixes like the US Enhanced ones)?" → "Yes"
- **Meaning:** one code set, the US release's, switched at run time; "JP original" is the US code in Japanese mode (region flag 0, language 0), not the Japanese release byte for byte, and keeps the US code's own changes. The edition is an entry in the game's options, saved in spare save bytes (the Cyberbots pattern). Four editions: JP original, US original, US Enhanced, JP Enhanced (its content to define).


### EDITION-002 - The edition byte and options entry (US code)

- **Status:** `DONE` (2026-11-16)
- **Milestone:** M7
- **Dependencies:** EDITION-001.
- **Objective:** One US image where an options entry, saved in spare save bytes, selects JP original, US original, US Enhanced or JP Enhanced at run time.
- **Acceptance criteria:** (1) Where the options screen and save block are, and spare bytes proven unused (as Cyberbots D-055 to D-058). (2) The region flag and language byte set from the saved edition at the points that set them now (`DISC-001`). (3) Every US Enhanced change turned from a static patch into a run-time test of the edition: `PL05`/`PL10`/`PL14` guards, Morrigan's script, `ENDING.O` hook; the English epilogues moved out of `ST1JPN.BIN` so the Japanese editions get it intact. (4) Each edition from a cold boot with the user against its reference (JP 1M for JP original; stock US for US original), differences listed.
- **Notes:** Known differences the US code keeps in Japanese mode: only player 1's Start begins a game (`EXP-0017`), pause on a missing pad (D-016), and unexplained main-program changes (`EXP-0035`). Whether `P00.BIN`/`P03_.BIN`/`P03_.SPR` (data, 344 JP sectors, content UNKNOWN) must be carried for JP original is open; 150 sectors are free.
- **Progress 2026-11-16 (`EXP-0036`):** settings block `0x060830B4` (0x104 bytes saved in the 512-byte `N_WARRIORS_` file; load `0x06014588`, unpack `0x06014734`, pack `0x060148C4`); bytes `0x11`-`0x17` unused by both routines and untouched in boot, fight and win replays (SUPPORTED). The unpack runs after the start-up sets the flag and language, so it can apply the edition. Plan for criteria 2-4 in `EXP-0036`. Options screen found in two sessions with the user: `TITLE.O`, cursor `0x0608086C`, per-line handlers from `0x060052B8`, Start saves through the pack (the user's change was block byte `0x08`, `0x060809C6`). Menu layout found (`0x06018A1A` draws each line; APPENDIX shown only when `0x06080A2B` is set). **Decision 2026-11-16 (verbatim):** "Where should the EDITION line go? (OPTION MODE has 9 lines, a hidden APPENDIX slot below CONFIGURATION, then PRESS START TO EXIT; APPENDIX only shows once unlocked.)" → "Replace the blank slot": EDITION takes the APPENDIX slot (y `0xB8`) while APPENDIX is locked, and moves below it once unlocked. Open: free memory for the new menu code and Morrigan's Enhanced script (`EXP-0037`: nothing is free everywhere; while the title runs `0x06009565`-`0x0600FFFF` stays zero, so title-time code can apply the edition and patch `MAIN.BIN`'s RAM; an access watch from boot through OPTION, a save and a match start shows no access until the match loads player 2's overlay: CONFIRMED free while the title runs). **Decisions 2026-11-16 (verbatim):** "Which edition should the game use for a save that has no edition set yet (a new save, or one made by the stock US game)?" → "US Enhanced"; "How should the EDITION line read in the menu? (The menu is all-caps ASCII, like 'SOUND MODE  STEREO'.)" → "EDITION  US ENHANCED". Encoding (so 0 is the default): block byte `0x11` = 0 US Enhanced, 1 US original, 2 JP original, 3 JP Enhanced (hidden until `END-005`). Labels JP ORIGINAL, US ORIGINAL, US ENHANCED, JP ENHANCED. **Done 2026-11-16 (`EXP-0038`, D-034):** `build/us_edition` from the stock US image; a cold boot with the user in three editions (Morrigan wins): edition applied on each title load, voices and endings per edition, JP names in JP original. Differences from the references listed in `EXP-0038`. Progress (`EXP-0038`): patcher can grow and relocate files; the title code (wrapper on the title task, apply routine, EDITION line) works live on a test image. Build design in `EXP-0038` (each static US Enhanced change made edition-aware; English epilogue file in `ST2HIS.BIN`'s place; `ENDING.O` tests a new content byte C, room freed by merging two one-frame waits).

### EDITION-003 - Define JP Enhanced

- **Status:** `DONE` (2026-11-16)
- **Milestone:** M7
- **Dependencies:** EDITION-001.
- **Objective:** List what JP Enhanced adds to JP original (content the US release has and the Japanese lacks, or fixes), from the difference register, and get the user's choices.
- **Acceptance criteria:** Candidates with evidence presented to the user; the answers recorded verbatim.
- **Decision 2026-11-16 (verbatim, multiple choice):** "JP Enhanced = JP original plus what? The register shows little the US has that the Japanese release lacks. Pick any that should go in." → "US-only ending lines" (not chosen: "Pause on missing pad", "Win-quote differences"); "Until JP Enhanced actually differs from JP original, should the options menu offer it?" → "Hide until it differs (Recommended)".
- **Meaning:** JP Enhanced is JP original plus Japanese versions of the content the US main endings add (`EXP-0030`: Morrigan's added line, Bishamon's closing line, Rikuo's new lines, Huitzil's new page, Felicia's different story), as a new translation (rule 29), retimed to the pictures. The menu hides JP Enhanced until it differs from JP original. Work: `END-005`.

### END-005 - US-only main-ending content in Japanese, for JP Enhanced

- **Status:** `DONE`
- **Milestone:** M7
- **Dependencies:** EDITION-003, GATE-TRANSLATION (a new Japanese translation needs the user's source and approval).
- **Objective:** Give JP Enhanced the lines and pages the US main endings add, in Japanese, in the Japanese script and `ST2JPN` text, timed to the pictures.
- **Acceptance criteria:** (1) The exact US-only lines per character listed from `EXP-0030`, with which are additions and which are rewrites of Japanese lines (only additions qualify unless the user decides otherwise). (2) Japanese text from a source the user approves, marked as a new translation. (3) Encoded in the Japanese text codes (`MOJI`, D-011), inserted and retimed as `EXP-0031` did, shown forced and from a cold boot in JP Enhanced.
- **Done (2026-11-27, `EXP-0046`, D-046):** the user approved new
  Japanese translations of the four sets of additions, keeping Felicia's
  Japanese ending. JP Enhanced is now selectable and shows all six new
  pages in Mednafen from a cold-boot Arcade checkpoint. The existing
  Japanese text and the stock table path remain available in JP Original.
  Hardware verification is planned for the combined candidate.

## Phase G: M2, the Same Change From a Disc Image

### DISC-001 - Where the epilogue flag and language byte are set

- **Status:** `DONE` (2026-11-14)
- **Milestone:** M2
- **Dependencies:** GATE-M0.
- **Objective:** Find the code that writes the epilogue flag and language byte (D-012) in each release, so a disc patch can set them.
- **Acceptance criteria:** Every writer of both bytes from power-on through start-up identified by a write watch on both releases; a static search of every program file for other writers; the instruction and file offset that a patch would change named.
- **Result:** the US `MAIN.BIN` start-up routine writes flag 2 and language 1 as constants (file offsets `0x11A`, `0x11E`), once; the Japanese release never writes them (`EXP-0013`, D-013). The flag is also read by `TITLE.O`, `SOBJ08.O3` and `PL05`/`PL10`/`PL14` (HYPOTHESIS: a broad export switch).

### DISC-002 - The US Enhanced epilogue from a rebuilt US image

- **Status:** `DONE` (2026-11-14, `EXP-0018`, D-017; M2 reached for `END-01`, Morrigan)
- **Milestone:** M2
- **Dependencies:** DISC-001.
- **Objective:** Reproduce D-012 (English main ending, then the Japanese epilogue) from a patched copy of the US image with no RAM writes.
- **Acceptance criteria:** A same-size, in-place patch (`tools/disc/patch_image.py`, EDC/ECC regenerated) written to `build/`, every changed byte recorded; a cold boot of the patched image; Morrigan's ending forced as in D-009 (stage byte only) shows the Japanese epilogue after the English main ending; the unpatched image under the same forcing shows none (control); what else the cleared flag changes is checked on the screens the flag's other readers serve, or listed as open.
- **Notes:** Clearing the flag on disc is **not** the US Enhanced patch: it also restores the Japanese names, MODE SELECT graphics and text spacing (`EXP-0015`, D-015). The Japanese-only items are separate branches: the ST1 gate (`0x0603B902`), two `ENDING.O` tests, four in `PL05` (Morrigan), two in `PL14` (Donovan?); a patch can open those alone (e.g. make each test take the JP branch). Keeping the flag at 2 also keeps the US auto-pause when a controller is missing (`EXP-0016`, D-016). Clearing the flag is one byte (`MAIN.BIN` `0x11B`, `02` → `00`). The ST1 name array's USA entry and the language switch after the main ending (D-012) are not one-byte constants: the language byte is read per line by the main-ending renderer, so the epilogue needs either its own language test changed or the USA name entry pointed at `ST1JPN` plus a renderer change. That design is this task's first experiment.
- **Progress 2026-11-14 (`EXP-0018`):** patched image built (`build/us_enhanced_epilogue/`, five byte changes, flag and language untouched: the ST1 gate, the US ST1 name, `ST1JPN.BIN`'s slot header, two `ENDING.O` branches). Rehearsal from the old won-KO state shows the English ending, then the Japanese epilogue, then the credits. Remaining: a cold boot and a won KO played on the patched image (needs the user), then the stage-byte forcing and an unpatched control.
- **Progress 2026-11-14 (`EXP-0018`, cold boot 1):** the cold boot of version 1 failed: the user's won match showed Morrigan's win quote in **Japanese**. The `ST1` name array also serves the win screens (`ST1USA.BIN` is the US win-quote file). Version 2 leaves the array alone and makes only the ending's call load `ST1JPN.BIN` (15 bytes in all; Track 1 `93ca264c…`). Rehearsed: English win quote; forced ending shows the English ending, then the Japanese epilogue, then CAST. Remaining: a cold boot of version 2 with a won match (needs the user), then the forcing, the unpatched control and the cast-roll names.
- **Done 2026-11-14 (`EXP-0018`, D-017):** cold boot of version 2, Morrigan won 2-0 vs. Victor: English win quote; the ending forced with the stage byte only shows the English main ending, the Japanese epilogue, then the cast roll with US names (JON TALBAIN, HSIEN-KO, LORD RAPTOR); the unpatched control shows the art with no text. The flag stays 2, so nothing else it selects changes. Listed as open: the other 13 endings, the JP punctuation spacing (`0x06037AE4`, stays off), the ending script tables (`0x060367A4`, stay US), what the `0x0600CFCC` card branch adds, and the screens served by the other `ST1` load sites (`0x06014208`, `0x0601E16C`).
- **Progress 2026-11-14 (`EXP-0019`, D-018):** the ending's character is `0x06080980` (1-based: 1 Demitri, 2 Jon Talbain, 3 Victor, 4 Lord Raptor, 5 Morrigan, 6 Anakaris, 7 Felicia, 8 Bishamon, 9 Rikuo, 10 Sasquatch, 11 Huitzil, 12 Pyron, 13 Hsien-Ko, 14 Donovan); written with the stage byte at Morrigan's won-KO state it plays that character's ending. All 14 show their Japanese epilogue on the version 2 image; the unpatched controls show the art without text. Forced only: each preceding fight was Morrigan vs. Victor.
- **Progress 2026-11-14 (`EXP-0021`, D-020):** the version 2 patch at `0x0600CFCC` runs the Japanese text introduction: 416 frames in which the paragraph rises onto black before the art scroll, as in the Japanese release; the US release skips it. The emblem-card glyph strip (`EXP-0012`) is absent from both releases and the build; closed as a by-product of clearing the flag in RAM.

## Gates

### GATE-M0 - Confirm environment and checkpoint prerequisites

- **Status:** `DONE` (2026-11-14)
- **Milestone:** M0
- **Dependencies:** ENV-001 to ENV-006, EMU-001 to EMU-007, EMU-020, EMU-021, DBG-001 to DBG-004, DIFF-003.
- **Blockers:** Dependencies not done.
- **Objective:** Make an explicit go/no-go decision before the first live RAM mutation.
- **Acceptance criteria:** Every dependency is `DONE`; no unresolved workflow blocker can invalidate M1 evidence; the user's GO is recorded verbatim.
- **GO:** The user (2026-11-14), asked "Count this as M1 reached, with your GO recorded now?": "Yes, record GO". Given after the M1 outcome was shown (`EXP-0012`), not before the first RAM write as planned. `DIFF-003` and `DBG-002` to `DBG-004` were closed for `END-01` by `EXP-0010` to `EXP-0012`; `REF-004` was not done and the user accepted M1 without it.

### GATE-TRANSLATION - Confirm English sources and policy

- **Status:** `DONE`
- **Milestone:** before any English not already on the base disc goes on disc
- **Dependencies:** DOC-002, DOC-003, and whichever of REF-001/REF-002 the user keeps.
- **Blockers:** None. (`DOC-002`, `DOC-003` and `REF-002` are done; the user kept `REF-002` as the epilogue source; `REF-001` is not needed for this scope.)
- **Objective:** No new or donor English text goes on disc before its sources, the pairing method, and the user's policy are settled.
- **Acceptance criteria:** Every dependency is `DONE`; the user gives a recorded GO. Each later scope extension (new class, new donor source, names) is its own dated block under this gate.
- **2026-11-15, `END-01` epilogues (user decisions, `docs/localization_policy.md`):** source PSP *Chronicle* `HmovieNN_2` English for all 14 (`EXP-0020`); spelling and missing-word slips fixed, each logged; names spelled as the US Saturn has them (Raptor); line breaks free, any cut or rewording asked first. This is the user's GO for this scope. Opened 2026-11-15 when `DOC-003` was done; any other scope (main endings, names, a new donor) needs its own dated block.
- **2026-11-16, `END-02` Morrigan's main ending (user decisions):** restore only Morrigan's two missing lines and pause page in US Enhanced (`END-004`); English from the PSP *Chronicle* main-ending movie if present, a new translation only with the user's yes; every other US main-ending line unchanged.

## Post-v0.1.0 Playtester Follow-up

### ANI-002 - Reproduce mixed-matchup `FULL` and measure the loader

- **Status:** `DONE`
- **Dependencies:** EMU-021, DBG-001, EDITION-002.
- **Objective:** Identify what the stock engine loads for `CUT` and `FULL`
  in a mixed matchup and a mirror, and account for working memory before
  changing the allocator.
- **Acceptance criteria:** Trace actual fighter resource selections on US
  retail code under both settings, including one mixed matchup and one
  mirror with demonstrably different asset sets. Check the equivalent JP
  path on the JP retail image. Record a visual checkpoint, allocation
  high-water marks for a large pair, and the constraints on using extra RAM.
- **Progress (`EXP-0040`, D-036):** The retail US and JP attract replays
  confirmed the same reduced-set loads for Anakaris vs. Rikuo under `CUT`
  and `FULL`. A static tally puts the largest distinct US pair, Anakaris
  and Huitzil, at 2,256,056 bytes for their `.BIN` and `.SPR` allocations.
  The three stock pools together have at most 1,578,860 bytes before other
  allocations.
- **Done (`EXP-0041`, D-037, 2026-11-26):** with the attract fighters forced
  in US RAM, an Anakaris mirror loads `P06_` once under `CUT` (684,404 pool
  bytes) and `P06` once under `FULL` (1,162,868), both shown on screen. The
  fighter pools hold 1,372,412 bytes (WRAM-H 172,668, all 1,048,576 of WRAM-L,
  VDP2 151,168). Anakaris vs. Huitzil under `CUT` uses 1,367,788. With the
  equality branch forced, `FULL` requests 2,256,056, fails on a 112,784-byte
  request ("Out Of Memory") and resets to the BIOS CD player. Constraints:
  the pair needs 883,644 more bytes, the largest request is 112,784, and the
  1 MiB cart is two 512 KiB banks (`0x02400000`, `0x02600000`). A-bus RAM
  suitability is UNKNOWN. JP mirror not run (JP mixed path matched in
  `EXP-0040`).

### ANI-003 - Enable full animation for different fighters

- **Status:** `IN_PROGRESS` (only the real-Saturn check remains)
- **Dependencies:** ANI-002 (done).
- **Objective:** Make Appendix `FULL` work across different fighters when
  the required memory is available, with a playable cart-free configuration.
- **Acceptance criteria:** Preserve the shipped `CUT` behavior as a fallback.
  Prove cart detection and allocator bounds with no expansion, a 1 MiB cart,
  and a 4 MiB cart. Use the largest measured matchup in both player orders,
  cover all fighters, and check sustained play, round changes, rematches,
  Arcade opponent changes, VS, and save/options behavior. Verify a cold boot
  of the selected build in Mednafen and a real Saturn check before release.
  Decide whether one auto-detecting build suffices from the results.
- **Scope:** Start with the 4 MiB target. Qualify 1 MiB only if the measured
  allocations fit the usable banks. Consider cart-free mixed `FULL` if the
  measurements point to a viable alternate loading strategy.
- **Progress (`EXP-0043`, D-042, 2026-11-26):** one auto-detecting build
  (`build/us_edition` Track 1 `8882e154…72df`). With a 4 MiB cart, the title
  wrapper moves allocator pool 2 into the cart and opens the `FULL` branch.
  Confirmed in Mednafen from cold boots: the largest pair in both orders,
  every fighter's full set, Arcade rounds, opponent changes, continue and
  rematch, VS, saved `FULL`, and the stock pace. No cart, 1 MiB and `CUT`
  load stock sets. 1 MiB is not qualified (it needs two more pools). Open:
  a real-Saturn check with a 4 MiB cart before release (the user).

### AUD-004 - Reproduce and correct the P1 Anakaris sound issue

- **Status:** `IN_PROGRESS` (fixed and verified; Donovan's ice attack not
  yet triggered live)
- **Dependencies:** EMU-021, EDITION-002.
- **Acceptance criteria:** In stereo, capture Demitri's dash and fireball
  with Anakaris on P1, then swap players and repeat with the same moves and
  stage. Control for player order and sound-bank loading by repeating the
  move against a different opponent and in a fresh fight. Compare retail US,
  retail JP and Deluxe before locating the first diverging sound command,
  sample, or playback parameter. Verify the fix for both Demitri moves,
  Pyron's fireball, and the reported ice attacks from Sasquatch, Donovan,
  and Huitzil, including in Arcade and two-controller play. Check Anakaris's
  own sounds and ordinary matchups. Keep stereo WAVs and any live sound
  traces local.
- **Progress (`EXP-0044`, D-043, 2026-11-26):** reproduced on US and JP
  retail. The shared-sound lookup (`0x0603A1C8`) always prefers P1's
  character, and Anakaris owns copies of 17 shared types, so with him on P1
  the opponent's fireball, dash and ice sounds come from his bank. US
  Enhanced now tries P2's character first when P1 is Anakaris. Verified in
  VS and Arcade for Demitri (fireball, dash), Pyron (fireball), Sasquatch
  and Huitzil (ice) and the CPU Victor. Anakaris's own sounds and an
  ordinary matchup are unchanged. Since 2026-11-26 the fix applies in every
  edition (user decision, `EXP-0045`). Open: Donovan's ice attack, not triggered live (motion not found);
  same lookup and table entry as Sasquatch's and Huitzil's.

### AUD-005 - Reproduce and correct Morrigan's Soul Fist trail panning

- **Status:** `DONE`
- **Dependencies:** EMU-021, EDITION-002.
- **Acceptance criteria:** Isolate the trail from the voice and BGM in stereo
  captures. Compare the same move on the left and right with the player port
  fixed, then change ports with screen position controlled. Compare the
  retail releases and Deluxe. If the trail is pinned to one channel, trace
  what sets its pan and check that the revised trail follows the intended
  position while the voice, other effects and mono output still work.
- **Done (`EXP-0045`, D-044, 2026-11-26):** Morrigan's code clears the trail
  request's screen position with `and r4,r5` where every other character uses
  `or` (two sites, `PL05.O` and `PL05.O2`, both retail releases), so the trail
  always plays far left. With `or` the trail follows the fireball on either
  side, crosses over correctly, is centered in mono, and her voice and other
  effects are unchanged. User decision: fix in every edition, and extend the
  `AUD-004` fix to every edition too.

### APP-001 - Verify Capcom's Appendix code and options in Deluxe

- **Status:** `DONE`
- **Dependencies:** EDITION-002.
- **Acceptance criteria:** Enter the stock Appendix code on a fresh save on
  both retail releases and Deluxe. Check appearance, navigation, setting
  changes and persistence with the Deluxe `EDITION` row present. Check the
  cart-free setup and the cart setup selected for release. Repair any
  proven regression. Record release-specific code and menu differences.
- **Lead (`EXP-0040`):** US `TITLE.O` checks an input sequence before
  setting the Appendix availability byte at `0x06080A2B`. The current
  edition menu already has a layout for the unlocked Appendix (`D-034`).
- **Done (`EXP-0042`, D-038 to D-041, 2026-11-26):** the code is B, X, Down,
  A, Y on CONFIGURATION, each within 14 frames, the same on both retail
  releases. It unlocks, opens and saves on US, JP and Deluxe v0.1.0 (no cart;
  4 MiB cart on Deluxe), and persists across a cold boot. The one regression,
  EDITION touching PRESS START TO EXIT, is repaired. By the user's decision
  the Appendix is unlocked by default and the exit line is one line lower
  (`build/us_edition` Track 1 `a87f7f70…ab0d`, cold-boot checked). Unlocked,
  the attract demo randomizes the scenery variant (D-040). Input injection
  needed patch `0002` in the agent build (D-038). Open: what the line-2 code
  (`0x06080A2A`) unlocks. No release cart setup is chosen yet (`ANI-003`).

## Later Milestones (outline only)

Placeholders so the order is visible. Each becomes a full task, with its own
acceptance criteria, only when its prerequisites are done ("Write up the Mx
tasks" just in time). The method for each is in the three sibling documents.

| ID | Milestone | Outline |
| --- | --- | --- |
| RE-001 | M1 | **Done** (`EXP-0012`, D-012; no-write control `EXP-0010` `us-ko-n9-b`): Morrigan's Japanese epilogue in US RAM. |
| DISC-001 | M2 | **Done** (`EXP-0013`, D-013): see the task above. |
| DISC-002 | M2 | **Done** (`EXP-0018`, D-017): the Japanese epilogue from a 15-byte patch of the US image, cold-boot checked. |
| RE-002 | M3 | Selection: what picks each instance (character, opponent, health, route), and forcing it from a checkpoint. |
| RE-003 | M3 | Generator for one character; every instance verified live by forcing. |
| RE-004 | M4 | A second character through the same mechanism. |
| RE-005 | M5 | Whole roster for the class; capacity; regression references. |
| END-002 | M3-M5 for END-01 | Now a full task (above). |
| END-003 | M1 for END-02/03 | Now a full task (above). |
| AUD-002 | M2-M3 for AUD-01/02/03/05 | Now a full task (above): Morrigan's voices. The rest of the roster (Donovan, Sasquatch) is later. |
| QUO-001 | M1-M5 for QUO-01 | **Done (2026-11-27, EXP-0049, D-048):** mapped both retail inventories and verified the condition boundaries. US Enhanced keeps all stock quotes and adds one new translation from the Japanese Saturn record in every fighter/condition group. All 56 new records checked on the combined build. |
| LOC-001 | M7 | **Done (2026-11-27, EXP-0048, D-047):** saved EDITION / US / JAPANESE preference for the stock fighter-name surfaces in the Enhanced editions. Both Original editions use the edition names. The text audit records supporting names inside their scripts. |
| UI-001 | M8 | Title, attract, menus, credits, boot warnings: each surface the register marks different. |
| COV-001 | M8 | Coverage register: every row resolved (`docs/coverage_exceptions.md`). |
| SPECIAL-001 | M9, user approval | Unused or unreachable assets, debug features, hidden content. |
| REL-001 | after M5 | **Done (2026-11-25, v0.1.0 prepared):** `make_patch`, `make_zips`, `check_zips` and unit tests copied from Cyberbots (`bac6fde`) and parameterized for Night Warriors Deluxe (xdelta-only per user decision 2026-11-25). Patch `night_warriors_deluxe.Track1.xdelta` (54,362 bytes, SHA-256 `01f3aeab…fa82`, RA MD5 `8c7156c2…7e9e` unchanged) and zip `night_warriors_deluxe_0.1.0_xdelta.zip` (49,807 bytes, SHA-256 `92b8c26c…30e0`) built twice byte-identically and verified with `check_zips --expect 25e05ec1…f1be`. Release docs in `release/`; remaining backlog tasks (`END-005`, `QUO-001`, `LOC-001`, `REF-004`/`UI-001`/`COV-001`, `DIFF-002`, `REF-001`, `REF-003`) explicitly deferred by user decision 2026-11-25. Patches stay under `build/` as Release assets only (`AGENTS.md` rule 21). |
