# EXP-0052 — Isolate the regional title logos

Task: UI-002
Status: DONE (2026-11-28, Mednafen)
Confidence: CONFIRMED for the sprite groups, title rendering and
edition persistence in the tests below.

## Observation

The two retail title screens have different wordmarks over the same-looking
shattered glass. Deluxe currently always shows the US artwork (EXP-0038).
UI-002 calls for the regional logo and an Enhanced-only DELUXE tag.

## Hypothesis

The regional wordmark and shattered glass are separate VDP1 sprite groups at
the opening title. Selecting the wordmark can then be investigated separately
from the glass, subtitle and menu.

## Controlled Change

Vary the selected VDP1 color-bank group in an offline render of the same
retail title dump. Repeat on the other release.

## Prediction

One group will isolate the two different wordmarks. The glass group will
produce matching renders across the two releases.

## Inputs and Provenance

- Retail US T-1208H and JP 1M T-1202G. Disc component hashes are in
  `references/saturn_us/README.md` and `references/saturn_jp/README.md`.
- Instant H stock VDP1 dumps
  `research/memory_dumps/dbg001/{us,jp}-h-vdp1.bin` (512 KiB each, exact
  hashes in EXP-0006). VDP1 was examined because EXP-0006 found identical VDP2
  VRAM across these frames despite the visible title difference.
- Retail opening and title-menu captures
  `local/exp0049/live-{us,jp}/title{,-menu}.png`, 352×240. EXP-0049's
  `retail_run.py` records the frame and input sequence. Menu capture hashes
  are in `EXP-0050/surface_samples.json`. The opening frames are US
  `025b8fd8b0463a02e1aa229c6f8c69215e833e80b1c7a92269561cb586a12209`
  and JP `a166ccb4fd8e610e8151dbd60ab83c8d683c7514845956821056ae0ff7acf0fd`.

## Tools and Environment

Python 3.13.13 via `./invenv.sh`, `tools.memory.vdp1_sprites`, and Chrome
158.0.8127.37 for the preview. The sprite renderer produces grayscale
palette indices and serves to identify shapes.

## Procedure

Run `inspect_sprites.py` from the repository root. Render normal sprites in
color banks `0x7070/0x7080` and `0x7100/0x7110` separately at 352×240 with
the viewport origin `(16,-8)`. Compare the two layers to the region's
captured title. Hash the three named title files on each disc. Search all
extracted files for the first high-variety 32-byte sample from each logo
sprite that supplies one.

## Actual Result

| Group | US VDP1 command offsets and count | JP VDP1 command offsets and count |
| --- | --- | --- |
| Wordmark, banks `0x7070/0x7080` | `0x0BA0–0x0F00`, 28 | `0x0BA0–0x16A0`, 85 |
| Shattered glass, banks `0x7100/0x7110` | `0x0640–0x0B80`, 43 | `0x0640–0x0B80`, 43 |

The wordmark renders visibly isolate Night Warriors and Vampire Hunter.
The glass renders are byte-identical. The JP wordmark group has gaps between
its first and last commands. Grayscale identifies what each group draws.

| Local render under `local/exp0052/` | SHA-256 |
| --- | --- |
| `us-logo-commands.png` | `0bdb24f30f4df098c04a8b47b92d307e5dc02f16d958a6c332c2184c802ca1c5` |
| `jp-logo-commands.png` | `fe5f6d5a93d59c3320c106ce28f310093295871dba756fc93c8072a855bccbbc` |
| `us-glass-commands.png` and `jp-glass-commands.png` | `e2106c6928f06dc14850f6d08eea8038eeb7d74ab2b4fd8a8ab35b524248df75` |

`TITLE.BG`, `TTLDATA.BIN`, and `TTL.SPR` are each byte-identical across
the two discs. The direct search found zero disc matches for the 21 US and 37
JP high-variety samples.

## Conclusion

**CONFIRMED** at the captured opening title. VDP1 draws the two regional
wordmarks using separate commands from the common shattered glass. This
identifies the graphics output to trace back to the game's draw routine.

## Design preview

