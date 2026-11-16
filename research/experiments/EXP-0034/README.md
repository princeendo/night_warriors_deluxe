# EXP-0034: Sasquatch's Region-Gated Win Poses

Task: AUD-003 (`ANI-01`)
Status: IN_PROGRESS
Confidence: SUPPORTED (static reading of the US code); nothing run yet

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

## Planned Experiment

1. Sessions with the user, one per release (Japanese 1M, US original), as
   Sasquatch winning a match, holding Up + A + B + C after one KO.
2. From a post-KO US state: replays with the flag 2 and cleared (one
   variable), screenshots and `EXP-0008/dense.py`; the pose forced by
   writing the random call (`0x060045A4` `410B` → `E000`/`E001`, in RAM).
3. The same from the Japanese state.
