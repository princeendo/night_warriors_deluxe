# Lessons From Cyberbots (the third game)

Cyberbots: Fullmetal Madness (Saturn JP T-1217G) was the third project to use
the MSHvSF method. This digest was compiled on 2026-11-13, read-only, from
`/Users/colinwhite/workspace/personal/cyberbots_saturn_en_translation` at
commit `bac6fde` (its task list, log, docs, release docs, tools and history).

**Nothing here is a fact about Vampire Hunter.** Every Cyberbots fact is, for
this project, at most a HYPOTHESIS. Cyberbots IDs (`EXP-`, `D-`, task IDs)
and commits refer to that repository.

## Scale

| | XvSF | Cyberbots |
| --- | --- | --- |
| Active days | about 6 | 6 to 0.1.0 (2026-11-02 to 11-07), then fixes to 11-13 |
| Experiments | 74 | 88 |
| Commits | 120 | 127 |
| Tests | 272 | 273 |

Far more text than XvSF in the same time. The speed came from the copied
method and patch, agent-run play checks from M2 (`DISC-002`), and one game
fact: arcade and Saturn run the same scene-script bytecode (`EXP-0023`).

## 1. What Transferred, and What Did Not

Transferred unchanged (each re-validated on Cyberbots first):

- Mednafen 1.32.1 from XvSF's archive, BIOS, homes byte-equal to XvSF's
  (`EMU-001`, `EMU-002`); the agent patch, V1-V4 passed (`EXP-0006`); the
  extractor's 16-bit swap for WRAM-L/H and VDP1/VDP2 VRAM (`EXP-0005`).
- `patch_image.py`: identity rebuild byte-identical; no file checksums
  (`EXP-0019`). Pad bindings (`EMU-005`), `cold_boot.py` (`EXP-0001`),
  `hotkeys.py` (`EXP-0003`).
- Write breakpoint on RAM text names the loader and file (`EXP-0018`);
  write breakpoint on a glyph cell finds the font routine; prove the font
  by byte-identical repack (`EXP-0020`).
- MSHvSF's pair-glyph capacity route (`LAYOUT-001`, `EXP-0025`) and its
  EXTRA OPTIONS sub-menu design (`OPT-004`).
- Release tools with the RetroAchievements header guard (`REL-001`).

Did not transfer:

| Siblings | Cyberbots reality (evidence) |
| --- | --- |
| XvSF had a leftover arcade English mode | No native English path (`FONT-002`, `EXP-0021`, D-020) |
| Quote text not Shift-JIS in RAM; equality-pattern search | Plain Shift-JIS, found by a plain search (`EXP-0016`) |
| 4 MiB cart needed | No cart needed for boot/attract; DB gives 1 MiB (`EXP-0002`); `mcs_extract` refuses the 1 MiB cart section |
| Arcade English as 16-bit codes or ASCII tiles | One byte per character with an offset, found by relative search (`EXP-0008`) |
| XvSF traced its own quote selector | Same script bytecode: box N = slot N (`EXP-0023`) |
| `ERRn.BIN` boot warnings | Five `WARNINGn.PIX` bitmaps from a save check (`EXP-0051`) |
| (no sibling equivalent) | Story, ending and console-only endings use different font copies (`EXP-0038`, `EXP-0050`) |
| Decision: xdelta + SSP | SSP not viable once files are added (`EXP-0086`, `EXP-0087`) |

## 2. Process Lessons

1. **Let the agent run play checks from the start.** The user declined a
   manual check: "Yeah, I don't want to do that at all. Why can't you just
   boot the machine and take regular screenshots like I did with the XvSF
   and MSHvSF translations?" (`DISC-002`, 2026-11-02). Cold boots driven by
   pad keys through System Events (`EXP-0019/drive.py`) closed every
   image-changing task after that.
2. **Do not steal focus with repeated key presses.** A watcher pressing A
   every 1.5 s drew: "Please take a break as soon as possible. It's
   becoming impossible to use this computer because you keep switching
   focus" (`WIN-001`, 2026-11-03). Use RAM forcing; single presses only,
   screenshot before each. Other windows also take keys: an open MSHvSF
   Mednafen (`EXP-0025`), the user's own typing (`EXP-0066`).
