# EXP-0059: Trace KO by projectile chip damage

Task: TRN-002

Status: DONE

Confidence: CONFIRMED for Demitri’s blocked medium fireball in cart-free Deluxe VS.

## Observation

EXP-0057 established a recovery branch for a direct projectile hit.
Guarding can produce a different damage and reaction path.

## Hypothesis and prediction

Demitri's medium fireball does one point of chip damage to a guarding
Victor at one vitality. If the blocked projectile uses the EXP-0057
KO branch, the stock match can end on the second chip hit and the same
four-byte edit should keep the match running.

## Controlled change

Replay two fireballs from the EXP-0057 VS checkpoint. Keep the
right-side defender holding down-back during projectile contact, and seed
his vitality to one at the start. Compare stock combat code with the
EXP-0057 RAM edit.

## Inputs and tools

The image, muted Mednafen 1.32.1 agent binary, and Demitri/Victor VS state
are the same hashed inputs as [EXP-0057](../EXP-0057/README.md). Both runs
used US Enhanced with `CUT`, no cartridge, and two gamepads. Victor's
starting vitality was set to `0001` at `0x0607706A`. In both runs, two
fireballs were played with P2 down-back held (`A000`) through the whole
input sequence. This includes 57 neutral P1 frames after the final
forward-plus-punch input. The second motion starts 180 frames after the
first motion script completes.

## Actual result

An initial timing test used standing back (`8000` instead of `A000` in
`probe.py`) with just 28 neutral P1 frames. `chip-stock` blocked the first
shot for one damage, but the second shot arrived after back was released
and did four damage. This disproved the short timing as a two-guard test.

With crouch guard held longer, the unmodified and edited runs each logged
one point of damage in R4 at `0x06022992` on both contacts. The first
contact wrote zero and the round continued in both cases. At the second
contact the game wrote `FFFF` (-1) in both cases. The KO bytes became
`02 FF` in the unmodified control and a red K.O. screen appeared. The
clock stalled at `56` (hex). The trial fell through to the EXP-0057
branch at `0x0602299A` (`9015 04EE` replaced by `A029 0EB5` in RAM),
restored one in its delay slot at `0x0602299C`, and reached the shared
nonnegative path. The KO bytes stayed `00 00`. By the last capture the
clock had reached `51` (hex) and the fighters were idle.

| Capture under `local/exp0059/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `chip-stock/hit1-after-20.png` | 28,202 | `43f341a3eeb70d4334b52d307fdaa47f084a074e02298ec3cd1e62819d99251b` |
| `crouch-stock/hit2-after-20.png` | 11,973 | `e5efffd1a61cb6dac0760c033bcfc970055c34528dcda3d90bfdef37bf60fa15` |
| `crouch-clamp/hit2-after-20.png` | 29,058 | `3c0be52ce085e4cfb1c4fe7c0bd897d1cf79b0f4872eed3dc9e3a9a280487070` |
| `crouch-clamp/hit2-after-180.png` | 29,254 | `4c1948914ae250fcc1c74abf6eba9c27c7385022de3bac543878f3934b69bc70` |

## Conclusion

Demitri's medium fireball uses the same tested KO branch on a direct hit
and on chip. A zero-vitality result does not trigger that branch. The
next chip hit does, and the existing projectile clamp covers it. Chip
from other attacks and character-specific routes remain untested.

## Reproduction

Run from the repository root with new evidence directories as needed.
Use the stock `exp0053_deluxe_title` checkpoint from EXP-0057.

```bash
probe=research/experiments/EXP-0057/probe.py
cue="build/exp0053_deluxe_title/Night Warriors - Darkstalkers' Revenge (USA).cue"
state=local/exp0057/control/vs.mc0
motion=2000x4,A000x4,8000x2,8020x4,0000x57
./invenv.sh python "$probe" "$cue" local/exp0059/crouch-stock --state "$state" \
  --low-vitality --guard --motion "$motion"
./invenv.sh python "$probe" "$cue" local/exp0059/crouch-clamp --state "$state" \
  --low-vitality --guard --motion "$motion" --patch 0602299A:A0290EB5
```
