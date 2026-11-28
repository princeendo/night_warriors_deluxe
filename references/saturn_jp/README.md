# Vampire Hunter Saturn JP: Source Images

The Japanese release, *Vampire Hunter: Darkstalkers' Revenge* (Capcom, 1996,
T-1202G). Permitted provenance and factual metadata only; never commit the
images or anything extracted from them. Which release is the modification
base is a user decision (`DOC-002`); see `references/saturn_us/README.md` for
the other region.

## Local Source Images (`ENV-006`, 2026-11-13)

The user supplied three Redump-style zips in `~/Downloads/vh_nw_saturn/`. Each
was unzipped unchanged into its own ignored, previously empty folder. Treat
these files as immutable; derived images belong under `build/`.

| Supplied archive | SHA-256 | Local folder |
| --- | --- | --- |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).zip` | `aac5b2d0a36eee5cda62ec12c67ae2db896832baece72e885b373561e36e2c49` | `local/disc_images/vh_saturn_jp_1m/` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (2M, 4M).zip` | `1bbebc01d1c2874b39deeb63bc8307720804f64f3a4d1f43182c9093f4d97a7e` | `local/disc_images/vh_saturn_jp_2m4m/` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (3M).zip` | `1c320343fe0faf9a0807b8615952428345e5c93bbac26e2198de66517f5cd83c` | `local/disc_images/vh_saturn_jp_3m/` |

**Working image (user decision, 2026-11-13):** the project works from the
1M image only. The 2M/4M and 3M folders were deleted locally the same day,
since their data track is identical; their archives remain in
`~/Downloads/vh_nw_saturn/` and their hashes stay below as provenance.

Release description: `Vampire Hunter: Darkstalkers' Revenge (Japan), Sega
Saturn T-1202G V1.000 19960128; Redump discs 3677 (1M), 3681 (2M, 4M), and 1456
(3M)`.

**Database match: CONFIRMED (`ENV-007`, 2026-11-25).** The working 1M image's
Track 1 (`493,741,248` bytes, CRC-32 `94c313ab`, MD5
`beef086bf1235c752ef9d2b693a5642c`, SHA-1
`77390da7878762e3963bb54d8a7c3ba3f86800ed`) and Track 2 (`3,880,800` bytes,
CRC-32 `9921da39`, MD5 `93f7afdb4d52616e7ce7137e8f2fbf06`, SHA-1
`780688b058e41b5fa85440b74a9339723304bb84`) match Redump disc `3677`
(`http://redump.org/disc/3677/`) across size, CRC-32, MD5, and SHA-1.

The labels `1M`, `2M, 4M`, and `3M` are JVC glass-mastering batch ring codes
(`T-1202GP-00715 <batch> C 62`, Mastering SID `IFPI L223`). Every retail
pressing shares the exact same Track 1 and differs only by a 1-4 stereo sample
offset in Track 2:

| Redump ID | Label | Serial / Version | Ring batch(es) | Track 1 CRC-32 / SHA-1 | Track 2 CRC-32 / SHA-1 |
| --- | --- | --- | --- | --- | --- |
| `3677` | `(1M)` (working image) | `T-1202G` V1.000 | `1M1`, `1M2`, `1MB1` | `94c313ab` / `77390da7…800ed` | `9921da39` / `780688b0…4bb84` |
| `3681` | `(2M, 4M)` | `T-1202G` V1.000 | `2M2`, `2M3`, `2MC1`, `4MB3` | `94c313ab` / `77390da7…800ed` | `ea2afe21` / `bab86fcf…c01f` |
| `1456` | `(3M)` | `T-1202G` V1.000 | `3M1`, `3MB1` | `94c313ab` / `77390da7…800ed` | `8b3d5dce` / `d032b23e…22d0d` |
| `20095` | Sample | `ST-1202G` V0.001 (1995-08-25) | `1MM1` | `90b7af0c` / `be5fa9b7…3c4a` | `ea2afe21` / `bab86fcf…c01f` |