3. **Keep every state of the first play session.** `REF-005` kept 166
   states (`--keep-states 0`); state 4138 served forcing from M3 to
   `SPECIAL-017`. It still missed endings, versus mode and console pilots.
4. **Force, do not play.** Scene forcing (`RE-002` runbook in
   `docs/mednafen.md`), endings by four RAM writes (`EXP-0037`), vitality
   held per fight. Fight steps differ by pilot (`EXP-0083`).
5. **RAM-written pad input does not work**: the SH-2 reads pad words
   through its cache (`EXP-0051`, `EXP-0072`). Real presses are needed; a
   pad command in the agent patch is an open idea (`known_unknowns.md`).
6. **Screenshot comparison between runs is not evidence**: poll frames
   drift (`EXP-0038`); two identical controls differed in 64 of 174
   segments (`EXP-0064`). Compare predicted cells or VRAM bytes.
7. **Pair by the games' code, not by alignment.** `REF-006`'s alignment
   reader stopped at a space code; 13 "expanded" lines were that bug
   (`EXP-0023`). Absence of official English was shown from code (`EXP-0077`).
8. **Check every consumer of a shared asset.** Shared speaker names were
   checked in a list using one font; another list uses the story font and
   was garbled from M7 until M8's live check (`EXP-0050`).
9. **Free RAM needs logs plus an independent static review.** A range
   constant in every state was the VDP1 command list's tail, grown by DMA
   (`EXP-0064`, D-057).
10. **Have an independent reviewer fact-check task write-ups and designs.**
    Phase S's draft got 22 corrections; the `OPT-005` review found a
    "binary search" that was linear (`EXP-0065`).
11. **Verify numbers before asking.** Two questions went out wrong and were
    re-asked: the layout's "4 pixels" (really 13, `OPT-005`) and an
    "invisible" code that did not exist (`END-023`).
12. **Write tasks just in time.** Each phase was written up on the user's
    "Write up ..." and nothing started until "Start TASK-ID".
13. **Housekeeping.** Commit scratch scripts into the experiment (a cleared
    scratchpad lost a scan, `EXP-0027`). Reserve experiment IDs: a Windows
    session took `EXP-0087` and the Mac's run overwrote its README before
    moving to `EXP-0088`. Keep game text out of data files (`EXP-0041`).
14. **Plan disk space.** Two homelab backups at the user's request ("the
    same way that XvSF and MSHvSF did"; 2026-11-05, 2026-11-13), then
    finished `local/` data and `build/` images deleted.

## 3. Emulator and Tooling

- **Mednafen 1.32.1** (archive `de7eb94a…3832`), stock and agent builds in
  separate trees; BIOS hashes match Mednafen's `ss.html` (`EMU-002`). Cart:
  `ss.cart auto`, chosen by test, not copied (`EXP-0002`).
- **Stock automation fails silently** (lost F9, lost dumps, `option+3`
  ignored: `EXP-0003`-`EXP-0005`); that justified `EMU-020`.
- **Agent quirks:** no `savestate` while halted; breakpoint logs lack the
  access address (`EXP-0064/attribute.py` rebuilds it); a failed
  `session.launch` leaves Mednafen running; one Mednafen per home unless
  `MEDNAFEN_ALLOWMULTI=1` (`EXP-0082`); parallel `configure()` races
  (`EXP-0056`); per-frame agent calls are slow (`EXP-0060`).
- **Mednafen facts:** backup file named by disc identity, so a save must
  keep its name when moved to a built image (`EXP-0066`); screenshots are
  240 rows with 8 padded rows above and below a 224-line display
  (`EXP-0052`); `-qtrecord` frames are 10560x480 (`EXP-0084`).
- **MAME 0.289 (Homebrew), headless:** `qsound.zip` needed for every CPS-II
  set; read-tap end addresses must be odd; Lua names the stack pointer `SP`;
  the debugger reads `d0=10` as hex; share no NVRAM folder between runs;
  ROM writes need the `:maincpu` region (`EXP-0032`, `EXP-0040`,
  `EXP-0075`). Region branches forced both ways (D-060, D-061).
- **Sound (`EXP-0088`):** for a reported buzz on a burned disc, no-input
  cold boots of original and patch were recorded (`-qtrecord`) and compared
  per sample (`compare_audio.py`): identical for 59.1 s, then sounds ms
  apart, silences exactly zero. Mednafen only; the buzz is still open.