Colin named the original mockup **Design A** and requested alternatives.
`title_preview.html` compares designs on the same region and screen. The
Enhanced toggle controls whether the label appears.

| Design | Tag treatment | Native overlay origin and size |
| --- | --- | --- |
| A · Gold signature | Warm-gold italic serifs under the right side of the logo | `(264,144)`, 64×16 |
| B · Silver lettering | Cooler italic block letters in the same part of the composition | `(258,145)`, 64×16 |
| C · Crimson plate | Ivory letters on a dark red plate with a copper outline | `(252,142)`, 80×20 |
| D · Centered footer | Spaced gold lettering and short horizontal rules below the subtitle or menu | `(126,217)`, 100×16 |
| E · Painted serif | Gold-painted serif letters with a dark red edge | `(244,128)`, 84×17 |
| F · Chiseled silver | Angular silver-blue letters with a small glint | `(245,129)`, 84×17 |
| G · Crimson slash | Cream letters on a tapered red banner | `(242,128)`, 96×20 |
| H · Brush gold | Hand-drawn gold letters overlapping the lower-right edge of the wordmark | `(224,119)`, 112×34 |
| I · Blooded steel | Notched steel letters with a crimson edge along the lower points | `(245,127)`, 84×18 |
| J · Bloodstone | Angular garnet letters with a pale upper bevel | `(243,128)`, 84×17 |
| K · Fang serif | Bone-colored gothic lettering with narrow crimson fang tips | `(240,126)`, 88×19 |

E–K rotate the whole overlay by the fitted angle of the lower red edge of
the regional wordmark. For each x in 252–330, take the lowest y in 78–165
with red above 110 and above 1.7 times both green and blue. Regress y on x
over the 79 points. The opening and menu captures agree to six decimals
for each region. The fitted slopes are −0.111611 US (−6.3685°) and
−0.128092 JP (−7.2994°). JP overlays are raised three pixels to follow the
position of its wordmark. The table gives the US coordinates before rotation.

Colin supplied the *Street Fighter Alpha 2 Gold* title as a reference for
placing an edition name against a main logo. Design H uses newly drawn
lettering. F and H appear together in the first row of the aligned
comparison. Colin selected F for both Enhanced editions and requested one
more set of horror-themed studies. I–K are presented alongside F.

The earlier browser check matched Design A's overlay pixels to commit
`59ab485`. Design F's four rendered views match pixel for pixel across the
aligned and horror comparisons. The latest check verified capture selection,
overlay bounds and applied slopes in all 48 combinations. Design D's
legibility on a CRT with overscan remains unverified.

## Native implementation

The first US logo command matches the Work RAM staging bytes at
`0x06084CA8` (VDP1 offset `0x0BA0`). A write breakpoint on its first
16 bytes in a retail US replay halted at `0x0601BC3E` with R14 equal to
the staging address. The write watch on the end marker halted at
`0x0601AFE2`. The finalizer at `0x0601AFDC` reads the cursor in
`0x0608C188`, places the marker, and copies the list. The replay path
uses the matching backup cart setting for the EXP-0006 checkpoints.

| Retail title renderer input | US | JP 1M |
| --- | --- | --- |
| Wordmark sprite IDs, in renderer order | `0x00803806`, `0x00803805` | `0x0080381E`, `0x0080380E`, `0x00803825` |
| Resolved renderer positions | `(0xC0,0x50)`, `(0xC0,0x50)` | `(0xE0,0x80)`, `(0xA0,0x58)`, `(0x30,0)` |

These IDs are present in the shared `TTLDATA.BIN` and resolve to loaded
descriptors in the US build's `TTL.SPR` table. Calling the US sprite
writer with the JP IDs at the recorded origins rendered the Japanese
logo in a US retail replay. The first two parts replace the 28 US
wordmark commands and precede the copied subtitle or menu commands. The
last JP part follows them, matching the order in the retail trace.

