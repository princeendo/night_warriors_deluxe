# Mednafen Vendor Area

The stock Mednafen 1.32.1 source and build will stay unmodified in the ignored
`vendor/mednafen/src/` and `vendor/mednafen/build/` (`EMU-001`,
`docs/mednafen.md`). Do not commit source archives, binaries,
runtime state, BIOS files, or game data.

## Agent-Interface Patch (`EMU-021`)

- `patches/0001-agent-interface.patch`, SHA-256
  `c30146efab0cb60bfb7a4465bc95d9935c63c0d7bf172b02f886b4ae2cff5244`, 592
  lines, against 1.32.1. Written in the MSHvSF repository (commit `b9a6593`)
  and copied unchanged through XvSF (`a1c82ba`) and Cyberbots (`bac6fde`),
  from which it was copied here. GPL-2.0, like Mednafen.
- Frontend only: adds `src/drivers/agent.inc` and hooks in
  `src/drivers/debugger.cpp`, `debugger.h`, and `main.cpp`. The Saturn core is
  unchanged. Active only when `MEDNAFEN_AGENT_DIR` is set.
- Reuse here follows `AGENTS.md` rule 16: build it only after stock Mednafen
  boots Vampire Hunter (`EMU-003`), `EMU-020` records why stock is
  insufficient, and the user confirms reuse (`DOC-002`); then re-run
  validations V1-V4 on both releases (`EMU-021`).

## Cache-Coherent Agent Writes (`APP-001`)

- `patches/0002-agent-cache-coherent-writes.patch`, SHA-256
  `767104e0ac68cf687ee0bdf14a9dd0b77d1997f52b1aa5c4b5138d01116a3451`, 20
  lines, against 1.32.1 (`src/ss/debug.inc`). Written here on 2026-11-26
  with the user's approval ("Patch agent build"). It is the project's first
  change to the Saturn core and applies only to the agent tree.
- Why: debugger writes to work RAM (`PutAddressSpaceBytes`, used by the agent's
  `write` and `onhit`) changed RAM but not the emulated SH-2 caches. The game
  then read its stale cached copy: an injected Start press was in RAM, but
  the title task read `0` (`EXP-0042`). The patch calls Mednafen's own
  `SH7095::Cache_AssocPurge` on both CPUs for each byte written to WRAM-L
  or WRAM-H, like a software associative purge, so the next CPU read sees
  the written byte. Other address spaces are unchanged.
- Effect on emulation: none unless the debugger or agent writes work RAM,
  and then only one cache miss per purged line.
- Rebuilt with `make -j12` in `vendor/mednafen/build-agent` (exit 0):
  binary SHA-256
  `7040f6fece428a8a3a8d1e2f1f48e992ec15f2f9dd6267354e30fab377dc4cdd`
  (21,368,488 bytes). V1-V4 re-run on both releases with
  `research/experiments/EXP-0042/revalidate.sh`: all pass (`EXP-0042`).

Build, from the repository root, with the stock source already extracted
(the siblings' recipe; re-check it in `EMU-021`). Apply `0002` after `0001`:

```bash
cp -R vendor/mednafen/src vendor/mednafen/src-agent
patch -d vendor/mednafen/src-agent -p1 < vendor/mednafen/patches/0001-agent-interface.patch
patch -d vendor/mednafen/src-agent -p1 < vendor/mednafen/patches/0002-agent-cache-coherent-writes.patch
mkdir -p vendor/mednafen/build-agent && cd vendor/mednafen/build-agent
PKG_CONFIG=/opt/homebrew/bin/pkg-config CC=/usr/bin/clang CXX=/usr/bin/clang++ \
  ../src-agent/configure --prefix="$PWD/install" --enable-debugger --enable-ss
make -j12
```

Run, from the repository root:

```bash
MEDNAFEN_HOME="$PWD/local/mednafen_quiet" MEDNAFEN_AGENT_DIR="$PWD/local/RUN/agent" \
  vendor/mednafen/build-agent/src/mednafen "<image .cue>"
```

The client is `tools/mednafen/agent.py`. Validation on Vampire Hunter: V1-V4
pass on both releases (`EMU-021`, `research/experiments/EXP-0005/README.md`,
D-005). Patched binary SHA-256 with `0001` only
`7826b9b953ab80cdd6571f0a90829bb953d571ca215d00f9e2bdb50afdd0f887` (21,369,448
bytes, macOS 26.7.3 arm64); with `0001` and `0002`, see above.
