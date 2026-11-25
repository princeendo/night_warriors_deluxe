# Night Warriors Deluxe (Saturn) 0.1.0

A restoration and multi-edition patch for the US Sega Saturn release of **Night
Warriors: Darkstalkers' Revenge** (Redump disc `5836`, `T-1208H`, V1.001). It
restores content that the US release suppressed from the Japanese *Vampire
Hunter* release and lets you switch editions in-game.

## What's Changed

A new **`EDITION`** option in `OPTION MODE` (saved with your other settings;
defaults to **`US ENHANCED`** for new or stock US saves) switches between three
editions at run time:

- **`US ENHANCED` (default):**
  - **All 14 post-ending epilogues** restored in English over the scrolling
    character artwork, using the official English text from PSP *Darkstalkers
    Chronicle: The Chaos Tower* (spelling slips fixed and logged; US Saturn
    character names kept).
  - **Morrigan's missing main-ending lines:** the two Japanese-only lines and
    pause page cut from the US butler scene restored in a new English
    translation (*"I'm a little tired. / Prepare my bed."*, *"Certainly,
    mistress."*). All other US main-ending text stays as shipped.
  - **Morrigan's 4 suppressed Japanese voice samples:** normal throw, Vector
    Drain, bat-seat win pose, and hurt.
  - **Donovan's 2 suppressed Japanese voice samples:** post-round-1 win pose
    and sword-planted punch+kick.
  - **Sasquatch's Japanese win poses, snow creatures, and voice sample:**
    restores the shy win pose, small snow creatures, and voice sample in poses
    0, 1, and 4 (Up + A + B + C).
- **`US ORIGINAL`:** stock US behavior (no epilogue text, stock Morrigan
  ending, suppressed voices/poses disabled).
- **`JP ORIGINAL`:** runs the US code set in Japanese mode (Japanese names such
  as Gallon, Japanese main endings and epilogues, Japanese voices and poses, no
  US auto-pause on missing controller).

## Download

| File | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `night_warriors_deluxe_0.1.0_xdelta.zip` | 49,807 | `92b8c26c3b9236c2294a6d169fddc6c8edcc1e31b33cb30e089e905a471330e0` |

The zip holds the xdelta patch (`night_warriors_deluxe.Track1.xdelta`, 54,362
bytes) and a `README.txt` with the untouched and patched Track 1 SHA-256
hashes. Only Track 1 changes; keep Track 2 and the CUE sheet untouched.

## Apply

See [`release/README.md`](https://github.com/princeendo/night_warriors_deluxe/blob/main/release/README.md):
apply with `xdelta3`, Delta Patcher, Rom Patcher JS, or any VCDIFF patcher to
Track 1 of the untouched US Redump disc `5836` (`d0960087…70da`). The patched
Track 1 SHA-256 must be
`25e05ec14a258e7f2bea49e51023dfbf96c553aae688b67c5044728c4040f1be`.

## Known Limits

- Cold-boot verified across all three editions in Mednafen; real Saturn
  hardware / burned CD-R testing is not yet recorded for 0.1.0.
- The RetroAchievements disc header hash (`8c7156c2e38f75a9ec54016427967e9e`)
  is unchanged (there is currently no Saturn RetroAchievements set for this
  game).
- `JP ORIGINAL` runs the US code set in Japanese mode, so the US title screen,
  intro logo, and US-only code changes remain.
- `JP ENHANCED` (`END-005`), victory-quote comparison (`QUO-001`), a standalone
  names toggle in Enhanced (`LOC-001`), and a full surface audit are deferred
  to later versions.
