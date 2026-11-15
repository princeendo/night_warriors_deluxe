# EXP-0022: Latin Text in the Epilogue Renderer (English Mode)

Task: END-002 (acceptance criterion 1, the format)
Status: DONE
Confidence: CONFIRMED

## Observation

Static, on the US data track (`local/extracted/saturn_us/`):

- `ST1JPN.BIN` epilogue lines are records of x, y, `0001`, then 16-bit codes,
  ended by `FFFF` (next line) or `0000` (end of block). Morrigan's paragraph
  starts at `0xE1A` (x `002C`, y `0020`; 12 lines, y stepping `0x10`).
- `ST1USA.BIN` (slot `0x1BC`) holds the US win quotes in the same record
  shape, in a Latin set: capitals and punctuation = ASCII + `0x80`
  (`A` = `00C1`), lowercase `a`-`z` = `0201`-`021A`, space = `0020`. Their
  letter frequencies follow English (`0205` e, `020F` o, `0214` t, …).
- `MOJI.TBL` (1,026 codes) has the lowercase codes but **none** of
  `00C1`-`00DA` and neither `00AC` nor `00AE`; it does hold a second Latin
  set drawn like the kana (`08E1`-`090A` capitals, `0921`-`094A` lowercase,
  `02C0`-`02C9` digits). So English mode must map the win-quote codes some
  other way (D-012: the language byte also picks how text is drawn).

## Hypothesis

In English mode the epilogue renderer draws the win-quote Latin codes, as
the win-quote screen does.

## Controlled Change

On the DISC-002 version 2 image (`EXP-0018` `PATCHES`), the character codes
of the first three lines of Morrigan's record in `ST1JPN.BIN` (`0xE20`,
`0xE5C`, `0xE98`; 26, 26 and 25 codes) replaced in place by PSP *Chronicle*
English (`EXP-0020`, `Hmovie04_2`), re-wrapped and padded with spaces. Line
headers, lengths and everything else unchanged.

## Prediction

The three lines show as English over Morrigan's art; the other nine lines
stay Japanese. If the renderer only knows `MOJI.TBL`, they show blank or as
wrong glyphs.

## Procedure

```bash
./invenv.sh python research/experiments/EXP-0022/build_en_test.py   # build/us_en_test
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs local/end002/en-test \
  --image "build/us_en_test/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  --write 0608092B=09 --steps 240
```

## Actual Result

First run (`local/end002/en-test`, Track 1 `91168eda…`): the three lines
show in English, in the blue-green Latin font of the US win quotes, above
the nine untouched Japanese lines (`r006540` `a0e4cd92…`, text on black;
`r006845` `39de664c…`, over the art). Two marks were wrong: every comma
showed as a period and every period as a comma. In `ST1USA.BIN`, `00AE`
stands before " but" and `00AC` ends sentences, so **comma = `00AE`,
period = `00AC`**, not ASCII + `0x80`. The apostrophe shows as a raised
mark, the same shape the PSP shows. A 24-character line reaches about
x = 312 of 352: an advance of about 12 pixels, so about 26 characters fit
from x = `0x2C`.

The script was corrected (`SWAPPED`) and rerun (`local/end002/en-test2`,
Track 1 `32ecfc22…795d`): "Fatigued from battle," / "Ma'am, I am afraid
the" / "master has... passed on." with the right comma and periods
(`r006540` `627808fc…`; `r006845` `fa3d53a1…`).

## Conclusion

**CONFIRMED:** in English mode the epilogue renderer draws the Latin codes
of `ST1USA.BIN` (capitals and most punctuation ASCII + `0x80`, lowercase
`0201`-`021A`, space `0020`, comma `00AE`, period `00AC`) in the US
win-quote font, at about 12 pixels per character, and mixes them freely with
`MOJI` codes in one paragraph (D-021). An English epilogue therefore needs
no new font or renderer, only records in this encoding.

## Uncertainty and Alternatives

- How the game finds a character's record is open: the table at `0x0C`
  holds offsets (Morrigan's entry, `0xDFE`, lands 13 codes before her first
  line, after a `0000`), and `ST1USA.BIN`'s epilogue entries point at
  placeholder records. A read trace is the next step.
- Line limits: about 26 characters at x = `0x2C`; how many lines fit, and
  whether y may step less than 16 pixels, is untested. The PSP lines run to
  32 characters, so every paragraph must be re-wrapped (allowed), and some
  may need more lines than the Japanese.
- Digits and other marks in this set (`&`, `0`-`9`) were not drawn here.
