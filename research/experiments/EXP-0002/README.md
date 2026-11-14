# EXP-0002: Cartridge Settings on Boot and Attract, Both Releases

Task: EMU-004
Status: DONE
Confidence: CONFIRMED (boot and attract only)

## Observation

`EXP-0001` (D-001): with `ss.cart auto`, Mednafen gives both releases a
backup-memory cart (`Cart: Backup Memory`); neither release has an entry in
Mednafen's database, and both headers' peripheral field reads `J`. The
siblings needed a 4 MiB extended-RAM cart (MSHvSF, XvSF) or none for boot
(Cyberbots); that is no evidence here.

## Hypothesis

Neither release needs an extended-RAM cart to boot and run its attract mode:
with `ss.cart` set to `none`, `extram1` or `extram4`, each boots to the same
screens as with the backup cart, with no warning.

## Controlled Change

One setting per run: `ss.cart` = `none`, `extram1` or `extram4`, passed as
`--setting ss.cart=VALUE` to `tools.mednafen.cold_boot`. Everything else as
`EXP-0001`. The backup-cart case is `EXP-0001` itself (`auto` resolved to
`Backup Memory`), so `backup` was not run again. After each run
`tools.mednafen.home` restored the pinned `ss.cart auto` (Mednafen saves
command-line settings on exit). The user was present ("Yes, start EMU-004",
2026-11-13).

## Prediction

Each log shows the chosen `Cart:` line and no other change; frames match
`EXP-0001` (allowing time shifts); no warning or error screen.

## Inputs and Provenance

As `EXP-0001`: Japanese 1M and US images, stock Mednafen `de542817…582a`,
quiet home, both BIOS files.

## Tools and Environment

`tools/mednafen/cold_boot.py`, `tools/mednafen/home.py`; macOS 26.7.3,
ffmpeg 9.0.1. Frames compared by SHA-256 with `EXP-0001` boots `jp1` and
`us1`, and each differing frame looked up among all of that boot's frames to
tell a whole-second shift from other content; contact sheets reviewed by the
agent.

## Procedure

```bash
JD=local/disc_images/vh_saturn_jp_1m; UD=local/disc_images/nw_saturn_us
./invenv.sh python -m tools.disc.hash_source --json $JD/* $UD/* > local/emu004/source-before.json
for r in jp us; do for c in none extram1 extram4; do
  if [ $r = jp ]; then CUE="$JD/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
  else CUE="$UD/Night Warriors - Darkstalkers' Revenge (USA).cue"; fi
  find local/mednafen_quiet/sav -type f -delete
  ./invenv.sh python -m tools.mednafen.cold_boot "$CUE" local/emu004/$r-$c \
    --seconds 120 --setting ss.cart=$c
  ./invenv.sh python -m tools.mednafen.home
  shasum -a 256 local/mednafen_quiet/mednafen.cfg
done; done
./invenv.sh python -m tools.disc.hash_source --json $JD/* $UD/* > local/emu004/source-after.json
cmp local/emu004/source-before.json local/emu004/source-after.json
```

## Actual Result

| Run | Start (UTC) | Exit | Log line | Log SHA-256 | Frames equal to `EXP-0001` |
| --- | --- | ---: | --- | --- | ---: |
| `jp-none` | 2026-11-14 05:42:48 | 0 | `Cart: None` | `bea12179…0a9c` | 52 of 119 |
| `jp-extram1` | 05:45:04 | 0 | `Cart: 1MiB Extended RAM` | `81a957f0…215e` | 52 of 119 |
| `jp-extram4` | 05:47:21 | 0 | `Cart: 4MiB Extended RAM` | `3268f852…2103` | 52 of 119 |
| `us-none` | 05:49:37 | 0 | `Cart: None` | `453f587f…a351` | 90 of 119 |
| `us-extram1` | 05:51:53 | 0 | `Cart: 1MiB Extended RAM` | `8aef2ec4…a9bf` | 90 of 119 |
| `us-extram4` | 05:54:10 | 0 | `Cart: 4MiB Extended RAM` | `b480de27…a2fc` | 90 of 119 |

- Each log differs from `EXP-0001`'s only in the `Cart:` line and the output
  file name.
- **`none`, `extram1` and `extram4` give byte-identical frames** (all 119)
  within each release.
- Against `EXP-0001` (backup cart), the differing frames are not whole-second
  shifts (only one, US 037, equals another `EXP-0001` frame). The agent
  reviewed the contact sheets: every differing frame shows the same scene as
  the `EXP-0001` frame of the same second at another point of its animation
  (logo fades, Morrigan's hand, the attract fight's moves), and the title
  frames match in place (US 065 equals `EXP-0001`'s `d6617a89…177a`). So the
  backup cart shifts timing by a fraction of a second; it adds or removes no
  screen.
- No run shows a warning, error or Japanese text.
- Each run wrote only `.bkr` and `.smpc` to `sav/` (no `.bcr`, as expected
  without a backup cart).
- Every run restored the quiet config to `ef897288…5019`; all source
  components are unchanged (`cmp` of the manifests).

Side observation (for `INT-01`): Japanese frame 038 without the backup cart
(`jp-none/frames/038.png`, `db3cf88c…c09c`) shows a red, hand-drawn logo
whose first letters read "VAM", on black, at the point where the US release
shows its red `DARKSTALKERS` card. `EXP-0001`'s white screen at 038 was
another moment of the same card's animation.

## Conclusion

**CONFIRMED for boot and attract.** Neither release needs an extended-RAM
cart to boot and run its attract mode; `none`, `extram1` and `extram4` give
identical frames, and the backup cart changes only sub-second timing. The
project keeps `ss.cart auto` (backup memory, as D-001), which lets saves go
to a cart as well as internal backup RAM.

## Uncertainty and Alternatives

- Play was not tested: a mode, a fight, Appendix options or a save could
  still check for a cart. Re-test only if a later task sees a cart message.
- One boot per setting; `EXP-0001` showed boots repeat exactly.

## Reproduction

Run the procedure above from the repository root, with the user present.
Evidence stays in the ignored `local/emu004/`.