- **Windows** Mednafen for the user's tests: see `docs/mednafen.md`
  (2026-11-08) for the three build-flag fixes. zsh word-splitting broke
  several runs (`EXP-0005`, `EXP-0027`, `EXP-0038`).

## 4. Release

- **xdelta only.** Adding files to Track 01 (NAMES and SIGNS tail files,
  `tools/disc/add_files.py`) makes the image unpatchable by the open-source
  SSP applier (`saturn-patcher-egui`, `REL-002` research). `make_ssp
  --add-new` writes `._NEW` entries (`EXP-0086`); official patcher 1.91
  added them but rebuilt the disc as one 1,050,753,648-byte BIN, about
  99 minutes, too long for a CD (`EXP-0087`). The user withdrew the `.ssp`
  on 2026-11-13 (`REL-004`). Untested hypothesis: it copies the 61
  ISO entries that point at audio tracks into the data track.
- **RA guard:** `make_patch` and `make_ssp` refuse a changed sector-0
  header and record `ra_md5`. A third-party mirror of RA hash lists had the
  source hash; achievement triggering is recorded as untested.
- **Zips:** `make_zips`/`check_zips` built twice byte-identical, checked by
  applying with plain `xdelta3 -d` to an untouched Track 01 (`EXP-0085`).
- **Publishing:** `gh` is the work account; the agent tags and pushes, the
  user creates the release on github.com, the agent checks asset digests
  through the public API (`REL-004`).
- **Hardware:** deferred before release; afterwards a burned xdelta disc
  buzzed (open) and the release image on a Satiator "works totally fine"
  (2026-11-13). Checklist: `release/RELEASING.md`.

## 5. Tools

Game-independent, worth copying (Cyberbots path; test in `tests/unit/`):

