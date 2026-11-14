# EXP-0015: A Map of Everything the Region Flag Selects

Task: DISC-002 (what a one-byte patch would change)
Status: DONE
Confidence: CONFIRMED (the flag selects the cast-roll name; the paired tables
are in both `MAIN.BIN` files); SUPPORTED (the role of each other reader, from
code and tables); UNKNOWN where stated

## Observation

`EXP-0014` (D-014): the byte called the epilogue flag (`0x0608089A` US = 2,
`0x060808EA` Japanese = 0) also gates Morrigan's voices, and about 20
`MAIN.BIN` readers plus `TITLE.O`, `SOBJ08.O3`, `PL10` and `PL14` test it.
The user chose to map them before any disc patch ("Map them first").

## Hypothesis

The flag is a region switch: each reader picks between a Japanese and a US
version of one item, and both versions are in both releases' data.

## Controlled Change

For the one runtime check, the flag only: the cast roll of the `EXP-0012`
`us-enhanced-test` run (flag 0 at the KO, language still 1) was continued
to the credits and compared with the unpatched US run of `EXP-0010`
(`us-ko-n9-b`, same won-KO state `f00011016`, same stage forcing). The rest is
static reading and a census with no change.

## Prediction

The flag-cleared US cast roll shows the Japanese name (GALLON) where the
unpatched one shows JON TALBAIN; each table pair is present in both
`MAIN.BIN` files.

## Inputs and Provenance

- US `MAIN.BIN` `b4a3c192…16e8` (base `0x06012000`), Japanese
  `08e042ad…5f21` (base `0x06013A00`).
- The 411 US session states of `EXP-0007` (`local/aud001/us-session/rec/states`,
  one per second of the user's play: title, menus, character select, two
  fights vs. Victor and Bishamon, win quotes, pause).
- `local/end001/us-enhanced-test/states/r008224.mc0` (`EXP-0012`).
- Patched Mednafen `7826b9b9…f887`, quiet home.

## Tools and Environment

- [`pc_census.py`](pc_census.py): PC breakpoints in log mode on a list of
  addresses; runs from power-on, or loads each state of a folder and runs N
  frames with no input; writes hit counts per source.
- `EXP-0013/xref.py`, `EXP-0014/readers.py`, `tools/sh2/disasm.py`.

## Procedure

1. **Census** of the 21 US `MAIN.BIN` readers (load sites):

```bash
PCS="06018032 06018E00 0601A13E 0601A1A8 0601D4C0 0601F17E 0602FC58 0603411C 06034150 \
060341B4 0603487A 060348CC 06035016 060367A4 06036800 06037AE4 06037B5E 0603B902 06042CF0 \
06042EEC 0604468C"
ARGS=(); for x in ${=PCS}; do ARGS+=(--pc $x); done   # zsh
./invenv.sh python research/experiments/EXP-0015/pc_census.py us local/disc001/census-us-boot "${ARGS[@]}" --boot 7200
./invenv.sh python research/experiments/EXP-0015/pc_census.py us local/disc001/census-us-session "${ARGS[@]}" \
  --states local/aud001/us-session/rec/states --frames 60
```

   Each state's nearest session screenshot (`rec/shots`) was reviewed by the
   agent to name the screen.
2. **Reading.** Each reader disassembled with its function; each table pair
   dumped and compared entry by entry.
3. **Same tables in the Japanese file:** each US table's bytes searched for
   in the Japanese `MAIN.BIN`.
4. **Cast roll:**

```bash
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/end001/us-enhanced-test/states/r008224.mc0 local/disc001/us-flag0-credits \
  --steps 100 --step-frames 30
```

## Actual Result

**Character numbering.** The name tables have 14 entries; the US entries
differ for numbers 2, 4, 9, 11 and 13 only. Morrigan's code `PL05` and
Victor's `PL03` (`EXP-0014`) fix 5 and 3; the five differing numbers match
the five characters the US release renamed, in the usual roster order
(1 Demitri, 2 Gallon, 3 Victor, 4 Zabel, 5 Morrigan, 6 Anakaris, 7 Felicia,
8 Bishamon, 9 Rikuo, 10 Sasquatch, 11 Lei-Lei, 12 Pyron, 13 Huitzil, 14
Donovan). SUPPORTED; it makes `PL10` Sasquatch and `PL14` Donovan
(HYPOTHESIS until their files are seen loaded).

**Census.** Power-on to frame 7,200 (title, attract): only `0602FC58`
(11 hits). Session: `0601D4C0` in 303 states (every fight frame);
`0603411C`/`06034150` on six NOW LOADING states; `06035016` at character
select (MODE SELECT box); `0601A13E`/`0601A1A8` once at seven round
starts/K.O.s; `06042CF0` at five win-quote screens; `06037AE4`/`06037B5E`
on a win-quote screen; `0602FC58` on the title menu. The other 11 readers did
not run in these states.

