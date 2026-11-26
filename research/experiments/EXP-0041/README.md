# EXP-0041: Mirror control and fighter allocations for a large pair

Task: ANI-002

Status: DONE

Confidence: CONFIRMED for the US retail mirror, the large-pair `CUT`
allocations and the forced `FULL` out-of-memory reset. SUPPORTED (arithmetic
only) for what a RAM cart would need to add.

## Observation

`EXP-0040` (D-036) showed that `FULL` loads the reduced sets in the mixed
attract fight on both retail discs, and estimated from file sizes that the
stock pools cannot hold the largest distinct full pair. The mirror and the
live allocations were still untested.

## Hypothesis

In a mirror, `FULL` loads one unsuffixed full set and `CUT` one underscore
set, each once. In a distinct pair, the pools that the loader fills cannot
hold both full sets, so opening the `FULL` path for a distinct pair fails in
the allocator.

## Controlled Change

From the US retail title checkpoint (the same one as `EXP-0040`), replay the
first attract fight with no input. All changes are made in emulator RAM only,
and no disc byte changes:

1. **Fighter IDs.** The attract code writes the one-based P1 and P2 IDs with
   `mov.b r0,@r1` at `0x06035908` (discovery run below). Halt on the P2 write,
   step once, and overwrite both IDs: `6 6` (Anakaris mirror) or `6 11`
   (Anakaris vs. Huitzil).
2. **Animation byte** `0x06080A29`: `00` (`CUT`) or `01` (`FULL`).
3. **Equality branch**, only in the last run: original bytes `89 0F`
   (`bt 0x0602194C`) at `0x0602192A`, replaced in RAM by `A0 0F`
   (`bra 0x0602194C`). Purpose: let `FULL` skip the reduced-set path for a
   distinct pair. Expected result: both full sets requested, then an
   allocation failure. Observed result: below.

Each run changes one of these against its control: the mirror pair differs only
in the animation byte. The `CUT` large pair differs from the demo only in P2's
ID. The forced `FULL` large pair differs from the `CUT` large pair in the
animation byte and the branch.

## Prediction

The mirror logs one load each: index `0x13` (`P06_`) for `CUT`, index 5 (`P06`)
for `FULL`. The allocations match the static sizes from `EXP-0040`
(684,404 and 1,162,868 bytes). The `CUT` large pair fits. The forced `FULL`
large pair stops at the allocator's "Out Of Memory" path.

## Inputs and Provenance

- Untouched US `Night Warriors`, `T-1208H` V1.001, Track 1 SHA-256
  `d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da`
  (`references/saturn_us/README.md`), rechecked after the runs.
- Extracted US `MAIN.BIN` SHA-256
  `b4a3c192e2b358c1b3635e8ab0025874a2833db4942a913e2014a8619cce16e8`, load
  base `0x06012000`.
- US title checkpoint `local/emu007/us-a-state/*.mc0`, SHA-256
  `2eb7dbd08bf9cc2f2092e121db3f1d76d5760d8f9ce94a588f1bef6f2eda49db`.
- Fighter IDs: 6 Anakaris, 9 Rikuo, 11 Huitzil (one-based, file `Pnn`);
  `docs/discoveries.md` line 274.

## Tools and Environment

Python 3.13.13 via `./invenv.sh`, `tools.sh2.disasm`, pinned Mednafen 1.32.1
with the validated agent interface (binary SHA-256
`7826b9b953ab80cdd6571f0a90829bb953d571ca215d00f9e2bdb50afdd0f887`), quiet
configuration `local/mednafen_quiet/mednafen.cfg` (SHA-256
`aad9a7ef68d31d249fcb12383bf6e3323d04b0d3986d355ed8cf9faa303c57cf`), volume 0,
backup-memory cart. The scripts are `force_match.py` (run) and
`tally_allocations.py` (log summary) in this folder.

## Procedure

1. Disassemble the loader (`0x06021868`-`0x060219F8`) and the allocator
   (`0x06013D94`-`0x06013FAC`) in US `MAIN.BIN`.
2. Discovery: log writes to the ID bytes `0x06076FD7` and `0x060773DB`
   (`0x06076C20 + 0x3B7` and `+ 0x7BB`, the bytes read at `0x06021916` and
   `0x0602191E`).
3. Run each case once: halt at the loader entry `0x0602190C`, then log the
   loader and every allocator entry and exit for 1,120 frames and take a
   screenshot. Log points: bottom-up `0x06013E9C`/`0x06013EC0`, top-down
   `0x06013EC4`/`0x06013EE8`/`0x06013EEE`, VDP1 `0x06013F7C`, VDP2 carve
   `0x06013F9E`, "Out Of Memory" `0x06013F1C`/`0x06013F68`.
