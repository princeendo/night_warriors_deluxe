# EXP-0018: The Japanese Epilogue From a Patched US Image

Task: DISC-002
Status: IN_PROGRESS (version 2 built and rehearsed; the cold-boot run of
version 2 needs a won KO played on it)
Confidence: SUPPORTED (rehearsal); the M2 criterion is not yet met

## Observation

D-012: in US RAM, clearing the region flag, pointing the ST1 name array's US
entry at `ST1JPN.BIN` and switching the language to Japanese after the main
ending shows the Japanese epilogue after the English ending. `EXP-0015` to
`EXP-0017`: the flag also selects names, menu graphics and US-only
behaviour, so it must stay 2 on disc; the language byte also selects the
win-quote and main-ending text.

## Hypothesis

The Japanese epilogue can be shown with the flag at 2 and the language at 1
by changing only the epilogue's own paths:

1. **Why the text was missing with language 1** (found here): every text
   file starts with a list of (slot, offset) pairs, and the loader
   (`0x06013D94`) stores each pointer in the slot table at `0x06091758` that
   the **file** names. `ST1JPN.BIN` names slot `0x1BA` (`0x06091E40`, the JP
   slot); `ST1USA.BIN` names `0x1BC` (`0x06091E48`). The epilogue text
   routine (`0x06037960`, which also draws the win quotes) picks the slot by
   the language byte (table `0x0605B814`), so in English mode it reads
   `0x06091E48`. On a win-quote screen that slot holds the win-quote text; it
   is free at the ending, where `ST1USA.BIN` would fill it.
2. **The ending's own flag tests** (`ENDING.O`, loaded at `0x06001000`):
   `0x0600CFC6` runs the card sequence before the text only when the flag is
   0, and `0x0600D04E` sets the epilogue's length: `0x564` frames (flag 0)
   or `0x384` (US).

## Controlled Change

Byte changes on a copy of the US image, nothing else
([`build_epilogue.py`](build_epilogue.py), every original byte checked
before it is changed). **Version 2** (current; version 1 failed, see below):

| File | Offset | Original | Modified | Address | Purpose |
| --- | --- | --- | --- | --- | --- |
| `MAIN.BIN` | `0x29902` | `D338` | `D438` | `0x0603B902` | load the literal at `0x0603B9E4` into `r4` instead of `r3` |
| `MAIN.BIN` | `0x29904` | `6030` | `0009` (`nop`) | `0x0603B904` | the flag read, no longer needed |
| `MAIN.BIN` | `0x29908` | `8B02` (`bf`) | `0009` | `0x0603B908` | the ending loads an `ST1` file although the flag is 2 |
| `MAIN.BIN` | `0x299E4` | `0608089A` | `0605B850` | `0x0603B9E4` | literal (used only at `0x0603B902`): flag address → the `ST1JPN.BIN` name |
| `MAIN.BIN` | `0x299E8` | `0603790E` | `06013DF8` | `0x0603B9E8` | literal (used only at `0x0603B90A`): the language-indexed `ST1` loader → the file loader it ends in |
| `ST1JPN.BIN` | `0x3` | `BA` | `BC` | (file header) | the file's text goes to the US slot, which the English-mode renderer reads |
| `ENDING.O` | `0xBFCC` | `8B2F` (`bf`) | `0009` | `0x0600CFCC` | the Japanese card sequence before the text |
| `ENDING.O` | `0xC0D0` | `8B02` (`bf`) | `0009` | `0x0600D0D0` | the Japanese epilogue length (`0x564` frames) |

So the ending's own call loads `ST1JPN.BIN` by name; the shared `ST1` name
array (`0x0606BEB8`, indexed by the language byte) is unchanged. The region
flag (2), the language byte (1) and every other file are unchanged.
`ST1JPN.BIN` is loaded by the US release only on this path (language 1
always selects `ST1USA.BIN` through the array), so its header change affects
only this path.

**Version 1 (failed)** changed the array's US entry instead (`MAIN.BIN`
`0x59EBF` `5C` → `50`, `0x0606BEBF`), with the gate, the header and the two
`ENDING.O` changes as above. See "Cold boot of version 1".

## Prediction

From a cold boot of the patched image and a won KO as Morrigan, forcing the
ending with the stage byte alone (D-009) shows the English main ending,
then the Japanese epilogue over her art, then the credits, with US names.
The unpatched image under the same forcing shows the art without text.

## Inputs and Provenance

- Source: the untouched US image, `local/disc_images/nw_saturn_us/` (Track 1
  `d0960087…70da`; all three components are in
  `references/saturn_us/README.md`, checked by `patch_image`).
- Output: `build/us_enhanced_epilogue/` (ignored): Track 1
  `1e050815ec0789dd798c8f1ae5d3c9c9710a3c60827f9026594e5b681f689237`;
  Track 2 and the cue sheet copied unchanged (`271844bf…`, `203a53df…`);
  `build_manifest.json` beside them.
- Patched Mednafen `7826b9b9…f887`.

## Procedure and Result So Far

1. **Build:** `./invenv.sh python research/experiments/EXP-0018/build_epilogue.py`.
   Five sectors rewritten (LSNs listed in `build_manifest.json`).
2. **Check the image:** extracting every file from both tracks and comparing:
   only the eight bytes above differ (`MAIN.BIN` 3, `ENDING.O` 4,
   `ST1JPN.BIN` 1). `python -m tools.disc.sector` on the new Track 1:
   209,924 sectors, 0 invalid.
