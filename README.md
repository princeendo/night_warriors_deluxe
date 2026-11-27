# Night Warriors Deluxe (Saturn)

This repository builds a patch for the US Sega Saturn release of Capcom's 1996
Darkstalkers sequel, **Night Warriors: Darkstalkers' Revenge** (T-1208H), that
restores Japanese-only content from **Vampire Hunter: Darkstalkers' Revenge**
(T-1202G) and adds an in-game edition switcher. Wherever official English text
exists (PSP *Darkstalkers Chronicle: The Chaos Tower*), the patch uses it;
where none exists, it uses a new translation marked as such. The full policy,
as decided by the user, is in
[docs/localization_policy.md](docs/localization_policy.md).

The repository holds the tools, difference inventory, build scripts, and
expected hashes. It holds no game data. How the work is done is recorded in
[TASKS.md](TASKS.md), [research_log.md](research_log.md), and
`research/experiments/`.

It follows the method of three sibling projects that shipped Saturn English
patches: Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter, and
Cyberbots. See [docs/playbook_from_mshvsf.md](docs/playbook_from_mshvsf.md),
[docs/lessons_from_xvsf.md](docs/lessons_from_xvsf.md), and
[docs/lessons_from_cyberbots.md](docs/lessons_from_cyberbots.md).

## Download

