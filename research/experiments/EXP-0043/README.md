# EXP-0043: Cart-backed FULL animation for different fighters

Task: ANI-003

Status: IN_PROGRESS (Mednafen checks done; the real-Saturn check with a
4 MiB cart remains, before release)

Confidence: CONFIRMED in Mednafen for detection, the fallbacks, both orders of
the largest pair, every fighter's full set, Arcade (rounds, opponent changes,
continue and rematch), VS, and game pace. Real hardware: UNKNOWN.

## Observation

D-037: `FULL` fits one full set in the 1,372,412-byte fighter pools, so
it works only in mirrors. A forced Anakaris vs. Huitzil `FULL` pair needs
883,644 more bytes and resets the console. The allocator has three bump
pools at `0x06076AD8`, with baseline bounds at `0x06076AC0` copied once at
boot (`0x060121D8`). P1's set fills each pool from the bottom
(`0x0601B632` resets the lows) and P2's from the top (`0x0601B654` resets
the highs).

## Hypothesis

If pool 2 (the 151,168-byte VDP2 carve) is pointed at a 4 MiB cart, live and
baseline, the stock allocator can hold any two full sets. Opening the
`FULL` same-fighter branch then lets mixed matchups load full sets, with
no other code change.

## Controlled Change

The RAM prototype changes exactly these in RAM after the title: pool 2 live
(`0x06076AE8`) and baseline (`0x06076AD0`) set to `0x22400000`-`0x22800000`
(the 4 MiB cart, cache-through), both loaded-set slots (`0x0609022C`/`D`)
set to `FF`, and the branch at `0x0602192A` changed from `89 0F` to `A0 0F`.

The build moves the same writes into the Deluxe title wrapper
(`research/experiments/EXP-0038/title_code.py`, routine `cart`, 148 bytes),
which runs every title frame:

| Step | Detail |
| --- | --- |
| Detect | The cart ID at `0x24FFFFFF` must read `0x5C` (4 MiB) four times. A non-destructive RAM test writes `address ^ 0x5AA5C33C` to `0x22400000`, `0x22480000`, `0x225FFFFC` and `0x227FFFFC`, verifies all four, and restores them. It runs once per `TITLE.O` load; the result is kept in a title byte. |
| Redirect (once per boot) | If baseline pool 2 is not yet the cart: baseline and live pool 2 = `0x22400000`-`0x22800000`, both slots = `FF`. |
| Branch | With the cart: `0x0602192A` = `A0 0F` (`bra`): `FULL` skips the reduced-set path for any pair. Without: `89 0F` (stock) is written back. |

The `CUT` test at `0x06021924` comes first and is untouched, so `CUT` still
loads the reduced sets. This lead is from the XvSF sibling (cart ID at
`0x24FFFFFF`, RAM at `0x22400000`): `CPK.EMM` in XvSF `EXP-0053`. It was
used only as a lead and is re-checked here.

## Prediction

With a 4 MiB cart and `FULL`, any pair loads two full sets (indexes below 14)
with no out-of-memory call, and P2's set lands in the cart. With no cart,
a 1 MiB cart, or `CUT`, the loads are stock.

## Inputs and Provenance

- Untouched US `T-1208H` (Track 1 `d0960087…70da`) for the RAM prototype.
- Test image `build/exp0043_cart` (from `build_edition.py`), identical to
  the final `build/us_edition` rebuilt from the same scripts: Track 1
  `8882e154a6c17a04e37cdf02046df53ce145f8e439bc98144d5173c6736872df`,
  `TITLE.O` 35,316 bytes,
  `c3d7459c4644b291653eca3f56904f4d2b10a8a9c1ba4777bd3e933fce2dfb34`.
- Fighter IDs as in `EXP-0041` (one-based `Pnn`).

## Tools and Environment

Python 3.13.13 via `./invenv.sh`; Mednafen 1.32.1 agent build with patches
`0001` and `0002` (`7040f6fe…4cdd`); `EXP-0042/drive.py` for presses,
reads and dumps; `proto.py` (forced attract fights) and `play.py` (Arcade
and VS) here. Carts: Mednafen `-ss.cart extram4`, `extram1`, `none`.

