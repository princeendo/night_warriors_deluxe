# EXP-0001: Unattended Cold Boots of Both Releases to the Title Screen

Task: EMU-003
Status: DONE
Confidence: CONFIRMED

## Observation

`EMU-002` pinned project-local Mednafen homes with the Japanese BIOS
(`sega_101.bin`) and the North American BIOS (`mpr-17933.bin`), both matching
Mednafen 1.32.1's documented hashes. Neither release had been run. Stock
Mednafen has no scripted screenshot, and the agent interface may not be used
before `EMU-020`. Cyberbots' `EXP-0001` used the same method on its game; that
result is no evidence here.

## Hypothesis

Stock Mednafen 1.32.1, with the silent project home and no input, cold-boots
each untouched image (Japanese 1M, US) to a stable title screen, picks each
release's own BIOS from the disc's area code, and does so the same way each
time.

## Controlled Change

None to the games, BIOS, binary or configuration. Each run adds only the
command-line option `-qtrecord FILE` so the agent can see the screen without
sending input. Before each run the silent home's `sav/` is emptied, so every
boot starts with no backup RAM. The user was present ("Yes, boot them now",
2026-11-13).

## Prediction

Each of three boots per release logs `SGID: T-1202G` (Japan) or
`SGID: T-1208H` (US), shows a title screen within 120 seconds with no input,
and leaves every source component unchanged.

## Inputs and Provenance

- Japanese: `local/disc_images/vh_saturn_jp_1m/` via
  `Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue`
  (`references/saturn_jp/README.md`).
- US: `local/disc_images/nw_saturn_us/` via
  `Night Warriors - Darkstalkers' Revenge (USA).cue`
  (`references/saturn_us/README.md`).
- BIOS: `local/mednafen/firmware/sega_101.bin` (`dcfef4b9…deac`) and
  `mpr-17933.bin` (`96e106f7…266f`) (`docs/mednafen.md`).
- Emulator: `vendor/mednafen/build/src/mednafen`, stock 1.32.1, SHA-256
  `de542817…582a`.
- Home: `local/mednafen_quiet/` (config SHA-256 `ef897288…5019`), firmware
  linked to `local/mednafen/firmware/`.

## Tools and Environment

- macOS 26.7.3, Darwin 25.6.0 arm64; ffmpeg 9.0.1 (Homebrew).
- `tools/mednafen/cold_boot.py` (copied from Cyberbots, `ENV-003`): runs
  Mednafen with `-qtrecord`, sends SIGTERM after `--seconds`, extracts one
  frame per second scaled to 352x240, builds 5x5 contact sheets, writes
  `run.json` with log, video and frame hashes, then deletes the video. Frames
  are scaled from the recording canvas, not native screenshots. This run is
  the tool's re-validation on Vampire Hunter: all six boots stopped cleanly
  and produced the expected files.

## Procedure

No pilot run: Cyberbots' 120 s was used directly, and the frames show both
titles well inside it.

```bash
JD=local/disc_images/vh_saturn_jp_1m; UD=local/disc_images/nw_saturn_us
./invenv.sh python -m tools.disc.hash_source --json $JD/* $UD/* > local/emu003/source-before.json
for r in jp us; do for n in 1 2 3; do
  if [ $r = jp ]; then CUE="$JD/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
  else CUE="$UD/Night Warriors - Darkstalkers' Revenge (USA).cue"; fi
  rm -f local/mednafen_quiet/sav/*
  ./invenv.sh python -m tools.mednafen.cold_boot "$CUE" local/emu003/$r$n --seconds 120
done; done
./invenv.sh python -m tools.disc.hash_source --json $JD/* $UD/* > local/emu003/source-after.json
cmp local/emu003/source-before.json local/emu003/source-after.json
```

Each boot took about 2 min 16 s wall time (23:19:21-23:33:00 local for all
six). zsh printed `no matches found` for the first `rm` (the folder was
empty); later ones matched the previous boot's files.

## Actual Result

| Boot | Start (UTC) | Exit | Log SHA-256 | Video size / SHA-256 (deleted) |
| --- | --- | ---: | --- | --- |
| jp1 | 2026-11-14 05:19:21 | 0 | `171d3af9…2460` | 1,432,511,040 / `9c798570…76fb` |
| jp2 | 05:21:38 | 0 | `b024ba00…` | 1,435,602,844 / `a7dc35b9…` |
| jp3 | 05:23:54 | 0 | `7c6d0f9b…` | 1,435,929,130 / `33c8db49…` |
| us1 | 05:26:11 | 0 | `33c3b62b…f84b` | 1,440,817,776 / `fd48598b…237f` |
| us2 | 05:28:27 | 0 | `99a21b08…` | 1,439,589,010 / `bfc450e2…` |
| us3 | 05:30:43 | 0 | `f6550037…` | 1,440,209,224 / `b4ab2bef…` |

Full hashes are in each ignored `local/emu003/<boot>/run.json`.

