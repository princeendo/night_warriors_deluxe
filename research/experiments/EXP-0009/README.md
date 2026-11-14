# EXP-0009: Find Morrigan's Samples in the Session Recordings

Task: AUD-001
Status: DONE
Confidence: CONFIRMED (throw voice); SUPPORTED (Vector Drain and hurt voices)

## Observation

`EXP-0008` found four Morrigan samples (`50C2C` throw, `41220` air carry,
`4F10C` hurt, `56D60` bat-seat line) in the Japanese session's one-second
states and never in the US session's. One-second states can miss a sound of
under half a second, and the US throws were not located.

## First Attempt: Live Slot Logging (stopped)

`live.py` and `session.sh` (this folder) logged the SCSP slots while the user
played, by saving a state every 4 frames. The user (2026-11-14): "I already
did this. Why are we doing it again?" and then "It's going to be hard to do
this. The game is very obviously stuttering from what you're doing." Saving a
state that often stalls emulation visibly. The session was stopped after
1,041 rows of the Japanese session (no throw played); its data is not used.
Lesson: do not save states several times a second during user play.

## Hypothesis

Each sample's waveform, played at its slot's pitch, can be found by matched
filtering in the continuous `EXP-0007` recordings (`sound.wav`); the
Japanese-only samples occur in the Japanese recording and nowhere in the US
one, while a sample both releases play is found in both.

## Controlled Change

None to the games. Offline analysis of the `EXP-0007` WAV files (Mednafen
`-soundrecord`, 48 kHz stereo) and screenshots.

## Inputs and Provenance

- `local/aud001/<r>-session/sound.wav` (`EXP-0007`: Japanese `fa659bc4…`,
  US `62f34275…`).
- `MORRIGA.BIN` (identical on both discs); each sample is at offset
  `SA - 0x3B2C0` (D-007's load address), `LEA + 1` bytes of signed 8-bit PCM.
- Pitch from the slot registers in `EXP-0007` Japanese states, register 8
  (OCT 14-11, FNS 9-0; rate = 44,100 x 2^OCT x (1024 + FNS) / 1024):

| SA | Japanese state(s) | reg8 | Rate | Length |
| --- | --- | --- | ---: | ---: |
| `50C2C` | 4436, 4549, 18663 | `70C7` | 13,168 Hz | 3,477 (0.26 s) |
| `41220` | 11491, 21564 | `69CF` | 8,005 Hz | 4,799 (0.60 s) |
| `4F10C` | 16603, 22491 | `6AA2` | 9,141 Hz | 6,943 (0.76 s) |
| `56D60` | 13315, 23474 | `69A8` | 7,795 Hz | 8,544 (1.10 s) |
| `424E0` (control, played in both releases) | 7671 | `699B` | 7,725 Hz | 8,174 (1.06 s) |

The same register value appears in every state for a sample.

## Tools and Environment

[`wavsearch.py`](wavsearch.py): builds the sample's waveform, resamples it
and the recording to 16 kHz mono with ffmpeg 9.0.1, cross-correlates with
`afir` (reversed sample as impulse response, normalization off), divides by
the sample's norm and the recording's norm over the same window, and reports
peaks. No new dependency (no numerical library is installed; adding one
would need the user's approval).

## Procedure

```bash
./invenv.sh python research/experiments/EXP-0009/wavsearch.py \
  local/aud001/<r>-session/sound.wav local/extracted/saturn_jp/MORRIGA.BIN \
  <SA-0x3B2C0> <LEA+1> <rate> local/aud001/wav-<r>/<SA> 0.35
```

for each release and sample. Then the agent reviewed half-second US
screenshots of the Victor match for Morrigan's throws.

## Actual Result

| Sample | Japanese recording (start s, score) | US recording |
| --- | --- | --- |
| `50C2C` throw | 71.39 (0.54), 73.78 (0.60), 76.02 (0.45), 142.32 (0.49), 311.41 (0.60) | **none** |
| `41220` air carry | 191.36 (0.85), 360.37 (0.82) | **none** |
| `4F10C` hurt | 375.33 (0.69) | **none** |
| `56D60` bat-seat line | 221.83 (0.75), 391.62 (0.83) | **none** |
| `424E0` control | 128.19 (0.73), 290.51 (0.73) | 136.22 (0.73), 357.09 (0.70) |

- **Validation:** the Japanese `50C2C` hits at 73.78, 76.02 and 311.41 s
  match the states that showed it playing (frames 4436, 4549, 18663 =
  74.0, 75.9, 311.4 s at 59.94 frames/s); 71.39 and 142.32 s are throws the
  one-second states missed. The control sample scores about the same in both
  recordings, so the search works on US audio.
- **A US throw with no voice:** US screenshots at frames 4,263-4,313 show
  Morrigan grabbing Victor at close range (her wings wrapped around him, frame
  4,293) and tossing him overhead (frame 4,313), as the Japanese throws look
  at frames 4,368-4,425. No `50C2C` occurs anywhere in the US recording.
- A US Vector Drain was not identified with confidence in the screenshots.
- The user says the throws were done in both sessions ("I already did this").
- Threshold 0.35 is below every true hit found (lowest 0.45); nothing in the
  US recording reached it for the four samples.

## Conclusion

- **CONFIRMED (AUD-01):** Morrigan's normal-throw voice (sample `50C2C`,
  `MORRIGA.BIN` offset `0x1596C`) plays at her throws in the Japanese release
  and at none in the US release, including an observed US throw; the sample
  is on both discs (D-008).
- **SUPPORTED (AUD-02, AUD-05):** the Vector Drain (`41220`) and hurt
  (`4F10C`) voices occur in the Japanese recording and nowhere in the US one;
  a matching US event was not observed for Vector Drain, and the hurt
  voice's trigger is not identified.
- `AUD-03` (D-007) is confirmed again by the whole recordings.

## Uncertainty and Alternatives

- Matched filtering can miss a sample masked by louder sounds (the Japanese
  hurt voice was found once in the audio but in two separate states).
  Absence in the US recording is absence of a match, which together with the
  control and the observed throw makes suppression the only explanation in
  play for the throw voice.
- What selects each sample remains **UNKNOWN**.

## Reproduction

Run the procedure above; the recordings stay in the ignored
`local/aud001/`.
