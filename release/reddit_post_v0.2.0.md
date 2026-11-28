**Suggested title**

Night Warriors Deluxe (Saturn) — US/JP restoration & edition-switch patch, v0.2.0

**Post**

I've released version 0.2.0 of Night Warriors Deluxe, my patch for the US Sega
Saturn release of *Night Warriors: Darkstalkers' Revenge*. The first version
brought back all 14 Japanese epilogues in English, Morrigan's missing ending
lines, and several voices and win poses the US release skipped.
This update adds **JP Enhanced**, more victory quotes in US Enhanced, and full
animation for matches between different fighters with a 4 MiB RAM cart.

**What changed**

* **JP Enhanced** is the fourth choice under **EDITION** in OPTION MODE,
  alongside US Enhanced, US Original, and JP Original. It adds Japanese
  translations of the US-only scenes and lines in Morrigan's, Bishamon's,
  Rikuo's, and Huitzil's main endings.
* **56 more victory quotes in US Enhanced** are translated from the Japanese
  Saturn release. All the official US quotes are still in the game.
* **Japanese or US fighter names** can be selected in either Enhanced edition.
  The game saves your **NAMES** setting with your other options.
* **Full animation with a 4 MiB Expansion RAM cart** works for matches between
  different fighters in Arcade and VS when you select **FULL**. The game uses
  the original reduced animation sets in those matchups without the cart.
* **Two sound fixes.** When Anakaris is Player 1, his opponent's attacks now use
  their own sounds. Morrigan's Soul Fist trail now pans with the fireball.
* **The Appendix** is unlocked by default.

**Caveats**

* Testing in Mednafen included two Arcade rounds with **FULL** and a 4 MiB
  cart. Real Saturn timing and stability for that feature are still unverified.
* **JP Original** runs the US game in Japanese mode, so you'll still see the US
  title screen and intro logo.
* The screen and audio comparison is still in progress.
  [Remaining differences to check](https://github.com/princeendo/night_warriors_deluxe/blob/main/docs/coverage_exceptions.md)

**Downloads**

You need your own untouched US BIN/CUE of *Night Warriors: Darkstalkers'
Revenge* (Redump disc 5836, T-1208H). The zip contains the xdelta patch and a
README with the expected hashes.

* [xdelta Patch](https://github.com/princeendo/night_warriors_deluxe/releases/download/v0.2.0/night_warriors_deluxe_0.2.0_xdelta.zip)

**Further Development**

* [GitHub Repo](https://github.com/princeendo/night_warriors_deluxe)
* [Release Page](https://github.com/princeendo/night_warriors_deluxe/releases/tag/v0.2.0)

You can use the tools and build scripts in the repo to make your own version.

**How to patch**

* Apply the xdelta patch to the original Track 1 BIN using
  [Delta Patcher](https://github.com/marco-calautti/DeltaPatcher/releases) or
  [Rom Patcher JS](https://www.marcrobledo.com/RomPatcher.js/).
* Give the patched Track 1 BIN its original filename and keep Track 2 and the
  CUE as they are. The full steps and expected hash are in the
  [release README](https://github.com/princeendo/night_warriors_deluxe/blob/main/release/README.md#apply-the-patch).

**Images to attach (remove this note before posting):** use the four files in
`build/reddit_0.2.0/`, in the order and with the descriptions in
[`reddit_images_v0.2.0.md`](reddit_images_v0.2.0.md).
