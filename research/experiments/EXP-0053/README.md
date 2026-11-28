# EXP-0053 — Select the regional wordmark at the start of the title

- Task: UI-002
- Status: DONE (2026-11-28, Mednafen)
- Confidence: CONFIRMED at the tested title and OPTION MODE checkpoints.

## Observation

With JP Enhanced saved, EXP-0052 draws Night Warriors at the start of the
opening title, then switches to Vampire Hunter. It adds the Design F DELUXE
mark in the Enhanced editions and hides it in OPTION MODE. Colin asked for
the correct wordmark from the start, the same release mark in every edition,
and a dimmed mark behind the OPTION MODE text.

## Hypothesis

The EXP-0052 finalizer waits for the settled Night Warriors signature.
Selecting the regional sprites at the stock writer call will use the saved
edition from the first frame and preserve the stock entrance motion.
Inserting the tag there will also place the Options foreground after it.

## Controlled change

Use the same US T-1208H source and JP Enhanced startup record. Compare the
wordmark IDs from the writer before and after moving the selection upstream.
Add the tag after the regional wordmark in every edition and quarter its
RGB555 channel values in mode 3. Keep each pixel's opacity bit and the
existing brighter palette for the opening and title menu.

## Prediction

The first JP animation frame submits only the three Vampire Hunter IDs.
The regular tag is present in Original and Enhanced. OPTION MODE submits a
dimmed texture before its labels. Leaving Options restores the regular tile
and uses the newly selected wordmark.

## Inputs, tools and procedure

- US T-1208H source files and SHA-256 values are in
  [the source inventory](../../../references/saturn_us/README.md). The JP
  sprite IDs come from the JP 1M checkpoints in [EXP-0052](../EXP-0052/README.md).
- Before image `build/exp0052_title_persist_v2` at commit `90c0037`.
  Use its Japanese Enhanced startup record on both images for the paired
  early screenshot. The five-boot validation generates a separate backup
  history by pressing through the game menus.
- After image `build/exp0053_deluxe_title`, Track 1 (493,741,248 bytes)
  SHA-256 `9b0ed0c4f4b0ad7949b98dd2effce9089984b8e1a727dcbb5be23c46ab05b491`.
  `build_manifest.json` records all output files and changed sectors. The
  read-only sector check found zero header errors across 209,924 sectors.
- Python 3.13.13 and Mednafen 1.32.1 with agent patches 0001/0002. The
  driver uses an isolated internal backup-memory home with audio disabled.
  Log the entry of the shared sprite writer at `0x0601B7A2` with a PC
  breakpoint in log mode. At each hit, record the sprite ID in R4 and
  origin in R5/R6. For the updated builds, begin the log after 3,760 frames
  and continue to the settled title. Capture the pre-glass opening after
  3,804 requested frames, then capture the main menu, OPTION MODE, and
  the main menu after the edition switch.

## Actual result

### Opening wordmarks

The prior build sent US IDs `0x00803806` and `0x00803805` starting at
frame 3785 with the saved edition set to 3. The first JP replacement was
at frame 3875, 90 frames later. The revised build submitted JP IDs
`0x0080381E`, `0x0080380E`, and `0x00803825` starting at frame 3785 on
both JP boots. None of the 122 logged wordmark frames on either JP boot
submitted a US wordmark ID. The origin moved during the entrance. The
three US boots submitted their two stock US IDs throughout.

### Branding in all editions

The driver checked the opening, title menu, OPTION MODE and post-switch
title across five cold boots. The sequence was fresh US Enhanced, saved
US Original, saved JP Original, saved JP Enhanced, and saved US Enhanced.
Each capture had one DELUXE sprite at the region's expected position.
Opening and main-menu VRAM matched the original Design F tile byte for
byte. The two Original title menus matched their regions' Enhanced
title-menu screenshots. Switching the edition at Options updated the
logo and restored the normal tile. Both JP saves preserved the US
settings outside the edition byte, and both US saves preserved a prior
JP settings block when present.

### OPTION MODE layering

Each Options capture contained the quarter-intensity RGB555 tile and
submitted the tag before the foreground sprites. In the fresh US
Enhanced screenshot pair, the 632 changed pixels fall within
`(250,128)–(324,145)` on the 352×240 image. Every changed pixel had been
black. All 39 pixels in the comparison box with a previous channel at
or above 128 stayed identical. The brightest added channel was 48 on
the 8-bit screenshot. The screenshot pairs provide a visual check of
the dark tag and the unaffected text.

