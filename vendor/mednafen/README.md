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

Build, from the repository root, with the stock source already extracted
(the siblings' recipe; re-check it in `EMU-021`):

```bash
cp -R vendor/mednafen/src vendor/mednafen/src-agent
patch -d vendor/mednafen/src-agent -p1 < vendor/mednafen/patches/0001-agent-interface.patch
mkdir -p vendor/mednafen/build-agent && cd vendor/mednafen/build-agent
PKG_CONFIG=/opt/homebrew/bin/pkg-config CC=/usr/bin/clang CXX=/usr/bin/clang++ \
  ../src-agent/configure --prefix="$PWD/install" --enable-debugger --enable-ss
make -j12
```
