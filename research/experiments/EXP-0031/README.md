# EXP-0031: Morrigan's Missing Main-Ending Lines in US Enhanced

Task: END-004 (criteria 1-3; the cold boot follows)
Status: DONE (forced); cold boot pending
Confidence: CONFIRMED (forced from a state, `MAIN.BIN` changes written in RAM)

## Observation

`EXP-0030`: Morrigan's US main ending lacks two Japanese lines (`ST2JPN`
`36`, she asks for her bed; `37`, the butler accepts) and a pause page
(`B1`). User decisions of 2026-11-16: restore only these, English from the
PSP first, every other US line unchanged.

## Step 1: the PSP Has No English for Them

`movie/hunend/Hmovie04_1.pmf` (2,863 frames; SHA-256 of the file
`93d44114…`), tiled every 2 s and read (agent-reviewed): the PSP main ending
reuses the US Saturn English word for word, nine pages, without the two
lines (frames 360 `e18b5058…`, 1,560 `a08fda49…`). So the English is a new
translation, approved by the user on 2026-11-16 (rule 29): Morrigan, "I'm a
little tired. / Prepare my bed."; the butler, "Certainly, mistress."

## Step 2: Where the New Data Fits

- `ST2USA.BIN` has no unused record (only one unreferenced entry, `0x12C`,
  whose target is inside Demitri's record). Its table runs past the highest
  page id any script uses (`0x102`), and an "A" placeholder record follows
  that nothing points at: `0x418`-`0x4BD` (166 bytes) is free. The two
  records take 132 bytes (`0x418`, `0x46C`), reached by the unused entries
  `0xB1`, `0xB2`.
- The script grows from 9 to 11 pages (110 → 134 bytes) and the scripts are
  packed. A 1,537-byte zero run in `MAIN.BIN` (`0x0606CA5D`) is a working
  buffer (`--log-write`: 631,222 writes during an ending), so it was not
  used. Morrigan's Japanese script (`0x0605ADBC`) is exactly 134 bytes and
  unread while the region flag is 2: the new US script goes there, and the
  US table entry 4 (`0x0605B740`) points at it. In Japanese mode this image
  would now show her pages out of order (`EDITION-001`).

## Step 3: First Build — Pages After the Insert Fall Out of Step

With the pages simply inserted, everything after them is late: "Nothing,
just having a little fun…" ran into the emblem card, its letters corrupted
by the card's "1ST A" (`local/end004/morr-main`). The pictures run on their
own timeline. In the control (`EXP-0027` build, `local/end002/fix-end-05`),
each page starts at script time + 422 frames; the butler scene ends near
script time 3,850, the bed scene runs about 3,980-4,870, the card follows.

## Step 4: Retimed Inside the Butler Scene

`research/experiments/EXP-0031/build_morrigan_main.py` (Track 1
`f4edd2a41db23db6b44aa7b06e091efb229666870eed668b56dfb5862b581091`): pages
`33`-`36` shortened (480 → 420, 540 → 480, 300 → 240, 300 → 240 frames,
waits shortened), the two new pages (160 and 120 frames) placed before the
scene change; `37` and `B0` start and end exactly as shipped (3,980 and
4,420-4,820). The Japanese pause page has no room; the shipped wait before
`B0` stands for it.

| Change | File / offset | Original → modified |
| --- | --- | --- |
| her record | `ST2USA.BIN` `0x418` (84 bytes) | table tail → x `1D`, y `B0`/`C0`, the two lines |
| butler record | `ST2USA.BIN` `0x46C` (48 bytes) | placeholder → x `1D`, y `B0`, one line |
| entries | `ST2USA.BIN` `0x2D0`, `0x2D4` | placeholder offsets → the two records |
| script | `MAIN.BIN` `0x48DBC` (`0x0605ADBC`, 134 bytes) | her Japanese script → her new US script |
| pointer | `MAIN.BIN` `0x49740` (`0x0605B740`) | `0605B344` → `0605ADBC` |

Forced from the version 2 bonus-screen state with the two `MAIN.BIN`
changes written in RAM (`local/end004/morr-main2`, agent-reviewed): butler
scene — "You worry too much…", "Hurry…", "I'm a little tired. / Prepare my
bed.", "Certainly, mistress."; fade; bed scene — "So what did you do on
earth this time?", "Nothing, just having a little fun…"; the card clean.

Others unchanged (same state, same RAM writes): win screen, Pyron's and
Anakaris's endings (`local/end004/chk-*`) against `EXP-0027`'s runs. The
shots are not byte-identical (runs land a frame or two apart, so animated
sprites differ), so the text pages' on and off frames were compared: the
win screen identical; Pyron's and Anakaris's within one shot (30 frames),
apart from blips where animated cyan sprites trip the detector.

## Conclusion

**CONFIRMED (forced):** Morrigan's main ending in US Enhanced shows her two
missing lines, in the Japanese order and inside the butler scene, with her
other US lines and the scene timing unchanged; the other endings and the win
quote are unaffected (D-030).

## Uncertainty and Alternatives

- Not yet from a cold boot.
- Pages 33-36 are shown 60 frames shorter; read on screen, still readable.
- Japanese mode on this image would play the new US script over `ST2JPN`
  (wrong order); the edition switch must restore her Japanese script.