## Procedure

1. RAM prototype from a cold boot of the US retail image (`proto.py
   --branch --pool`).
2. Build the routine into a test image. Cold-boot it, press Start once so
   the title task runs, then force the attract fighters (`proto.py
   --start-press`) under each cart and setting.
3. Cover every fighter's full set with six more mixed pairs.
4. Arcade and VS from the player's path: OPTION, APPENDIX, ANIMATION FULL,
   save, then play with rounds ended by time-over (`play.py`). The timer
   is `0x06080977` and vitality is P1 `0x06076C67`, P2 `0x0607706B`, found
   by diffing WRAM-H dumps at timer 99, 86 and 71.

## Actual Result

**Title task first.** From a cold boot with no input, the game stays on the
logo and the title task never runs (unlock byte still 0 at frame 3,904), so
nothing changes. In play the title task always runs before ARCADE or VS.
The forced runs press Start once.

**Cart and setting conditions** (Anakaris vs. Huitzil unless noted):

| Run | Cart, setting | Loads (index P1, P2) | Pool 2 after | Result |
| --- | --- | --- | --- | --- |
| `proto-4m` (retail, RAM) | 4 MiB, FULL | `P06`, `P11` (5, `0x0A`) | `0x226F51BC`-`0x22800000` (1,093,188 = `P11`) | fight plays |
| `img4m-full-b` | 4 MiB, FULL | `P06`, `P11` (5, `0x0A`) | `0x226F51BC`-`0x22800000` | fight plays |
| `img4m-rev` (Huitzil P1) | 4 MiB, FULL | `P11`, `P06` (`0x0A`, 5) | `0x226E418C`-`0x22800000` (1,162,868 = `P06`) | fight plays |
| `img4m-cut` | 4 MiB, CUT | `P06_`, `P11_` (`0x13`, `0x18`) | `0x22759288`-`0x22800000` (683,384 = `P11_`) | stock sets |
| `imgnone-full` | none, FULL | `P06_`, `P11_` | VDP2, stock values | stock (trace identical to 1 MiB) |
| `img1m-full` | 1 MiB, FULL | `P06_`, `P11_` | VDP2, stock values | stock |

No run logged an out-of-memory call. With the cart, P1's set stays in
WRAM-H and WRAM-L as in stock, and P2's set is wholly in cart RAM, since
top-down allocation tries pool 2 first.

**Every fighter's full set** (4 MiB, FULL): pairs 1-14, 2-13, 3-12, 4-10,
5-9 and 7-8 loaded indexes 0-13 as full sets (`0`/`D`, `1`/`C`, `2`/`B`,
`3`/`9`, `4`/`8`, `6`/`7`), plus 5 and `0x0A` above. There was no
out-of-memory call, and the fights render (`cover-sheet.png`).

**Arcade** (`arcade1`): FULL set through the Appendix and saved, then
ARCADE with the default pick (Hsien-Ko). Stage 1 vs. Victor loaded full
sets `0x0C`/`0x02`: P1's 721,344 bytes in WRAM, P2's 1,012,516 bytes in the
cart. Stage 2 vs. Bishamon reloaded only P2 (`0x07`, 991,736 bytes in the
cart). Stage 3 is a Hsien-Ko mirror (one shared set). Round transitions
(ROUND 2) and the BONUS screen appear.

**Continue and rematch** (`arcade-lose2`): both stage-1 rounds lost by
time-over. CONTINUE? appears, and the game frees both sets (slots `FFFF`,
pools at baseline). After Start and the same pick, the rematch with Victor
reloads `0x0C`/`0x02` to the same pool values as the first fight. Two won
rounds then lead to stage 2 (Bishamon, `0x07` in the cart) and stage 3 (the
mirror). The first attempt (`arcade-lose`) pressed during the select
screen's load and stayed at PRESS START; it was rerun with a longer wait.