4. Tally successful allocations per pool. The string passed to the failure
   handler `0x0601B078` at `0x060529E0` is `Out Of Memory`.

## Actual Result

**Discovery.** Both IDs are written at `0x06035908` in frame 321 after loading
the checkpoint (P1 `R0=6`, P2 `R0=9`). After each forced write the bytes
read back as forced, and the CPU's loads at `0x06021928`/`0x0602194C` used
the forced values (R13/R14 below).

**Allocator.** Three bump pools at `0x06076AD8` (low, high per pool). Pool 0 is
WRAM-H, pool 1 WRAM-L, pool 2 the VDP2 carve. `0x06013E9C` allocates from the
bottom of one pool and `0x06013EC4` from the top, each rounding the size to 4
bytes and returning 0 when it does not fit. `0x06013EF2` tries pools 0, 1, 2
bottom-up. `0x06013F30` tries 2, 1, 0 top-down. Either calls `0x0601B078`
with `Out Of Memory` when all three fail. P1's set is loaded bottom-up
(`0x06021892`, `mov #0,r5`) and P2's top-down (`0x060218BA`, `mov #1,r5`).

| Run | Fighters, setting | Loads (R13/R14 at `0x0602194C`) | Pool bytes allocated | Result |
| --- | --- | --- | ---: | --- |
| `demo-0` | Anakaris vs. Rikuo (stock demo), `CUT` | `P06_`, `P09_` (`0x13`, `0x16`) | 1,369,848 | fight plays |
| `mirror-0` | Anakaris mirror, `CUT` | `P06_` once (`0x13`, `0x13`) | 684,404 | fight plays |
| `mirror-1` | Anakaris mirror, `FULL` | `P06` once (5, 5) | 1,162,868 | fight plays |
| `pair-0` | Anakaris vs. Huitzil, `CUT` | `P06_`, `P11_` (`0x13`, `0x18`) | 1,367,788 | fight plays |
| `pair-1-branch` | Anakaris vs. Huitzil, `FULL`, branch forced | `P06`, `P11` (5, `0x0A`) | 1,270,072, then a 112,784-byte request fails | "Out Of Memory" in frame 739; Saturn BIOS CD player screen |

Each allocated total equals the static `.BIN` plus `.SPR` storage from
`EXP-0040`'s `size_fighter_assets.py`: `P06_` 684,404, `P06` 1,162,868,
`P09_` 685,444, `P11_` 683,384. The loader's window holds no other pool
allocation.

**Pool capacity for fighters.** The pools are refilled from their bases for the
fighter loads (the first bottom-up WRAM-L allocation returns `0x00200000`).
At the end of `pair-0`, WRAM-H was full, WRAM-L had 4,624 bytes free
(`0x0027CEF8`-`0x0027E108`) and the VDP2 carve was full. In `demo-0` the free
bytes were 2,560 and 4. Both give a fighter capacity of **1,372,412 bytes**:
WRAM-H 172,668, WRAM-L 1,048,576 (all of WRAM-L) and VDP2 151,168. Where the
pools are reset is UNKNOWN; the pointers at the loader entry still hold title
values.

**High-water marks.** The `CUT` large pair uses 1,367,788 of 1,372,412 bytes
(99.7 %). In the mirror, `FULL` uses 1,162,868 bytes (84.7 %). The forced
`FULL` large pair needs 2,256,056 bytes, 883,644 more than the capacity. It
failed with 102,340 bytes still free across the pools. The largest single
request in any run is 112,784 bytes (`0x1B890`, three requests in
`pair-1-branch`).

**Visual checkpoints.** `mirror-0.png` and `mirror-1.png` show Anakaris against
Anakaris. `pair-0.png` shows Huitzil in the fight. `pair-1-branch.png` shows the
Saturn BIOS CD player screen with no game picture.

**Cart layout in the pinned emulator** (`vendor/mednafen/src/src/ss/cart/extram.cpp`,
lines 59-85): the 1 MiB cart (ID `0x5A`) maps two 512 KiB banks at
`0x02400000` and `0x02600000`, each mirrored through its 2 MiB window. The
4 MiB cart (ID `0x5C`) maps two 2 MiB banks there. The ID byte is read at
`0x04FFFFFF`.

