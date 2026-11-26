# EXP-0040: The Appendix animation setting and fighter memory

Task: ANI-002

Status: IN_PROGRESS

Confidence: CONFIRMED for the mixed demo in both releases. SUPPORTED for the loader's
capacity bound.

## Observation

A playtester reported that Appendix `FULL` does not give full animation for
different fighters. Both retail titles display `FULL` or `CUT` on that line.
`EMU-004` covered boot and attract with expansion carts, so it left the
match loader untested.

## Hypothesis

With `FULL` selected, the retail loader uses each fighter's smaller asset set
when available if their fighter IDs differ. A mirror can load one full set and
reuse it. The stock work-RAM pools cannot hold every distinct full pair.

## Controlled Change

Replay each retail title checkpoint through its first attract fight twice with
no input. Change only the live animation byte, from `00` (`CUT`) to `01`
(`FULL`). Verify the value read by the CPU before comparing the loaded IDs.
No disc bytes are changed.

## Prediction

When IDs differ, both runs take the same asset-loading path and request the
same files. In a mirror of a fighter who has both sets, `FULL` selects the
unsuffixed filenames and `CUT` selects the underscore variants.

## Inputs and Provenance

- Untouched US `Night Warriors`, `T-1208H` V1.001, and Japanese `Vampire
  Hunter` 1M, `T-1202G` V1.000. Full source component sizes and hashes are in
  `references/saturn_us/README.md` and `references/saturn_jp/README.md`.
- Extracted `TITLE.O` and `MAIN.BIN` SHA-256 values, respectively:
  - US `bd9fed5055c10be243b117f6c5ac33d92ee2897b5a654ea131c8449a0ad60cd0`,
    `b4a3c192e2b358c1b3635e8ab0025874a2833db4942a913e2014a8619cce16e8`.
  - JP `884f8aed4e79563ad26421e45374b79cc1635631fb4ab7d38a974b709577c91e`,
    `08e042ad554dda61769d8d989e63c6f6b40c7cf33f4506a018b1dee5a7bd5f21`.
- The retail title checkpoints used to validate work-RAM extraction in
  `EXP-0004` and `EXP-0006`. Under `local/emu007/`, the US `us-a-state/`
  checkpoint SHA-256 is `2eb7dbd08bf9cc2f2092e121db3f1d76d5760d8f9ce94a588f1bef6f2eda49db`.
  The JP `jp-a-state/` checkpoint SHA-256 is
  `f945cb512b38243c170d0a3ff8044f826614958878039b340e0708518c6d91a0`.
- The initial pilot used US Deluxe v0.1.0 `build/us_edition` (Track 1 SHA-256
  `25e05ec14a258e7f2bea49e51023dfbf96c553aae688b67c5044728c4040f1be`),
  which uses the stock US fighter graphics loader, and its P2 Donovan
  `SPEED SELECT` checkpoint `local/reddit_0.1.0/char_sel2/cs.mc0`
  (SHA-256 `e7b8d4da73b213b8fc147646ca7b3ce03f5a1e76eb3823f3fe61820c8fdda558`).

## Tools and Environment

Python 3.13.13 via `./invenv.sh`, `tools.sh2.disasm`, the PC-relative literal
search from `EXP-0013`, pinned Mednafen 1.32.1 with the validated agent
interface (binary SHA-256
`7826b9b953ab80cdd6571f0a90829bb953d571ca215d00f9e2bdb50afdd0f887`).
The trace uses a separate quiet home with volume 0 and a backup-memory cart
to match the checkpoint.

## Procedure

1. Follow each `TITLE.O` reference to the `FULL` string into the display
   branch. Follow the setting byte into `MAIN.BIN` and compare the US and JP
   branch predicates and destinations.
2. Follow the US load calls to the name tables and allocator. Tally each
   matched `.BIN` and `.SPR`, then sum the two largest separate full sets.
3. Replay each title checkpoint with the two animation values and compare
   the registers at the flag test and at the fighter load calls. Record the
   frame and the three allocator address pairs after the fight starts.

## Actual Result

**Static loader.** The US display reads `0x06080A29` at `0x06004E66`, and
uses `FULL` for nonzero and `CUT` for zero. Appendix row 6 toggles the byte
at `0x060058D8`–`0x060058DE`. Pack/unpack use save offset `0x5B`, zero by
default. Japanese `TITLE.O` reads `0x06080A79` at `0x06004DB2` and displays
the same labels. The US unlock code at `0x060045FA` calls an input-sequence
checker and sets `0x06080A2B` after success. The sequence table starts at
`0x06001AC2` with count 5 (`0100 0040 2000 0400 0020`). Stock input and saving
are to be verified under `APP-001`.

In US `MAIN.BIN`, `0x06021916` and `0x0602191E` read the two fighter IDs.
`0x06021924` takes the reduced-set selection path for `CUT`.
`0x06021928`–`0x0602192A` skips that path for `FULL` only when the IDs match.
The JP equivalent is at `0x06022190`–`0x06022196` (`MAIN.BIN` base
`0x06013A00`). The US reduced-set
selection adds 14 to the zero-based fighter index where the bitmask permits
it. The `.BIN` table at `0x0606AB04` and `.SPR` table at `0x0606A070` then
select the underscore files. Lord Raptor (`P04`) and Morrigan (`P05`) have
no separate reduced set. The loader at `0x06021868` checks for a set already
loaded on either side, which is how a mirror can reuse one set.

