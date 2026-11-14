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

## Project-Local Configuration (`EMU-002`, 2026-11-13)

Mednafen never reads the user's global configuration here: every run sets
`MEDNAFEN_HOME` to an ignored folder in this checkout.

| Home | Use |
| --- | --- |
| `local/mednafen/` | Interactive runs (the user plays, hears the game). |
| `local/mednafen_quiet/` | Unattended runs: `sound.volume 0`, `video.glvsync 0`, `video.blit_timesync 0`; `firmware/` is a symlink to `../mednafen/firmware`; own `sav/` and `mcs/`. |

The silent home is the siblings' practice (carried preference, not yet
confirmed for this project). Sound stays enabled at volume 0, so emulation
timing is unchanged. Whether a volume-0 home still records sound for
`AUD-001` is **UNKNOWN**; use the interactive home for sound captures until
tested. The siblings found that, with vsync on, emulation stalls while the
display sleeps; that is a **HYPOTHESIS** here.

The interactive configuration is the file Mednafen 1.32.1 generated on its
first run (`EMU-001`'s `-help`). Both homes are pinned by
`tools/mednafen/home.py` (copied from Cyberbots, `ENV-003`, unchanged), which
creates the quiet home from the interactive one if it is missing:

```bash
./invenv.sh python -m tools.mednafen.home
```

The tool rewrites only existing `key value` lines and fails on a key with no
line. Mednafen saves command-line settings into the configuration on exit, so
rerun it after any run that passed settings on the command line. Its first run
reported `local/mednafen: no change` and `local/mednafen_quiet: sound.volume,
video.blit_timesync, video.glvsync`; a second run reported `no change` for
both.

Pinned settings (both homes), all equal to the 1.32.1 defaults; pinning guards
against settings saved from a command-line run:

| Setting | Value | Purpose |
| --- | --- | --- |
| `filesys.path_firmware` | `firmware` | BIOS files below the home. |
| `filesys.path_sav` | `sav` | Saturn backup RAM. |
| `filesys.path_savbackup` | `b` | Backup-RAM backups. |
| `filesys.path_state` | `mcs` | Save states. |
| `filesys.path_snap` | `snaps` | Screenshots. |
| `filesys.path_movie` | `mcm` | Movies. |
| `filesys.path_pgconfig` | `pgconfig` | Per-game overrides. |
| `filesys.path_cheat` | `cheats` | Cheats. |
| `filesys.fname_state` | `%f.%M%X` | Stable state filenames. |
| `filesys.fname_snap` | `%f-%p.%x` | Stable screenshot filenames. |
| `autosave` | `0` | No implicit state at load or exit. |
| `debugger.autostepmode` | `0` | No debugger step mode at launch. |
| `ss.bios_jp` | `sega_101.bin` | Japanese BIOS, for the `JT` release. |
| `ss.bios_na_eu` | `mpr-17933.bin` | North American/European BIOS, for the `U` release. |
| `ss.bios_sanity` | `1` | BIOS sanity checks on. |
| `ss.cart` | `auto` | Neither release is in Mednafen's database (above), so what `auto` gives them is `EMU-004`'s test. |
| `ss.region_autodetect` | `1` | Region taken from the disc, so each release gets its own BIOS. Which BIOS each boot used is `EMU-003`'s check. |

Result: with each home, `-help` reports `Base directory:` that home and
`Loaded 7904 valid settings and 0 unknown settings` (ignored
`local/logs/emu002-help-mednafen.log`, `emu002-help-mednafen_quiet.log`):

| File | Size | SHA-256 |
| --- | ---: | --- |
| `local/mednafen/mednafen.cfg` | 652,752 | `48a7cf6b03224ab6fc485965ec13a0a9d657f678b3f187d3791469686ab228fc` |
| `local/mednafen_quiet/mednafen.cfg` | 652,750 | `ef89728844860b8334411d3bbd6195b84828956c5e446744efdc9e59ea305019` |

`diff` between the two shows only the three quiet settings. Both hashes equal
Cyberbots' and XvSF's pinned files: Mednafen's generated default holds no
host- or game-specific content. Pad bindings are not set yet (`EMU-005`).

### Saturn BIOS

Copied unchanged (`cp -p`, `cmp` clean) from the Cyberbots ignored
`local/mednafen/firmware/` (itself a copy of XvSF's and MSHvSF's) into
`local/mednafen/firmware/`. Each matches the SHA-256 that Mednafen 1.32.1's
own `Documentation/ss.html` (from the verified archive) gives:

| File | Size | SHA-256 | Mednafen use |
| --- | ---: | --- | --- |
| `sega_101.bin` | 524,288 | `dcfef4b99605f872b6c3b6d05c045385cdea3d1b702906a0ed930df7bcb7deac` | `ss.bios_jp` |
| `mpr-17933.bin` | 524,288 | `96e106f740ab448cf89f0dd49dfbac7fe5391cb6bd6e14ad5e3061c13330266f` | `ss.bios_na_eu` |

This project is the first sibling to need the North American BIOS for a
boot. Whether each BIOS boots its release is `EMU-003`'s test.

### Launch Commands

Interactive, from the repository root:

```bash
MEDNAFEN_HOME="$PWD/local/mednafen" \
  vendor/mednafen/build/src/mednafen \
  "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
```

```bash
MEDNAFEN_HOME="$PWD/local/mednafen" \
  vendor/mednafen/build/src/mednafen \
  "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
```

Unattended: the same with `MEDNAFEN_HOME="$PWD/local/mednafen_quiet"`, with
stdout and stderr redirected to a file under the ignored `local/logs/`. Stock
Mednafen has no log-directory setting. No disc has been loaded yet; the first
boots are `EMU-003`, run with the user present.