- **Japanese logs** (3,990 bytes each): `SGID: T-1202G`,
  `SGNAME: VAMPIRE HUNTER`, `SGAREA: JT`, `Region: 0x1`,
  `Cart: Backup Memory`. **US logs** (3,945 bytes each): `SGID: T-1208H`,
  `SGNAME: NIGHT WARRIORS`, `SGAREA: U`, `Region: 0x4`,
  `Cart: Backup Memory`. Within a release the logs differ only in the line
  naming the output file. Other "Error"/"Failed" lines are absent optional
  files: the `.sbi`, `ss.cfg`, the per-game `pgconfig` file, and
  `cheats/ss.cht`.
- **BIOS.** The log does not name the BIOS file. Mednafen 1.32.1's
  `src/ss/ss.cpp` (lines 1429-1434) uses `ss.bios_jp` for areas Japan and
  Asia-NTSC and `ss.bios_na_eu` otherwise, and with `ss.bios_sanity 1` (pinned)
  refuses a known BIOS for the wrong area (lines 1468-1479). With regions
  `0x1` and `0x4` logged and no error, the Japanese release booted with
  `sega_101.bin` and the US release with `mpr-17933.bin`. The BIOS screens
  agree: Japanese `©SEGA ENTERPRISES, LTD. 1994,1995 Ver.1.01`, US
  `TM & © 1995 SEGA. All rights reserved.` with the Saturn orb.
- **Determinism.** All 119 per-second frames are byte-identical across the
  three boots of each release. The video container hashes differ; the
  frames do not.
- **Japanese sequence** (agent-reviewed, frame N ≈ second N-1): 001-013
  BIOS animation and SEGA licence; 014-022 Capcom logo; 026-033
  `NOW LOADING` (blinking); 034-037 a werewolf silhouette against the moon;
  **038 a white screen with a dark mark**; 039-061 the intro (character group
  art, Bishamon, Morrigan, Demitri with bats); **063-070 the title `VAMPIRE
  HUNTER` / `Darkstalkers' Revenge`**; 071-080 `NOW LOADING`; 081-119 an
  attract fight, Anakaris vs. Rikuo/Aulbath, English HUD (`ROUND 1`, `FIGHT`,
  `FIRST ATTACK`, `REVERSAL`, `3 HIT`, `PRESS START BUTTON`).
- **US sequence:** the same structure with the US BIOS screens, **039 a red
  `DARKSTALKERS` logo card** (038 black), **063-070 the title `NIGHT
  WARRIORS` / `Darkstalkers' Revenge`**, and the same attract fight about one
  second later; the fight's moves diverge from the Japanese one after a few
  seconds.
- **Japanese vs. US frames:** 22 of 119 are byte-identical (001-002,
  011-013, 023, 026-032, 072-080: black, Capcom and loading screens).
- Title frames (352x240): Japanese `frames/065.png` = `frames/068.png`
  `216118a852117d9bd957752e99b6a08a35790a6c4a3c12c4cc2bc9377f1858a3`; US
  `frames/065.png` `d6617a8984dff59fe3eaea6876d27d48f95253a7fc352eaad2b11db88854177a`,
  `frames/068.png` `a7f306024053f9e772fde5ae801c08570f6d42a88c249fe86d807d34eb9b265e`.
- Every source component (both releases) is identical before and after
  (`cmp` of the two manifests); the binary and both config files hash as
  before.
- Backup RAM: each boot wrote `<cue name>.<hash>.bkr`, `.bcr` and `.smpc` to
  the quiet home's `sav/` (Japanese hash part `d5e0b9bd980bc403f93b3253613b3c79`,
  US `4d965b46d9ac92f88ac7f839e90e8983`). The `.bcr` is the backup-RAM
  cartridge's file.

Side observations (for `REF-004`, `EMU-004` and the register, not part of the
hypothesis):

- `ss.cart auto` gives both releases a **backup-memory cartridge**, with no
  database entry for either (`docs/mednafen.md`). Whether either game needs
  or uses an extended-RAM cart is `EMU-004`.
- No Japanese text appears in 119 s of either boot; the Japanese title, HUD
  and attract text are English.
- The intro difference at second 39 is a new regional difference
  (`docs/difference_register.md`, `INT-01`). One-second sampling cannot show
  how long each card is shown or whether the Japanese release shows a logo
  between samples.

## Conclusion

**CONFIRMED.** Stock Mednafen 1.32.1 with the project's silent home
cold-boots both untouched images to a stable title screen with no input, the
title showing about 63 s after launch in both, identically in three runs per
release at one-second sampling. Each release boots with its own region's
BIOS. `ss.cart auto` gives both a backup-memory cart.

## Uncertainty and Alternatives

- Identical per-second frames do not prove frame-exact determinism between
  samples, or with input. The boots ran within 14 minutes of each other; XvSF
  found late boot frames can depend on when the boot runs (its `EXP-0018`).
- The title screen never showed `PRESS START BUTTON` at the sampled seconds
  (it does during the attract fight); whether it blinks between samples is
  not known.
- Whether emulation stalls when the display sleeps was not tested.
- A Mednafen window opens during each run; the runs are silent, not hidden.

## Reproduction

Run the procedure above from the repository root, with the user present.
Evidence stays in the ignored `local/emu003/` (`jp1`-`jp3`, `us1`-`us3`, each
with `run.json`, `mednafen.log`, `frames/`, `sheet-*.png`; the source
manifests). Expect Japanese frame 065 to hash `216118a8…58a3` and US frame
065 `d6617a89…177a`.
