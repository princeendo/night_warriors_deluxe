# EXP-0008: Which Morrigan Samples Each Release Plays

Task: AUD-001
Status: DONE
Confidence: CONFIRMED (sample present on both, played in the Japanese bat-seat
pose only); SUPPORTED (throw and hurt voices Japanese-only)

## Observation

`EXP-0007` recorded one Morrigan session per release with a state every
second; the bat-seat pose occurs in both. The user heard "some more
dialogue" in the Japanese session. Every sound file is byte-identical on both
discs.

## Hypothesis

Morrigan's Japanese-only voices are samples in `MORRIGA.BIN` that both
releases load into sound RAM, and the US release does not play them.

## Controlled Change

None to the games. States from `EXP-0007` are replayed without input in the
patched Mednafen (D-005), quiet home, and the SCSP (sound chip) slot
registers are read from save states.

## Prediction

During the Japanese bat-seat pose a slot plays a sample inside Morrigan's
region of sound RAM; during the US bat-seat pose none does; the sample's
bytes are the same in both releases' sound RAM.

## Inputs and Provenance

- `EXP-0007` states: Japanese `f00023129` (before the round 3 KO vs.
  Bishamon), US `f00010960` (before the round 3 KO vs. Victor); all session
  states for the inventory.
- Extracted `MORRIGA.BIN`, `BISHAMON.BIN`, `VICTOR.BIN`, `ALWAYS.BIN`
  (identical on both discs).

## Tools and Environment

In this folder: [`sndlog.py`](sndlog.py) (frame-by-frame sound-RAM changes
and WAV), [`slots.py`](slots.py) (active SCSP slots in a state: key-on set,
envelope not in release; sample start SA, loop end LEA, 8/16-bit), and
[`dense.py`](dense.py) (replays a state while saving a state every few frames,
parsing each with `slots.py`).

## Procedure

1. Pilot of `sndlog.py` (60 frames, Japanese): sound-RAM `0x700`-`0x7BF`
   changes in bursts (`01 50 00 00`, `01 00 2b 06`, ...), a candidate command
   area; the format was not decoded. Reading the SCSP slot registers through
   the agent's `physical` space at `0x25B00000` returned **only zeros** for
   every frame: the debugger does not map them there. They are in each save
   state (`[SCSP] SlotRegs`, 32 slots x 16 little-endian 16-bit registers).
2. `sndlog.py` for 600 frames through each pose (`local/aud001/pose-<r>/`):
   the command-area writes differ in detail; not decodable yet.
3. `slots.py` over the session states around each pose (1 s apart).
4. `dense.py` for 600 frames through each pose: 151 samples each, about one
   every 4 frames (`local/aud001/dense-pose-<r>/`).
5. Located each `.BIN` in the start-of-run sound RAM by 64-byte probes every
   4 KiB; classified every played SA by region.
6. `slots.py` over all 828 session states (both releases) for samples in
   Morrigan's region; the agent reviewed the Japanese screenshots at each.

## Actual Result

**Sound-RAM layout** (both releases, at the pose; each file's probes all at
one base):

| Region | Japanese | US |
| --- | --- | --- |
| `ALWAYS.BIN` | `0x0B000`-`0x3B294` | same |
| `MORRIGA.BIN` | `0x3B2C0`-`0x58EC0` | same |
| opponent | `BISHAMON.BIN` `0x58EC0`- | `VICTOR.BIN` `0x58EC0`- |

**Dense pose replays** (frames counted from the state; `dense.py` takes no
screenshots, so the pose's place comes from the `EXP-0007` session
screenshots: about 170-310 after the Japanese state and 170-345 after the US
one, then the bonus screen; a replay without input follows the recorded play
here because the round is already won):

| Release | Samples played (source, SA, frames) |
| --- | --- |
| Japanese | ALWAYS `12440` 1, ALWAYS `10048` 1-29, BISHAMON `636DC` 5-185, ALWAYS `1ACCA` 21-69, ALWAYS `219AE` 145-201, **MORRIGA `56D60` (LEA `215F`, 8-bit) 297-389** |
| US | ALWAYS `10048` 1-33, MORRIGA `519C2` 1-29, ALWAYS `34D10` 1-37, VICTOR `5C6E4` 5-257, ALWAYS `219AE` 113-173, ALWAYS `1B4B2` 149-241, ALWAYS `2D93A` 241-481 |

- The US pose plays **no** sample from Morrigan's region after frame 29 (the
  `519C2` at 1-29 is during the KO).
- The Japanese pose sample's 8,544 bytes at `0x56D60` are **identical** in
  the US sound RAM (`f5c868ca…`), as is the whole `MORRIGA.BIN` region; they
  are `MORRIGA.BIN` offset `0x1BAA0`.

**Session inventory** (1 s states; samples in Morrigan's region after she is
loaded):

| SA (LEA) | Japanese states | US states | Japanese screenshots at those frames |
| --- | ---: | ---: | --- |
| `424E0` (`1FED`), `444D0`, `46064`, `4A1FE`, `4CD56`, `519C2`, `546D4` | 3-21 each | 2-12 each | (shared; not reviewed) |
| `50C2C` (`0D94`) | 3 | **0** | Morrigan grabbing Victor, then Bishamon, at close range |
| `41220` (`12BE`) | 6 | **0** | Morrigan carrying the opponent up into the air |
| `4F10C` (`1B1E`) | 6 | **0** | Morrigan being hit |
| `56D60` (`215F`) | 2 | **0** | win poses (vs. Victor round 3; vs. Bishamon round 3) |

The US session has no Morrigan-region sample the Japanese session lacks.

## Conclusion

- **CONFIRMED (AUD-03):** in the Japanese release the bat-seat win pose plays
  Morrigan sample `0x56D60` (`MORRIGA.BIN` offset `0x1BAA0`); in the US
  release the same pose plays none of her samples, although the sample is on
  the disc and in sound RAM at the same address. Change type: **conditionally
  suppressed** (asset present). D-007.
- **SUPPORTED (AUD-01, AUD-02, and a new hurt voice):** three more Morrigan
  samples play in the Japanese session at a close grab (`50C2C`), an air
  carry (`41220`, matching Vector Drain) and when she is hit (`4F10C`), and
  never in the US session's one-second states. The US throws were not located,
  so a US throw that plays nothing is not yet observed.

## Uncertainty and Alternatives

- The two poses are different matches (Bishamon vs. Victor). The opponent
  does not plausibly decide Morrigan's own pose line, but a matched pair
  (same opponent) would remove the doubt.
- One-second states miss short sounds; "never seen in the US session" is not
  "never played".
- What selects a sample (driver command, sequence number in `MORRIGA1.SEQ`,
  game code in a `PL*` overlay) is **UNKNOWN**; the command-area format is
  not decoded.
- `slots.py`'s release-phase value (3) is a HYPOTHESIS; it only filters.

## Reproduction

```bash
./invenv.sh python research/experiments/EXP-0008/dense.py jp local/aud001/jp-session/rec/states/f00023129.mcs 600 local/aud001/dense-pose-jp
./invenv.sh python research/experiments/EXP-0008/dense.py us local/aud001/us-session/rec/states/f00010960.mcs 600 local/aud001/dense-pose-us
./invenv.sh python research/experiments/EXP-0008/slots.py local/aud001/<r>-session/rec/states/*.mcs
```
