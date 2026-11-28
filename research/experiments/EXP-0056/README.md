# EXP-0056: Shared ending text and Victor's reduced assets

- Task: COV-001 (FILE-05)
- Status: DONE for the static identification
- Confidence: CONFIRMED for the archive contents and stock loader selection

## Observation and Hypothesis

EXP-0035 identified three differing data files. The stock fighter loader
from EXP-0040 suggests `P03_` is a reduced fighter set, while `P00` is
outside the fighter index. If the two loaders use them for separate
purposes, the disassembly should show a startup call for `P00` and a
fighter-indexed call for `P03_`. Comparing the files after identifying
their readers should locate the content changes.

## Controlled Comparison

Read the same calls, tables and file structures on the untouched JP 1M
`T-1202G` (Redump 3677) and US `T-1208H` (Redump 5836) images, varying
only the region. The full `P03` archives and `P00.SPR` are byte-equality
controls. The extracted files and `MAIN.BIN` match the source ISO
listings for [JP](../../../references/saturn_jp/iso_listing.json) and
[US](../../../references/saturn_us/iso_listing.json).

## Result

### Demitri and Pyron main endings

Both releases preload `P00.SPR` and `P00.BIN` at startup. `P00.BIN`
provides the main-ending page tables for fighter IDs 1 (Demitri) and 12
(Pyron). The main-ending renderer adds 3 to the language byte for those
two fighters and indexes six pointer-and-mode entries. This selects
shared slots `0x1E5`, `0x1E6` or `0x1E7` in place of the general ST2
slots. A page pointer is relative to the address of its own 32-bit table
entry.

| Item | JP 1M | US |
| --- | --- | --- |
| Startup calls to load `P00.SPR` and `P00.BIN` | `0x06013F44`, `0x06013F4A` | `0x060121CC`, `0x060121D4` |
| Ending renderer tests fighter IDs 1 and 12 | `0x06036C76` | `0x0603641E` |
| Ending slot table | `0x0605ACF0` | `0x0605AC10` |
| Japanese, English and Spanish `P00` slot pointers in WRAM-H | `0x06091F3C`, `0x06091F40`, `0x06091F44` | `0x06091EEC`, `0x06091EF0`, `0x06091EF4` |

The 1,179 differing file bytes cover English page pointers and seven
English page records (IDs `00`, `02`, `05`, `06`, `08`, `09`,
`0A`). Japanese and Spanish records match across discs. The stock US
selector draws the US English copies. All 11 US English page bodies
match the corresponding `ST2USA.BIN` entries used in EXP-0030 as
comparison text. All 14 Japanese bodies likewise match `ST2JPN.BIN`.

The archived US Demitri ending checkpoint from EXP-0029 has
`P00.BIN` at `0x060C1C38`. Its English slot points to
`0x060C4DD0`, and the bytes there match the disc English table and
payload. The active page ID at `0x06076462` is `06`. The text
cursor at `0x06076468` has reached `0x060C55B0`, the end of page
06. The checkpoint preview shows the matching English page over
Demitri's ending artwork.

### Victor's reduced animation set

Fighter index 2 (roster ID 3, Victor) uses `P03.BIN` and `P03.SPR`.
For the reduced set the loader adds 14, yielding index 16 and the
`P03_` filenames. Both regions use those same mappings.

| Table | JP 1M | US |
| --- | --- | --- |
| Fighter BIN filenames | `0x0606ABA4` | `0x0606AB04` |
| Fighter SPR filenames | `0x0606A110` | `0x0606A070` |

The full set matches exactly across regions. In the reduced set,
`P03_.BIN` has the same slot directory and changes 28 bytes under
slot `0x01E` and 18 under `0x253`. `P03_.SPR` has 1,099 sprite
blocks on JP and 1,102 on US. In order, 1,094 payload blocks are
byte-identical. The archive also has descriptor and auxiliary
sections, so the block counts alone do not establish a change in
the number of displayed frames.

## Conclusion and Open Check

The shared-archive change is a disc text difference for two main
endings. The other two files are a retail Victor difference confined
to his reduced set. It remains open which movements or displayed
frames use the altered Victor records. The discriminating follow-up
is a paired retail Victor match in the reduced set with identical
inputs and a traced sprite block selection. A `FULL` mirror gives
a same-content control.

## Reproduction

Python 3.13.13. Run from the repository root with the already-hashed
retail extractions.

```sh
./invenv.sh python research/experiments/EXP-0056/audit_assets.py
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x060121C8 --end 0x060121D8
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_jp/MAIN.BIN \
  --base 0x06013A00 --start 0x06013F40 --end 0x06013F4E
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x060363FA --end 0x06036498
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_jp/MAIN.BIN \
  --base 0x06013A00 --start 0x06036C52 --end 0x06036CE0
shasum -a 256 local/end003/us-01-dump/{wram_h.bin,preview.png}
```

The existing EXP-0029 evidence was read from the D-006-validated WRAM-H
extraction in `local/end003/us-01-dump/`.

| Evidence | Bytes | SHA-256 |
| --- | ---: | --- |
| `wram_h.bin` | 1,048,576 | `19eb4bea339be318bb3c2f8b74fb1415a44911e62a790cceb4d8fa6342add67d` |
| `preview.png` | 38,233 | `cf1daf5bf3c82090fd602e4785103ba306f4d4261f065222f9c21f09c23d8c18` |