`tag_probe.py` demonstrated a normal direct-color sprite for Design F.
The probe replaces the current END and advances the cursor by one
32-byte record so the stock copier places a new END. A single submission
did not reliably reach the displayed framebuffer. Repeating it over
four frames showed the tag. The command was
`0000000000a8000006000b1c0103007400000000000000000000000000000000`
at the US title checkpoint. The original control at the cursor began
`8000`. The tile occupies VDP1 offset `0x3000–0x433F` in the active
title command area beyond the end of the list.

### Binary changes in the experimental image

| File and offset | Original bytes | Modified bytes and purpose |
| --- | --- | --- |
| `MAIN.BIN` `0x1D0C` (RAM `0x06013D0C`) | `0601AFDC` | `06045638`, dispatch to a title-gated hook before the stock finalizer |
| `MAIN.BIN` `0x33638` (RAM `0x06045638`) | 60 zero bytes | `d0086202d30832308b09d0086202d30832308b044f22d007400b00094f26d006402b000906001000000004d40600b000444c58310600b0040601afdc` |
| `TITLE.O` `0x42F8` (RAM `0x060052F8`) | `060148C4` | `0600DC00`, Options save wrapper |
| `TITLE.O`, extension after the edition build's 40,446 bytes | EOF | Zero padding to `0xA000` and 4-byte marker `444C5831`. The assembled code, commands and two tiles follow. Wrapper at `0xCC00` (RAM `0x0600DC00`), 144 bytes, SHA-256 `59f58d354b6980f0c3e80c7dd828c082a41202c4a51cedb47b26c3d66102bad1`. Whole extension SHA-256 `d0a104f28c23fddf6bfc7deff212c4356f81e89994ce6387ac99c3372370e1b5`. |

The dispatcher checks the overlay header `0x000004D4` and the appended
marker. The title hook requires the stock US logo signature, a bounded
staging list, and opening-title or title-menu mode (10 or 2). It uses
the existing edition byte, preserves the stock US commands in US modes,
and calls the shared writer in JP modes. It appends one transparent
RGB555 sprite only in the Enhanced editions. Tag textures and commands
are generated by `chiseled_silver.py`. The source disc components remain
T-1208H as recorded in `references/saturn_us/README.md`.

### Brightness and menu overlap

The first disc prototype put the bright tag above the dimmed logo in
OPTION MODE. Colin flagged its brightness and overlap with the labels.
Mode gating keeps the tag on the opening title and Arcade / VS / Option
menu. OPTION MODE retains the game's own dimmed background. The softer
silver highlights lower the mean RGB intensity of the 306 changed pixels
from 230.4 to 179.7 between the bright and softer US title-menu captures.
All 306 pixels are in the tag, bounded by `(251,129)–(322,145)`. The
title menu text is outside this rectangle. The new Options captures
have zero tag commands in all editions.

### Runtime evidence

The experimental combined image is
`build/exp0052_title_persist_v2/Night Warriors - Darkstalkers' Revenge (USA).cue`.
Track 1 SHA-256 is
`7b7fcaee9ad84090a9641443a85b8a3f8cdc5b4b6d3d94660087accd6d6d22f6`.
The sector check found zero sync, mode or address errors in 209,924
sectors. Rebuilding the standard candidate through EXP-0038 reproduced
all prior output hashes.

| Boot check | Opening and title menu | Options and next title |
| --- | --- | --- |
| No saved edition | Night Warriors with Design F | Tag absent in Options. Saving US Original removes it from the title menu. |
| Saved US Original | Night Warriors | Tag absent in Options. Saving JP Original redraws Vampire Hunter. |
| Saved JP Original | Vampire Hunter | Tag absent in Options. Saving JP Enhanced adds Design F. |
| Saved JP Enhanced | Vampire Hunter with Design F | Tag absent in Options. Saving US Enhanced redraws Night Warriors with Design F. |
| Saved US Enhanced | Night Warriors with Design F | Tag absent in Options. Saving US Original removes it from the title menu. |

The previous regular candidate read edition 1 on cold boot with edition
1 in `N_WARRIORS_` and edition 2 in `V_HUNTER_01`. The intermediate
renderer build behaved the same. The stock save selector at `0x060143C6`
and loader at `0x060145BC` both read the language byte at `0x06080882`.
The US base initializes that byte to English before it reads the backup.

