# EXP-0007: Recorded Morrigan Play Sessions in Both Releases

Task: AUD-001
Status: DONE (capture only; the comparison is the next experiment)
Confidence: SUPPORTED (what was seen); UNKNOWN (what was heard)

## Observation

`AUD-01` to `AUD-03` (`docs/difference_register.md`) are a web report, from
memory, of Japanese-only Morrigan voices: normal throw, command throw (Vector
Drain), and a spoken line in the win pose where she sits on bats. Every sound
file and Morrigan's own files are byte-identical on both discs
(`SESSION-0002`). No checkpoint near any of these events existed.

## Hypothesis

A recorded session per release, with the user playing Morrigan, yields
states and screenshots near each event, from which the events can be found
and later replayed without input.

## Controlled Change

None to the games. The patched Mednafen (D-005) ran in the interactive home
(sound on) with `-soundrecord`, and `tools/mednafen/session_recorder.py`
saved a state every second (all kept) and a screenshot every half second.
The user played; no keys were sent by the agent.

## Inputs and Provenance

Japanese 1M and US images; agent binary `7826b9b9…f887`; interactive home
(`cb1c2d3b…a1e9`); [`session.sh`](session.sh) (Japanese, then US when the
first window closes). User requests: "Morrigan voices first"; the inputs for
the command throw were looked up for the user (StrategyWiki, Night Warriors
moves: half-circle back + medium or heavy punch, close).

## Procedure

```bash
research/experiments/EXP-0007/session.sh
```

The user played an arcade game as Morrigan in each release, then closed the
window. The user's report (2026-11-14, verbatim): "My controller became
disconnected toward the end. Sorry. I also noticed that Morrigan seemed to
have some more dialogue in the JP version."

## Actual Result

| | Japanese (02:00:08-02:07:30) | US (02:07:30-02:14:45) |
| --- | --- | --- |
| Sound | `sound.wav`, 48 kHz stereo 16-bit, 404.2 s, `fa659bc4…` | 396.6 s, `62f34275…` |
| States | 417 (frames 7-24,168) | 411 (frames 7-23,718) |
| Screenshots | 828 | 811 |
| Boot log | `T-1202G`, backup cart | `T-1208H`, backup cart |

All in the ignored `local/aud001/<r>-session/` (1.1 GB each). The agent
reviewed overview sheets of every fourth screenshot and the frames around
each win.

**What was played** (frame numbers approximate, from 2 s sampling):

- Japanese: vs. Victor: round 1 lost (~7,850), rounds 2 and 3 won (~10,610,
  ~11,800), a win-quote screen (Morrigan portrait, two lines of Japanese);
  vs. Bishamon: round 1 lost, rounds 2 (~19,670) and 3 (~23,270) won, a
  win-quote screen.
- US: vs. Victor: round 1 won (~4,920), round 2 lost, round 3 won
  (~11,090), a win-quote screen in English; vs. Bishamon: round 1 won
  (~17,970), round 2 lost, round 3 unfinished (the controller disconnected).
- Pauses in both (the `PAUSE` screen).

**Win poses seen** (agent-reviewed frames):

| Release | Win | Pose |
| --- | --- | --- |
| Japanese | vs. Victor, round 2 | standing, lightning behind |
| Japanese | vs. Bishamon, round 2 | standing, bats flying |
| Japanese | vs. Bishamon, round 3 (~23,300-23,440) | **sitting cross-legged on bats** |
| US | vs. Victor, round 1 | standing |
| US | vs. Victor, round 3 (~11,130-11,300) | **sitting, on the left** |
| US | vs. Bishamon, round 1 | standing, bats flying |

So the bat-seat pose occurs in **both** releases (`ANI`-type absence ruled
out for this pose); whether a spoken line accompanies it, in either, is not
yet measured.

States bracketing the bat-seat poses: Japanese `f00023129`-`f00023474` (one
per second), US `f00010960`-`f00011365`.

Throw events could not be located from 2 s sampling; they need the
half-second screenshots or the sound logging below.

**Side observation (static).** `SDDRVS.TSK` begins with
`Ver1.33b95/08/31SATURN(S)`: Sega's standard library sound driver.
`MORRIGA1.SEQ` (986 bytes, identical on both discs) begins with `0x0017`
(23) and a table of offsets: HYPOTHESIS, Morrigan's sequence bank of 23
sound sequences.

## Conclusion

The capture worked: both releases have states one second apart across two
matches each, with a bat-seat win pose captured in each. The user heard more
Morrigan dialogue in the Japanese release; which events, and why, is
**UNKNOWN**.

## Uncertainty and Alternatives

- The two bat-seat cases are on different stages with different music, so a
  direct audio comparison would be weak; replay with sound-command logging
  is needed.
- The user's "more dialogue" may be voice or the win-quote text.

## Next Experiment

Replay each release's state from about one second before the bat-seat pose
(and, once found, before each throw) with the agent, logging writes to the
sound driver's command area in sound RAM (`0x25A00000`-based; the standard
driver's host command area is a HYPOTHESIS to locate first), and record the
sound to WAV. Compare the sequence numbers each release requests at the same
event.
