# EXP-0050: Match the retail text and UI surfaces

Tasks: REF-004, UI-001, COV-001

Status: DONE for the surface comparison. COV-001 stays open in the ledger.

Confidence: CONFIRMED for matched reported surfaces and the new
AUTO GUARD / AUTOMATIC wording comparison.

## Observation, hypothesis and prediction

The two retail discs already had independently captured boots, menus,
voices and endings. A matched Arcade victory, loss, continue and cast
roll should expose the text regions under the same game actions and
identify differences that aren't visible at the title.

## Inputs

- JP T-1202G, 1M V1.000, Track 1
  `73cc150ba563e39a420ac57589cc318cb01eec0365fe405aa386249019384c39`.
- US T-1208H V1.001, Track 1
  `d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da`.
- Existing stock Mednafen 1.32.1 captures (EXP-0001, EXP-0002) and
  Appendix inputs (EXP-0042). New Arcade runs use Mednafen 1.32.1 agent
  build with patches 0001/0002, quiet isolated homes, no RAM cart, and
  Python 3.13.13.

## Controlled procedure

The source discs are unchanged. Cold-boot both, select the same player
slot, default speed and NORMAL, lose the matchup and continue, then win
the rematch to reach the second stage. Set the loser vitality and timer
to end rounds reproducibly. Each replay uses its own disc's checkpoint.
For the ending, force the stage byte at the won KO as in EXP-0019 and
record the first main-ending page, epilogue and two cast names.

```sh
US="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
JP="local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
./invenv.sh python research/experiments/EXP-0049/retail_run.py us "$US" local/exp0049/live-us
./invenv.sh python research/experiments/EXP-0049/retail_run.py jp "$JP" local/exp0049/live-jp
./invenv.sh python research/experiments/EXP-0049/retail_endings.py us "$US" \
  local/exp0049/live-us/before-last-round.mc0 local/exp0049/end-us
./invenv.sh python research/experiments/EXP-0049/retail_endings.py jp "$JP" \
  local/exp0049/live-jp/before-last-round.mc0 local/exp0049/end-jp
```

The first sampled JP main-ending frame was before the text had drawn.
The `--main-only` capture in `main-us` and `main-jp` matches the actual
first page read, via the corresponding main CPU breakpoints.

## Actual result

- The player-selection menu uses the same NORMAL and TURBO speed labels.
  The second MODE SELECT choice reads AUTO GUARD on JP and AUTOMATIC on US.
  Both displays retain NORMAL as the first choice. The distinct menu art
  was already mapped to the region flag in D-015.
- The matched fights are Lei-Lei / Hsien-Ko vs. Victor, and then
  vs. Bishamon. Both continue screens use an English countdown with the
  reference's quote language. Continued play returns to the first fight.
- The same first ending scene draws different JP and US dialogue in its
  respective fonts. The Japanese epilogue over scrolling art appears
  only on JP. Both cast rolls start with DEMITRI. The next name is
  GALLON on JP and JON TALBAIN on US.
- EXP-0030's original pages establish the script renames for supporting
  characters. Donovan's companion is Anita on JP and Amanda on US.
  Lei-Lei's sister is Lin-Lin on JP and Mei-Ling on US.
- The surface record and the remaining research exceptions are in
  [text surfaces](../../../docs/text_surfaces.md) and
  [coverage exceptions](../../../docs/coverage_exceptions.md).

[Capture metadata](surface_samples.json) gives the local path, length
and SHA-256 for each selected frame. Only metadata is checked in.
Gameplay snapshots at different attack frames provide no controlled
comparison of hit effects. The results apply to the two tested retail
images and the paths recorded here.