| Capture under `local/exp0053/` (352×240) | Bytes | SHA-256 |
| --- | ---: | --- |
| `before-early/opening-first.png` (saved JP Enhanced, old build) | 8,643 | `ad868e6f70f0ebba333b9dd3b7e999fd3666e854b3cc90f1bece8290ec290d79` |
| `after-arcade/opening-first.png` (same save, new build) | 9,023 | `72ddd428524db0d391f070b3cf583de2e0968ddf1ad40ba411d87dc748a75d22` |
| `title-check/boot-0-edition-0/options.png` (US Enhanced) | 15,416 | `8c4c393f3c799a1138ddd1ef5bb28d27c762ac396c98443152e5281ae41c8ec5` |
| `title-check/boot-2-edition-2/options.png` (JP Original) | 15,878 | `489b3f061d151d65a77d3325f70cc0473aefa31511c7c367efca0927297b141b` |
| `after-arcade/arcade.png` (first JP Enhanced Arcade round) | 30,070 | `c7f54b97998f3f01732330cf2a1774ec0c074a069b72761f2fbc6417f3229013` |

The previous US Options capture for the pixel comparison is
`local/exp0052/probes/title-persist-check/boot-0-edition-0/options.png`,
recorded in EXP-0052. Decode PNGs using `EXP-0026/pick_text_frame.py`;
compare RGB triplets at equal pixel coordinates. The foreground comparison
box is `(250,127)–(324,146)`, inclusive.

### Binary changes

| File and location | Original bytes | Replacement or emitted bytes |
| --- | --- | --- |
| `MAIN.BIN` file `0xA184`, RAM `0x0601C184` | `0601B7A2` | `06045638`, redirect the sprite-writer call |
| `MAIN.BIN` file `0x33638`, RAM `0x06045638` | 76 zero bytes | `d10a34108902d10a34108b0cd0096202d30932308b07d0096202d30932308b02d008402b0009d008402b0009008038060080380506001000000004d40600b000444c58310600b0040601b7a2` |
| `MAIN.BIN` file `0x1D0C`, RAM `0x06013D0C` | `06045638` in EXP-0052 | `0601AFDC`, stock finalizer |
| `TITLE.O` extension after edition build's 40,446 bytes | EOF | Padding to `0xA000`, marker `444C5831`, then 10,224 bytes of code, commands and tiles from `render()`. SHA-256 of those bytes `876778098125a78216e466ec7b58884dd7a2ac95c744029ff158d62f2f039c56`. SHA-256 of full extension `3bd970a4dc78e5f7933716fb1fdf76905065655b57ce5164a0e1c07ed71760eb`. |
| `TITLE.O` file `0x42F8`, RAM `0x060052F8` | `060148C4` | `0600DC00`, same save wrapper and bytes as EXP-0052 |

The writer caller at `0x0601C0B2` passes an ID and animated position.
The dispatcher checks the two original IDs and the active title overlay
signature before rerouting. The JP positions use the retail differences
relative to the incoming position. The command uses the same VDP1 tile
offset `0x3000` as EXP-0052. In option mode, the SH-2 masks two RGB555
pixels at a time with `0x739C739C`, shifts right by two, and reinserts
the opacity bits from `0x80008000`. The staged tag precedes the
foreground, and the stock finalizer submits the composed list.

## Conclusion

**CONFIRMED** in Mednafen. Selecting the regional ID at the stock writer
removes the US logo flash on saved JP boots. The Design F release mark
appears in all four editions and dims behind the Option Mode foreground.

## Uncertainty

The physical Saturn timing of the extra JP calls and direct-color transfer
remains unverified. The tests used internal backup memory.

## Reproduction

Use a fresh output directory for the emulator so the first boot has no
backup records. The build uses the earlier combined builder as its base.

```bash
./invenv.sh python research/experiments/EXP-0052/build_tag.py build/exp0053_deluxe_title
./invenv.sh python research/experiments/EXP-0052/check_tag.py \
  build/exp0053_deluxe_title/*.cue local/exp0053/title-check
./invenv.sh python -m tools.disc.iso9660 --check \
  build/exp0053_deluxe_title/*' (Track 1).bin'
```

For the before screenshot, use commit `90c0037` and the prior build CUE.
Copy a backup with JP Enhanced saved by OPTION MODE into both quiet
homes, start from power-on, run 3,804 frames and capture the screen. To
reproduce the original trace, log `0x0601B7A2` through settled title with
that same save.

For the Arcade smoke check, continue the new build to 3,900 frames, use
`check_tag.to_menu`, press Start and wait 300 frames, then press A three
times with 60 frames after each press. Run 1,200 frames and verify the
live Arcade overlay header at `0x06001000` is `0x00000676`.
