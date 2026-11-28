# EXP-0058: Trace lethal throws in cart-free VS

Task: TRN-002

Status: DONE

Confidence: CONFIRMED for the two tested throws in cart-free Deluxe VS.

## Observation

EXP-0057 kept Demitri's projectile from ending a VS round when it hit a
one-vitality Victor. A throw can change both fighters' states before it
applies damage, so its KO path needs a separate check.

## Hypothesis

Demitri's close normal throw uses the same vitality and KO path as his
projectile, and the EXP-0057 RAM edit will let Victor recover from it.

## Controlled change

Use the same Deluxe cart-free `CUT` VS save state as EXP-0057. Walk into
throw range and use forward plus heavy punch, first with stock combat
code and then with the EXP-0057 edit. Set only Victor's vitality word to
one in each low-vitality replay.

## Prediction

The lethal stock control enters KO. If the existing patch covers throws,
Victor takes the throw, returns to an actionable state, and can be thrown
again during the same round.

## Inputs and tools

Use the `build/exp0053_deluxe_title` image, checkpoint
`local/exp0057/control/vs.mc0`, and muted Mednafen 1.32.1 agent build
identified by hash in [EXP-0057](../EXP-0057/README.md). The checkpoint
is Demitri on P1 versus Victor on P2, US Enhanced, both gamepads present,
`-ss.cart none`, animation setting `00` (`CUT`), and loaded slots `0E 10`.
VS restarts from this same checkpoint in each trial.

Extend `EXP-0057/probe.py` to select the active pad and feed a fixed
approach and attack. Every matched run walks forward 115 frames, inputs
forward plus heavy punch for three frames, releases for two frames, and
runs 180 further frames before repeating. The defender gets no input.
The probes set the idle fighter's aligned vitality word to `0001` once
before the first walk, and log writes around that word. The screenshot
and watch address show whether the throw connected.

## First result and refined hypothesis

The first stock trial visibly threw Victor and entered KO, but there was
no write at the projectile's `0x06022992`. Demitri's throw writes the
negative vitality result at `0x0602B71E`. The signed check at
`0x0602B722`–`0x0602B724` falls through and the tail branch at `0x0602B72E`
enters `0x0602AB90`. The KO bytes become `01 00` and the timer stops. The
hypothesis of a shared projectile branch is disproven for this throw.

The new hypothesis is that this throw can restore vitality to one on
its own negative path and resume at its own nonnegative continuation.
Repeat the test with Victor attacking Demitri to check the other side.
Victor's normal throw has a separate store at `0x0602B8DC` and a negative
path through `0x0602B8EE` to `0x0602BAEA`. The same intervention can be
attempted on that path, using its defender register.

## Actual result

| RAM address | Original | Trial | Effect |
| --- | --- | --- | --- |
| `0x0602B726`–`0x0602B729` | `64E3 4F26` | `A046 0EB5` | Branch to `0x0602B7B6`, with a one-vitality store in the delay slot through R14. |
| `0x0602B8E4`–`0x0602B8E7` | `4F26 64E3` | `A014 0CB5` | Branch to `0x0602B910`, with a one-vitality store in the delay slot through R12. |

In both patched traces, the delay slot uses observed `R0 = 0x46` and
`R11 = 1`. Each comparison used the relevant four-byte change alone.

| Run folder | First damage and KO bytes | Later in the same round |
| --- | --- | --- |
| `throw-lethal` | Victor vitality `FFFC` (-4); `01 00` | KO and round transition |
| `throw-clamp` | Victor vitality `FFFC` then `0001`; `00 00` | Victor returned to idle and took a second throw, 300 frames after the first damage write |
| `p2-stock` | Demitri vitality `FFFF` (-1); `01 00` | KO and round transition |
| `p2-clamp` | Demitri vitality `FFFF` then `0001`; `00 00` | The hold ticks continued, Demitri got free, and Victor started a second hold 300 frames after the first damage write |

Victor's hold has successive damage ticks. The stock sign branch accepts
zero. The edited run therefore alternated between zero on some ticks and
one after each negative result was corrected. The second hold was still
in progress at the last sample. The KO bytes stayed clear throughout
both edited replays and the clock advanced from `5D` to `4F`.

| Frame capture under `local/exp0058/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `throw-lethal/hit1-after-90.png` | 28,910 | `71ab3752b308a16185a1ec88e94403f43b12bfac4e600b45849563106f2ed27d` |
| `throw-clamp/hit1-after-180.png` | 28,697 | `8f269a9550ca23acda86dc83b29861e8d211be25525566c27121a6e5ab5ed308` |
| `throw-clamp/hit2-after-40.png` | 29,624 | `4339fffda897ed4da9df3b679a58097eb36382df934c2834164c14439805850d` |
| `p2-stock/hit1-after-90.png` | 10,410 | `cbdc15e27dfff6baa5924daedf6b98ff40bf92ea5b6b103738b63c330ed96f6f` |
| `p2-clamp/hit1-after-90.png` | 29,730 | `38e69a888c825c9206363170f71096ff692a8ac16af7a2e542b330736c0084fd` |
| `p2-clamp/hit2-approach.png` | 29,554 | `50e807edc6e8c4f65e90612599dab91ff74812de4d91e180be97129872433089` |
| `p2-clamp/hit2-after-40.png` | 29,195 | `ce660fb46384782eb95abf2613b9d36a86a4124ada73e7e5814e5a6a6e46a182` |

## Conclusion and open checks

Each tested throw can finish, release the defender, and be started again
in the same round. The two moves have separate KO branches, and this
experiment exercised an attacker on each pad. The two pairs vary in
both move and controller role. The effect of swapping controller ports
for the same move remains open. Character-specific
or alternate throws are still open. The trial code is installed only in
Mednafen RAM. A mode-aware image patch is future work.

## Reproduction

Run from the repository root. Recreate `vs.mc0` via EXP-0057 if needed.
Use new output directories when rerunning.

```bash
probe=research/experiments/EXP-0057/probe.py
cue="build/exp0053_deluxe_title/Night Warriors - Darkstalkers' Revenge (USA).cue"
state=local/exp0057/control/vs.mc0
./invenv.sh python "$probe" "$cue" local/exp0058/throw-lethal --state "$state" \
  --low-vitality --approach 8000x115 --motion 8010x3,0000x2
./invenv.sh python "$probe" "$cue" local/exp0058/throw-clamp --state "$state" \
  --low-vitality --approach 8000x115 --motion 8010x3,0000x2 --patch 0602B726:A0460EB5
./invenv.sh python "$probe" "$cue" local/exp0058/p2-stock --state "$state" \
  --low-vitality --attack-pad 2 --approach 4000x115 --motion 4010x3,0000x2
./invenv.sh python "$probe" "$cue" local/exp0058/p2-clamp --state "$state" \
  --low-vitality --attack-pad 2 --approach 4000x115 --motion 4010x3,0000x2 \
  --patch 0602B8E4:A0140CB5
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x0602B702 --end 0x0602B732
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x0602B8CC --end 0x0602B94A
```
