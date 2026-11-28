# EXP-0055: ISO 9660 descriptive files

- Task: COV-001 (FILE-09)
- Status: DONE
- Confidence: CONFIRMED for the descriptor fields and file contents

## Observation and Hypothesis

The regional file inventory found three nonempty `VH_*.TXT` files in
Japan and zero-length files at the same paths in the US. The hypothesis
was that they were attached to the ISO volume as disc metadata. If so,
the JP primary volume descriptor should name each file in its
corresponding identifier field, and the contents should match those roles.

## Controlled Comparison

Read the same descriptor fields and directory entries from the untouched
JP 1M `T-1202G` (Redump 3677) and US `T-1208H` (Redump 5836) tracks.
The track SHA-256 values are in the
[JP](../../../references/saturn_jp/README.md) and
[US](../../../references/saturn_us/README.md) source manifests.
The field offsets follow Table 4 of the
[ECMA-119 specification](https://ecma-international.org/wp-content/uploads/ECMA-119_5th_edition_december_2024.pdf).

## Result

Both primary volume descriptors reference the same three filenames. Each
root directory record ends in version suffix `;1`. In Japan the entries
occupy distinct sectors and their contents match the descriptor roles.
In the US all three entries have length zero and point to LSN 30.

| Descriptor field | Identifier | JP LSN / bytes | JP contents |
| --- | --- | --- | --- |
| Copyright | `VH_CPY.TXT` | 30 / 59 | Company copyright notice, years 1994–1996 |
| Abstract | `VH_ABS.TXT` | 31 / 431 | Japanese description of the Saturn arcade port, its 14 selectable monsters, and combat features including chain combos and special gauge stocks |
| Bibliographic | `VH_BIB.TXT` | 32 / 40 | English title and subtitle |

JP primary volume descriptor SHA-256
`9b948cbf533f48a86510f7acfaf21fbb732d9443480ba5930d01f6bcb34439bf`.
US descriptor SHA-256
`b3e4a023b1145c2fd10ee0b638d1d7a0f0697d0dff6ba584bffc8f69505ba657`.
Payload hashes also appear in the two source ISO listings. The abstract
decodes as Shift-JIS. The copyright and title files contain ASCII.

The files have an established disc metadata role and the US preserves
the identifiers while omitting their contents. A case-insensitive
literal scan of the extracted files found no references to the names.
The comparison did not test whether a game path reads those sectors.

## Reproduction

Python 3.13.13 with the repository's ISO 9660 reader. Run from the
repository root.

```sh
./invenv.sh python - <<'PY'
from hashlib import sha256
from pathlib import Path

from tools.disc.iso9660 import Track, primary_volume, walk

fields = (
    ("copyright", 702, "VH_CPY.TXT"),
    ("abstract", 739, "VH_ABS.TXT"),
    ("bibliographic", 776, "VH_BIB.TXT"),
)
for folder in ("vh_saturn_jp_1m", "nw_saturn_us"):
    path = next((Path("local/disc_images") / folder).glob("*(Track 1).bin"))
    with path.open("rb") as stream:
        track = Track(stream, path.stat().st_size)
        volume = primary_volume(track)
        pvd = track.user(16)
        entries = {
            entry.path.split(";")[0]: entry
            for entry in walk(track, int(volume["root_lsn"]), int(volume["root_size"]))
        }
        print(folder, "PVD SHA-256", sha256(pvd).hexdigest())
        for label, offset, filename in fields:
            assert pvd[offset : offset + 37].decode("ascii").rstrip() == filename
            entry = entries[filename]
            data = track.read(entry.lsn, entry.size_bytes)
            print(label, entry.path, entry.lsn, entry.size_bytes, sha256(data).hexdigest())
            if data:
                print(data.decode("shift_jis"))
PY
rg -i -a -l 'VH_(ABS|BIB|CPY)(\.TXT)?' local/extracted/saturn_{jp,us}
```
