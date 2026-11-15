# EXP-0020: The PSP Chronicle's English Epilogues

Task: REF-002 (intake), for END-002 (an English donor for END-01)
Status: DONE
Confidence: CONFIRMED that the PSP holds 14 English epilogues; SUPPORTED that
each one renders the Saturn Japanese epilogue of the same character

## Observation

The web research names *Darkstalkers Chronicle: The Chaos Tower* (PSP) as the
likeliest official English source for the epilogues (its sources 6 and 7),
unverified. The user supplied the US UMD image (`references/psp_chronicle_us/`)
and asked to try it before any new translation.

## Hypothesis

The PSP image holds an official English text for each of the 14 Vampire
Hunter epilogues that `ST1JPN.BIN` shows on the Saturn.

## Method

Static, no emulator. List the ISO; search every file for character names in
plain and shifted 8/16-bit encodings; then look where the endings are.

1. Extract (ignored output):
   `bsdtar -xf "local/disc_images/psp_chronicle_us/…(USA).iso" -C local/psp_extract/chronicle_us`
   (bsdtar 3.7.4, macOS).
2. Name search (a difference-pattern search for "Morrigan", "Demitri",
   "Felicia", "Anakaris", "Bishamon" in 8-bit, 16-bit LE and BE): hits only in
   `USRDIR/english/mess00.bin` and `USRDIR/psp/common/mess00.bin`
   (16-bit LE, code = ASCII + `0x20A0`). Those are menu, network and gallery
   labels; the gallery menu lists "NIGHT WARRIORS(SP) ENDINGS". No epilogue
   text is stored as characters anywhere.
3. `USRDIR/movie/hunend/` holds 28 PMF movies, `HmovieNN_1.pmf` and
   `HmovieNN_2.pmf` for NN = 01-14 (PSMF header of 2,048 bytes, then an MPEG
   program stream with H.264 480x272 at 29.97 fps; 1,253 frames in
   `Hmovie04_2`). Each `_2` movie shows an English paragraph typed over the
   character's scrolling art: the text is part of the picture.
4. `research/experiments/EXP-0020/frames.sh` (ffmpeg 9.0.1) extracts frame 300
   of each `_2` movie; frame 300 shows the complete paragraph. A strip of
   the top 40 pixels every 60 frames shows the first line unchanged from its
   appearance to the end, so no line scrolls out. Rerun, the frames hash the
   same.
5. Each frame was read and compared, by meaning, with the Japanese epilogue
   of the same character on the Saturn (the `EXP-0019` key frames; Morrigan's
   from `EXP-0018` `m2-v2` `r006842`). An agent transcription is kept in the
   ignored `local/ref002/psp_epilogues/transcript.md`.

## Actual Result

The PSP order is its own. Every Saturn character has one `_2` movie:

| PSP movie | Character (Saturn N) | Frame 300 SHA-256 | Opens | Against the Saturn Japanese epilogue |
| --- | --- | --- | --- | --- |
| `Hmovie01_2` | Hsien-Ko (13) | `0b8c3ad5…` | "The girls grew quickly…" | same story; mother's words told, not quoted |
| `Hmovie02_2` | Donovan (14) | `3df29b28…` | "Deep in a Romanian forest…" | same story; shortened |
| `Hmovie03_2` | Demitri (1) | `40353d31…` | "Demitri returned to his realm…" | same story; the dialogue with Morrigan dropped |
| `Hmovie04_2` | Morrigan (5) | `78232c2e…` | "Fatigued from battle, Morrigan…" | same story; dialogue shortened, speaker labels added |
| `Hmovie05_2` | Anakaris (6) | `d026ebfa…` | "Anakaris returned to the world…" | same story; his one quoted line dropped |
| `Hmovie06_2` | Victor (3) | `a9e44971…` | "All Victor longed for…" | same story; his quoted lines dropped |
| `Hmovie07_2` | Lord Raptor (4) | `e205b15b…` | "Rapter, confident in his newly…" | **meaning changed**: in the Japanese, Le Malta has leaked Zabel's whole plan to Ozomu; the English makes Le Malta a loyal sidekick and the master simply aware; dialogue rewritten |
| `Hmovie08_2` | Jon Talbain (2) | `0f328d72…` | "Talbain's lycanthropic blood…" | same story; the children's lines dropped |
| `Hmovie09_2` | Felicia (7) | `bd21c2c3…` | "And that's how my dream…" | close throughout |
| `Hmovie10_2` | Rikuo (9) | `ae08b160…` | "The Mermen were not extinct…" | same story; details changed (the hidden mountains become an underground chamber; the closing line becomes his thought) |
| `Hmovie11_2` | Sasquatch (10) | `71c961a1…` | "The Bigfoot clan began…" | **meaning changed**: the Japanese ends with the clan going to the humans for world conquest and a banana joke; the English ends with revealing themselves "and hope for the best" |
| `Hmovie12_2` | Bishamon (8) | `7a32b2c1…` | "In the end, it was nothing…" | same story; the last sentence changed (Japanese: do they still wander the dark seeking blood; English: do they still fight the darkness) |
| `Hmovie13_2` | Huitzil (11) | `96ab6727…` | "The guardians, their duty fulfilled…" | close throughout |
| `Hmovie14_2` | Pyron (12) | `c31fd6c2…` | "To an immortal like Pyron…" | close throughout |

The English carries the US names (Demitri, Jon Talbain, Hsien-Ko, Rikuo,
Victor, Morrigan; "Rapter", "Le marta", "Berial", "Dr.Von Gerdenheim",
"Orin") and several typos ("new without speakig", "exaulted", "kindom's",
"nothing more a horrible nightmare").

## Conclusion

**CONFIRMED:** the US PSP *Chronicle* image holds an English epilogue for
each of the 14 characters, as text drawn into the `movie/hunend/HmovieNN_2.pmf`
videos (not as character data). **SUPPORTED:** each renders the Saturn
Japanese epilogue of the same character, usually shortened by dropping
quoted dialogue; Lord Raptor's and Sasquatch's change the meaning, and
Bishamon's and Rikuo's change details. It is an official English source
(Capcom, 2005) for `END-002`; using it, and how to treat its typos, names
and changed meanings, is a `GATE-TRANSLATION` decision.

## Uncertainty and Alternatives

- The comparison is by meaning, read by the agent from screenshots; it is a
  judgement, not a byte comparison. The transcription has not had a second
  reading.
- Whether the PSP English was translated from these Saturn epilogues or from
  another release's Japanese (the arcade) is UNKNOWN.
- The `_1` movies (the main endings), `movie/hun2end/` (`H2movie01`,
  `H2movie02`) and `ed/ending.pac` were not examined; whether the PSP main
  endings match the US Saturn English is UNKNOWN.
- Length: the PSP shows about 13 lines of about 32 characters; whether a
  paragraph fits the Saturn epilogue's text layout is a later question.
