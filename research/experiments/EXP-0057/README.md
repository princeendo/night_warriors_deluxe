# EXP-0057: Keep a VS dummy in play after a lethal projectile

Task: TRN-001

Status: DONE

Confidence: CONFIRMED for Demitri's medium fireball against Victor in
cart-free Deluxe US Enhanced VS under Mednafen.

## Observation

EXP-0043 used the US combat vitality bytes and timer to force VS round
results. EXP-0044 drove a VS match with one attacking pad and the other
idle. A [Saturn-era guide](https://gamefaqs.gamespot.com/saturn/573987-night-warriors-darkstalkers-revenge/faqs/5186)
reports that the hidden stop-energy-loss switch can leave fighters stuck
when struck at low health. That report is a lead. This test uses ordinary
VS combat.

## Hypothesis

The damaging projectile can retain its hit reaction while the engine keeps
the round in play, if the defender's negative vitality is corrected before
the stock routine commits to the KO transition.

## Controlled change and prediction

From one VS save state, run the same two fireball motions with Victor at
stock vitality `0090` and at `0001`. Repeat both vitality conditions with
four code bytes changed in RAM after the checkpoint loads. The healthy
case should take damage in both runs. The low-vitality control should
enter KO, while the RAM variant should register both hits in the same
round and still have one point of vitality.

## Inputs and tools

- `build/exp0053_deluxe_title`, derived from untouched US T-1208H. See
  [the stock inventory](../../../references/saturn_us/README.md) and
  [EXP-0053](../EXP-0053/README.md). Track 1 SHA-256
  `9b0ed0c4f4b0ad7949b98dd2effce9089984b8e1a727dcbb5be23c46ab05b491`.
  Track 2 SHA-256
  `271844bfb734ab4fd322bc753bfad63b8a6e31d7d24272d52b5d10989065cdbb`.
- Mednafen 1.32.1 agent build with patches 0001 and 0002 (binary SHA-256
  `7040f6fece428a8a3a8d1e2f1f48e992ec15f2f9dd6267354e30fab377dc4cdd`),
  Python 3.13.13, `-ss.cart none`, volume 0, and both ports configured as
  gamepads. Fresh settings select `CUT` (`0x06080A29 = 00`). The matchup
  loads reduced animation slots `0E 10`, Demitri and Victor.
- `local/exp0057/control/vs.mc0`, 2,680,220 bytes, SHA-256
  `44d7b32f4ce927613b6555773e641b2dc55157ebe1f294c3559a8220ec7aee8f`.
  `probe.py` starts VS through the title and joins P2 with injected Start.
  It forces the fighter IDs after both picks, saves during the first round,
  and then replays the fixture with P2 idle. Use this state only with the
  same image. Agent RAM reads supply the data below.

## Actual result

The first stock run located the write at `0x06022992`. The actual vitality
fields are aligned signed 16-bit values at `0x06076C66` (P1) and
`0x0607706A` (P2), both at offset `0x46` in their player objects. The
previous timeout driver wrote starting at the low byte and also touched
the following display field. The exploratory run in `lethal/` did the
same and established a lead. The paired runs below set the aligned word.

The US `MAIN.BIN` code at `0x06022990` subtracts damage from R2, then stores
it to the defender at `0x06022992`. The signed test and branch at
`0x06022994`–`0x06022998` route a nonnegative result to `0x060229F0`. In the
lethal control, the negative result falls through and `0x060229EA` and
`0x060229EE` write KO bytes `02 FF` at `0x06080981`–`0x06080982`.

| RAM address | Original | Trial | Effect |
| --- | --- | --- | --- |
| `0x0602299A`–`0x0602299D` | `9015 04EE` | `A029 0EB5` | Branch to `0x060229F0` on the negative path. The delay slot uses the observed `R11 = 1` and `R0 = 0x46` to restore the defender's vitality to one. |

The two negative writes to `0x0607706A` in the low-vitality RAM trial had
`R2 = -4`. The delay-slot store at `0x0602299C` followed each write in the
same frame. Both hits reached the reaction write at `0x06022A6C`. The
frame captures show Victor reacting to both hits and returning to idle
between them. The KO bytes stayed zero and the timer continued through
both hits. The healthy trial with the four-byte edit matched stock damage.

| Run folder | Starting P2 vitality | After first fireball | After second fireball | KO bytes |
| --- | ---: | ---: | ---: | --- |
| `control-healthy` | `0090` | `0080` | `0071` | `0000` |
| `control-lethal` | `0001` | `FFFC` (-4), KO | Round ending | `02FF` |
| `clamp` | `0001` | `0001`, hit registered | `0001`, hit registered | `0000` |
| `clamp-healthy` | `0090` | `0080` | `0071` | `0000` |

Samples are from `reads.txt`. The two fireballs are separated by 180
emulated frames after the first motion completes. Absolute agent frame
numbers can differ by a frame or two on startup. Compare the sample labels
and the two logged write sequences.

| Capture under `local/exp0057/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `control-healthy/hit1-after-40.png` | 26,699 | `761cbd3bd6d3297c518d417da989102f585989c1ddc3d06817e3470b6f4661af` |
| `control-lethal/hit1-after-40.png` | 13,800 | `7995a21a8fb9a29ed0d6c18bb3128bc9fba490746dd02cafa3aef3aa4cb33988` |
| `clamp/hit1-after-40.png` | 27,735 | `0bcef085f3a48ac31db65ef4a68ffe1d11f1669be3ccd96e94f5acdfa1f491e0` |
| `clamp/hit1-after-180.png` | 28,438 | `f9a2589524ad86858c183584dc717d94fe61de7b322978ac2a1041ec5526b053` |
| `clamp/hit2-after-40.png` | 27,217 | `8d61a7304ce481acc299282ac939e9635605eaad53adf8ae6c08affa3f268b1f` |

## Conclusion and open checks

The four-byte RAM edit can keep this fight in play across successive
otherwise lethal Demitri fireballs. The edit is global while installed.
An image implementation needs a Training-only guard. Throws, chip damage,
and multi-hit moves still need tracing, along with vitality restoration timing
and physical Saturn behavior. The first follow-up is a matched lethal
throw against the same opponent.

## Reproduction

Run from the repository root. The first command below recreates the
checkpoint if needed. Use new output directories for repeated runs.

```bash
probe=research/experiments/EXP-0057/probe.py
cue="build/exp0053_deluxe_title/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python "$probe" "$cue" local/exp0057/recreated
state=local/exp0057/recreated/vs.mc0
./invenv.sh python "$probe" "$cue" local/exp0057/repro-healthy --state "$state"
./invenv.sh python "$probe" "$cue" local/exp0057/repro-lethal --state "$state" \
  --low-vitality
./invenv.sh python "$probe" "$cue" local/exp0057/repro-clamp --state "$state" \
  --low-vitality --patch 0602299A:A0290EB5
./invenv.sh python "$probe" "$cue" local/exp0057/repro-clamp-healthy --state "$state" \
  --patch 0602299A:A0290EB5
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x0602298C --end 0x06022A1C
```