| Path | Purpose | Test |
| --- | --- | --- |
| `tools/disc/add_files.py` | New files into free tail sectors and the root directory (new) | `test_add_files.py` |
| `tools/disc/make_patch.py` | xdelta patch + record, RA guard, `--reference` (improved) | `test_disc_make_patch.py` |
| `tools/disc/make_ssp.py` | `.ssp` patch, `--add-new` (improved) | `test_make_ssp.py` |
| `tools/release/make_zips.py` | Reproducible zips, `--kinds` (promoted, improved) | `test_release_zips.py` |
| `tools/release/check_zips.py` | Apply zipped patches; safe work folder; `--expect` (Python rewrite) | `test_release_zips.py` |
| `tools/text/script_census.py` | Shift-JIS string blocks and load base, no text out (new) | `test_script_census.py` |
| `tools/text/arcade_pairing.py` | Learn an arcade code map from two scripts; align (method only; record layout is Cyberbots') | `test_arcade_pairing.py` |
| `research/experiments/EXP-0019/drive.py` | Cold boot + pad keys via System Events in a scratch home | none (promote) |
| `research/experiments/EXP-0066/boot.py` | Cold boots carrying a save between runs | none (promote) |
| `research/experiments/EXP-0055/regress.py` | Rebuild regression references, compare hashes | none (promote) |
| `research/experiments/EXP-0064/attribute.py` | SH-2 access address from a logged instruction | none (promote) |
| `research/experiments/EXP-0088/compare_audio.py` | Sample-level audio comparison (ffmpeg) | none (promote) |

The XvSF copies Cyberbots took in `ENV-003` (disc, mednafen, memory, sh2,
text search, reference) were never changed there (one commit each); the
gap: `mcs_extract` still expects a 4 MiB cart section.

Cyberbots-specific (patterns only): `font/kanji.py` (KANJI.BIN format),
`font/pairs.py` (pair glyphs; palette and 7-pixel narrowing are Cyberbots'),
`reference/cybots_text.py`, `text/dialogue.py`, `ending*.py`,
`name_art.py`, `pattern_t2.py`, `names_switch.py` (SH-2 menu and load
hooks), `boot_warnings.py`, `city_signs.py`, `vs_captions.py`,
`EXP-0027/play_route.py`.

## 6. User Decisions Worth Re-asking

Put each as a multiple-choice question with a "(Recommended)" option; record
the answer verbatim with its date. Cyberbots answers:

- English source: "Official; fixes opt-in (Recommended)" (`DOC-002`, 11-02).
- No official English: "Recorded new translation (Recommended)"; later
  "Claude, arcade tone (Recommended)", "Page per pilot, gloss beside
  (Recommended)", "US Capcom conventions (Recommended)" (`SPECIAL-012`,
  11-07).
- Names: "Both variants, US default" (against the recommendation), then "I
  definitely want the toggle and I want it placed in the options screen. We
  may need an expanded options screen like I'm currently working on in the
  MSHvSF repo." (`REF-007`, 11-02). Location: "Sub-menu" over the
  recommended 9th row (`OPT-004`, 11-06).
- Region-variant art as a setting, the user's own words: "Let's make it
  part of the extra options. Choices are blank, English, and Japanese
  (blank is the default)." (`UI-005`, 11-06).
- Scope: "Boss & hidden pilots", "Menus, UI art & warnings", "Attract &
  opening demos", "Rare & region-gated text" (`DOC-002`). References: "No,
  arcade only (Recommended)" (`REF-002` `REJECTED`).
- Release timing: "After open tasks (Recommended)"; asked to defer five
  items: "Do them first" (`REL-002`, 11-06).
- Formats: "xdelta + SSP (Recommended)" (11-02), then "xdelta only
  (Recommended)" (11-07), then "I actually want to create the SSP patch. I
  know we can't test it fully. But let's try it anyway." (11-07), then the
  withdrawal (11-13).
- Push and hardware: "Let's push now. In general, I'm not going to want to
  burn a disc until we're much, much closer to finished. Mednafen does a
  fantastic job of replicating real hardware so I don't feel the need to
  constantly check." (11-02); "Defer the hardware test (Recommended)" (11-06).
- RetroAchievements: "Yes, look it up (Recommended)"; "Record as untested
  (Recommended)" (`REL-002`).

Preferences in `local_agent_guidance.md` that `lessons_from_xvsf.md` does not
state: commit only as the `princeendo` noreply identity, never the work
identity, and check `git config user.email` first; ask only for gameplay,
the user does not read Japanese, verify screenshots yourself; manual steps
as a "Do this" / "What you should see" table placed last, after the wrap-up,
saying "left Option", never `F7` while halted; the agent runs cold-boot
play checks itself; per-task hardware check before push retired; `gh` is
the work account, so the user publishes releases; tasks are written up just
in time and started by "Start TASK-ID"; headless MAME may go to subagents,
but no parallel sessions and one experiment at a time; ask before installs,
downloads, gate, scope or capacity changes and side effects outside scope.

## 7. Relevance to Merging Two Regional Releases

- **Region branches, not missing data.** The US arcade kept both versions
  of region-specific art and text and chose by a region byte: it skipped
  the VS caption and blanked the city signs (D-060, D-061). Forcing the signs'
  branch both ways in MAME made one set's tile RAM equal the other's. Look
  for the same in the two Saturn images before rebuilding any asset.
- **The other release as oracle, paired by code.** Cyberbots paired by the
  shared script (box N = slot N), confirmed on screen in both games
  (`EXP-0023`). With two Saturn images, the same code-traced pairing is
  available in one emulator. Alignment alone hid a bug (`EXP-0023`).
- **Show absence by code.** "Not in the other release" was proven by
  reading the readers (`EXP-0077`); every box was classified by how it is
  reached (`TXT-010`), and rare paths were forced (`TXT-011`).
- **Counts may differ between regions.** The US arcade had one English win
  quote per pilot and level for two Japanese ones; the user chose "Shared
  official line (Recommended)" (`WIN-002`; gate, 2026-11-04).
- **Toggles:** an EXTRA OPTIONS sub-menu; saved in spare bytes of the
  game's settings block with 0 as the default, so old saves give the
  default; extra assets in Track 01's free tail, loaded by hooks per screen;
  code in RAM proven free (D-055 to D-058, D-062).
- **Restored text must fit timing.** Longer ending text needed retiming that
  keeps scene changes and music on their frames (`END-011`, D-045).
- **Voice:** names in voice were checked with the user, one clip at a time
  (`LOC-003`); `EXP-0088`'s sample comparison can show that restored voice
  changes only what it should.
- **Regression references** per feature: each build option adds one
  approved part; `data/regression/*.json` holds each rebuild command.
  Adding files rules out SSP (section 4): decide formats early.
