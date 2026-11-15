# EXP-0024: Room for an English Epilogue (the Sprite Arrays)

Task: END-002 (criterion 2, one character)
Status: DONE
Confidence: CONFIRMED (Morrigan, forced; cold boot not yet run)

## Observation

`EXP-0023`: an epilogue draws at most 238 non-space characters. The glyph
list starts at `0x060839D4` (literal at `0x06037A98`, used only by the
epilogue builder at `0x060379E0`; three other text builders and two scratch
users have their own literals for the same address).

## Static Reading

Each frame, three stubs call the list reader `0x060188D4(base, count)`,
which turns each 8-byte entry with a non-zero glyph into a 32-byte VDP1
command: array 1 `0x06083344` × 128 (`0x0601899C`), array 2 `0x06083744` ×
128 and array 3 `0x06083B44` × 192 (`0x060189C2`, which falls through to
array 3). The epilogue list starts at array 2 slot 82 and so has 46 + 192 =
238 slots.

## Logs and Dumps During the Epilogue

Version 2 image, Morrigan's ending forced (`EXP-0018` step 9):

- reads (`--log-read 06083344-0608334F --log-read 06083744-0608374F`,
  `local/end002/arr-read`): the reader visits arrays 1 and 2 every frame
  from 6,140 to 7,143.
- writes (`--log-write 06083344-060839D3`, `local/end002/arr-write`):
  `0x06018BA8` clears from array 1 slot 17 at frame 6,109; `0x06018D2C`
  writes 18 entries at `0x06083944`-`0x060839CC` (array 2 slots 64-81) every
  frame, for player 1 (`0x06083944`) and player 2 (`0x0608398C`), literals
  at `0x06037930`/`0x06037938`. Nothing else writes arrays 1-2 then.
- WRAM-H at frame 6,681 (`tools/memory/mcs_extract.py`, D-006): those 18
  entries are blank sprites (glyph `0020`) at y = 224, below the picture;
  every other slot in arrays 1-2 is empty.

## Hypothesis

Starting the list earlier, with an off-screen line of filler characters
covering the 18 player slots, gives the text the empty slots of arrays 1
and 2 with no other code change.

## Controlled Changes and Results

`research/experiments/EXP-0023/build_en_epilogue.py --move-list 5` builds
Morrigan's whole PSP paragraph (16 lines, spacing 13 from y = `0x10`) and
changes the literal at `0x06037A98`. A forced test from a state needs the
same literal in RAM (`--write 06037A98=…`): `MAIN.BIN` is loaded at boot,
so a state keeps the old code (the first run without it,
`en-morrigan-moved`, still started at `0x060839D4`).

| Run | List start | Result |
| --- | --- | --- |
| `en-morrigan-moved2` | array 1 slot 17 (`0x060833CC`), 431 slots | the whole paragraph, but the first 111 entries (array 1) are drawn **under** Morrigan's art (`r007622`) |
| `en-morrigan-a2` | array 2 slot 0 (`0x06083744`), 320 slots, player slots at entries 64-81 | the whole paragraph rises on black and stays on top of the art (`r007634` `c32f228f…`); no filler mark visible |

Build of the second run: Track 1 `6ec651e6…b6c5` (`build/us_en_epilogue_moved`).

## Conclusion

**CONFIRMED:** with the list literal at `0x06037A98` changed to `0x06083744`
and the filler line over the player slots, Morrigan's whole English
epilogue shows on top of her art (D-023). Array 1 is drawn before the art,
so text there is hidden. The room on top is 320 − 18 = **302** characters.
Fitting: Morrigan 278, Donovan 282, Bishamon 297, Pyron 263. Over: Huitzil
307, Lord Raptor 309, Sasquatch 310, Felicia 315, Victor 323, Rikuo 327,
Demitri 329, Hsien-Ko 335, Jon Talbain 337, Anakaris 345.

## Uncertainty and Alternatives

- Not yet from a cold boot of the built image (rule: with the user present).
- Two ways to more room, untested: move the player slots out of array 2
  while the ending runs (+18, to 320), or draw array 1 after the art
  (+111, to 413) by changing the order of the per-frame draw calls.
- Whether a line straddling the player slots wastes slots: up to one line's
  worth (fillers pad to the hole), not counted above.
