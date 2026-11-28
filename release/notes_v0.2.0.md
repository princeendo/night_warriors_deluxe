# Night Warriors Deluxe (Saturn) 0.2.0

This release expands the first edition-switch patch with a fourth edition and
new improvements to endings, names, victory quotes, animation and sound.

## What's Changed

`OPTION MODE` now offers four saved editions:

- **US ENHANCED** — restores Japanese-only material in English, keeps the
  official US text and quotes, and now includes translated Japanese victory
  quote variants.
- **US ORIGINAL** — the stock US presentation.
- **JP ORIGINAL** — the US code set in Japanese mode, as in 0.1.0.
- **JP ENHANCED** — the Japanese presentation with Japanese translations of
  the US-only additions to Morrigan's, Bishamon's, Rikuo's and Huitzil's main
  endings. Felicia's Japanese ending remains as shipped.

Other changes:

- A saved **NAMES** preference lets either Enhanced edition display the
  Japanese or US fighter names. Original editions keep their edition's names.
- US Enhanced keeps all official US victory quotes and adds 56 new English
  variants translated from the Japanese Saturn records: one for each fighter
  and mirror/vitality condition.
- The Appendix is unlocked by default.
- With a **4 MiB Expansion RAM cartridge**, `FULL` animation now loads full
  animation sets for different fighters during Arcade and VS. Without that
  cartridge, the game keeps the shipped reduced-set behavior. A 1 MiB
  cartridge is not qualified for this feature.
- Corrected shared sound effects when Anakaris is Player 1, so the opponent's
  attacks use that opponent's sounds. Corrected Morrigan's Soul Fist trail
  panning so it follows the fireball.
- The previous release's restorations remain: all 14 English epilogues,
  Morrigan's missing English main-ending lines and suppressed voices, and
  Donovan and Sasquatch voice/pose content.

## Download

| File | Size (bytes) | SHA-256 |
| --- | ---: | --- |
| `night_warriors_deluxe_0.2.0_xdelta.zip` | 66,177 | `45f8ea0883b7db1dc97cacaa2bf8357113a817a738d23abf408a533d5369bef5` |

The zip contains the xdelta patch and a `README.txt` with source and patched
Track 1 hashes. Only Track 1 changes; keep Track 2 and the CUE sheet untouched.
Apply the patch to the untouched US Redump disc 5836 Track 1, whose SHA-256 is
`d0960087520ff305a919dba3b4921edecb5c02d593c73143e0cb9f872c9970da`. The
resulting Track 1 SHA-256 must be
`d74e7476e73b24b2a21f0f3824795cfc9bb5ded698d8ed6678a7a83c72555d6d`.
Application instructions are in the [project release guide](https://github.com/princeendo/night_warriors_deluxe/blob/main/release/README.md).

## Verification and Known Limits

The exact candidate was cold-booted in Mednafen, and the 4 MiB cart-backed
`FULL` path was checked through two Arcade rounds. The user accepted assuming
hardware parity for this feature; real Saturn timing, sprite behavior and
stability have not been independently verified. The full regional surface
coverage task (`COV-001`) remains open, with its remaining areas listed in
[the coverage exceptions](https://github.com/princeendo/night_warriors_deluxe/blob/main/docs/coverage_exceptions.md). `JP ORIGINAL`
continues to use the US code and graphic set, so the US title screen, intro
logo and US-only code differences remain.

The disc header RetroAchievements hash remains unchanged:
`8c7156c2e38f75a9ec54016427967e9e`.