| Evidence under `local/exp0041/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `watch/watch.log` | 1,252 | `7b4fa8d0ee55ee0db0414049d4dba0d49525abb22650a12f7f42731a40113f03` |
| `demo-0/demo.log` | 2,293,637 | `847fa91cf12a5aa3b0dc817135821543e1f625114e01bd06531f6c8d080937cb` |
| `demo-0/demo.png` | 24,686 | `518dd8bddba455a2181b6705506c5e0e5d741cfdc1b0fca5f0fbb04b294de944` |
| `mirror-0/mirror.log` | 1,443,362 | `14573063c9249189f53ab471049d855eac116099b3ba2d3f7b8d84af00ba8bbc` |
| `mirror-0/mirror.png` | 24,264 | `1fae0f07b125a3341add11f69a2399ee1ae6c9f4fd82d8dae2f9c223dd0d7b22` |
| `mirror-1/mirror.log` | 2,793,825 | `b8f478d4553fbd7c6caaaa055fd06b9c132c6a9c1bc239e279135c877109c2e3` |
| `mirror-1/mirror.png` | 27,447 | `239f4edb6491f6cc16ae053868223c2fdb51d882cb6404625432bda571d40b9c` |
| `pair-0/pair.log` | 2,182,439 | `35f9ed46051ea56d40f9edd938293f84b94401aa8f8bcd603c1e331d787e5bc2` |
| `pair-0/pair.png` | 27,197 | `2ed1bb4495c439271762c67de19098c70dfcf56d051dad42f14fc055d8c93558` |
| `pair-1-branch/pair.log` | 2,800,117 | `14e7fa028db6347f7698dd892694428c5a55e570d70cea10446c6b8f16c57d86` |
| `pair-1-branch/pair.png` | 34,462 | `39bfa2c07654644cbb35b5ab5c6d6f8084143f5fb79a6ab3a11b6130521ae757` |

A first set of forced runs halted on the P2 write rather than the loader entry,
so its "pools before" line and early allocator lines came from frame 321. The
script was corrected to halt, step, verify the IDs and clear the write
breakpoint first. Those runs were deleted and rerun, with the same loads and
fighter allocations.

## Conclusion

The hypothesis is confirmed for the US retail code. `FULL` gives full
animation only in a mirror because one full set fits in the 1,372,412-byte
fighter pools and two do not. Opening the path for Anakaris vs. Huitzil
without more memory resets the console. A cart-backed allocator would have to
add at least 883,644 bytes for this pair. By the static set sizes, only 3 of
the 91 distinct pairs fit both full sets in 1,372,412 bytes, each with
Morrigan (`P05`): with Demitri (`P01`), Lord Raptor (`P04`) or Hsien-Ko
(`P13`).

## Uncertainty and Alternatives

- The 883,644-byte figure covers the fighter sets only. The match's other
  allocations happen outside this window and were not measured as a peak.
- A 1 MiB cart offers 1,048,576 bytes in two 512 KiB banks. The largest
  request (112,784 bytes) is much smaller than a bank, so by size alone the
  pair could fit as two more pools. Whether the `.BIN`/`.SPR` data works from
  A-bus cart RAM (CPU access speed, DMA source, cache behavior) is UNKNOWN
  and is for `ANI-003`.
- The JP mirror was not run. The JP mixed path matched the US path in
  `EXP-0040`.
- Arcade and VS selection were not used; the attract fight was forced.

## Reproduction

```bash
CUE="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
ST=$(ls local/emu007/us-a-state/*.mc0)
S=research/experiments/EXP-0041/force_match.py
./invenv.sh python $S "$CUE" "$ST" local/exp0041/watch --name watch --watch
./invenv.sh python $S "$CUE" "$ST" local/exp0041/demo-0 --name demo --setting 0
./invenv.sh python $S "$CUE" "$ST" local/exp0041/mirror-0 --name mirror \
  --ids 6 6 --force-pc 06035908 --setting 0
./invenv.sh python $S "$CUE" "$ST" local/exp0041/mirror-1 --name mirror \
  --ids 6 6 --force-pc 06035908 --setting 1
./invenv.sh python $S "$CUE" "$ST" local/exp0041/pair-0 --name pair \
  --ids 6 11 --force-pc 06035908 --setting 0
./invenv.sh python $S "$CUE" "$ST" local/exp0041/pair-1-branch --name pair \
  --ids 6 11 --force-pc 06035908 --setting 1 --branch-full
./invenv.sh python research/experiments/EXP-0041/tally_allocations.py \
  local/exp0041/{demo-0/demo,mirror-0/mirror,mirror-1/mirror,pair-0/pair,pair-1-branch/pair}.log
```
