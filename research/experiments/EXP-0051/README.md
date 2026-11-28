# EXP-0051: Cart-backed FULL on the combined candidate

Task: ANI-003
Status: DONE
Confidence: CONFIRMED in Mednafen; real-hardware behavior is assumed by user decision and was not independently verified.

## Observation

EXP-0043 confirmed the 4 MiB cart path in Mednafen on `build/us_edition`, but
the combined candidate adds later features. The exact candidate needed a
cart-backed Arcade run before ANI-003 could close on emulator evidence.

## Hypothesis

The combined candidate cold-boots through its title code, saves `FULL`, and
allocates the second fighter's full set in 4 MiB cart RAM during Arcade play.

## Controlled Change

Use the combined candidate and `extram4` for this run. The driver cold-boots
the game, sets and saves `FULL` through OPTION MODE / APPENDIX, and plays
Arcade. Mednafen audio volume is zero.

## Prediction

At the first fight, ANIMATION remains `1` (`FULL`), both full fighter set
slots are loaded, and pool 2's bounds point into the cart address range
starting at `0x22400000`. Those values remain through both rounds.

## Inputs and Provenance

- Combined candidate CUE:
  `build/next_release_candidate/Night Warriors - Darkstalkers' Revenge (USA).cue`
  SHA-256 `203a53dff34c4adea6a709c822fa485d4325a4bd63aa6b0ea03f1ed7a141fbb2`
- Track 1 SHA-256:
  `d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d`
- Track 2 SHA-256:
  `271844bfb734ab4fd322bc753bfad63b8a6e31d7d24272d52b5d10989065cdbb`
- Prior cart matrix and coverage: `research/experiments/EXP-0043/README.md`.

## Tools and Environment

- Python 3.13.13 via `./invenv.sh`.
- Mednafen 1.32.1 agent build, patches 0001 and 0002, binary SHA-256
  `7040f6fece428a8a3a8d1e2f1f48e992ec15f2f9dd6267354e30fab377dc4cdd`;
  `ss.cart extram4`.
- Repository revision: `f65ecc4`.
- Driver: `research/experiments/EXP-0043/play.py`, which drives the normal
  OPTION / APPENDIX path and records WRAM readings and screenshots.

## Procedure

From the repository root:

```bash
./invenv.sh python research/experiments/EXP-0043/play.py \
  "build/next_release_candidate/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  local/exp0050/ani003-final-candidate-check arcade --stages 1 --cart extram4
```

The ignored output is under `local/exp0050/ani003-final-candidate-check/`.
The driver's fight and round screenshots and logs are kept locally. Key
outputs:

| File | Bytes | SHA-256 |
| --- | ---: | --- |
| `reads.txt` | 982 | `05515fd56d39372bd2107370e6e3c753641d67f109c8ed6ca88446ee3f818fdc` |
| `stage1-start.png` | 29,140 | `2f0283faf07e5d86a68115721c834f0eccdffd5fe22a0e0f04512da9843fc2b1` |
| `stage1-r1.png` | 29,608 | `8e7ed52c9b681eacb6c034ae3f248277a3d2ebc7e8a6034e1ce628abbd163f40` |
| `events.log` | 20,721 | `1ebbbc9cf0e0f968df033565ed7139da28f58f2e5d1b6de19f0bec1178e0b3a1` |

## Actual Result

At frame 6294, after OPTION MODE saved `FULL`, `reads.txt` recorded
`anim=01`, loaded-set slots `0c02` and pool 2
`0x22400000`-`0x22708cdc`. The same animation setting, set slots and cart
pool bounds were recorded after each of the two rounds. The game then reached
the next Arcade opponent transition and freed both slots. The driver completed
with exit code 0.

## Conclusion

The exact combined candidate takes the 4 MiB cart-backed FULL path in
Mednafen during Arcade play. Combined with EXP-0043's Mednafen matrix, this
meets the emulator-side evidence requested for ANI-003.

On 2026-11-27, the user said: “Let's just assume it works the same on hardware
as on the emulator and call it closed if you've verified it, emulator-side.”
ANI-003 is closed on that basis. This is an explicit acceptance assumption;
it does not establish real-Saturn timing, stability, or sprite behavior.

## Uncertainty and Alternatives

Mednafen is the only independently verified environment for this experiment.
Real-hardware behavior remains UNKNOWN and is accepted by the user's stated
assumption for task closure.

## Reproduction

Run the command in Procedure using the recorded candidate hashes. Expected
frame-6294 values are `anim=01`, slots `0c02`, and pool 2 beginning at
`0x22400000`; the cart-backed upper allocation bound should be below the
baseline `0x22800000` after the fighter loads.
