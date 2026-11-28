# Release Patch: Night Warriors Deluxe (Saturn)

This folder describes version 0.2.0 of the patch for the US Sega Saturn
release of **Night Warriors: Darkstalkers' Revenge** (Capcom, 1996, T-1208H):
what it changes, how to apply it, and how to rebuild it from this repository.

**The patch files are not in the repository.** Their bytes include game-derived
data, which this project never commits (`AGENTS.md` rule 21). They are
published as GitHub Release assets.

[`night_warriors_deluxe_v0.2.0.json`](night_warriors_deluxe_v0.2.0.json) is
the xdelta patch's record (hashes, sizes, xdelta3 version and flags): metadata
only. The 0.1.0 metadata remains in
[`night_warriors_deluxe.json`](night_warriors_deluxe.json).

## What the Patch Changes

The patch adds an **`EDITION`** row to `OPTION MODE` (saved in spare bytes of
the game's `N_WARRIORS_` backup-RAM save; existing stock US saves default to
`US ENHANCED`). It switches between four editions at run time:

- **`US ENHANCED` (default):** the US release with the suppressed Japanese
  content restored in English:
  - **All 14 post-ending epilogues:** restored in English over the scrolling
    character artwork, using the official English text from PSP *Darkstalkers
    Chronicle: The Chaos Tower* (spelling and missing-word slips fixed and
    logged, US Saturn character spellings kept).
  - **Morrigan's missing main-ending lines:** the two Japanese-only lines and
    pause page dropped from the US butler scene restored in a new English
    translation (*"I'm a little tired. / Prepare my bed."*, *"Certainly,
    mistress."*), timed to the scene. All other US main-ending text stays as
    shipped.
  - **Morrigan's 4 suppressed Japanese voice samples:** normal throw, Vector
    Drain, bat-seat win pose, and hurt.
  - **Donovan's 2 suppressed Japanese voice samples:** post-round-1 win pose
    and sword-planted punch+kick.
  - **Sasquatch's Japanese win poses, snow creatures, and voice sample:**
    restores the shy pose, the small snow creatures, and their voice sample in
    poses 0, 1, and 4 (Up + A + B + C).
- **`US ORIGINAL`:** plays as the stock US release (no epilogue text, original
  Morrigan ending, suppressed voices and poses disabled).
- **`JP ENHANCED`:** Japanese presentation with Japanese translations of the
  US-only additions to Morrigan's, Bishamon's, Rikuo's and Huitzil's main
  endings. Felicia's Japanese ending remains as shipped.
- **`JP ORIGINAL`:** runs the US code set in Japanese mode — Japanese fighter
  names (Gallon, Zabel, Aulbath, Phobos, Lei-Lei), Japanese main endings and
  epilogues, Japanese voices and poses, and no US auto-pause on missing
  controller. *(Because `JP ORIGINAL` runs on the US code and graphic set, the
  US title screen, intro logo, and US-only code differences remain; see "Known
  Limits".)*

Additional changes in 0.2.0:

- The Enhanced editions have a saved `NAMES` preference for Japanese or US
  fighter names; Original editions use their edition's names.
- US Enhanced retains the official US victory quotes and adds 56 translated
  Japanese variants, one for each fighter and mirror/vitality condition.
- The Appendix is unlocked by default.
- With a 4 MiB Expansion RAM cartridge, `FULL` animation loads complete sets
  for different fighters in Arcade and VS. Without the cart, the stock
  reduced-set behavior remains. A 1 MiB cartridge is not qualified.
- Two sound corrections: opponent attacks use that fighter's sounds when
  Anakaris is Player 1, and Morrigan's Soul Fist trail follows the fireball's
  screen position.

## Apply the Patch

### You need

1. **The original US disc image**, as BIN/CUE with 2 tracks: Redump disc `5836`
   (`Night Warriors: Darkstalkers' Revenge`, USA, `T-1208H`, V1.001). Only
   Track 1 is patched, and it must be the untouched original:

   | Component | Size (bytes) | SHA-256 |
   | --- | ---: | --- |
   | `Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin` | 493,741,248 | `d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da` |
   | `Night Warriors - Darkstalkers' Revenge (USA) (Track 2).bin` | 1,766,352 | `271844bfb734ab4fd322bc753bfad63b8a6e31d7d24272d52b5d10989065cdbb` |
   | `Night Warriors - Darkstalkers' Revenge (USA).cue` | 281 | `203a53dff34c4adea6a709c822fa485d4325a4bd63aa6b0ea03f1ed7a141fbb2` |

2. **A VCDIFF patcher:** `xdelta3` (3.2.2 is tested), Delta Patcher, Rom
   Patcher JS, or any program that applies xdelta / VCDIFF patches.

### Steps

```bash
xdelta3 -d -s "Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin" \
  night_warriors_deluxe.Track1.xdelta "Track 1 patched.bin"
```

1. Run it in the folder with the original image. The patch is plain VCDIFF: no
   secondary compression, a 16 MiB window, no application header.
2. The result's SHA-256 must be
   `d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d` (also in
   the zip's `README.txt`, "patched Track 1").
3. Replace Track 1 with it under its original file name so the CUE still finds
   it. Keep Track 2 and the CUE unchanged.

The game boots with the same hardware as the stock US release. A 4 MiB
Expansion RAM cartridge is required for the new mixed-matchup `FULL`
animation option; without it, shipped reduced-set behavior remains. A 1 MiB
cart is not qualified for `FULL`.

### Why there is no .ssp patch

Version 0.2.0 ships **xdelta only**. The build relocates and resizes `TITLE.O`
and `ST2HIS.BIN` into Track 1's free tail sectors; xdelta patches Track 1 in
place while keeping every sector layout and Track 2 unchanged.

## Known Limits

- **Emulation vs. real hardware:** the combined 0.2.0 candidate cold-booted in
  Mednafen. The 4 MiB `FULL` path was observed through two Arcade rounds in
  Mednafen. Per user decision, the release assumes hardware parity for this
  feature; real Saturn timing, stability and sprite behavior are not
  independently verified (`EXP-0051`).
- **RetroAchievements:** the disc header RetroAchievements hashes (first 512
  bytes of Track 1 sector 0 user data, MD5 `8c7156c2e38f75a9ec54016427967e9e`)
  is unchanged. RetroAchievements currently has no Sega Saturn set for *Night
  Warriors*; achievement triggering is untested.
- **`JP ORIGINAL` differences from the standalone Japanese disc:** runs the US
  code set in Japanese mode (`EDITION-001`), so the US title screen, intro
  logo, and US-only code changes remain.
- **Regional coverage:** the surface audit is recorded, but `COV-001` remains
  open. Remaining items and evidence gaps are listed in
  [`docs/coverage_exceptions.md`](../docs/coverage_exceptions.md).
- **Epilogue text differences:** the official PSP *Darkstalkers Chronicle*
  English epilogues shorten some Japanese epilogues and alter details/meaning
  in a few (notably Lord Raptor and Sasquatch; documented in `EXP-0020`).

## Rebuild the Patch from This Repository

You supply the untouched US Saturn image and extract its Track 1 files (and the
local PSP epilogue transcript from `EXP-0020`); see the top-level
[`README.md`](../README.md), "Files You Need". Then:

```bash
# 1. Build the combined candidate. This script incorporates the tracked source
#    specifications and local transcript required by the README's Files You Need.
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/next_release_candidate
# 2. Generate and round-trip verify the xdelta patch.
./invenv.sh python -m tools.disc.make_patch --built-dir build/next_release_candidate \
  --stem night_warriors_deluxe --out-dir build/release/v0.2.0-patch/patch \
  --record release/night_warriors_deluxe_v0.2.0.json
# 3. Package the reproducible zip and verify applying it to the untouched Track 1.
./invenv.sh python -m tools.release.make_zips 0.2.0 build/release/v0.2.0 --kinds xdelta \
  --records release --patches build/release/v0.2.0-patch \
  --variant night_warriors_deluxe_v0.2.0 patch \
  "US Enhanced, US Original, JP Enhanced, and JP Original (switched in OPTION MODE)"
./invenv.sh python -m tools.release.check_zips 0.2.0 build/release/v0.2.0 local/rel/v0.2.0-check \
  --kinds xdelta --expect d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d
```

The full publishing checklist is in [`RELEASING.md`](RELEASING.md).
