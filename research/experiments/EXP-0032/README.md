# EXP-0032: Morrigan's Japanese-Only Voices in US Enhanced

Task: AUD-002
Status: DONE
Confidence: CONFIRMED (all four play from a cold boot); guard-to-event CONFIRMED for three, SUPPORTED for the hurt voice

## Observation

`EXP-0014` (D-014): Morrigan's code (`PL05`) skips four voice calls when the
region flag is non-zero; clearing the flag in US RAM after her winning KO
made the bat-seat line play.

## Hypothesis

Making the four guards' `bf` a `nop` (flag kept at 2) plays her voices as
clearing the flag did, and each guard is one event.

## Static Reading (US `PL05.O`, base `0x06001000`)

| File offset | Address (P1) | Branch | Guarded call |
| --- | --- | --- | --- |
| `0x1490` | `0x06002490` | `8B0B` `bf` | `0x0603A4D6`, codes `0x137` or `0x136` (by a byte at `+0xBC`) |
| `0x1A1E` | `0x06002A1E` | `8B09` `bf` | `0x0603A76E`, codes `0x134` or `0x136` (by a byte at `+0x75` = 2) |
| `0x3342` | `0x06004342` | `8B05` `bf` | `0x0603A4D6`, code `0x139` |
| `0x5280` | `0x06006280` | `8B04` `bf` | `0x0603A4D6`, code `0x135` |

`PL05.O2` (player 2) has the same branches at the same offsets. The US and
Japanese `PL05.O` differ in 465 bytes, all address literals (relocation).

## Test 1: the Win Line, Forced

As `EXP-0014` step 3, from `local/aud001/us-session/rec/states/f00011016.mcs`
(Morrigan's winning KO, US), 40 × 15 frames with sound, the flag untouched:

```bash
S=local/aud001/us-session/rec/states/f00011016.mcs
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/aud002/nops-winpose \
  --write 06002490=0009 --write 06002A1E=0009 --write 06004342=0009 --write 06006280=0009 \
  --steps 40 --step-frames 15 --wav
./invenv.sh python research/experiments/EXP-0009/wavsearch.py local/aud002/nops-winpose/sound.wav \
  local/extracted/saturn_jp/MORRIGA.BIN 0x1BAA0 8544 7795 local/aud002/wav-nops-winpose 0.35
```

| Guards opened | Bat-seat sample `56D60` |
| --- | --- |
| all four | found at 5.021 s (score 0.734), as `EXP-0014`'s cleared flag |
| `0x06002490` only | found at 5.021 s (0.734) |
| `0x06002A1E` only | not found |
| `0x06004342` only | not found |
| `0x06006280` only | not found |

So the guard at `0x06002490` is the bat-seat win line.

## Build

`research/experiments/EXP-0032/build_voices.py`: the `EXP-0031` build plus
the four `bf` → `nop` in `PL05.O` and `PL05.O2` (Track 1
`2985ff7366b3d0e28cbbf63be4e5399f73d2802923c36eadac1e2d0e0edc1ae8`).

## Test 2: Cold Boot and Play

With the user present: `research/experiments/EXP-0018/session.sh
local/aud002/play-session "build/us_en_voices/…(USA).cue"` (the script now
records sound, `-soundrecord`; WAV 52,522,584 bytes). The user played
Morrigan against Jon Talbain: throws, a Vector Drain, taking hits, a win.
Sample search (`EXP-0009/wavsearch.py`, threshold 0.35):

| Voice | Sample | Found at | Score | Screenshots there (agent-reviewed) |
| --- | --- | --- | --- | --- |
| normal throw (`AUD-01`) | `50C2C` | 174.4 s | 0.405 | Morrigan throwing him (frame ≈ 10,433) |
| hurt (`AUD-05`) | `4F10C` | 204.4 s | 0.586 | his attack landing on her (≈ 12,228) |
| Vector Drain (`AUD-02`) | `41220` | 249.2 s | 0.661 | her flying up carrying him (≈ 14,908) |
| bat-seat line (`AUD-03`) | `56D60` | 261.0 s | 0.731 | the bat seat with the bonus tally (≈ 15,614) |

(Time to frame: × 59.83.) The control sample `424E0` was not found in this
session (its event did not occur). The unpatched US control is `EXP-0009`'s
US recording, where none of the four occurs. The win quote after the match
is English.

## Test 3: Which Guard Is Which

The session's states just before each event, replayed 12 × 15 frames with
`--log-pc` on the four guarded call sites (`0x060024A6`, `0x06002A30`,
`0x0600434C`, `0x06006288`):

| Event | State | Call site that fired | Guard |
| --- | --- | --- | --- |
| throw | `f00010418` | `0x06006288` | `0x5280` (code `0x135`) |
| Vector Drain | `f00014824`, `f00014881` | `0x06002A30` | `0x1A1E` (`0x134`/`0x136`) |
| win | `f00015511`, `f00015568` | `0x060024A6` | `0x1490` (`0x137`/`0x136`) |
| hurt | `f00012128`, `f00012186` | none (the replay, without the user's inputs, did not repeat the hit) | `0x3342` (`0x139`) by elimination |

## Conclusion

**CONFIRMED:** with the four region-flag guards in Morrigan's code made
`nop` (both player sides, flag kept at 2), US Enhanced plays her four
Japanese-only voices at the same events as the Japanese release, from a cold
boot; three guards are tied to their events by PC log, the hurt one by
elimination (D-031). The win quote is unchanged.

## Uncertainty and Alternatives

- One instance of each voice was played; the throw match is the weakest
  (0.405).
- Player 2 Morrigan (`PL05.O2`) was patched but not played.
- Whether the Japanese release plays exactly these code pairs at these
  events (`0x136` is shared by two guards) is not compared call by call.