RetroAchievements disc header MD5 (1M Track 1 sector 0 user data, first 512
bytes): `0028d288ca2e19d5267e4601bee148dc`.

Hashes were produced with
`./invenv.sh python -m tools.disc.hash_source --json local/disc_images/<folder>/*`
(logs: ignored `local/logs/env006-hashes-*.json`) and agree with an
independent `shasum -a 256` of each CUE and track 1.

| Filename | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (1M) (Track 1).bin` | 493741248 | `73cc150ba563e39a420ac57589cc318cb01eec0365fe405aa386249019384c39` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (1M) (Track 2).bin` | 3880800 | `d251a9d05e356d251bab9e8ecf9130dc790e26c8efe32f621a222f22e4d8eeaf` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue` | 295 | `548e780dc8254e0e85038c74e2075df393bfe3e59498b08b26b186884b0c2c67` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (2M, 4M) (Track 1).bin` | 493741248 | `73cc150ba563e39a420ac57589cc318cb01eec0365fe405aa386249019384c39` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (2M, 4M) (Track 2).bin` | 3880800 | `deb011d334e19728d1ae584f1a5c51045a16dd00e18e0925157c6346d4350f02` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (2M, 4M).cue` | 303 | `98eb26db5fc024fe08ec77846f70709e598ab6cc827b043132aeb60d2e05f974` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (3M) (Track 1).bin` | 493741248 | `73cc150ba563e39a420ac57589cc318cb01eec0365fe405aa386249019384c39` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (3M) (Track 2).bin` | 3880800 | `ed12a6985395e3fe536ba952aafe33d36e5b8fca5c5a48d137d2fa027fca3c82` |
| `Vampire Hunter - Darkstalkers' Revenge (Japan) (3M).cue` | 295 | `1b75aa2a5735d249381f1b826b0d434360ad4ed8214d3a3083a1a07d3a79c8e7` |

## Observations (2026-11-13, static, no emulator)

- **The three pressings share one data track.** Track 1 is byte-identical in
  all three (`73cc150b…4c39`). Track 2 differs only by position: its
  non-zero audio runs from byte 417,076 (1M), 417,080 (2M, 4M) and 417,060
  (3M), and the 3,234,280-byte runs are identical once aligned (a write
  offset of +1 and -4 stereo samples against 1M). Only the CUE's file names
  differ otherwise. So the game data is one Japanese release; a patch built
  for track 1 fits all three pressings. Which pressing a release names is
  part of `DOC-002`.
- **Layout.** Track 1 `MODE1/2352` (209,924 sectors, FAD 150-210,073), track
  2 `AUDIO` (1,650 sectors including a 2-second `INDEX 00` pregap and a
  20-second playable track). `CATALOG 0000000000000`. Track 2 contains a
  repeated Japanese data-disc playback warning (**CONFIRMED**, D-054).
- **System area (track 1, sector 0).** `SEGA SEGASATURN`, maker
  `SEGA TP T-12`, product `T-1202G`, version `V1.000`, date `19960128`,
  `CD-1/1`, area `JT`, peripherals `J`, title `VAMPIRE HUNTER`. These first
  512 user-data bytes are what RetroAchievements hashes; a release patch must
  keep them unless a decision says otherwise
  (`docs/lessons_from_xvsf.md`, lesson 3).
- **ISO 9660.** `tools.disc.iso9660 --check`: 0 bad sync, 0 non-Mode-1, 0
  address mismatches. Volume ID `VAMPIRE_HUNTER`; root at LSN 20, 20,480
  bytes; 415 files, no subdirectories, none past track 1. Volume space size
  211,574 blocks = track 1 plus track 2. All 415 files (429,299,487 bytes)
  were extracted to the ignored `local/extracted/saturn_jp/` (from the 1M
  image; the others are identical). `iso_listing.json`: name, LSN, size and
  SHA-256 of each file.
- **Comparison with the US release** is in `references/saturn_us/README.md`.
