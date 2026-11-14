# EXP-0004: Stock Debugger: Work-RAM Dumps, a Memory Write, a Write Breakpoint

Task: EMU-007
Status: DONE
Confidence: CONFIRMED

## Observation

`EXP-0003` (D-003) showed hotkeys reach Mednafen with `--keep-focus`. The
stock debugger dumps (`d`) and loads (`l`) memory ranges from its memory
editor, and sets write breakpoints (`shift+w`). Cyberbots' `EXP-0004` did this
on its game with the step files reused here; that is no evidence here.

## Hypothesis

In each release, with emulation frozen on the title, the stock debugger dumps
WRAM-L (`0x00200000-0x002FFFFF`) and WRAM-H (`0x06000000-0x060FFFFF`)
repeatably, a 16-byte load changes memory and a second load restores it, and a
write breakpoint over WRAM-H halts the game.

## Controlled Change

Debugger keys only, sent by `tools/mednafen/hotkeys.py --keep-focus
--script`. No game, BIOS, binary or setting change. The quiet home's `sav/`,
`mcs/` and `snaps/` were emptied before each run.

## Prediction

Two dumps of each bank at one frozen instant are identical and 1 MiB; the
write test reads back the pattern, then the original; after the breakpoint,
two window captures seconds apart are identical and the debugger shows a
store into WRAM-H.

## Inputs and Provenance

As `EXP-0001`: Japanese 1M and US images, stock Mednafen `de542817…582a`,
quiet home (`aad9a7ef…57cf`, unchanged after all runs). Pattern file
`research/memory_dumps/emu007/<r>/w-pattern.bin`: the 16 ASCII bytes
`EMU-007 WRITE OK` (`b0771fd5…a3fe`), the same as Cyberbots'.

## Tools and Environment

`tools/mednafen/hotkeys.py` with `--keep-focus` and `--script`; `window=FILE`
captures the Mednafen window alone (`screencapture -l`), since Mednafen's own
screenshots leave out the debugger. Screen Recording and Accessibility were
already permitted.

## Procedure

