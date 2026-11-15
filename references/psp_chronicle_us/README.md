# Darkstalkers Chronicle (PSP, US): Reference Image

The US PSP release *Darkstalkers Chronicle: The Chaos Tower* (Capcom, 2005,
ULUS-10005). It is a reference for official English text only (`REF-002`):
never a build input, never committed, and nothing extracted from it is
committed. Text from it goes on disc only after `GATE-TRANSLATION`, with its
provenance (rule 29).

## Local Source Image (`REF-002`, 2026-11-14)

The user supplied one ISO, placed in the repository root; it was moved
unchanged (`mv`, same file system; SHA-256 equal before and after) into the
ignored, previously absent folder `local/disc_images/psp_chronicle_us/`.
Treat it as immutable.

Release description: `Darkstalkers Chronicle: The Chaos Tower (USA), PSP UMD
ULUS-10005, PARAM.SFO version 1.00; ISO supplied by the user 2026-11-14;
release identity as named, not independently verified`.

**Database match: not checked.** Identity is **SUPPORTED** by `UMD_DATA.BIN`
(`ULUS-10005|972DF1973B65CD66|0001|G`) and `PARAM.SFO` (`DISC_ID ULUS10005`,
`TITLE DARKSTALKERS CHRONICLE The Chaos Tower`, versions `1.00`).

| Filename | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `Darkstalkers Chronicle - The Chaos Tower (USA).iso` | 692551680 | `c465f42d8187b2731fe0a690214b1f73e868b3ddc3f87a00e1cd1b9ac21149ac` |

Produced with `tools.disc.hash_source --json` (ignored
`local/logs/ref002-hashes-psp_chronicle_us.json`), agreeing with `shasum -a 256`.

## Observations (2026-11-14, static, no emulator)

- ISO 9660, 880 entries (`bsdtar -tf`). `PSP_GAME/SYSDIR/BOOT.BIN` and
  `EBOOT.BIN` begin with a plain ELF header (not encrypted).
- `PSP_GAME/USRDIR/english/` holds English variants of five files
  (`cock.bin`, `dm00.bin`, `dm00_tbl.bin`, `dm02.bin`, `dm02_tbl.bin`) and
  `mess00.bin`; `PSP_GAME/USRDIR/ed/` holds `ending.pac` and ten other files.
  What the others contain is UNKNOWN.
- The epilogues are video (`EXP-0020`, D-019): `USRDIR/movie/hunend/`
  holds `HmovieNN_1.pmf` and `HmovieNN_2.pmf` for NN = 01-14, the `_2`
  movies showing each character's English epilogue drawn into the picture.
  `movie/savend/` and `movie/vamend/` are the other two games' endings (by
  name; not examined), `movie/hun2end/` holds two more (not examined).
- `mess00.bin` (`english/` and `psp/common/`) is 16-bit little-endian text,
  code = ASCII + `0x20A0`: menu, network and gallery labels only.
