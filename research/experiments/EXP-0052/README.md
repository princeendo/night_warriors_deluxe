# EXP-0052 — Isolate the regional title logos

Task: UI-002
Status: IN_PROGRESS
Confidence: CONFIRMED for the sprite groups at the captured opening title.

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

## Uncertainty and Alternatives

The texture and sprite descriptor sources, selection point and draw hook
remain open. The direct byte search tests literal contiguous storage.
Encoded data, a different pixel layout, or framebuffer-dependent processing
could all explain the miss. The identical title files could contain both
wordmarks. For the next runtime test, trace the writer of the first logo
command at VDP1 VRAM offset `0x0BA0` or its staging buffer back to its input
on the US opening title.
Before editing the loader, check whether the same draw path runs on return
from OPTION MODE.

## Reproduction

```bash
./invenv.sh python research/experiments/EXP-0052/inspect_sprites.py
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
