# EXP-0032: Morrigan's Japanese-Only Voices in US Enhanced

Task: AUD-002
Status: IN_PROGRESS (forced part done; play session next)
Confidence: CONFIRMED for the win line (forced); the other three pending

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

## Next

A cold-boot play session with the user (throws, Vector Drain, being hit, a
win), sample search of the recording for `50C2C`, `41220`, `4F10C` and
`56D60`, and offline PC logs of the session's states to tie the other three
guards to their events.
