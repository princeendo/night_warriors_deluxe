# EXP-0012: The Switch Behind the Epilogue

Task: END-001
Status: DONE
Confidence: CONFIRMED (Morrigan's ending)

## Observation

`EXP-0011` (D-011): the Japanese release loads `ST1JPN.BIN` (epilogue text)
and `ST2JPN.BIN` at the ending; the US release loads only `ST2USA.BIN`. All
of these files, and the font, are on both discs.

## Hypothesis

The same code in both releases chooses the `ST1`/`ST2` files by a data value,
and the US release differs only in that data; changing it in US RAM makes
the US release show the Japanese epilogue.

## Controlled Change

RAM writes only, in the US release, from the `EXP-0010` states, one variable
at a time (each run below), with the forcing method of D-009. No disc change.

## Procedure and Result

**1. Name tables.** Both `MAIN.BIN` files hold `ST2JPN/ST2USA/ST2HIS.BIN` and
`ST1JPN/ST1USA/ST1HIS.BIN` as 12-byte entries. `MAIN.BIN` is loaded at
`0x06013A00` (Japanese) / `0x06012000` (US). Each table is reached through an
array of three pointers (JPN, USA, HIS): ST2 at `0x0606BED4` / `0x0606BE34`,
ST1 at `0x0606BF58` / `0x0606BEB8`.

**2. The ST1 loader** (Japanese `0x06038166`, US `0x0603790E`; the same
instructions in both, `tools/sh2/disasm.py`):

```text
mov.l  @(..),r3   ; 0x060808D2 (JP) / 0x06080882 (US): language byte
mov.l  @(..),r0   ; ST1 pointer array
mov.b  @r3,r4
mov.l  @(..),r2   ; 0x06013FDC / 0x06013DF8: file loader
shll2  r4
jmp    @r2
mov.l  @(r0,r4),r4 ; file name = array[language]
```

**3. Its caller** (found with a PC breakpoint in a forced Japanese ending:
halt at frame 641, `PR` = `0x0603C168`), identical in both releases apart
from addresses:

```text
0603C15A  mov.l @(..),r3   ; 0x060808EA (JP) / 0x0608089A (US): epilogue flag
0603C15C  mov.b @r3,r0
0603C15E  tst   r0,r0
0603C160  bf    skip       ; flag != 0: no ST1 file is loaded
0603C162  mov.l @(..),r2   ; the ST1 loader
0603C164  jsr   @r2
```

**4. The values** (WRAM-H from `EXP-0007` fight states and `EXP-0010`
ending states):

| Byte | Japanese | US |
| --- | --- | --- |
| Language (`0x060808D2` / `0x06080882`) | 0 | 1 |
| Epilogue flag (`0x060808EA` / `0x0608089A`) | 0 | **2** |

The same in every state examined, from the first fight to the ending.

**5. Forced US runs** (`EXP-0010/force.py`; `--halt-pc` added for step 3):

| Run (`local/end001/`) | Writes | Result (agent-reviewed) |
| --- | --- | --- |
| `us-lang0` | language = 0 at a state inside the English main ending | the English dialogue box freezes on one line and the ending stalls to black: the dialogue renderer reads the language per line. Dead end. |
| `us-lang0-emblem` | language = 0 during the emblem card | art scrolls with no text (no `ST1` file was ever loaded) |
| `us-lang0-ko` | stage 9 and language = 0 at the KO | Japanese main ending (`ST2JPN`), then still **no** epilogue text: language alone is not the gate |
| `us-flag0` | stage 9 and flag = 0 at the KO | English main ending; `ST1USA.BIN` is loaded (at `0x060CB408`) and the epilogue routine draws rows of the letter "A" over the art, plus a strip of filler glyphs across the top of the emblem card |
| `us-enhanced-test` | stage 9, flag = 0, and the ST1 array's USA entry (`0x0606BEBC`) pointed at the `ST1JPN.BIN` name (`0x0605B850`) | English main ending; `ST1JPN.BIN` loaded; epilogue art with **no** text (the epilogue renderer also reads the language when it draws) |
| `us-enhanced-epi` | from `us-enhanced-test`'s emblem-card state (`r006089`), language = 0 | **the Japanese epilogue paragraph over Morrigan's scrolling art, in the US release after its English main ending** (`r001364`, `c815220a…`; the English ending frame `us-enhanced-test` `r005177`, `61c92459…`) |

## Conclusion

**CONFIRMED (Morrigan):** the US release has the same ending code as the
Japanese one; its epilogue is switched off by data. An **epilogue flag**
(Japanese `0x060808EA` = 0, US `0x0608089A` = 2) decides whether the ending
loads an `ST1` file at all, and a **language byte** (Japanese `0x060808D2`
= 0, US `0x06080882` = 1) picks the file (`ST1JPN`, `ST1USA`, `ST1HIS`) and
how the epilogue and dialogue text are drawn. With the flag cleared, the
`ST1JPN.BIN` name in the US slot, and the language set to Japanese only for
the epilogue, the US release shows its English main ending followed by the
Japanese epilogue: the first US Enhanced behaviour, in live RAM (D-012).

## Uncertainty and Alternatives

- **`ST1USA.BIN` is a placeholder** (HYPOTHESIS, strong): the epilogue
  routine draws it as rows of "A"; its records repeat the 16-bit value
  `0x00C1`. An English epilogue in the US format would replace it, which
  needs the format of `ST1USA.BIN` records and the English renderer's
  character codes (`GATE-TRANSLATION`).
- The strip of filler glyphs over the emblem card with the flag cleared is
  unexplained; it appears whether `ST1USA` or `ST1JPN` is loaded.
- Where the two bytes are set (boot, region, a setting) is not traced; that
  decides how an edition switch would set them.
- Only Morrigan's ending was run. The workaround for the language byte (set
  only after the main ending) is a test procedure, not a design.
- This is the M1 outcome (a Japanese-only element shown by the US release
  through a live RAM change) reached inside `END-001`, before the formal
  `GATE-M0` go-ahead; recorded so the user can decide how to treat it.

## Reproduction

```bash
S=local/aud001/us-session/rec/states/f00011016.mcs
./invenv.sh python research/experiments/EXP-0010/force.py us $S local/end001/us-enhanced-test \
  --write 0608092B=09 --write 0608089A=00 --write 0606BEBC=0605B850 --steps 270
./invenv.sh python research/experiments/EXP-0010/force.py us \
  local/end001/us-enhanced-test/states/r006089.mc0 local/end001/us-enhanced-epi \
  --write 06080882=00 --steps 90
```