**The readers** (US addresses; "JP" = the flag-0 branch, the Japanese
release's behaviour):

| Reader(s) | Where | What the flag selects | Class |
| --- | --- | --- | --- |
| `0603B902`; `ENDING.O` x2 | ending | load an `ST1` epilogue file or not; epilogue scroll (D-012) | Japanese-only content |
| `PL05` x4 | Morrigan's moves | four voice calls, made only in JP (D-014) | Japanese-only content |
| `PL14` x2 | Donovan (HYPOTHESIS) | two sound calls (`0x0603A76E`, codes `0x01B2`, `0x01B4`), made only in JP | Japanese-only content (lead `AUD-04`) |
| `06042CF0`, `06042EEC`, `0604468C`, `06034150` | win-quote screen, loading screen, cast roll | name graphic per character: table `0x06066CBC` (JP) or `0x06066E7C` (US), graphic IDs `0x3829-0x3836`; US uses `0x3837-0x383B` for 2, 4, 9, 11, 13 | US rename (`NAM-02`) |
| `0603411C`, `060341B4` | loading screen | name positions, `0x0605A748`/`0x0605A7B8` and `0x0605A956` (+14 words); differ for 2, 4, 9, 13 | US rename (layout) |
| `0601A13E`, `0601A1A8` | round start, K.O. | the fight display's name tiles per character, `0x06053FE4` (+`0xE0` US): different tiles for 2, 4, 9, 11, 13 | US rename |
| `06035016`, `0603487A`, `060348CC` | character select | MODE SELECT box graphics (JP `0x37E5`/`0x37E6`, US `0x37E8`/`0x37E9`) and a related table offset | US menu graphic |
| `06037AE4`, `06037B5E` | win-quote text | JP only: move listed character codes left by 3 or 8 pixels (Japanese punctuation spacing; list `0x0605B82C`) | text layout |
| `06018E00` | a text routine | US only: `#`, `$`, `%`, `{`, `}` drawn with special glyphs `0x140`-`0x146` | text layout |
| `060367A4`, `06036800` | ending | per-character script table `0x0605B1C0` (JP) or `0x0605B730` (US); US also branches for characters 11 and up | ending timing/script (UNKNOWN which part) |
| `0601F17E` | not seen | two table offsets (+28, +56) | UNKNOWN |
| `0601D4C0` | every fight frame | the Start-button pause check; US adds a path that toggles pause without the pad test | behaviour (UNKNOWN effect) |
| `TITLE.O` x1 | title | US only: a pad-bit (`0x0800`) test that may branch away | behaviour (UNKNOWN) |
| `PL10` x6 | Sasquatch (HYPOTHESIS) | calls `0x06030ABA` or sets object fields only in JP | UNKNOWN |
| `06018032`, `0602FC58`, `SOBJ08.O3` | title, others | act only when the flag is 4 | inert at 0 and 2 |

Several readers (`0601F17E`, `0603411C`, `060341B4`, `0604468C`) also take
the JP branch when `0x060808A9` is non-zero (UNKNOWN byte).

**Both releases hold both versions.** The US tables are found byte for byte
in the Japanese `MAIN.BIN`: name graphics (both 14-entry tables), name
positions, fight-display name tiles, MODE SELECT graphics, the spacing list
and `0x060549F4`. The ending script tables hold pointers and differ by
relocation (not compared).

**Cast roll.** Flag cleared, language still English: CAST, DEMITRI,
**GALLON** (`r002162`, `72b4dc38…`), VICTOR. Unpatched US: CAST, DEMITRI,
**JON TALBAIN** (`us-ko-n9-b` `r006226`, `25dec1b0…`), VICTOR, HSIEN-KO.

## Conclusion

**CONFIRMED:** the flag is a region switch, not an epilogue switch: with it
cleared and English kept, the US cast roll shows GALLON instead of JON
TALBAIN (D-015). Both `MAIN.BIN` files contain both regions' name tables and
layouts. From the code, the flag selects three kinds of things:

- Japanese-only content: the epilogue, Morrigan's voices, and probably
  Donovan's sounds.
- US localisation: the renamed characters' name graphics wherever names
  are drawn, the MODE SELECT graphics, and text-layout rules.
- Behaviour whose effect is unknown: the pause check, a title-screen pad
  test, and `PL10`.

**Consequence for US Enhanced:** clearing the flag on disc would bring back
the epilogue and voices but also the Japanese names, the Japanese menu
graphics and the Japanese spacing, which the edition policy does not ask for
(`LOC-001`). The Japanese-only items are separate branches (`0603B902`, the
`ENDING.O` and `PL05`/`PL14` tests), so a patch can open those alone.

## Uncertainty and Alternatives

- Roles other than the cast-roll name come from code and tables, not from
  screens; only GALLON was seen. The win screen, loading screen, fight
  display and MODE SELECT box with the flag cleared are not yet seen (the
  session has no renamed character).
- The census used the US session only (Morrigan vs. Victor and Bishamon); 11
  readers never ran there.
- `PL10`/`PL14` identities depend on the roster order (SUPPORTED, two points).
- `0x060808A9` and the pause and title behaviours are UNKNOWN.

## Reproduction

The commands above; outputs in the ignored `local/disc001/`.
