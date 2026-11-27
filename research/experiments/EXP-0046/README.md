# EXP-0046: JP Enhanced's US-only main-ending additions

Task: END-005

Status: DONE

Confidence: CONFIRMED for the six added pages rendering, the fourth menu
choice, and the Japanese control and script selection in Mednafen.

## Observation and hypothesis

EXP-0030 identified US-only additions inside four main endings. A separate
Japanese script table can use their translations while keeping the same
Japanese language and region flag. The two stock script banks are never
selected together, so JP Enhanced can reuse part of the US script bank in
RAM. Its text should use unused Japanese table IDs with the stock font.

## Controlled change and prediction

Cold-boot Deluxe, select JP Enhanced in OPTION MODE, form a won-Arcade
checkpoint, then force a roster and the ending trigger. For a matched
control, replay the same checkpoint and change only the Japanese script
table selection back to the stock table. The new text should appear in
the JP Enhanced run and the original Japanese pages should appear in both.

## Scope and provenance

The user approved a new Japanese translation of the additions with
Felicia's original Japanese ending retained. Source: the US Saturn's
main-ending records, as identified alongside the Japanese retail pages
in EXP-0030. The approved additions and their positions are:

| Character | US `ST2USA` source | JP Enhanced insertion |
| --- | --- | --- |
| Morrigan | `35`, reassures the butler that she can handle the master | `A1` after stock `34`, before the butler urges her to bed |
| Bishamon | `4F`, promise to remain together | `A2` after his last line to Orin |
| Rikuo | `54` and `56`, other survivors and building a future together | `A3` and `A4` after `54` and `55` |
| Huitzil | `64` and `65`, detection of outsiders and the Omega defense order | `A5` and `A6` during the wait before the stock repair/standby page |

The alternate Felicia story and rewrites of existing dialogue remain in
their source editions. Existing Japanese records, including the epilogues,
remain in the Japanese script path.

## Inputs and binary changes

Source: US T-1208H V1.001, Track 1
`d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da`.
Japanese control text is the byte-identical `ST2JPN.BIN` from JP 1M
T-1202G V1.000 and the stock Japanese table inside the US executable.
Tools: Python 3.13 via `./invenv.sh`, Mednafen 1.32.1 agent build, patches
0001 and 0002. Agent inputs and captures use an isolated, silent home.

- Appended 444 bytes at `ST2JPN.BIN:0x1FA4`, encoded in the stock MOJI
  glyph codes. Relocated the enlarged file on Track 1 with its original
  loader slot. Entry offsets (four-byte big-endian values):

  | Page | File offset | Original | Replacement |
  | --- | --- | --- | --- |
  | `A1` | `0x290` | `0000172E` | `00001D14` |
  | `A2` | `0x294` | `0000172A` | `00001D60` |
  | `A3` | `0x298` | `00001726` | `00001D86` |
  | `A4` | `0x29C` | `00001722` | `00001DD4` |
  | `A5` | `0x2A0` | `0000171E` | `00001E14` |
  | `A6` | `0x2A4` | `0000171A` | `00001E5E` |

- JP Enhanced sets the Japanese table literal at `0x06036840` from
  `0605B1C0` to `0605B1F8`. The 508-byte replacement at `0x0605B1F8`
  holds a new table and the four scripts. Original span SHA-256
  `a17390ded0e0617051bdb9bf97939c1ce06fa4e7aded1abaa1f55a21bc5f6796`,
  replacement `b0769b97cb1524b460aa2541887e80c7e9154488513de87fcb44fb2c685d89ab`.
  `jp_enhanced.patches()` reproduces the bytes. The title wrapper applies
  the JP Enhanced column only at E=3. In other editions it writes the
  original bytes to these locations.
- `TITLE.O` now cycles over 0–3. The two edition-menu bounds that accept
  a saved value or wrap the cursor around the values use 4. Left wrap
  selects 3 rather than 2. The appended apply routine carries three
  columns per patch, all encoded by `EXP-0038/title_code.py`.

## Actual result

The initial Huitzil pages overlapped the results card. Putting them
inside the unused gap before the original last page kept the ending
timing and removed the card overlap. Rikuo's first new page lost its
first seven glyphs with a 10-frame lead-in. Moving it vertically left
the same seven missing. Changing only the lead-in to 84 frames showed
the full first line after Aquaria's entrance. This adds 74 script
frames. The final stock page still shows on the same art.

The fourth option is selectable and the Japanese table literal switches
from a cold boot. Morrigan, Bishamon and Huitzil showed the complete new
text in v2 (`f003d7d9…4156`). V3 changes only the Rikuo lead-in, with Track
1 SHA-256 `6f93cccf5d23bb77001b42215b08a3e48a5a40e054320aee247833bf305f8498`.
The matched stock-table runs showed the original last pages. After the new
pages the enhanced runs returned to the stock dialogue where applicable.

| Page | Local capture | Bytes | SHA-256 prefix |
| --- | --- | ---: | --- |
| Morrigan `A1` | `pages-v2/05-0605b1f8-0a1.png` | 9,025 | `9d5114e632d8cbd5` |
| Bishamon `A2` | `pages-v2/08-0605b1f8-0a2.png` | 6,581 | `44b40f40848019ef` |
| Rikuo `A3` | `v3/pages/09-0605b1f8-0a3.png` | 10,154 | `092e637e4fbad5cb` |
| Rikuo `A4` | `v3/pages/09-0605b1f8-0a4.png` | 10,325 | `5116ee8fdc93a306` |
| Huitzil `A5` | `pages-v2/0b-0605b1f8-0a5.png` | 9,263 | `105d407f96bd5dd4` |
| Huitzil `A6` | `pages-v2/0b-0605b1f8-0a6.png` | 11,884 | `94f49eb57fa6a41e` |

All captures are under `local/exp0046`. Main-ending entry is forced from
a cold-boot match, as in EXP-0019. Physical Saturn verification is pending.
The enhanced scripts run 130 frames longer for Bishamon and 74 for Rikuo.

## Reproduction

```sh
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/jp_enhanced_v3
./invenv.sh python research/experiments/EXP-0046/check_endings.py \
  "build/jp_enhanced_v3/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  local/exp0046/recheck
```

The checks capture by breaking on the actual script page read. Sampling
from a sum of nominal per-page durations was too early on some endings.
