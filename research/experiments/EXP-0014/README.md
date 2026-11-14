# EXP-0014: What Else the Epilogue Flag Controls

Task: DISC-002 (scope of the one-byte patch); AUD-001
Status: DONE
Confidence: CONFIRMED (the flag gates Morrigan's bat-seat line); SUPPORTED
(her other guarded voice calls); UNKNOWN (most other readers)

## Observation

`EXP-0013` (D-013): the US start-up code sets the epilogue flag
(`0x0608089A`) to 2; the Japanese release leaves its flag at 0. The flag is
read not only by the ending but by `MAIN.BIN`, `TITLE.O`, `SOBJ08.O3`, and
the character overlays `PL05`, `PL10` and `PL14`. Before a disc patch clears
it, what each reader does must be known.

## Hypothesis

`PL05` is Morrigan's code, and its flag readers skip voice calls when the
flag is non-zero: the flag is what silences her Japanese-only voices in the
US release (`AUD-01` to `AUD-03`, `AUD-05`).

## Controlled Change

One byte: the flag written to 0 right after loading the US won-KO state
`f00011016` (Morrigan beats Victor). Control: the same state with no write.
No input in either run.

## Prediction

With the flag cleared, Morrigan's bat-seat win line (sample `56D60`, D-007)
plays during her win pose; in the control it does not.

## Inputs and Provenance

- US state `local/aud001/us-session/rec/states/f00011016.mcs` (`EXP-0007`).
- `MORRIGA.BIN` (identical on both discs); the sample parameters of
  `EXP-0009` (offset `0x1BAA0`, 8,544 bytes, 7,795 Hz).
- WRAM-H of the US and Japanese Victor fights (`EXP-0007` state dumps
  `us-f00005273`, `jp-f00005996`).
- Patched Mednafen `7826b9b9…f887`, quiet home.

## Tools and Environment

- [`readers.py`](readers.py): one line per reader of an address (the next N
  instructions), using `EXP-0013/xref.py`.
- `EXP-0010/force.py` (`--wav`), `EXP-0009/wavsearch.py`.

## Procedure

1. **Which character `PL05` is.** Whole-file matches of every `PL*.O*` and
   `SOBJ*` file in WRAM-H of a Morrigan-vs-Victor state, per release.
2. **Readers.** `readers.py` on `PL05.O` (base `0x06001000`), `PL10.O`,
   `PL14.O`, `SOBJ08.O3`, `TITLE.O`, `ENDING.O` (base 0) and `MAIN.BIN`
   (`0x06012000`), US.
3. **Controlled run.**

```bash
S=local/aud001/us-session/rec/states/f00011016.mcs
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/aud001/exp14-control \
  --steps 40 --step-frames 15 --wav
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/aud001/exp14-flag0 \
  --write 0608089A=00 --steps 40 --step-frames 15 --wav
for r in control flag0; do
  ./invenv.sh python research/experiments/EXP-0009/wavsearch.py local/aud001/exp14-$r/sound.wav \
    local/extracted/saturn_jp/MORRIGA.BIN 0x1BAA0 8544 7795 local/aud001/exp14-wav-$r 0.35
done
```

## Actual Result

**1.** In both releases `PL05.O` is loaded whole at `0x06001000` (player 1,
Morrigan) and `PL03.O2` at `0x06009000` (player 2, Victor); `SOBJ03.O3` at
`0x06011000`. `PL05` is Morrigan's code (SUPPORTED: one matchup per
release). Which characters `PL10` and `PL14` are is not tested.

**2. Readers** (US):

| File | Readers | What the flag decides |
| --- | --- | --- |
| `PL05.O` (Morrigan) | 4 (`0x0600248A`, `0x06002A04`, `0x0600433C`, `0x0600627A`) | each: if the flag is 0, call `0x0603A4D6` with a code pair (`0x0134`-`0x0139` with `0x02xx`); otherwise skip the call |
| `PL14.O` | 2 | if 0, call `0x0603A76E` with `0x02B401B4` or `0x02B201B2`; otherwise skip |
| `PL10.O` | 6 | if 0, call `0x06030ABA` or set object fields; purpose UNKNOWN |
| `SOBJ08.O3` | 1 | runs a routine only when the flag is **4** |
| `TITLE.O` | 1 | if non-zero, tests a pad bit (`0x0800`) and may branch away (UNKNOWN) |
| `ENDING.O` | 2 | if 0, sets scroll values (the epilogue path, D-012) |
| `MAIN.BIN` | 20 (besides the start-up write) | mostly picks one of two tables (`0x0605A748`/`0x0605A7B8`, `0x0605AA34`/`0x060668E8`, `0x06066884`/`0x06066864`, ...); two places test for 4; one gates the ST1 loader (D-012). Each table's content is UNKNOWN |

**3. Controlled run.** Bat-seat sample `56D60`: **found once in the
flag-cleared run, at 5.02 s (score 0.73); not found in the control.** Both
runs show the same sequence: "MORRIGAN WINS", then Morrigan seated on her
bat with the bonus tally (frame 305: control `12eba8d0…`, cleared
`a7ea885a…`). The frames also differ in the confetti scatter and in the
colour of the portrait frames (UNKNOWN cause; random or timing, not
tested). WAVs: control `d1ece404…`, cleared `b48e2a84…`.

## Conclusion

**CONFIRMED:** the epilogue flag also silences Morrigan's bat-seat win line
in the US release; clearing it in US RAM makes the US release play the
Japanese line at the same pose (D-014). Her other three flag-guarded calls
have the same shape, so the flag is the likely switch for her throw, Vector
Drain and hurt voices too (SUPPORTED, statically; each needs its move played
with the flag cleared). The flag is a broader export switch than the epilogue:
`PL14`'s sound calls and many `MAIN.BIN` tables depend on it.

## Uncertainty and Alternatives

- Which `PL05` reader played the line, and what the `0x0603A4D6` codes are,
  is not traced.
- Clearing the flag from boot will also change whatever the `MAIN.BIN`
  tables, `PL10`, `PL14` and `TITLE.O` readers select. Some may be wanted
  (Japanese-only content), some may be US conversion choices (for example,
  differences the web research lists for the US release); each needs its own
  comparison before the flag is cleared on disc.
- One state, one matchup, no input. The throw and Vector Drain voices need
  play (or an input-driving tool) with the flag cleared.

## Reproduction

The commands above; outputs stay in the ignored `local/aud001/exp14-*`.