[Version 0.1.0](https://github.com/princeendo/night_warriors_deluxe/releases/tag/v0.1.0),
as a GitHub Release asset (an xdelta patch for Track 1): what it changes, how
to apply it, and its known limits are in
[release/README.md](release/README.md) and
[release/notes_v0.1.0.md](release/notes_v0.1.0.md).

## What's Changed

In 0.1.0, a new **`EDITION`** setting in `OPTION MODE` (saved in spare bytes
of the `N_WARRIORS_` save; defaults to **`US ENHANCED`** for new or stock US
saves) switches between three editions at run time:

- **`US ENHANCED` (default):**
  - **All 14 post-ending epilogues** restored in English over the scrolling
    character artwork, using the official English from PSP *Darkstalkers
    Chronicle: The Chaos Tower* (spelling slips fixed and logged; US Saturn
    character names kept; `END-002`).
  - **Morrigan's missing main-ending lines:** the two Japanese-only lines and
    pause page dropped from the US butler scene restored in a new English
    translation (*"I'm a little tired. / Prepare my bed."*, *"Certainly,
    mistress."*), timed to the scene (`END-004`). All other US main-ending text
    stays as shipped.
  - **Morrigan's 4 suppressed Japanese voice samples:** normal throw, Vector
    Drain, bat-seat win pose, and hurt (`AUD-002`).
  - **Donovan's 2 suppressed Japanese voice samples:** post-round-1 win pose
    and sword-planted punch+kick (`AUD-003`, `EXP-0039`).
  - **Sasquatch's Japanese win poses, snow creatures, and voice sample:**
    restores the shy pose, small snow creatures, and voice sample in poses 0,
    1, and 4 (`AUD-003`).
- **`US ORIGINAL`:** stock US behavior (no epilogue text, stock Morrigan
  ending, suppressed voices and poses disabled).
- **`JP ORIGINAL`:** runs the US code set in Japanese mode (Japanese fighter
  names like Gallon, Japanese main endings and epilogues, Japanese voices and
  poses, no US missing-pad auto-pause; keeps US title/intro art and US code
  changes).

**Deferred to later versions:** `JP ENHANCED` (`END-005`, hidden in the menu
until it differs from `JP ORIGINAL`), victory-quote comparison (`QUO-001`),
standalone names toggle in Enhanced (`LOC-001`), and a full screen/audio
surface audit (`REF-004`, `UI-001`, `COV-001`). The difference register is
[docs/difference_register.md](docs/difference_register.md).

## Patch Files

One xdelta (VCDIFF) patch for Track 1 of the US Saturn image named in
[references/saturn_us/README.md](references/saturn_us/README.md) (Redump disc
`5836`, `T-1208H`), published as a GitHub Release asset only. There is no
`.ssp` patch (`release/README.md`, "Why there is no .ssp patch").

### Applying a Patch

The steps, tested patchers, and expected Track 1 SHA-256 hash are in
[release/README.md](release/README.md), "Apply the Patch".

## Build the Patch

The build follows the checked-out source. Use tag `v0.1.0` to reproduce the
published v0.1.0 checksums. The current source adds JP Enhanced, an
Enhanced names option, and new US Enhanced quote variants. The build
candidate and hardware verification status are in [TASKS.md](TASKS.md).
The paired retail comparison is in [the surface audit](docs/text_surfaces.md).

The release image is built from the untouched US source image, with game data
kept under the ignored paths below.

### Files You Need

None of these are in the repository. They go at these paths (all ignored by
git):

| File | Where it goes | What it is |
| --- | --- | --- |
| `Night Warriors - Darkstalkers' Revenge (USA).cue` and Tracks 1-2 | `local/disc_images/nw_saturn_us/` | The untouched US Saturn BIN/CUE (Redump disc `5836`, never modified). Track 1 SHA-256: `d0960087…70da` (493,741,248 bytes); full hashes in [references/saturn_us/README.md](references/saturn_us/README.md). |
| The 415 files of Track 1 | `local/extracted/saturn_us/` | Extracted from untouched US Track 1 using the command in "Set Up". |
| Local PSP epilogue transcript | `local/ref002/psp_epilogues/transcript.md` | Transcribed from the user's US PSP *Darkstalkers Chronicle* ISO (`EXP-0020`, [references/psp_chronicle_us/README.md](references/psp_chronicle_us/README.md)). |

### Set Up

Python 3.12+ and [uv](https://docs.astral.sh/uv/). No runtime dependencies.

```bash
./setup_venv.sh
```

Extract the files of US Track 1 (the source image is only read):

```bash
./invenv.sh python -m tools.disc.iso9660 "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin" --extract local/extracted/saturn_us/
```

### Build the Release Patch

```bash
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/us_edition
```

Patch generation, zip packaging, and round-trip verification commands are in
[release/README.md](release/README.md), "Rebuild the Patch from This
Repository", and [release/RELEASING.md](release/RELEASING.md).

## Development

### Python Tooling

```bash
./invenv.sh pytest -q
```

```bash
./invenv.sh ruff check .
```

```bash
./invenv.sh ruff format --check .
```

```bash
./invenv.sh mypy
```

Run every tool through `./invenv.sh python -m tools.<area>.<tool>`. Tools
copied from the sibling projects carry a provenance note and are not evidence
for Night Warriors Deluxe until a task re-validates them (`AGENTS.md` rule 26).

### Local Data

Game data stays under ignored paths:

| Path | Holds |
| --- | --- |
| `local/disc_images/nw_saturn_us/` | The untouched US BIN/CUE set, Redump disc 5836 (never modified) |
| `local/disc_images/vh_saturn_jp_1m/` | The untouched Japanese 1M BIN/CUE set, Redump disc 3677 (never modified) |
| `local/extracted/saturn_us/`, `local/extracted/saturn_jp/` | Files extracted from each Track 1 |
| `local/logs/` | Tool output |
| `build/` | Derived images and release patches/zips |
| `vendor/mednafen/src*`, `build*` | Mednafen source and builds |

### Project Guides

- [AGENTS.md](AGENTS.md): the rules every session follows.
- [TASKS.md](TASKS.md): the dependency-controlled plan and current state.
- [research_log.md](research_log.md): chronological record, failures
  included.
- [docs/difference_register.md](docs/difference_register.md): every
  regional difference, with both releases' evidence.
- [docs/discoveries.md](docs/discoveries.md): confirmed findings only.
- [docs/known_unknowns.md](docs/known_unknowns.md): open questions and the
  experiment that would answer each.
- [docs/localization_policy.md](docs/localization_policy.md): the user's
  edition, source, scope, and release decisions.
- [docs/research_protocol.md](docs/research_protocol.md) and
  [research/experiments/README.md](research/experiments/README.md): how an
  experiment is run and recorded.
- [references/](references/): hashes and identity of the source images, and
  the web research the project started from.
