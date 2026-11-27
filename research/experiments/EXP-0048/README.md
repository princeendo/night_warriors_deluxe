# EXP-0048: Keep displayed fighter names independent of edition

Task: LOC-001

Status: DONE

Confidence: CONFIRMED for the saved preference, original-edition behavior,
in-fight name tiles and retained English quote in the tested Arcade match.
SUPPORTED for the remaining readers by the region-flag and table trace.

## Observation and hypothesis

D-015 identified stock JP and US fighter-name graphics in both retail
programs. Seven identified call sites share six literals for fight names,
loading and win artwork. Two additional literals select results and cast
names. These reads can consult a saved name preference without changing the
region setting used by dialogue, quotes, sound and other behavior.

## Controlled change and prediction

Add NAMES to OPTION MODE with EDITION, US and JAPANESE values. EDITION uses
the selected edition's usual names. US and JAPANESE force that set of
displayed fighter names in either Enhanced edition. Both Original editions
use their own names. A cold boot with the same backup save should remember
the preference. The quote language and edition flag should follow EDITION.

## Inputs and change record

US T-1208H V1.001 Track 1 `d0960087…70da`. JP 1M's alternate sprite data
and the corresponding pointers were compared in EXP-0015. Mednafen 1.32.1
agent build with patches 0001 and 0002. The test build's Track 1 SHA-256 is
`60f3d607f2d713dc92785f09d8d02265cc4331cf6a5a21b766081163e12e4361`.

The settings block uses spare byte `0x13` (`0x060830C7`) for the
preference and byte `0x14` (`0x060830C8`) for the resolved value. Stock
and existing Deluxe saves default to zero, meaning EDITION. Out-of-range
values use the edition names. The resolver reads the stock region flag
as a fallback and runs after edition application on title frames.

Each listed MAIN literal originally contains `0608089A` and is changed to
`060830C8` in every edition. The resolver leaves the original flag and
language addresses alone.

| Main CPU literal | Surface |
| --- | --- |
| `0x0601A198`, `0x0601A250` | Fight HUD for P1 and P2 |
| `0x0601F244` | VS result board's fighter labels and positions |
| `0x06034188`, `0x060342F0` | Fight-loading name positions and art |
| `0x06042D30`, `0x06042F60` | Win presentation name art |
| `0x060446E4` | Cast-roll name position and art |

The US region flag remains authoritative for the MODE SELECT graphics.
The new preference selects the fighter labels in the table-driven UI.
Names inside prose are part of their edition's scripts, including the
supporting names and PSP epilogue text.

Title cursor end patches at `0x0600536A` (`E109E108` → `E10BE10A`) and
`0x06005384` (`E209E208` → `E20BE20A`) extend the cursor to NAMES.
The three bottom rows begin at `0xB4`, `0xC0` and `0xCC` with Appendix
unlocked. The exit hint stays at `0xD8` (stock `0xD0`). The generated
wrapper and menu path are in EXP-0038's `title_code.py`.

## Actual result

The first build placed the exit hint at `0xE0`. Four frames sampled across
the blink cycle showed it missing. Keeping the hint at `0xD8` and spacing the
bottom rows by 12 pixels made it visible without overlapping NAMES.
In the corrected build, menu input reached all four editions. The saved
Japanese preference remained in storage after switching to the Original
editions and their own resolved names. JP Enhanced accepted US names
while its language and flag stayed Japanese. After restarting with the
same save, US Enhanced showed Lei-Lei in a normal Arcade HUD. Hsien-Ko's
victory quote still drew in English after the forced round ends.

| Capture under `local/exp0048/v2` | Bytes | SHA-256 prefix |
| --- | ---: | --- |
| `reboot/saved-option-c.png` | 15,272 | `804350435091f0f3` |
| `reboot/fight.png` | 30,086 | `0b5528cebe354f1b` |
| `reboot/win.png` | 17,496 | `281eef0646c0a75b` |
| `fresh/jp-enhanced-us-names.png` | 15,197 | `03d2807286c81e4d` |

Use of the independent name value on the remaining surfaces follows from
the traced readers and literals. The cold-boot check directly reviewed
the menu, an Arcade HUD and the English quote. A console check remains.

## Reproduction

```sh
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/names_v2
./invenv.sh python research/experiments/EXP-0048/check_names.py \
  "build/names_v2/Night Warriors - Darkstalkers' Revenge (USA).cue" \
  local/exp0048/review
```