3. **Rehearsal (not the M2 test).** The existing won-KO state comes from the
   unpatched image, so its RAM already holds the unpatched `MAIN.BIN`. Loaded
   into the patched image, with the stage byte and the two `MAIN.BIN` changes
   written to RAM (`ENDING.O` and `ST1JPN.BIN` then load from the patched
   disc):

```bash
C="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/aud001/us-session/rec/states/f00011016.mcs local/disc001/enh-rehearsal --image "$C" \
  --write 0608092B=09 --write 0603B908=0009 --write 0606BEBC=0605B850 --steps 300
```

   Agent-reviewed screenshots: the English main ending (Morrigan, Lucien),
   the emblem card ("1ST A", **no** stray glyph strip), the Japanese epilogue
   paragraph appearing line by line, then scrolling with Morrigan's art,
   then NOW LOADING. The language byte stayed 1 throughout.

4. **Cold boot of version 1** (Track 1 `1e050815…9237`; user request "Yes,
   start it"). The user played Morrigan vs. Sasquatch from power-on and won
   2-0 ([`session.sh`](session.sh); 173 states, 342 screenshots in the
   ignored `local/disc002/us-enhanced-session/rec`). **The win-quote screen
   showed Morrigan's Japanese win quote** (`f00010133.png`, `f1c9c47c…`),
   where the unpatched US release shows English. Not a pass.
5. **Why.** `MAIN.BIN` calls the `ST1` loader `0x0603790E` from three places:
   `0x06014208` and `0x0601E16C` with no flag test, and `0x0603B90A` (the
   ending, behind the flag). The loader takes the file name from the array
   `0x0606BEB8` by the language byte (entries `0x0605B850` `ST1JPN.BIN`,
   `0x0605B85C` `ST1USA.BIN`, `0x0605B868` `ST1HIS.BIN`) and jumps to the file
   loader `0x06013DF8` (`r4` = name). Version 1's array change therefore also
   made the win screens load `ST1JPN.BIN`. So `ST1USA.BIN` is the US
   win-quote file (SUPPORTED: the one-entry change turned the win quote
   Japanese; restoring it in version 2 turns it English), not only the
   placeholder that D-012 saw at the ending. Each literal version 2 changes is
   loaded by one instruction only (a scan of every `mov.l @(disp,PC)` in
   `MAIN.BIN`).
6. **Version 2 build:** Track 1
   `93ca264c25b0a21c0264a61bf8c4301ca123d2cb4062c9cd316b8ba88c4139ab`
   (Track 2 and the cue unchanged). Every file of the track compared with the
   US original: 415 files, only the 15 bytes above differ (`MAIN.BIN` 10,
   `ENDING.O` 4, `ST1JPN.BIN` 1); 209,924 sectors, 0 invalid. Version 1 kept
   in the ignored `build/us_enhanced_epilogue_v1/`.
7. **Version 2 rehearsal** from the version-1 session's bonus-screen state
   `f00009647` (before any `ST1` load), with version 2's `MAIN.BIN` code put
   in RAM (the state holds version 1's):

```bash
C="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
S=local/disc002/us-enhanced-session/rec/states/f00009647.mcs
FIX=(--write 0606BEBC=0605B85C --write 0603B902=D4380009 --write 0603B9E4=0605B85006013DF8)
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/disc002/v2-winquote \
  --image "$C" "${FIX[@]}" --steps 40 --step-frames 15
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/disc002/v2-ending \
  --image "$C" "${FIX[@]}" --write 0608092B=09 --steps 300
```

   Agent-reviewed screenshots. Win screen: "My victories, like my beauty are
   eternal!" in English (`r000305`, `e792e5e7…`). Forced ending: the English
   main ending ("Welcome back mistress.", Lucien), the emblem card, the
   Japanese epilogue (`r006597`, `c52227c3…`), Morrigan's art, then CAST
   (`r008780`). (A first attempt at the win-screen run left no screenshots or
   `run.json`, and its log ends in a SIGTERM; rerun unchanged, it worked.
   Cause not found.)
8. **To do (M2):** a cold boot of version 2, one match won as Morrigan by
   the user (`session.sh local/disc002/us-enhanced-session-v2`), with the
   win quote checked; then the ending forced with the
   stage byte only from the post-KO state, and the same forcing on the
   unpatched image as control; the cast roll checked for US names.

## A Tooling Fault Found Here

Mednafen saves command-line settings into its config file on exit. The
`EXP-0016` runs with `--setting ss.input.port1=none` left port 1 empty in the
quiet home, so later runs had no pad: the first rehearsal paused (the US
auto-pause, D-016), and the `EXP-0016` Japanese "pad" control in fact had port
1 empty (corrected there). `force.py` now restores the config after each run.

## Uncertainty and Alternatives

- Morrigan only; the other 13 epilogues are expected to work the same way
  (one `ST1JPN.BIN`), not tested.
- The JP-only punctuation spacing (`0x06037AE4`, flag-gated) stays off, so a
  few Japanese punctuation marks may sit 3-8 pixels wider than in the
  Japanese release (not compared).
- `MAIN.BIN`'s per-character ending script tables (`0x060367A4`, flag-gated)
  stay US; the rehearsal's main ending matched the US one.
