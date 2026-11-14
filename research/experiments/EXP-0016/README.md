# EXP-0016: The Region Flag's Pause Check

Task: DISC-002 (what the region flag changes)
Status: DONE
Confidence: CONFIRMED

## Observation

`EXP-0015`: the US `MAIN.BIN` routine at `0x0601D474` runs every fight frame
and reads the region flag (`0x0608089A`) at `0x0601D4C0`. Its code: a human
player's Start press (pad bit `0x0800`) toggles pause in both regions; with
the flag non-zero it also toggles pause, when not already paused, if a human
player's bit in `0x06076ABE` is clear. The pad routine at `0x06013C20`
rebuilds `0x06076ABE` every frame, setting one bit per port that reports a
standard pad (device type 2).

## Hypothesis

The US release pauses a fight by itself when a player's controller is
removed; the Japanese release does not; the region flag alone decides it.

## Controlled Change

Port 1 set to no device (`-ss.input.port1 none`) when Mednafen starts,
before loading a fight state; separately, the flag written to 0. No input.

## Prediction

US, port 1 empty: PAUSE within a frame. US, port 1 empty, flag 0: the fight
continues. Japanese, port 1 empty: the fight continues. Controls with a pad
in port 1 continue in both releases.

## Inputs and Provenance

- US fight state `local/aud001/us-session/rec/states/f00005443.mcs`
  (Morrigan vs. Victor, round in progress); Japanese
  `local/aud001/jp-session/rec/states/f00006054.mcs` (the same matchup).
- Patched Mednafen `7826b9b9…f887`, quiet home.

## Tools and Environment

`EXP-0010/force.py`, extended here with `--setting NAME=VALUE` (passed to
Mednafen), `--log-pc PC` (log the registers at each execution of PC) and
`--onhit PC:ADDRESS=HEX` (a write applied each time PC executes).

## Procedure

```bash
F=research/experiments/EXP-0010/force.py
U=local/aud001/us-session/rec/states/f00005443.mcs
J=local/aud001/jp-session/rec/states/f00006054.mcs
L="--log-pc 0601D4C8 --log-pc 0601D500"
./invenv.sh python $F us $U local/disc001/pause-control --steps 20 --step-frames 15
./invenv.sh python $F us $U local/disc001/pause-unplug --setting ss.input.port1=none ${=L} --steps 20 --step-frames 15
./invenv.sh python $F us $U local/disc001/pause-unplug-flag0 --setting ss.input.port1=none \
  --write 0608089A=00 ${=L} --steps 20 --step-frames 15
./invenv.sh python $F jp $J local/disc001/pause-jp-control --steps 20 --step-frames 15
./invenv.sh python $F jp $J local/disc001/pause-jp-unplug --setting ss.input.port1=none --steps 20 --step-frames 15
```

## Actual Result

| Run | Screens (300 frames, agent-reviewed) | Frame 150 | Logged |
| --- | --- | --- | --- |
| US, pad | fight continues (timer 96 → 90) | `81ee8014…` | — |
| US, port 1 empty | **PAUSE** from the first screenshot to the last | `39633423…` | `0x0601D4C8` x310 with R4 = 1 (a player's pad missing), R5 = 2 (flag); `0x0601D500` (pause toggle) once |
| US, port 1 empty, flag 0 | fight continues (timer 96 → 90) | `cdbf01db…` | neither PC reached (the flag-0 branch skips both) |
| Japanese, pad (rerun in `EXP-0018`, see the correction below) | fight continues; Victor wins the round | `5c30b50c…` | — |
| Japanese, port 1 empty | fight continues the same way; Victor wins | `5c30b50c…` | (a US address was logged by mistake; not used) |

**A failed first method, kept as a lesson.** Writing `0x06076ABE` = 0 with
`--onhit` just before the routine reads it did not change what the routine
read (R4 = 3 at `0x0601D4A6`, both pads present), whether the write was made
one or seven instructions earlier. HYPOTHESIS: the SH-2 data cache holds the
byte, and the agent's `write` goes to RAM behind the cache. Earlier RAM
writes (D-009, D-012, D-014) took effect, so the effect depends on what is
cached at the time; check that a write was read (a logged register) before
trusting a negative result.

**Correction (found in `EXP-0018`).** Mednafen saved `ss.input.port1 none`
into the quiet home's config when the `--setting` runs exited, so the first
Japanese "pad" run (`797c44e2…` at frame 150) in fact had port 1 empty. Rerun
with the config restored, the Japanese pad run's frame 150 is byte-identical
to the Japanese port-1-empty run (`5c30b50c…`): the Japanese fight is the
same with or without the controller. The US control ran before any
`--setting` run and is unaffected.

## Conclusion

**CONFIRMED:** with a controller missing from port 1, the US release pauses
the fight by itself; the Japanese release plays on. The US behaviour depends
on the region flag alone: with the flag cleared, the US release plays on too
(D-016). This is a US-only behaviour, and the usual reason for it is a
console platform requirement, not localisation (HYPOTHESIS). A patch that
keeps the flag at 2 and opens only the Japanese-only branches (`DISC-002`)
keeps it.

## Uncertainty and Alternatives

- Port 2 and a removal during play (rather than an empty port at load) were
  not tested; the code treats port 2 the same way, gated by the second bit of
  `0x06080888`.
- The `TITLE.O` reader also tests pad bit `0x0800` (Start) when the flag is
  non-zero; whether it is the same kind of check is UNKNOWN.

## Reproduction

The commands above; outputs in the ignored `local/disc001/pause-*`.
