# EXP-0005: Build and Validate the Agent Interface on Both Releases

Task: EMU-021
Status: DONE
Confidence: CONFIRMED

## Observation

`EMU-020` (`docs/mednafen_agent_interface.md`): stock hotkey and debugger
runs lose keys, take the user's front window, and give registers only by eye.
The user approved reusing the sibling patch ("Yes, reuse it", 2026-11-14).
Cyberbots validated the same patch on its game (its `EXP-0006`, D-007); that
is no evidence here.

## Hypothesis

The patch applies unchanged to Mednafen 1.32.1 and builds; without
`MEDNAFEN_AGENT_DIR` the patched binary behaves like stock (V1); with it, on
both releases, reads equal the extractor's output of a state saved in the
same poll (V2), writes round-trip and halt control works (V3), and write
breakpoints log and continue (V4) or halt with machine-readable registers
(V4b).

## Controlled Change

A separate patched copy of the stock source and a separate build; the stock
tree and binary are untouched. Runs use the quiet home. No game, BIOS or
setting change. No hotkeys.

## Prediction

Patch applies without fuzz; build exits 0. V1: 119 of 119 per-second frames
equal `EXP-0001`. V2: four reads byte-identical to `mcs_extract`. V3: round
trip exact, `frames 30` halts 30 frames later, `savestate` refused while
halted. V4: hits logged while frames advance. V4b: a halt with registers.

## Inputs and Provenance

- Patch `vendor/mednafen/patches/0001-agent-interface.patch`, SHA-256
  `c30146ef…5244` (MSHvSF `b9a6593`; identical in XvSF and Cyberbots).
- Stock source `vendor/mednafen/src/` from `mednafen-1.32.1.tar.xz`
  (`de7eb94a…3832`, `EMU-001`).
- Images, BIOS and quiet home as `EXP-0001` (config `aad9a7ef…57cf`).

## Tools and Environment

macOS 26.7.3, Apple clang 21.0.0; `tools/mednafen/agent.py`,
`tools/mednafen/cold_boot.py`, `tools/memory/mcs_extract.py` (copied from
Cyberbots, `ENV-003`); [`validate.py`](validate.py), adapted from Cyberbots'
`EXP-0006/validate.py` (`bac6fde`): the release is an argument, the title
frame is 3900 (about 65 s), and the V4 range is chosen at run time (the first
16-byte WRAM-H block below `0x060F0000` that changes between the V2 read and
a read 30 frames later, with its `0x26` cache-through mirror) instead of
Cyberbots addresses; V4 runs 600 frames.

## Procedure

```bash
cp -R vendor/mednafen/src vendor/mednafen/src-agent
patch -d vendor/mednafen/src-agent -p1 < vendor/mednafen/patches/0001-agent-interface.patch
mkdir -p vendor/mednafen/build-agent && cd vendor/mednafen/build-agent
PKG_CONFIG=/opt/homebrew/bin/pkg-config CC=/usr/bin/clang CXX=/usr/bin/clang++ \
  ../src-agent/configure --prefix="$PWD/install" --enable-debugger --enable-ss
make -j12
cd ../../..
for r in jp us; do
  env -u MEDNAFEN_AGENT_DIR ./invenv.sh python -m tools.mednafen.cold_boot "$CUE" \
    local/emu021/$r-v1-equiv --seconds 120 --mednafen vendor/mednafen/build-agent/src/mednafen
  ./invenv.sh python research/experiments/EXP-0005/validate.py $r local/emu021/$r-run1
  ./invenv.sh python -m tools.memory.mcs_extract local/emu021/$r-run1/v2.mc0 \
    --region wram_l --region wram_h --region vdp1_vram --region vdp2_vram \
    --out-dir research/memory_dumps/emu021/$r-run1-v2
  cmp local/emu021/$r-run1/wram_l.bin research/memory_dumps/emu021/$r-run1-v2/wram_l.bin  # and the others
done
```

## Actual Result

