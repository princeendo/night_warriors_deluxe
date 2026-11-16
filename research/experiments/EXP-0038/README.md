# EXP-0038: The Edition Switch Build (design)

Task: EDITION-002 (criteria 2-3)
Status: IN_PROGRESS (design; patcher can grow files; hook point found)
Confidence: each element below is SUPPORTED by the cited reading; the whole
is a HYPOTHESIS until built and played

## Today's Static Changes and What Each Must Become

| Change (US Enhanced build) | Problem for the other editions | Edition-aware form |
| --- | --- | --- |
| `PL05`/`PL10`/`PL14` (`.O`, `.O2`) guards made `nop` (D-031-D-033) | US original would get the Japanese content | Restore the guards; their literal `0x0608089A` (every flag reader in these files is a guard) points at a new byte **C** = block byte `0x12` (`0x060830C6`) instead |
| English epilogues and the late routine written over `ST1JPN.BIN` (D-027) | The Japanese editions need it intact | Restore `ST1JPN.BIN`. The English file goes in place of **`ST2HIS.BIN`** (12,572 bytes plus 1,764 of room): language 2 ("HIS") is never selected, and its slots `0x1BE`/`0x1BF` are declared by no other file. New file: header (`0x1BC`, table), (`0x1BE`, `0x20000000` + routine), table of 14, records (12,884 bytes), routine; about 13,000 bytes (directory size updated) |
| `MAIN.BIN` `ST1` call loads `ST1JPN.BIN` by name, no flag gate (D-017) | US original must load none, Japanese the language's file | Original bytes on disc; in US Enhanced the title code writes the five changed words in RAM, the name literal pointing at `MAIN.BIN`'s own "ST2HIS.BIN" string (`0x0605B784`) |
| `MAIN.BIN` Morrigan US Enhanced script over her Japanese one, US table entry 4 repointed (D-030) | The Japanese editions need her Japanese script | Original on disc; the title code writes the Enhanced script and entry in US Enhanced, and the Japanese script and the original entry otherwise (both carried by the title code) |
| `ENDING.O`: the Japanese-branch tests made `nop`; r12 = slot `0x1BC` + delta | US original must take its own branches; the delta trick needs the English file loaded | Both tests read **C** (literal `0x0600D0B8`). The two consecutive one-frame waits (`0x0600CF86`, `0x0600CF8C`, each `0x06007BBC(1)`, a loop of `0x0601F6B0`) become one two-frame wait, freeing 6 bytes; `0x0600CF92`-`0x0600CFC1` move up 6 bytes (literal displacements re-encoded); r12 = `@0x06091E50` (slot `0x1BE`), the C test and the branch fit in `0x0600CFBC`-`0x0600CFCD` |
| `ST2USA.BIN` Morrigan records (unused entries `0xB1`, `0xB2`) | none (the US original script never shows them) | Keep |

Slot `0x1BE` (`0x06091E50`): the title code writes `0x26020766` (the
original r12 routine, cache-through) in every edition; in US Enhanced the
ending's English file overwrites it with its routine.

## Title-Time Code (in `TITLE.O`, grown into the free RAM, EXP-0037)

- **Apply** (idempotent, called each title frame): from E = block `0x11`
  (0 US Enhanced, 1 US original, 2 JP original, 3 JP Enhanced): flag
  `0x0608089A` (2, 2, 0, 0), language `0x06080882` and `0x060808A8` (1, 1,
  0, 0), C (0, 2, 0, 0); slot `0x1BE`; the `ST1` call words; Morrigan's
  script and table entry.
- **EDITION line**: drawn by `0x06018A1A` in the APPENDIX slot (y `0xB8`)
  while `0x06080A2B` is 0, else below it; left/right cycle E over 0-2 (3
  hidden until `END-005`); the cursor gains one stop.
- Room: `TITLE.O` + 740 bytes (to `0x06009800`), keeping `0x06009564` zero.

## Tool Needed

`tools/disc/patch_image.py` replaces files at their exact size. Growing
`TITLE.O` and `ST2HIS.BIN` within their room needs the directory record's
size (both-endian) rewritten too.

## Progress

- **Patcher.** `tools/disc/patch_image.py --grow` lets a file change size
  within the room before the next extent and rewrites its directory record
  (both byte orders); unit test `test_grow_file_rewrites_directory_size`.
- **Hook.** Text on the title and options screens is drawn once, not every
  frame (`--log-pc 06018A1A` over title and options states: no calls). A
  boot replay with no input (`f00000008`, 2,000 frames) runs three
  `TITLE.O` entries: `0x060024B8` (slot `0x4D8`, frame 553 only),
  `0x060032A4` (slot `0x4D9`, every frame from 1,936, reached from
  `MAIN.BIN`'s title-mode table `0x0606BDF8` with return `0x06036062`) and
  `0x06005AA0` (slot `0x4DA`, the object runner). Pointing slot `0x4D9`'s
  header entry at a wrapper (apply, then jump to `0x060032A4`) runs the
  apply each title frame without touching `MAIN.BIN` on disc. Not yet
  checked: that it also runs on the options screen and after a game.
- Options exit with Start calls the pack through a `TITLE.O` literal
  (`0x060052AE`), a second hook if needed.

## Open Risks

- The flag and language are set at start-up (D-013); changing them later
  at the title may miss values computed from them in between.
- `TITLE.O` must be loaded by its directory size, and reloaded on each
  return to the title.
- The loader must accept a header offset with `0x20000000` set.