Step files are in [`steps/`](steps/): Cyberbots' `run-a2.steps` and
`run-f.steps` (its `EXP-0004`, `bac6fde`) with the same actions, the freeze
moved from 63 s to 65 s (this game's title shows from about 63 s, D-001),
run F's times shifted by two seconds, and the paths split by release.

```bash
for r in jp us; do for run in a f; do
  find local/mednafen_quiet/sav local/mednafen_quiet/mcs local/mednafen_quiet/snaps -type f -delete
  ./invenv.sh python -m tools.mednafen.hotkeys "$CUE" local/emu007/$r-$run.log \
    --script research/experiments/EXP-0004/steps/$r-$run.steps --keep-focus
  # after run a: moved the state to local/emu007/$r-a-state/
done; done
```

- Run A (freeze at 65 s on the title): `option+a` (frame advance, which
  pauses), `F5`, `option+d`, `option+3` (memory editor), `period` (Low Work
  RAM), two dumps `00000000 000fffff …/wraml-N.bin`; `period` (High Work RAM),
  two dumps `wramh-N.bin`; then on `000f0000 000f000f`: `d` before, `l`
  pattern, `d` after, `l` before, `d` revert; window captures throughout.
- Run F: captures at 65 s and 67 s; `option+d`, `shift+w`, type
  `06000000-060fffff 26000000-260fffff`, `return`, `option+d`; captures at
  75 s and 79 s; `option+d`; captures at 81 s and 83 s.

**First attempt disturbed (2026-11-14 01:19).** The user used the computer
during it ("I'm pretty sure I messed you up, sorry"). The Japanese run A
wrote no dump files and its F12 timed out; the runs were stopped (no Mednafen
left; settings and sources unchanged) and their output moved to the ignored
`local/emu007/disturbed/`. The rerun below (01:22:54-01:29:26) was
undisturbed. Lesson: a `--keep-focus` run needs the user hands-off for its
whole length.

## Actual Result

All four runs exited 0 (F12). Source manifests identical before and after
(`local/emu007/source-*.json`); no Mednafen process left.

| File (per release) | Size | Japanese SHA-256 | US SHA-256 |
| --- | ---: | --- | --- |
| `wraml-1.bin` = `wraml-2.bin` | 1,048,576 | `b7caad6501ed9f8094cd39f50e2177dca4f68dfb7d45c1673566b66e052218bb` | `914d4e2bd58885303a941c18af07aac29add728052c67278138dad874d84ec43` |
| `wramh-1.bin` = `wramh-2.bin` | 1,048,576 | `a6c4aaa36dfad49920aff2f2204d218a872c9fc8322e26ea9b145c0c73e23db0` | `78715324e8ce10dfe513f5a7b800fc2e2cbb064e0160df326e1d161344700702` |
| `w-before.bin` = `w-revert.bin` | 16 | `5ac6a594…461b` | same |
| `w-pattern.bin` = `w-after.bin` | 16 | `b0771fd5…a3fe` | same |

- In each release the two dumps of each bank are identical, and WRAM-L and
  WRAM-H differ. Both releases' WRAM-L begins
  `B5 00 7F 42 88 6F 0F 07 77 D9 08 CD 87 69 10 76` and WRAM-H begins
  `06 00 09 4A` repeated; the Japanese and US WRAM-L dumps first differ at
  byte 27,900 (0-based), and the WRAM-H dumps differ in 693,622 bytes (one
  frozen title instant each; not a structural comparison).
- **Write test** at WRAM-H offset `0xF0000` (`0x060F0000`), both releases:
  before `FF` × 16; after the load, the pattern; after loading the saved
  original, `FF` × 16 again.
- **States** saved during the run A freeze, the same instant as the dumps
  (for `DBG-001`): Japanese `local/emu007/jp-a-state/…(1M).d5e0b9bd980bc403f93b3253613b3c79.mc0`,
  1,633,705 bytes, `f945cb512b38243c170d0a3ff8044f826614958878039b340e0708518c6d91a0`;
  US `local/emu007/us-a-state/…(USA).4d965b46d9ac92f88ac7f839e90e8983.mc0`,
  1,630,993 bytes, `2eb7dbd08bf9cc2f2092e121db3f1d76d5760d8f9ce94a588f1bef6f2eda49db`.
- **Run F**, both releases: the captures at 65 s and 67 s differ (running);
  after the breakpoint, the captures at 75 s and 79 s are identical, and with
  the debugger shown, those at 81 s and 83 s are identical. The CPU view
  (read from the capture's small font; a digit may be misread):
  - Japanese: PC `0605186C`, highlighted `mov.l r0,@(4,r15)`, R15
    `060FFE8C`: the store target `060FFE90` lies in WRAM-H. The `NOW LOADING`
    screen shows behind the debugger.
  - US: PC `06000864`, highlighted `mov.l r0,@-r15`, R15 `060FFFD0`, branch
    trace ending `[INT47]`: a stack push in an interrupt handler, target
    `060FFFCC`, in WRAM-H.

## Conclusion

**CONFIRMED.** In both releases the stock debugger dumps WRAM-L and WRAM-H
repeatably at a frozen instant, loads memory and restores it, and halts on a
WRAM-H write breakpoint with the store shown. The dumps and the states saved
at the same instant are ready for `DBG-001`.

## Uncertainty and Alternatives

- The breakpoint halted on the first write after it was set, so the two
  releases stopped at different code (a stack store at a different moment);
  this says nothing about their code differing.
- Hotkey runs need the user hands-off; the first attempt lost every dump.

## Reproduction

Run the procedure above from the repository root, with the user present and
not using the computer. Dumps stay in the ignored
`research/memory_dumps/emu007/<r>/`, captures in `local/emu007/win/`, states
in `local/emu007/<r>-a-state/`.
