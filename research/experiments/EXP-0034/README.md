# EXP-0034: Sasquatch's Region-Gated Win Poses

Task: AUD-003 (`ANI-01`)
Status: IN_PROGRESS (criteria 1-2 met; the cold boot is left)
Confidence: CONFIRMED (forced replays from both regions' play sessions)

## Observation

`EXP-0014`: `PL10.O` reads the region flag (`0x0608089A`) six times. Lead
(`references/web_research/`, item `ANI-01`): the arcade restoration reports
Japanese pose and sound differences for Sasquatch, and a US Saturn guide
documents a hidden "steam from the nose" win pose. `PL10` is Sasquatch by
roster order (HYPOTHESIS, `EXP-0015`).

## Static Reading (US `PL10.O`, base `0x06001000`)

```bash
./invenv.sh python research/experiments/EXP-0014/readers.py local/extracted/saturn_us/PL10.O 0x06001000 0x0608089A
./invenv.sh python tools/sh2/disasm.py --base 0x06001000 --start 0x060042A0 --end 0x06004600 local/extracted/saturn_us/PL10.O
```

All six readers sit in one per-object state machine, `0x060044FC` (state at
`+5`), which picks a pose after the round ends. In state 1, when a timer at
`+0x20` wraps:

1. If a round-result test against `0x0608097B` fails: pose 2 (both regions,
   no flag test).
2. If the player's pad word (`0x06080A18`, or `0x06080A1C` for player 2;
   `& 0x0F7F`) is exactly `0x0708`: pose 4 (`0x060044C0`).
3. Otherwise a random bit (`0x060140B0`): 1 → pose 1 (Japanese) or pose 5
   (US) (`0x060045B2`); 0 → pose 0 (`0x06004456`).

| Pose | Flag 0 (Japanese) | Flag non-zero (US) |
| --- | --- | --- |
| 0 (random) | `+0x20`, `+0x21` = `0x40`; spawns two `0x01007300` objects (`0x06004348`) | `+0x21` = 1; no objects |
| 1 / 5 (random) | pose 1: spawns four `0x01003900` (`0x060042BC`) and two `0x01003A00` (`0x060043B6`) objects | pose 5 instead; no objects |
| 4 (held input) | `+0x20`, `+0x21` = `0x30`; spawns two `0x01007300` objects | `+0x21` = 8; no objects |

Objects are allocated by `0x06030ABA`; what they show or play is UNKNOWN.

**Pad word.** `MAIN.BIN` `0x0601CB68` builds `0x06080A18`/`0x06080A1C` each
frame from the raw words at `0x06076AB6`/`0x06076ABA` through a 13-entry
table (`0x0606792C`, the same in `MAIN.BIN` and in RAM: `1 2 4 8 0 100 400
200 70 10 20 40 700`). Read in the standard Saturn pad's bit order (Right,
Left, Down, Up, Start, A, C, B, R, X, Y, Z, L; the order is a HYPOTHESIS),
`0x0708` is **Up + A + B + C** (or Up + L), with nothing else held.

## Hypothesis

In the US release Sasquatch's win poses 0 and 4 run without the effect
objects the Japanese release spawns, and the random pose 1 is replaced by
pose 5.

## Sessions (with the user, sound recorded)

`EXP-0018/session.sh` on the stock images:

| Session | Image | Play |
| --- | --- | --- |
| `local/aud004/jp-session` | Japanese 1M | Sasquatch beat Victor 2-0, Up + A + B + C held after each KO |
| `local/aud004/us-session` | US original (`nw_saturn_us`) | the same |

From the live states (object `0x06076C70` JP, `0x06076C20` US; `+5` state,
`+0x61` pose; the Japanese addresses are US + `0x50`): in both releases the
pad word read **`0x0708`** while the user held Up + A + B + C, and both
rounds took **pose 4** (JP `f00005660`, `f00007307`; US `f00006254`,
`f00007858`). This confirms the button reading above. `PL10.O` has the same
layout in both releases (only literals differ), so the code addresses are
shared. Japanese replays from post-KO states, no input: round 1 took random
pose 1 (`0x060044A0`, then both spawners), round 2 pose 0 (`0x06004456`,
then `0x06004348`). The Japanese hidden pose shows steam from his nose
(live shots after `f00005603`).

## Forced Replays

From the US state `f00007802` (round 2, state 1, just before the choice)
and the Japanese `f00007249`, the pose was forced by a RAM write to the
chooser: `060045A0=A019` (`bra` to pose 4), or `060045A4=E000`/`E001` (the
random call replaced by `mov #0/#1,r0`). Then, one variable at a time, the
US flag left at 2, the flag written to 0, or only the six guards made `nop`
in RAM (`060042D0 06004354 060043C2 06004460 060044CA 060045B8` = `0009`).
`force.py --log-pc` (30 × 10 frames, screenshots) and `dense.py` (300
frames):

| Pose | Japanese | US flag 2 | US flag 0 | US six `nop`s |
| --- | --- | --- | --- | --- |
| 1 (random) | shy, blushing pose; six small snow creatures; sample `0x53116` | **pose 5**, a roar; no creatures; no `0x53116` | as Japanese | as Japanese |
| 0 (random) | two creatures; `0x53116` | no creatures; no `0x53116` | as Japanese | as Japanese |
| 4 (Up + A + B + C) | steam; two creatures; `0x53116` | steam; no creatures; no `0x53116` | as Japanese | as Japanese |

The spawned objects are the creatures (`0x01003900`/`0x01003A00` for pose
1, `0x01007300` for poses 0 and 4). `0x53116` (8-bit, `0x3271` bytes) is the
only sample that differs in each pair; the Japanese pose 1 plays it at
frame 97, and its bytes are at the same sound-RAM address in both regions.
So the asset is on the US disc and loaded; only the code skips it. The
steam of pose 4 is not region-gated: the hidden pose the US guide describes
exists in both releases.

## Build

`research/experiments/EXP-0034/build_sasquatch.py`: the `EXP-0033` image
plus the six guards made `nop` in `PL10.O` and `PL10.O2` (file `0x32D0`
`8F1D`, `0x3354` `8F2B`, `0x33C2` `8F27`, `0x3460` `8B08`, `0x34CA` `8B08`,
`0x35B8` `8B04`). Track 1
`e6e81ccc10264cea70aed3bc35c9b007d4705ac620fee5914775fde71fbbdc99`. It
loads from disc: replaying the US state `f00003511` (before the match loads
`PL10`) on this image for 400 frames, all six read `0009` in RAM.

## Conclusion

**CONFIRMED (forced replays):** in the US release Sasquatch's win poses 0, 1
and 4 lose the small snow creatures and their sample `0x53116`, and the
random pose 1 is replaced by pose 5. Six `nop`s in `PL10` restore the
Japanese behaviour with the flag kept at 2 (D-033). Left: a cold boot of the
build with the user (`AUD-003` criterion 3).

## Uncertainty and Alternatives

- The sample was identified by address and bytes, not listened to.
- Pose 2 (the round-result branch) has no flag test and was not shown.
- Player 2's copy (`PL10.O2`) is patched at the same offsets but was not
  played.
