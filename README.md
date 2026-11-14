# Vampire Hunter Ultimate (Saturn)

This repository will build one Sega Saturn image of Capcom's 1996
Darkstalkers sequel that combines its two releases: the Japanese **Vampire
Hunter: Darkstalkers' Revenge** (T-1202G) and the US **Night Warriors:
Darkstalkers' Revenge** (T-1208H). Each release has content the other lacks:
the web research behind the project points at the Japanese ending epilogues,
rewritten endings and victory quotes, voice samples, poses, and character
names. Which release is the base, which differences are merged, and which
become options are not decided yet (`DOC-002` in [TASKS.md](TASKS.md)).

Any English the base release lacks will come from an official source where
one exists and be marked as a new translation where none does.

The repository holds the tools, the difference inventory, and the expected
hashes. It holds no game data. How the work is done is recorded in
[TASKS.md](TASKS.md), [research_log.md](research_log.md), and
`research/experiments/`.

It follows the method of three sibling projects that shipped Saturn English
patches: Marvel Super Heroes vs. Street Fighter, X-Men vs. Street Fighter, and
Cyberbots. See [docs/playbook_from_mshvsf.md](docs/playbook_from_mshvsf.md),
[docs/lessons_from_xvsf.md](docs/lessons_from_xvsf.md) and
[docs/lessons_from_cyberbots.md](docs/lessons_from_cyberbots.md).

## Download

Nothing is released yet. The project is at milestone M0 (environment); see
"Current State" in [TASKS.md](TASKS.md).

## What's Changed

Nothing yet. The inventory of differences to resolve is
[docs/difference_register.md](docs/difference_register.md).

## Patch Files

Not yet. Formats are a `DOC-002` decision; the siblings published xdelta
(and, where possible, Sega Saturn Patcher `.ssp`) patches as GitHub Release
assets only. The images a patch applies to are named in
[references/saturn_jp/README.md](references/saturn_jp/README.md) and
[references/saturn_us/README.md](references/saturn_us/README.md).

## Build the Patch

Not yet.

## Development

### Python Tooling

Python 3.12+ and [uv](https://docs.astral.sh/uv/). No runtime dependencies.

```bash
./setup_venv.sh
```

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
for Vampire Hunter until a task re-validates them (`AGENTS.md` rule 26).

### Local Data

Game data stays under ignored paths:

| Path | Holds |
| --- | --- |
| `local/disc_images/vh_saturn_jp_1m/`, `vh_saturn_jp_2m4m/`, `vh_saturn_jp_3m/` | The untouched Japanese BIN/CUE sets (never modified) |
| `local/disc_images/nw_saturn_us/` | The untouched US BIN/CUE set (never modified) |
| `local/extracted/saturn_jp/`, `local/extracted/saturn_us/` | Files extracted from each track 1 |
| `local/logs/` | Tool output |
| `build/` | Derived images and patches |
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
- [docs/research_protocol.md](docs/research_protocol.md) and
  [research/experiments/README.md](research/experiments/README.md): how an
  experiment is run and recorded.
- [references/](references/): hashes and identity of the source images, and
  the web research the project started from.
