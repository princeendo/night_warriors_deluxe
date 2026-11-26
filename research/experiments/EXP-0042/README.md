# EXP-0042: Capcom's Appendix code and options in the retail releases and Deluxe

Task: APP-001

Status: DONE

Confidence: CONFIRMED for the code, the menus and persistence on all three
images, the layout regression and its repair, and the attract-demo effect of
the unlock byte.

## Observation

`APP-001` asks whether Capcom's stock Appendix code still works in Deluxe
with the `EDITION` row added, and whether Appendix settings persist.
`EXP-0040` found the US unlock call (`0x060045FA`) and its sequence table.
`EXP-0038` added EDITION under CONFIGURATION but never saw the unlocked
layout. `EXP-0036` noted that a line at y `0xC8` sits next to PRESS START
TO EXIT at y `0xD0`.

## Hypothesis

The code is the same five presses on both retail releases and unchanged in
Deluxe, entered in OPTION MODE on the CONFIGURATION line. Deluxe keeps
APPENDIX at index 9 and moves EDITION to 10 when unlocked. The unlock byte
and the Appendix settings persist through the stock save.

## Controlled Change

The code and menu runs change no disc bytes. Pad presses are injected in RAM
through the agent (`drive.py`), one press per step, after the game stores
its pad words for the frame. The repair (after the user's decisions) changes
two things in the Deluxe `TITLE.O`. Rule 12 record:

| Address | Original | Modified | Purpose | Expected | Observed |
| --- | --- | --- | --- | --- | --- |
| `0x06004C46` (file `0x3C46`) | `00 D0` | `00 D8` | PRESS START TO EXIT y | exit line one line below EDITION | even spacing (`after-zoom.png`) |
| `0x06009568` (wrapper start, added code) | (wrapper began `4F22`) | `D0 6B E1 01 20 10` (`mov.l` `0x06080A2B`,r0; `mov #1`,r1; `mov.b r1`,@r0) | Appendix unlocked by default | unlock byte 1 on any save without the code | 1 from the first OPTION frame on an empty save; saved as 1 |

The rest of the appended code moved 6 bytes; its labels are re-assembled by
`title_code.py`.

## Prediction

On each image, the five presses on CONFIGURATION set the unlock byte, and
APPENDIX appears. On Deluxe, EDITION moves to index 10, and changing
`FULL`/`CUT` and saving survives a reboot with the same backup memory.

## Inputs and Provenance

- Untouched US `T-1208H` V1.001 (Track 1 `d0960087…70da`) and Japanese 1M
  `T-1202G` V1.000 (Track 1 hash in `references/saturn_jp/README.md`).
- Deluxe v0.1.0 `build/us_edition` (Track 1 `25e05ec1…f1be`); its `TITLE.O`
  (relocated to LSN 209,774, 35,072 bytes) SHA-256
  `b830f85d527a22b7df46dcd448c0f0690db79f6ebba7002fcf86540d251137c6`.
- Extracted `TITLE.O`: US `bd9fed50…0cd0`, JP `884f8aed…c91e` (`EXP-0040`).

## Tools and Environment

Python 3.13.13 via `./invenv.sh`, `tools.sh2.disasm`, Mednafen 1.32.1 agent
build with patches `0001` and `0002` (`vendor/mednafen/README.md`).

## Procedure

1. Disassemble the unlock checks, OPTION MODE handler and title task in US
   and JP `TITLE.O` (base `0x06001000`), and diff Deluxe `TITLE.O` against
   US.
2. Find why injected presses failed, fix the agent build, and re-run V1-V4.
3. Drive each image from a cold boot with an empty save: enter the code,
   open APPENDIX, change settings, save, and cold-boot again with the same
   backup memory.

## Actual Result

### Static

**Checker** (US `0x06004550`, JP `0x0600443C`). It reads the P1 pressed-buttons
word (US `0x06076AB8`, JP `0x06076B08`). Each frame it tests the next table
entry. A match advances the index and reloads a 14-frame timer. A frame without
a match decrements the timer, and the index resets at zero. So each press
must follow the previous one within 14 frames. Progress is at US
`0x06009418`/`0x06009419` (JP `0x060092DC`). Index 2 and up returns -1, so
the menu skips its own cursor handling (the Down in the code does not move
the cursor).

**Two codes in OPTION MODE** (US handler `0x060052A4`, JP `0x060051D0`;
cursor US `0x0608086C`, JP `0x060808BC`):

| Cursor line | Sets | Table (raw pad words) | Buttons |
| --- | --- | --- | --- |
| 8 (CONFIGURATION) | US `0x06080A2B`, JP `0x06080A7B` (Appendix unlocked) | `0100 0040 2000 0400 0020` | B, X, Down, A, Y |
| 2 | US `0x06080A2A`, JP `0x06080A7A` | `0040 0040 8000 0400 0010` | X, X, Right, A, Z |

Button names follow the standard Saturn pad word as the game stores it.
Start `0x0800` was already known (`EXP-0017`). The other bit names are
checked live below. The tables are byte-identical in both releases (US
`0x06001AB6`, JP `0x06001A48`). Each success calls `0x0603A4A6`/`0x0603ACFE`
with `60, 0x71020, 0xC0`. What `0x06080A2A` unlocks is UNKNOWN.

**Deluxe `TITLE.O` against US.** The tables, checker and code calls are
unchanged. Changed: the task slot header (`0x0600101E`), the APPENDIX draw
block (`0x06004B84`-`0x06004B8B`, literal `0x06004C54`, now a call to the
EDITION `draw`), the Up/Down wrap bounds (`0x0600536B`/`0x0600536D`,
`0x06005385`/`0x06005387`: 9/8 to 10/9), and the line dispatch for cursor 9 and up
(`0x060053FE`, now a jump to `dispatch`), plus 996 appended bytes. `dispatch` sends
cursor 9 to the stock APPENDIX handler `0x06005600` when unlocked. `draw` puts
EDITION at y `0xC8` when unlocked. The stock exit line is still at y `0xD0`.

### Injected presses and the agent build

Injected presses reached the logo but not the title menu (as in `EXP-0038`).
A trace (`local/exp0042/probe7`) showed the agent's write of `0800` to the
pressed word just before the title task ran. The task still read `0`
(R0 at `0x06004FDE`). The game read its emulated SH-2 cache, which the
debugger write had bypassed. With the user's approval ("Patch agent
build"), patch `0002` purges the matching cache lines on both CPUs after
each agent write to work RAM. With the rebuilt binary (`7040f6fe…4cdd`), the
same trace read `0800` and the title menu opened (`local/exp0042/cache1`).

### Live: the stock code and menus (v0.1.0 images and retail)

`app_check.py` cold-boots each image twice with one fresh Mednafen home
(an empty save). The first boot enters the code on CONFIGURATION, then opens
APPENDIX, sets ANIMATION to FULL, and saves. The second boot reads the
bytes back. The button names were confirmed live: Down (`2000`) moves the
cursor, B X Down A Y unlocks, A opens APPENDIX, and Right toggles ANIMATION.

| Image, cart | Unlock (before, after code) | Cursor after APPENDIX | APPENDIX, FULL | After reboot (unlock, FULL, edition) |
| --- | --- | --- | --- | --- |
| US retail, none | 0, 1 | 9, then wraps to 0 | mode 5, `00` to `01` | 1, 1 |
| JP retail 1M, none | 0, 1 (`0x06080A7B`) | 9, then 0 | mode 5, `00` to `01` (`0x06080A79`) | 1, 1 |
| Deluxe v0.1.0, none | 0, 1 | 9, then 10 (EDITION) | mode 5, `00` to `01` | 1, 1, US ORIGINAL |
| Deluxe v0.1.0, 4 MiB | 0, 1 | 9, then 10 | mode 5, `00` to `01` | 1, 1, US ORIGINAL (reads identical to no cart) |

The second code byte (`0x06080A2A`) stayed 0 in each run. The two retail
OPTION MODE and APPENDIX screens are identical, in English on both
(`retail-sheet.png`). The only release difference is the addresses: JP
work variables are US + `0x50`, and the code sits at different program
addresses.

**Regression (Deluxe v0.1.0).** With the Appendix unlocked, EDITION is drawn at y
`0xC8` and PRESS START TO EXIT at y `0xD0`. The 8-pixel text rows touch,
with no gap (`11-option-reboot.png`, `overlap-zoom.png`). The stock unlocked menu
has a free line there. Nothing else regressed.

### User decisions

Asked how to fix it, the user first asked whether EDITION could move to the
Appendix. Told that the Appendix is hidden without the code and that its
screen is full, the user chose "Let's keep it in options and also unlock
appendix by default." (`docs/localization_policy.md`).

### What the unlock byte does outside the menu

Besides `TITLE.O` and the save pack/unpack (`0x06014772`, `0x0601490C`),
two `MAIN.BIN` reads exist. Both are in the attract-demo setup (the function
that writes the demo fighters at `0x06035908`, `EXP-0041`):

- `0x060359B4`: unlocked, the BGM option `0x06080A26` is set to 2 (RANDOM;
  table `0x06009438`: HUNTER, CLASSIC, RANDOM). Locked, it is set to 0.
- `0x06035A8C`: unlocked, `0x06080962` takes a pseudo-random bit
  (`0x060140C6`). Locked, it is 0.

From the US title checkpoint with only the unlock byte changed, the demo
read BGM 0 and bit 0 at 0, and BGM 2 and bit 1 at 1. With bit 1 the
stage is drawn in its alternate colours (red, not green: `demo-pair.png`).
The two runs' sound recordings are byte-identical, so in this demo the
music did not change. `0x06080962` is the scenery variant, not the music.

### Live: the repaired image

`build/us_edition` rebuilt with the two changes (Track 1
`a87f7f705e038f1d8f668956340558ebde02c194db02ddb553b796f35279ab0d`,
`TITLE.O` 35,076 bytes,
`8ecf3a4b7ff0f0f628d1f57b5bcfaec5aee485a129a31f7fd553eae9ea409756`).
It was cold-booted twice with no cart and an empty save
(`app_check.py --unlocked-default`, no code entered). On the first OPTION
frame the unlock byte was 1 and APPENDIX showed. The cursor reached 9 and
10 and wrapped to 0. EDITION changed, APPENDIX opened, and FULL was set and
saved. After the reboot the unlock byte, FULL and the edition were all
back. PRESS START TO EXIT now sits one line below EDITION with the usual
gap (`01-option-a.png`, `after-zoom.png`), ending at y 224 of 240. The
same two boots with a 4 MiB cart (`app-next-4m`, Mednafen "Cart: 4MiB
Extended RAM") gave byte-identical read logs.

| Evidence under `local/exp0042/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `probe7/events.log` (stale cached read) | 4,502 | `d8250fb4f50bac7b3a78653b15eb7d310061cdc8c83aba0fcbcb2a232b0af076` |
| `cache1/events.log` (read after patch `0002`) | 1,998 | `452ddee110dff0c44ceba2dd4ade5fb62795f81ee7060fe24713be6ea74bb901` |
| `cache1/b.png` (title menu) | 14,059 | `9b69cc3f6e6d54b829db1a7f6236dfa8d920e15152f7775d443a89172edb8c3e` |
| `deluxe_TITLE.O` (v0.1.0) | 35,072 | `b830f85d527a22b7df46dcd448c0f0690db79f6ebba7002fcf86540d251137c6` |
| `new_TITLE.O` (repaired) | 35,076 | `8ecf3a4b7ff0f0f628d1f57b5bcfaec5aee485a129a31f7fd553eae9ea409756` |
| `app-us-none/boot1/reads.txt` | 633 | `a4c41f0647a0355cc428b848c220885214e88bc6577003fd34e42b8c939c64dd` |
| `app-us-none/boot2/reads.txt` | 220 | `a776d77608fb6476cb51dcc4a0bd221c45270aedb24a33929dda469b0c335329` |
| `app-jp-none/boot1/reads.txt` | 633 | `944d25e4227fae83231b34d28b03b7101acf971358876d2563911a550062f9b4` |
| `app-jp-none/boot2/reads.txt` | 220 | `da1421e6de3d20e3d9353208256f1a45a18f38697fc798267b656bfd015405c4` |
| `app-deluxe-none/boot1/reads.txt` (also `app-deluxe-4m`) | 695 | `d190e70e2be174ac45dead666a3e38139963d702282512196ea1f8be6b44ec64` |
| `app-deluxe-none/boot2/reads.txt` (also `app-deluxe-4m`, `app-next-none`, `app-next-4m`) | 251 | `e46fdcf2ea4dd611d425414456367a4cebfd8fb42d526e2c0d5cabac43079177` |
| `app-next-none/boot1/reads.txt` (also `app-next-4m`) | 604 | `8113134fbe20ba52c47217c25b211e2d80d51d5335cd3971cebeb8bab0f9bd19` |
| `app-deluxe-none/boot2/11-option-reboot.png` (before) | 15,101 | `2bf9fa38647a17c588b4743bf6e481e93351c0fbcc50f4d42a23a02ff1800fe5` |
| `app-next-none/boot1/01-option-a.png` (after) | 15,097 | `70cc835e1bbc730dd8eec5d9cbfe9d560797fee1497574f856ddbe1e56744cde` |
| `overlap-zoom.png`, `after-zoom.png` | 3,249; 3,562 | `007f4f36…6487`, `0a352ac7…d3af1` |
| `retail-sheet.png` | 68,672 | `de5270799560f5f20a6e83d9285f5e9eb4b3ca5caa4e9a31da4a87171675f90f` |
| `demo-unlock-00/reads.txt`, `demo-unlock-01/reads.txt` | 110 each | `94f5f343…40d4`, `f3f0ef40…ba19` |
| `demo-pair.png` | 68,457 | `f8a420f77840bb28e658b3aa297bb9f429532af6033cc528c4fd73783abd5497` |
| `demo-wav-00/sound.wav`, `demo-wav-01/sound.wav` (identical) | 3,873,564 | `6d5f2e05a101c7c27a85ac671808cf6974ef1f14c952d360b63d34340a5c6c67` |

## Conclusion

Capcom's code (B, X, Down, A, Y on CONFIGURATION, each within 14 frames)
works on both retail releases and on Deluxe v0.1.0. APPENDIX opens, settings
change and everything persists across a reboot, with or without a 4 MiB
cart. The one Deluxe regression was the EDITION line touching PRESS START
TO EXIT once unlocked. By the user's decision, Deluxe now starts with the
Appendix unlocked, and the exit line moves down one line. Both are
confirmed from cold boots. An unlocked Appendix also changes the attract
demo: it sets BGM to RANDOM and randomizes the stage's scenery variant.

## Uncertainty and Alternatives

- What the second code (X, X, Right, A, Z on line 2, `0x06080A2A`) unlocks
  is UNKNOWN. It was not entered.
- The new exit line ends at y 224. A TV's overscan may crop lower lines; a
  real-Saturn check before release covers it.
- Only the US attract demo was checked for the unlock byte's effect. Whether
  the BGM option set to RANDOM changes the demo's music in other demos is
  not settled; this run's audio did not change.
- No cart setup is selected for release yet (`ANI-003`). The 4 MiB cart was
  checked as the likely target.

## Reproduction

```bash
./invenv.sh python -m tools.sh2.disasm --base 0x06001000 \
  --start 0x06004550 --end 0x06004660 local/extracted/saturn_us/TITLE.O
./invenv.sh python -m tools.sh2.disasm --base 0x06001000 \
  --start 0x060052A4 --end 0x06005400 local/extracted/saturn_us/TITLE.O
research/experiments/EXP-0042/revalidate.sh
DX="build/us_edition/Night Warriors - Darkstalkers' Revenge (USA).cue"
US="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
JP="local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
A=research/experiments/EXP-0042/app_check.py
./invenv.sh python $A "$US" local/exp0042/app-us-none
./invenv.sh python $A "$JP" local/exp0042/app-jp-none --region jp
# the v0.1.0 runs used build/us_edition at Track 1 25e05ec1…f1be (git tag v0.1.0)
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/us_edition
./invenv.sh python $A "$DX" local/exp0042/app-next-none --deluxe --unlocked-default
./invenv.sh python $A "$DX" local/exp0042/app-next-4m --deluxe --unlocked-default --cart extram4
ST=$(ls local/emu007/us-a-state/*.mc0)
for u in 00 01; do
  ./invenv.sh python research/experiments/EXP-0042/drive.py "$US" local/exp0042/demo-wav-$u \
    --state "$ST" --wav write:06080A2B:$u 1200 read:classic:06080962:1 shot:demo
done
```
