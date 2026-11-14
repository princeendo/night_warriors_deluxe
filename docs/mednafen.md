# Mednafen

Stock Mednafen first (`AGENTS.md` rule 16). The sibling projects'
agent-interface patch is built only after `EMU-003` and `EMU-020`, and only if
the user confirms reuse there.

## Selected Stock Release (`EMU-001`, 2026-11-13)

Mednafen `1.32.1`, the release all three siblings used, so the
agent-interface patch (`vendor/mednafen/patches/0001-agent-interface.patch`)
can apply unchanged.

- Upstream project: <https://mednafen.github.io/>; releases:
  <https://mednafen.github.io/releases/>.
- Source archive URL:
  <https://mednafen.github.io/releases/files/mednafen-1.32.1.tar.xz>.
- Not downloaded again. The archive XvSF downloaded on 2026-10-28 was copied
  (`cp -c`) from the Cyberbots repository's ignored
  `local/downloads/mednafen-1.32.1/` into this repository's ignored
  `local/downloads/mednafen-1.32.1/`.
- Archive: `mednafen-1.32.1.tar.xz`, 3,571,236 bytes, SHA-256
  `de7eb94ab66212ae7758376524368a8ab208234b33796625ca630547dbc83832`, equal to
  the size and hash all three siblings recorded.
- License: GNU GPL version 2 (`COPYING` in the archive).

`bsdtar -tf` lists one top-level folder, `mednafen/`. It was extracted with
`bsdtar -xf` into an empty scratch folder under `local/`, then moved to the
ignored `vendor/mednafen/src/`. It is not modified.

## Exact Stock Build

Host: macOS 26.7.3 (25G342), Darwin 25.6.0 arm64, Apple clang 21.0.0
(clang-2100.3.34.2), GNU Make 3.81, `pkg-config` 3.0.10, SDL2 2.32.74, libFLAC
1.5.0, zlib 1.2.12. These build dependencies were already installed; nothing
was installed for this task. This is Cyberbots' toolchain on a newer macOS
point release (Cyberbots: 26.7.2, 25G332).

From the ignored `vendor/mednafen/build/`:

```bash
PKG_CONFIG=/opt/homebrew/bin/pkg-config \
CC=/usr/bin/clang CXX=/usr/bin/clang++ \
  ../src/configure --prefix="$PWD/install" --enable-debugger --enable-ss
make -j12
```

Both exited 0. `configure` took 30 s and `make -j12` 2 min 31 s
(23:02:28-23:05:29 local time). Logs: ignored
`local/logs/emu001-configure.log` and `local/logs/emu001-make.log`. The make
log's only warnings at the end are the linker's `-no_pie ignored for arm64`
and `ignoring duplicate libraries: '-liconv'`, as in Cyberbots.

Binary: `vendor/mednafen/build/src/mednafen`, Mach-O 64-bit arm64, 21,318,680
bytes, SHA-256
`de542817c6d90470b010283c02cc86d4f0772e41a597f01f913e69cc7bbb582a`. It differs
from the Cyberbots stock binary (`077ac658…669f`, 21,327,272 bytes) built from
the same archive with the same flags on macOS 26.7.2; a byte-identical binary
is not expected across host builds.

## `-help` Banner

```bash
MEDNAFEN_HOME="$PWD/local/mednafen" vendor/mednafen/build/src/mednafen -help
```

Output (ignored `local/logs/emu001-help.log`) begins:

```text
Starting Mednafen 1.32.1
 Build information:
   Compiled with gcc Apple LLVM 21.0.0 (clang-2100.3.34.2)
   Compiled against zlib 1.2.12, running with zlib 1.2.12(flags=0x000002a9)
   Compiled against libiconv 11.1, running with libiconv 11.1
   Compiled against SDL 2.32.74(SDL-release-2.32.74-0-ge4df8a5), running with SDL 2.32.74(SDL-2.32.74-no-vcs)
   Running with libFLAC 1.5.0
 Base directory: <checkout>/local/mednafen
 Emulation modules: apple2 nes snes gb gba pce lynx md pcfx ngp psx ss ssfplay vb wswan sms gg sasplay snes_faust pce_fast demo cdplay
```

The Saturn module `ss` is present. The process prints the usage text and exits
with status 255, as the siblings' 1.32.1 builds do for `-help` with a fresh
`MEDNAFEN_HOME`; this is not a build fault. The run created a default
`local/mednafen/mednafen.cfg` and its folders; project settings are
`EMU-002`'s work. No disc image was loaded.

## Game Database (static, for `EMU-004`)

`grep` of `src/ss/` in the 1.32.1 source for `T-1202G`, `T-1208H`, "Vampire
Hunter" and "Night Warriors" finds nothing: neither release has an entry in
Mednafen's Saturn database (unlike the siblings, whose entries named a cart).
Which cart each release needs, and what `ss.cart auto` gives it, is
`EMU-004`'s experiment.
