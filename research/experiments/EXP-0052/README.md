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
`title_preview.html` compares the four designs on the same region and
screen. The Enhanced toggle controls whether the label appears.

| Design | Tag treatment | Native overlay origin and size |
| --- | --- | --- |
| A · Gold signature | Warm-gold italic serifs under the right side of the logo | `(264,144)`, 64×16 |
| B · Silver lettering | Cooler italic block letters in the same part of the composition | `(258,145)`, 64×16 |
| C · Crimson plate | Ivory letters on a dark red plate with a copper outline | `(252,142)`, 80×20 |
| D · Centered footer | Spaced gold lettering and short horizontal rules below the subtitle or menu | `(126,217)`, 100×16 |

The browser check verified that Design A's overlay pixels match commit
`59ab485` and that all 16 combinations of design, region and screen fit
within the 352×240 captures. Design D uses the lower edge of the picture.
Its legibility on a CRT with overscan remains unverified.

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
Pick the region and screen to compare. Changing Enhanced edition hides or
shows the four tags. The local browser check is
`local/exp0052/comparison-check.html`.

```bash
'/Applications/Google Chrome.app/Contents/MacOS/Google Chrome' \
  --headless --disable-gpu --no-first-run \
  --user-data-dir="$PWD/local/exp0052/chrome-us-comparison" --window-size=800,680 \
  --hide-scrollbars --screenshot="$PWD/local/exp0052/designs-us-title.png" \
  "file://$PWD/research/experiments/EXP-0052/title_preview.html?region=us&screen=title"
```

For other captures, use `region=jp` or `screen=menu` as needed and change
the screenshot filename. SHA-256 for captures under `local/exp0052/`:

| Screenshot | SHA-256 |
| --- | --- |
| `designs-us-title.png` | `2435ded977602ac3f32999c5614f9a34c04358baaa2f1c7fd471f945b8e79f32` |
| `designs-us-menu.png` | `1e8988cab3f727281318174f8119cdb3faa964179baba56816065eb4eb121617` |
| `designs-jp-title.png` | `303b6db658c7404ce25951476ae15799bb10eb2cd0f3754ef105b5c36111f3c2` |
| `designs-jp-menu.png` | `f8b30a4d020db20c1aabd11ea821d8bb5b2ba095f0b5a347bf3f339c7d95fdc0` |