The Options wrapper first calls the stock settings pack/save. When the
active language is Japanese, it copies the live 260-byte settings block
to title-time RAM at `0x0600E800` and retains the regional backup device.
It selects the US filename by setting the language to English for the
stock load and write calls. The mirror changes byte `0x11` of the US
startup settings and restores the regional settings, device and language
in RAM afterward. The five-boot run used the same isolated backup memory
throughout. It verified the US settings block byte for byte outside
`0x11` during each JP save, and verified the prior JP settings block
across the switch back to US.

A separate cold boot of the same build entered the first Arcade round,
Hsien-Ko versus Victor. The active overlay header was `0x00000676`.
After the normal title-menu entry, the driver pressed Start, waited 300
frames, pressed A three times with 60 frames after each press, and ran
1,200 frames to the capture.

| Representative captures | SHA-256 |
| --- | --- |
| `title-persist-check/boot-0-edition-0/title-menu.png` | `d88df47a220f1bcc48a4cc99e31f40b29d4257ba0b0773ab6b6d3f866c5b8c21` |
| `title-persist-check/boot-0-edition-0/options.png` | `741a16eef1c6b1e513fe42727e4a62575d7fff45cdda809d2e5015a8b7d3b1d2` |
| `title-persist-check/boot-3-edition-3/title-menu.png` | `272ce9dbbd1904283f32d3db205f5056214e03b19f725b4d264fa55347009b13` |
| `title-persist-arcade/arcade.png` | `fad29b801b178c562c02e05a8a2081fcc23178eb875a67f8fe61d265c8b6e652` |

Paths above are relative to `local/exp0052/probes/`. The RGB555 assets are
4,928 bytes each. Texture SHA-256 is
`26b632dd50ca6775eede97e7c135a038f29c35f0e79565deff7967fe731f0704`
(US) and
`4528d144d3f024ae6873d1fce892902893b23a86d0eec3c43cc32cb7d789c0f2`
(JP).

## Uncertainty and Alternatives

Physical Saturn timing for the extra JP sprite submissions and direct-color
tile transfer remains unverified. Save integration was exercised using
Mednafen's internal backup memory.

## Reproduction

```bash
./invenv.sh python research/experiments/EXP-0052/inspect_sprites.py
```

Build and check the disc in Mednafen 1.32.1 with agent patches 0001/0002.
The drivers mute sound and use an isolated backup-memory home.

```bash
./invenv.sh python research/experiments/EXP-0052/build_tag.py build/exp0052_title_persist_v2
./invenv.sh python research/experiments/EXP-0052/check_tag.py \
  build/exp0052_title_persist_v2/*.cue local/exp0052/probes/title-persist-check
```

Open `title_preview.html` with the retail capture paths above available.
Pick the region, screen and design set to compare. Changing Enhanced edition
hides or shows the four tags. The local browser check is
`local/exp0052/horror-check.html`.

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless --disable-gpu --no-first-run \
  --user-data-dir="$PWD/local/exp0052/chrome-jp-horror" --window-size=800,700 \
  --hide-scrollbars --screenshot="$PWD/local/exp0052/horror-jp-title.png" \
  "file://$PWD/research/experiments/EXP-0052/title_preview.html?set=horror&region=jp&screen=title"
```

For other captures, use `region=us`, `screen=menu`, `set=aligned` or
`set=earlier` as needed and change the screenshot filename. SHA-256 for
horror captures under `local/exp0052/`:

| Screenshot | SHA-256 |
| --- | --- |
| `horror-us-title.png` | `60c708b5fc11ccaacf550c468dc261378538465d98a4c1c23c8f7a15734b02d2` |
| `horror-us-menu.png` | `83f5540646f3bdb9002d67598ed4fec6b331fa0d8765f9fac98f86d989dd635e` |
| `horror-jp-title.png` | `4f2dcb19d105f54cce13fe6d1f0ae4b660876cc7009a5268aea6b6d96521d3ca` |
| `horror-jp-menu.png` | `143a372f53fdb434f0f927e1aa418e514a9739d88c596772b34bd94f2dadc2cc` |