**Build.** `patch` applied all four files with no fuzz or offsets
(`local/logs/emu021-patch.log`). Configure 31 s, `make -j12` 2 min 17 s
(01:34:59-01:37:47 local), both exit 0. No warning names a patched driver
file; the build has 2,667 warning lines against stock's 2,671. Binary
`vendor/mednafen/build-agent/src/mednafen`, Mach-O arm64, 21,369,448 bytes,
SHA-256 `7826b9b953ab80cdd6571f0a90829bb953d571ca215d00f9e2bdb50afdd0f887`.
The stock binary still hashes `de542817…582a`.

| Check | Japanese | US |
| --- | --- | --- |
| V1 equivalence (no agent dir) | 119 of 119 frames equal `EXP-0001` jp1; `T-1202G`, `Cart: Backup Memory` | 119 of 119 equal us1; `T-1208H`, `Cart: Backup Memory` |
| V1 smoke | `status` at frame 4; 13 spaces; 50 registers | same |
| V2 (halted at frame 3901, one poll) | WRAM-L `b7caad65…`, WRAM-H `1c4103e3…`, VDP1 VRAM `808ce017…`, VDP2 VRAM `84881efa…`: each **equal** to `mcs_extract` of the state (1,633,415 bytes, `62869736…b5ea`) | WRAM-L `914d4e2b…`, WRAM-H `5a76fa38…`, VDP1 VRAM `cc4352e0…`, VDP2 VRAM `84881efa…`: each **equal** to `mcs_extract` of the state (1,631,034 bytes, `5d538bcd…ff47`) |
| V3 | `0x060F0000`: `FF`×16 → pattern → `FF`×16 restored; `pause` at 3903, `run`, `frames 30` from 3906 halted at 3937; `savestate` refused ("not allowed while halted") | same values and frames |
| V4 (log mode, frames 3937-4537) | range `06009410-0600941F` (+ mirror): 462 hits, frames 3937-4184, PCs `06003054`, `06003062`, `060030A6`, `060030B0` | range `06009550-0600955F`: 517 hits, frames 3937-4211, PCs `060030C4`, `060030D2`, `06003116`, `06003120` |
| V4b (halt, all of WRAM-H) | halted at frame 4538, PC `0604F8FE`, R15 `060FFE88`, registers as text | halted at 4538, PC `0604FA72`, R15 `060FFED0` |

- Each V2 screenshot (352x240) is the title.
- Cross-check with the stock debugger: both releases' V2 WRAM-L reads hash
  equal to `EXP-0004`'s stock-debugger WRAM-L dumps (`b7caad65…`,
  `914d4e2b…`), taken at a different title instant; WRAM-L does not change on
  the title.
- The two releases' V4 code addresses differ by a constant `0x70`
  (`06003054` vs `060030C4`, and so on), and their V4 blocks are `0x140`
  apart: the same routine at shifted addresses (HYPOTHESIS, for `DIFF-001`:
  `0.BIN` or `MAIN.BIN` code moved by the US changes).
- `status`'s `pc` after `step` changed in the Japanese run (`0600094C` →
  `06013D26`) and not in the US run (`06013CD2` both times). As MSHvSF
  noted, `PC` read by `pause` is not the instruction address; `RPC` and hit
  logs are. Not a failure.
- Source manifests identical before and after; both configs unchanged
  (`tools.mednafen.home`: no change); no Mednafen left running.

## Conclusion

**CONFIRMED.** The sibling agent-interface patch applies unchanged and
builds; without `MEDNAFEN_AGENT_DIR` the patched binary is frame-identical to
stock on both releases, and with it reads (equal to the extractor), writes,
halt control, log-mode and halt-mode write breakpoints work, with
machine-readable registers. Agent output may be used as evidence (D-005).

## Uncertainty and Alternatives

- The extractor was checked against agent reads here, not against stock
  debugger dumps of the same instant; that is `DBG-001` (with `EXP-0004`'s
  same-instant states and dumps).
- V4's range was found at run time; its meaning is unknown.

## Reproduction

Run the procedure above from the repository root. Evidence stays in the
ignored `local/emu021/` and `research/memory_dumps/emu021/`.