**VS** (`vs1`): VS mode with P2 joined by injected presses on pad 2.
Hsien-Ko vs. Donovan loaded full sets `0x0C`/`0x0D`, with P2's 1,013,864
bytes in the cart. Rounds ended by time-over (round marks on the HUD)
kept both sets until the VS RESULT screen, after which both slots are freed
(`vs-sheet.png`).

**Pace** (`pace.py`): first Arcade fight, timer read every 300 frames. With
no cart and CUT (sets `0x1A`/`0x10`), it read 91, 84, 77, 70, 63, 56, 52.
With 4 MiB and FULL (`0x0C`/`0x02`), it read 93, 86, 79, 72, 64, 57, 52.
The fight counts down at the same rate, so the emulated game does not
lag with P2's set in cart RAM.

**Options and save.** In every Arcade and VS run, ANIMATION FULL was set
through APPENDIX and saved, and it held (`0x06080A29` = 1) through every
fight. Persistence across a reboot with a 4 MiB cart is in `EXP-0042`
(`app-next-4m`). After the rebuild, the `EXP-0042` Appendix check
(`app_check.py --deluxe --unlocked-default`, no cart) was rerun on the final
image (`local/exp0043/app-regress-none`). Every value matches the
`EXP-0042` run, and boot 2's log is byte-identical. Boot 1's frame numbers
are one lower throughout.

