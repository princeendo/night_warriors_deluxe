# EXP-0017: The Region Flag's Title-Screen Check

Task: DISC-002 (what the region flag changes)
Status: DONE (static; the input test is not run)
Confidence: SUPPORTED (code reading, no runtime test)

## Observation

`EXP-0015`: `TITLE.O` reads the region flag (`0x0608089A`) once in the US
release, followed by a pad-bit (`0x0800`, Start) test. The Japanese
`TITLE.O` is a different file (33,760 bytes vs. 34,076) and reads its flag
(`0x060808EA`) somewhere else.

## Hypothesis

The US check limits who can start a game from the title menu, and the
Japanese check selects title-screen text; neither touches the content
US Enhanced is about.

## Controlled Change

None. Static reading, and one WRAM-H extraction to find the load address.

## Inputs and Provenance

- `TITLE.O`: US `bd9fed50…`, Japanese `884f8aed…`.
- US WRAM-H at the title menu: `mcs_extract` of session state
  `local/aud001/us-session/rec/states/f00001903.mcs` (`d1b50134…`, ignored
  path `research/memory_dumps/disc001/us-f00001903/`).

## Procedure

1. Locate `TITLE.O` in the title-menu WRAM-H: it is loaded whole at
   `0x06001000` (the same slot as Morrigan's `PL05.O` in a fight).
2. Disassemble both files at base `0x06001000` around each flag reader
   (`tools/sh2/disasm.py`, `EXP-0013/xref.py`), and the US language-byte
   reader for comparison.

## Actual Result

**US check (`0x06005138`, title menu).** The routine builds a combined pad
word (player 1 OR player 2, `0x06076AB6` and `0x06076ABA`) and acts when its
Start bit is set. With the cursor (`0x06080868`) on ARCADE (0) or VS (1):

```text
06005138  mov.l @(..),r1   ; 0x0608089A region flag
0600513A  mov.b @r1,r2
0600513C  tst   r2,r2
0600513E  bt    start      ; flag 0: either player's Start starts the mode
06005140  mov.l @(..),r2   ; 0x06076AB6 player 1 pad
06005142  mov.w @(2,r2),r0
06005144  ...  tst 0x0800  ; player 1's Start?
0600514A  bf    start
0600514C  bra   ignore     ; flag non-zero and only player 2 pressed Start
```

So in the US release only player 1's Start begins ARCADE or VS from the
title menu; with the flag at 0, player 2's Start works too. OPTION (2) is
not gated.

**Japanese check (`0x060043EC`).** With the flag 0 it draws two text lines
from `TITLE.O`, "~CAPCOM CO., LTD. 1994, 1995, 1996" and
"ALL RIGHTS RESERVED." (`~` is presumably the copyright sign); with 2 it
draws none.

**US language check (`0x06004462`, for comparison).** The US `TITLE.O`
picks the same two lines when the language byte is 0, and three lines
("~CAPCOM CO., LTD. ...", "~CAPCOM U.S.A., INC. 1994, 1995, 1996",
"ALL RIGHTS RESERVED.") when it is 1.

**Why the agent cannot test it.** It needs a Start press on player 2.
The agent interface sends no input; port 2's Start is unmapped in both
Mednafen homes; a key sent to the window would take focus (local guidance).
Faking the press in RAM is not reliable either: the agent's `write` goes
straight to the RAM array (`PutAddressSpaceBytes`, `ASPACE_WORKRAMH`, in
`src-agent/src/ss/debug.inc`) and not through the emulated SH-2 cache, which
explains the failed write of `EXP-0016` (SUPPORTED).

## Conclusion

**SUPPORTED:** the region flag's title check makes the US title menu accept
only player 1's Start for ARCADE and VS. In the Japanese release the flag
only selects whether its copyright lines are drawn, and in the US release
those lines are chosen by the language byte (a US copyright line is added).
None of this is Japanese-only content; a `DISC-002` patch that keeps the flag
at 2 keeps the US behaviour.

## Uncertainty and Alternatives

- Not run: confirming needs a player-2 Start press (the user's pad mapped to
  port 2, or one key press with a mapping) on the US title menu, with and
  without the flag cleared.
- Whether the copyright lines are actually on screen, and where, is not
  checked against a screenshot.

## Reproduction

```bash
./invenv.sh python -m tools.memory.mcs_extract local/aud001/us-session/rec/states/f00001903.mcs \
  --region wram_h --out-dir research/memory_dumps/disc001/us-f00001903
./invenv.sh python tools/sh2/disasm.py local/extracted/saturn_us/TITLE.O --base 0x06001000 \
  --start 0x06005108 --end 0x060051A4
./invenv.sh python tools/sh2/disasm.py local/extracted/saturn_jp/TITLE.O --base 0x06001000 \
  --start 0x060043E4 --end 0x0600443C
```
