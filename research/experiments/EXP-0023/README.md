# EXP-0023: How an Epilogue Record Is Found, and How Much Text Fits

Task: END-002 (criterion 1, the format; first try at criterion 2)
Status: DONE
Confidence: CONFIRMED (lookup, reads, 238-glyph cut); SUPPORTED (the cause
of the cut)

## Observation

`EXP-0022`: the epilogue renderer draws Latin codes, but the table at
`ST1JPN.BIN` `0x0C` did not seem to point at line starts, and Morrigan's
own record (268 words) is too small for her English paragraph.

## Part 1: the lookup (read trace)

`force.py` gained `--log-read RANGE` (breakpoint kind `read`, log mode).
Version 2 image, Morrigan's ending forced as in `EXP-0018` step 9:

```bash
F=research/experiments/EXP-0010/force.py
S=local/disc002/us-enhanced-session-v2/rec/states/f00007741.mcs
C="build/us_enhanced_epilogue/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python $F us $S local/end002/readlog --image "$C" --write 0608092B=09 \
  --log-read 060CB414-060CB45B --log-read 060CC200-060CC22F --steps 230
./invenv.sh python $F us $S local/end002/readlog-all --image "$C" --write 0608092B=09 \
  --log-read 060CB408-060D2693 --steps 300
```

`ST1JPN.BIN` is loaded at `0x060CB408`. At frame 6,141 (the text intro),
`0x060379BC` reads one table word, `0x060CB424` (file `0x1C`), with `R0` = 4.
The reader (`MAIN.BIN`, `0x060379B2`-`0x060379C2`) takes the table base for
the language (`0x0605B814` + language × 8), adds index × 4, and adds the
word **to the entry's own address**: `0x060CB424` + `0xDFE` = `0x060CC222`
(file `0xE1A`), Morrigan's first line header. Entries are self-relative;
the index is the roster number − 1. The whole-file read log shows the
ending reads only the header (frame 308, the loader), that one entry, and
the record's lines; the other hits are before the load, when the area
holds other data.

## Part 2: Morrigan's whole English paragraph

`research/experiments/EXP-0023/build_en_epilogue.py 5`: the PSP paragraph
(from the local transcript; game text is never committed) re-wrapped to 26
characters (16 lines), encoded as in D-021, written at line spacing 13 from
y = `0x10` as a new record at `ST1JPN.BIN` `0x20F0` (the first record after
the 14 epilogues, never read by this build's ending), and table entry 4 set
to point at it. Track 1 `b6ab544f…fe83c`.

Forced (`local/end002/en-morrigan`): the English text rises on black and
then sits over Morrigan's art, but it stops after "finished..." and "Butle"
(`r007021` `98a21a79…`, on black; `r007781` `fc33a468…`, over the art). The
cut falls at the **238th** non-space character. The longest Japanese
epilogue (Rikuo's) has exactly 238 non-space codes.

## Part 3: why 238

The per-glyph code (`0x06037B08`-`0x06037B46`) appends an 8-byte entry (x,
y, glyph, attribute) to a list starting at `0x060839D4` (literal at
`0x06037A98`) for each non-space code, with no length check; 238 entries end
at `0x06084144`. A write log of `0x06084138`-`0x060841FF`
(`local/end002/listwrite`) shows the text builder writing 25 entries there
at frame 6,140, then other routines (`0x0601BC3E`-`0x0601BC5A`,
`0x0601BD44`-…, `0x0601B75A`-…) writing that area every frame up to 6,992;
`0x0601BC3E` writes 32-byte records with `R11` in VDP1 VRAM, so it is a VDP1
command buffer. **SUPPORTED:** the glyph list has room for 238 entries
before a buffer that is rebuilt every frame, so later glyphs are lost.

## Size of the problem

Every PSP paragraph (after the logged edits) is longer than 238 glyphs:

| Roster | Glyphs | Lines at 26 | Over |
| --- | --- | --- | --- |
| 1 Demitri | 329 | 17 | 91 |
| 2 Jon Talbain | 337 | 17 | 99 |
| 3 Victor | 323 | 16 | 85 |
| 4 Lord Raptor | 309 | 16 | 71 |
| 5 Morrigan | 278 | 16 | 40 |
| 6 Anakaris | 345 | 18 | 107 |
| 7 Felicia | 315 | 16 | 77 |
| 8 Bishamon | 297 | 15 | 59 |
| 9 Rikuo | 327 | 17 | 89 |
| 10 Sasquatch | 310 | 16 | 72 |
| 11 Huitzil | 307 | 16 | 69 |
| 12 Pyron | 263 | 14 | 25 |
| 13 Hsien-Ko | 335 | 17 | 97 |
| 14 Donovan | 282 | 14 | 44 |

## Conclusion

**CONFIRMED:** an epilogue record is found through a self-relative 32-bit
table at `0x0C` indexed by roster number − 1; the ending reads nothing else
from the file, so a record can live anywhere in it (D-022). **CONFIRMED:**
at most 238 non-space characters of an epilogue are drawn; every English
epilogue needs 263-345. Without cutting text (which needs the user's
approval), the glyph list must move to a larger free RAM area (the literal
`0x060839D4` at `0x06037A98`), which requires showing that area unused
during the ending.

## Uncertainty and Alternatives

- That the following buffer is what destroys the entries is SUPPORTED, not
  isolated: the drawing side might also stop at a count.
- Line spacing 13 drew 13 lines and part of a 14th legibly; 16-18 lines at
  that spacing, and where the screen bottom is, are untested.
- Writing the English into `ST1JPN.BIN` serves the US Enhanced build only;
  the Japanese editions need that file intact (`EDITION-001`).