| Evidence under `local/exp0043/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `proto-4m/trace.log` | 1,741,689 | `f95a39ffb863841173c4c5e69ed083be39ad167a6a60570b0817a486763141a2` |
| `img4m-full-b/trace.log` | 1,741,062 | `e3c9d2fe17c221f40c71ba1861924055a597333e5ce75c212e046a02e6e8594b` |
| `img4m-rev/trace.log` | 1,378,812 | `76bfe71b16e5fbb17b3cab73c07671c9fb17c8f1a99d87cb4fd22b968c8a3c79` |
| `img4m-cut/trace.log` | 915,762 | `8b9b4bdfcc25120d3472fb3aae83fe1cea77a25cd82cf230ce91a6ed26b81074` |
| `imgnone-full/trace.log`, `img1m-full/trace.log` (identical) | 1,092,792 | `f0facc796e2393d0edc4269251e6afa40c73c772ba10b33dd2c30325ac091f6d` |
| `cover-1-14/trace.log` | 865,362 | `80012a14db37f7cf6ea7bfbf76a929a0b477846bdf3a5531da1acfd1f43157ea` |
| `cover-2-13/trace.log` | 733,692 | `70ea9e84604b642a5fe150e5047cbabf7e14514e5050eaebc269631f0d1f31e4` |
| `cover-3-12/trace.log` | 950,412 | `f3e9fe7273a5800db53145ffa2f735081db29d14be0b469770d6823f5caf6b85` |
| `cover-4-10/trace.log` | 830,082 | `e7d07d5a6db477832554e1b4a55377eb8e2acfe1c1875349ad5a942d2c5e34a9` |
| `cover-5-9/trace.log` | 924,581 | `30231ce7bcb75d4bdbf155439bc5efcd8521d05b5b0a37f242e2e656b17ccc18` |
| `cover-7-8/trace.log` | 1,030,421 | `33901fcf859c623548889ad325081be4276f3b63b36e28c85347fd8aa733fe45` |
| `arcade1/reads.txt` | 1,726 | `095cc3adb8f53e4982e320599f8deb6bd0e694bc9b793603eeb0ccf85fcec96d` |
| `arcade-lose2/reads.txt` | 2,535 | `2523d7ddef4cad45ccc06e926af19e2b498dacb0d341c64984358c975469cefa` |
| `vs1/reads.txt` | 1,145 | `507c0c4196dcf0f2104f84b3513e3cf38db9e44354f3a44c0f23393983c95fed` |
| `pace/none-cut/reads.txt` | 213 | `5061cb01eabb4c76f7fb2bf998954796b88d889c4a011f84bf224e5a7b943154` |
| `pace/4m-full/reads.txt` | 213 | `bf27ece3730b0d0ed286ff7bb8af38e38a24704fc4c9a5c0c41f7ccb946d7801` |
| `cover-sheet.png` | 221,273 | `44997441950a4590fda6ec477c542e71af7dbfc95fda2d9cbf10001e002e555b` |
| `arcade1-sheet.png` | 139,924 | `087aa0f27d463e5bf9c6a3bc69e2b7828d01fab59c9bda56cdec743a79758942` |
| `img4m-full-b-sheet.png` | 102,226 | `bbf2cf656d81291f96b9d32725962b9f0b2dc58882434fbcadd2965b65d1908a` |

## Conclusion

In Mednafen, one auto-detecting build is enough. With a 4 MiB cart, `FULL`
gives full animation for any pair, including the largest pair in both
orders and every fighter's full set. It holds through rounds, stage
changes, continue and rematch, and VS, at the stock pace. With no cart, a
1 MiB cart, or `CUT`, the fighter loads are stock. The only difference
with a 4 MiB cart and `CUT` is that P2's reduced set is stored in the cart.

## Uncertainty and Alternatives

- **Real hardware.** Cart RAM sits on the A-bus. Mednafen's timing for it
  is a model, and the stock code never reads fighter data from there. A
  real Saturn with a 4 MiB cart must confirm pace, sprites and stability
  before release.
- **1 MiB cart: not qualified.** Its two 512 KiB banks are not contiguous
  (Mednafen mirrors each through its 2 MiB window). As one pool, one bank
  gives 1,745,532 bytes, short of the 2,256,056 that the largest pair needs.
  Both banks would fit by size (2,420,988 with VDP2 kept) but need two more
  allocator pools. 1 MiB falls back to stock.
- **Before the title task runs** (attract demos shown before anyone presses
  Start after power-on), `FULL` is stock.
- **Editions.** The routine runs in every edition, original ones included.
  It changes nothing unless the player sets `FULL` with a 4 MiB cart.
- **Coverage.** Each fighter's full set was loaded and shown once. Arcade
  used one pick (Hsien-Ko) over three stages; sustained play beyond a few
  minutes of fights was not run.

## Reproduction

```bash
US="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python research/experiments/EXP-0043/proto.py "$US" local/exp0043/proto-4m \
  --branch --pool 22400000 22800000
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/exp0043_cart
C="build/exp0043_cart/Night Warriors - Darkstalkers' Revenge (USA).cue"
P=research/experiments/EXP-0043/proto.py
./invenv.sh python $P "$C" local/exp0043/img4m-full-b --cart extram4 --setting 1 --frames 1500 --start-press
./invenv.sh python $P "$C" local/exp0043/img4m-rev --cart extram4 --setting 1 --ids 11 6 --frames 1500 --start-press
./invenv.sh python $P "$C" local/exp0043/img4m-cut --cart extram4 --setting 0 --frames 1500 --start-press
./invenv.sh python $P "$C" local/exp0043/imgnone-full --cart none --setting 1 --frames 1500 --start-press
./invenv.sh python $P "$C" local/exp0043/img1m-full --cart extram1 --setting 1 --frames 1500 --start-press
for pair in "1 14" "2 13" "3 12" "4 10" "5 9" "7 8"; do  # bash; in zsh split the pair explicitly
  set -- $pair
  ./invenv.sh python $P "$C" local/exp0043/cover-$1-$2 --cart extram4 --ids $1 $2 --frames 1500 --start-press
done
./invenv.sh python research/experiments/EXP-0043/play.py "$C" local/exp0043/arcade1 arcade --stages 2
./invenv.sh python research/experiments/EXP-0043/play.py "$C" local/exp0043/arcade-lose2 arcade --stages 2 --lose-at 1
./invenv.sh python research/experiments/EXP-0043/play.py "$C" local/exp0043/vs1 vs
./invenv.sh python research/experiments/EXP-0043/pace.py "$C" local/exp0043/pace
```
