# EXP-0003: Screenshots and Save/Load States by Hotkey, Both Releases

Task: EMU-006
Status: DONE
Confidence: CONFIRMED

## Observation

Stock Mednafen takes screenshots (F9) and saves (F5) or loads (F7) states only
by hotkey. Cyberbots' `EXP-0003` found that handing focus back after each key
lost keys, and that `--keep-focus` with gaps of two seconds or more worked;
that is no evidence here.

## Hypothesis

In each release, F9 writes a screenshot, F5 saves a state, and F7 restores it,
in the same session and in a fresh cold boot, so that a screenshot after
loading a title-screen state equals the one taken when it was saved.

## Controlled Change

Hotkeys only, sent by `tools/mednafen/hotkeys.py --keep-focus` (the Mednafen
window stays in front for the run). No game, BIOS, binary or setting change.
The quiet home's `sav/`, `mcs/` and `snaps/` were emptied before each
release's first run, `sav/` and `snaps/` before its second. The user was
present ("Yes, start EMU-006", 2026-11-14).

## Prediction

Run A (cold boot): F9 on the title, F5 two seconds later, F9 on the attract
fight, F7, then F9 twice. Run B (fresh cold boot): F9, F7 (run A's state), F9
twice. A post-load screenshot equals the title screenshot taken at save time.

## Inputs and Provenance

As `EXP-0001`: Japanese 1M and US images, stock Mednafen `de542817…582a`,
quiet home `local/mednafen_quiet/` (config `aad9a7ef…57cf` since `EMU-005`).

## Tools and Environment

`tools/mednafen/hotkeys.py` (copied from Cyberbots, `ENV-003`); macOS 26.7.3;
`sips` for image sizes. This is the tool's re-validation on Vampire Hunter:
three runs recorded their key times; the fourth stopped on its exit step
(below).

## Procedure

```bash
Q=local/mednafen_quiet
for r in jp us; do
  # CUE = that release's .cue (EXP-0001)
  find $Q/sav $Q/mcs $Q/snaps -type f -delete
  ./invenv.sh python -m tools.mednafen.hotkeys "$CUE" local/emu006/$r-a.log --keep-focus \
    --at 65:F9 --at 67:F5 --at 95:F9 --at 98:F7 --at 100:F9 --at 103:F9
  # moved snaps/* to local/emu006/$r-a_snaps/, copied the state to local/emu006/$r-state/
  find $Q/sav $Q/snaps -type f -delete
  ./invenv.sh python -m tools.mednafen.hotkeys "$CUE" local/emu006/$r-b.log --keep-focus \
    --at 20:F9 --at 22:F7 --at 24:F9 --at 27:F9
  # moved snaps/* to local/emu006/$r-b_snaps/; re-hashed the state
done
```

Source manifests before and after (`local/emu006/source-*.json`);
`tools.mednafen.home` run afterwards.

## Actual Result

Key times (seconds after launch, from `local/emu006/<run>.json`):

| Run | F9 | F5 | F9 | F7 | F9 | F9 | F12 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| jp-a | 66.34 | 67.31 | 96.65 | 99.65 | 100.36 | 104.00 | 104.32 |
| us-a | 66.15 | 67.98 | 96.70 | 98.32 | 100.98 | 104.67 | 104.97 |

| Run | F9 | F7 | F9 | F9 | F12 |
| --- | ---: | ---: | ---: | ---: | ---: |
| jp-b | 21.17 | 22.31 | 24.33 | 28.66 | 28.99 |
| us-b | planned 20 | 22 | 24 | 27 | — (see below) |

Screenshots (agent-reviewed; 352x240 unless noted):

| Run | Shot | Screen | SHA-256 |
| --- | --- | --- | --- |
| jp-a | `-0000` | Title `VAMPIRE HUNTER` | `a166ccb4fd8e610e8151dbd60ab83c8d683c7514845956821056ae0ff7acf0fd` |
| jp-a | `-0001` | Attract fight | `06347af4…96ec` |
| jp-a | `-0002` | 0.71 s after F7: the title | `a166ccb4…f0fd` (**= `-0000`**) |
| jp-a | `-0003` | 4.35 s after F7: `NOW LOADING` | `4660da9f0c7a3fc7cf2e7587f72eca5b4d9e3cf258e7573dd64ebe0b4a95be26` |
| jp-b | `-0000` | Black, 330x240 (boot) | `aeb9399a…6bb2` |
| jp-b | `-0001` | After F7: `NOW LOADING` | `4660da9f…be26` |
| us-a | `-0000` | Title `NIGHT WARRIORS` | `025b8fd8b0463a02e1aa229c6f8c69215e833e80b1c7a92269561cb586a12209` |
| us-a | `-0001` | Attract fight with `PRESS START BUTTON` | `78b8b585…558e` |
| us-a | `-0002` | 2.66 s after F7: the title, slightly darker (fading) | `339533c2…a043` |
| us-a | `-0003` | 6.35 s after F7: `NOW LOADING` | `4660da9f…be26` |
| us-b | `-0000` | Black, 330x240 (boot) | `47aafdf5…7df4` |
| us-b | `-0001` | After F7: the title | `025b8fd8…2209` (**= us-a `-0000`**) |
| us-b | `-0002` | `NOW LOADING` | `4660da9f…be26` |

- **States:** Japanese `…(1M).d5e0b9bd980bc403f93b3253613b3c79.mc0`, 1,633,291
  bytes, `b5bc2ae272d68312a32b344ea4d2b120267382a24fc828b7bb77ddb02216137c`;
  US `…(USA).4d965b46d9ac92f88ac7f839e90e8983.mc0`, 1,630,946 bytes,
  `20ddd5ebbc83586f5ac6d2edfeb777dbe7aceb98a1a9d03ec8a63b46a9f663fb`. Each
  hashes the same after being loaded in run B. Kept in the ignored
  `local/emu006/jp-state/` and `us-state/`.
- **A reloaded title state reproduces the title screenshot byte for byte:**
  Japanese in the same session (jp-a `-0002` = `-0000`), US in a fresh cold
  boot (us-b `-0001` = us-a `-0000`). The `NOW LOADING` screen that follows
  is byte-identical in both releases (`4660da9f…be26`; compare `EXP-0001`
  frames 072-080).
- **Lost keys:** jp-b's three F9 presses gave two files; which of the two
  post-load presses (2.02 s and 6.35 s after F7) was lost is not known.
  Cyberbots' run 1 also lost an F9 about 2 s after F7.
- **us-b's exit:** after the last F9 the tool's F12 did not end Mednafen within
  its 30 s wait (`subprocess.TimeoutExpired`); the tool then stopped it with
  SIGTERM (the log ends `Signal has been caught and dealt with: SIGTERM`), so
  no `us-b.json` was written. No Mednafen process was left running. Its three
  screenshots and the state check were unaffected.
- Mednafen logs: jp-a and jp-b identical (75 lines, `ccf821e6…7d34`); us-a 75
  lines (`2927acf1…b780`), us-b the same plus the SIGTERM lines.
- Source manifests identical before and after; binary and both configs hash
  as before (`de542817…`, `aad9a7ef…`, `cb1c2d3b…`); `tools.mednafen.home`
  reported `no change`.
- `git check-ignore`: states and screenshots under `local/` (rule `local/`),
  and `*.mc*`/`*.png` under `research/experiments/`, are ignored.

## Conclusion

**CONFIRMED.** In both releases F9 writes a 352x240 screenshot (330x240 during
the BIOS phase), F5 saves a state of about 1.6 MB, and F7 restores it in the
same session and in a fresh cold boot; a reloaded title state shows a screen
byte-identical to the one taken at save time.

## Uncertainty and Alternatives

- One F9 in four post-load presses was lost and one F12 was not acted on
  within 30 s: hotkey timing is not fully reliable, as in every sibling.
  This is a reason to move to the agent interface (`EMU-020`, `EMU-021`), not
  to tune key gaps further.
- The Japanese title was not captured after a cross-session load (the
  surviving post-load shot is the following `NOW LOADING` screen).

## Reproduction

Run the procedure above from the repository root, with the user present.
Evidence stays in the ignored `local/emu006/`. Expect the US post-load title
`025b8fd8…2209`.