**Capacity calculation.** The US loader allocates the `.BIN` rounded to
4 bytes. The sprite path allocates descriptors, auxiliary data, the block
size table and groups of sprite blocks (`0x0601B544`–`0x0601B5DC`). The
sum of those allocations is the `.SPR` size less its 24-byte header.
`size_fighter_assets.py` verifies the archive sizes against the header and
block tables. Anakaris needs 1,162,868 bytes and Huitzil 1,093,188 bytes
for these two files each. Their full sets need 2,256,056 bytes together.

The stock allocator (`0x06013E9C`–`0x06013F78`) draws from the three pools
initialized in `0x06012164`–`0x06012198`. WRAM-H contributes at most
`0x060F0000 - 0x06093714`, WRAM-L at most `0x100000`. The third pool is
initialized via `0x06013F9E` by taking `0x24E80` bytes from VDP2 VRAM.
The US title checkpoint puts the pool at `0x25E5A17C`–`0x25E7EFFC`
(exclusive upper endpoint).
The WRAM-only bound is 1,427,692 bytes before any other allocations. The
third pool raises that bound to 1,578,860 bytes, still 677,196 bytes below
the fighter total. Pool fragmentation, other match resources and effects
are not included in this limit.

**Initial pilot.** The Deluxe speed-select checkpoint did not advance on its
own. The early pad write and a write to the P2 pressed word (`0x06076ABC`,
`0000` to `0800`) just before the confirm read did not advance it either.
The latter write was logged, but the subsequent CPU read still put zero in
R1 at `0x06031DA2`. The attempted keyboard confirm stopped at macOS's
System Events permission error 1002. Those runs provide no loader evidence.
The retail attract checkpoint provided the mixed matchup without input.

**US mixed matchup.** Both attract runs started the Anakaris vs. Rikuo demo.
R1 at `0x06021922` was `0` for `CUT` and `1` for `FULL`. Only `FULL` reached
the fighter equality test (`0x06021928`, R13 = 5, R14 = 8). Both reached
`0x0602194C` with resource indexes R13 = `0x13`, R14 = `0x16`. The two file
loads used the same `.BIN` table slots (`0x0606AB50`, `0x0606AB5C`) and thus
selected `P06_.BIN` and `P09_.BIN`, with the corresponding underscore sprite
sets in each run. After 1,120 frames the three allocator intervals had
0, 2,560 and 4 bytes free in both replays. The two screenshots of the demo
fight are byte-identical.

**JP mixed matchup.** The same replay with Vampire Hunter 1M produced the
same results. At `0x0602218E`, R1 was `0` and `1` respectively. `FULL` alone
reached the fighter equality test at `0x06022194` with R13 = 5 and R14 = 8.
Both settings reached `0x060221B8` with R13 = `0x13`, R14 = `0x16`, and the
same two `.BIN` table slots (`0x0606ABF0`, `0x0606ABFC`). After 1,120 frames,
both runs had 0, 2,488 and 4 bytes free in their allocator intervals and
byte-identical screenshots. An initial JP attempt used the US image's
`MAIN.BIN` load base. It played the demo but recorded no hits. The corrected
base `0x06013A00` was checked against the validated Japanese WRAM-H dump.

| Evidence under `local/exp0040/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `attract-us/cut.log` | 3,130 | `d6cdf2412d7bfb9eb1fb6ef1b5122fdf33297bee87c4b16eba15e89339d7aa0b` |
| `attract-us/full.log` | 3,764 | `12e62ae9eccc2ef3fed129e613eb8a6d914186319d30d16a0d09be6eea90d495` |
| `attract-us/cut.png` and `full.png` | 26,639 each | `8edbd0a3c908a634fa0a3824990451c3aa0b3171bbaed89c8795fe48e1527988` |
| `attract-jp-corrected/cut.log` | 3,130 | `bd876347edb9f5dccd4b09e42ae695620727d2f199b44760b92942a399e8a570` |
| `attract-jp-corrected/full.log` | 3,764 | `8b6858673a67673c863f12adbbc6639761a5e435fa0634b7cf6f1550daa38e35` |
| `attract-jp-corrected/cut.png` and `full.png` | 27,453 each | `a3bb758035739b2f44c64bfe9a98785419fcdb56d6114b55ca4564bcc8dce7aa` |

## Conclusion

The demo on both discs reproduces the reported `FULL` restriction with a
controlled change. Making the loader request both full sets would also
require a memory change for the largest pair.

## Uncertainty and Alternatives

The estimate gives a bound on the current loader. A revised loader could use
other memory or stream some resources. The pinned emulator models the 1 MiB
cart as two 512 KiB banks (`ss/cart/extram.cpp`). Total bytes alone cannot
establish that the allocations fit either that layout or a 4 MiB design.
Full mirrors, live allocation peaks for the largest pairs, Arcade and VS
remain to be checked.

## Reproduction

```bash
./invenv.sh python research/experiments/EXP-0013/xref.py \
  local/extracted/saturn_us/MAIN.BIN 06012000 06080A29 --after 14
./invenv.sh python research/experiments/EXP-0013/xref.py \
  local/extracted/saturn_jp/MAIN.BIN 06013A00 06080A79 --after 14
./invenv.sh python research/experiments/EXP-0040/size_fighter_assets.py
TRACE=research/experiments/EXP-0040/trace_animation.py
./invenv.sh python "$TRACE" \
  "local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  local/emu007/us-a-state/*.mc0 local/exp0040/attract-us
./invenv.sh python "$TRACE" \
  "local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue" \
  local/emu007/jp-a-state/*.mc0 local/exp0040/attract-jp-corrected --region jp
```
