# EXP-0061: Select the combat hooks when entering a Training fight

Task: TRN-002

Status: DONE

Confidence: CONFIRMED for the tested entry, combat paths, and reset in Mednafen.

## Observation

EXP-0058 through EXP-0060 found three KO sites for Demitri's normal
throw, Victor's hold, and strikes/projectiles. The existing Deluxe
`TITLE.O` task already installs edition-specific code in `MAIN.BIN`
before play. The large zero run in `MAIN.BIN` is a gameplay work buffer
(EXP-0031). The Training experiment uses a title overlay extension.

## Hypothesis

The accepted title-to-game transition can install the three tested
Training variants for a single requested VS fight. A title re-entry can
restore the stock words before another mode starts.

## Controlled change and prediction

Use one derived image and replay two selections from its own cold-boot
VS-menu checkpoint. Both replay the same Demitri/Victor cart-free fight
and the same crouching chain at one vitality. For the Training replay,
set only the request byte before confirming VS. The accepted entry
consumes it and installs the proved variants. Normal VS should KO on
the first strike and enter a new round. Training should keep the clock
running and report the full chain. Returning to the title should restore
the original bytes.

## Inputs and tools

- Untouched US T-1208H source components and hashes are listed in
  [the source inventory](../../../references/saturn_us/README.md).
  `build_training.py` uses the same release builder as the regional
  title build from EXP-0053.
- Before image `build/exp0053_deluxe_title`, Track 1 SHA-256
  `9b0ed0c4f4b0ad7949b98dd2effce9089984b8e1a727dcbb5be23c46ab05b491`.
  Trial image `build/exp0061_training`, Track 1 (493,741,248 bytes)
  SHA-256 `922de53955e659fce19a6dff92e94e9d5932095f1e63dc66becfac48f7ba09fb`.
- Comparing all 415 ISO file payload hashes isolated the change to
  `TITLE.O`; `MAIN.BIN` on-disc SHA-256 remains
  `f9da6413363aaa00adc63ea348621bea10769e0813824f8781b52ef5106e3b3e`.
  `TITLE.O` is 56,066 bytes at relocated LSN 209774, SHA-256
  `8ac668ae58d8cb62607c28334619f656b012cc8e73a0cff7c49b42c9bbe35e78`.
  The sector check reported zero sync, mode, or address errors across
  209,924 sectors. CUE and Track 2 hashes match the stock US inventory.
- Python 3.13.13 and the Mednafen 1.32.1 agent binary identified in
  [EXP-0057](../EXP-0057/README.md). Two gamepads, `CUT`, no cart, volume 0,
  and an isolated save directory. Both branches use the same title
  checkpoint created on this image. The driver sets matchup IDs and
  starting vitality to reproduce EXP-0060 in the first round.

## Binary changes

| Location | Before | After or emitted code |
| --- | --- | --- |
| `TITLE.O` `0x1C`, task slot `0x4D7` | `00008568` | `0000DA04`, one-shot stock restore and tail-jump to the edition wrapper |
| `TITLE.O` `0x3234`, RAM `0x06004234` | `2FD6 4F22 D347 430B E405 D247` | `D301 432B 0009 0009 0600 EA4C`, absolute jump to entry wrapper |
| `TITLE.O` `0xDA00`, RAM `0x0600EA00` | EOF | Zero padding from the prior 52,368-byte EOF, followed by 258 bytes emitted by `overlay()`, SHA-256 `05e70f1c62461789af1165750d05fe736c3b65460a219ddebc0d808dde08c135` |

On the first title task after each overlay load, the task wrapper writes
the stock words below and runs the existing Deluxe edition task.
`0x06004234` is the stock game's start routine. Its wrapper checks for
return address `0x060051A0` (the accepted title-menu start call), cursor
word `1` (VS), and request byte `1` at `0x0600EA00`. This byte is zero in
the emitted overlay. If all checks match, the wrapper clears it and
writes the Training words. Both branches replay the displaced prologue
and initial call, load the next function pointer, and rejoin at
`0x06004240`. The hook uses known title-overlay RAM; the selection happens
before the fighter overlays load.

| Combat RAM | Stock | Training |
| --- | --- | --- |
| `0x0602299A` | `9015 04EE E075 044C 2448` | `0EB5 E048 E202 A026 0E25` |
| `0x0602B726` | `64E3 4F26` | `A046 0EB5` |
| `0x0602B8E4` | `4F26 64E3` | `A014 0CB5` |

A later menu entry can set that one-shot request. This experiment sets it
at the paused title checkpoint using the agent. Once confirmed, the VS
match holds the chosen combat bytes through its in-game rounds.

## Actual result

The image cold-booted to the Deluxe title menu. The request was `00` and
all three sites held the stock words. The matched branches each reached
VS character select and the first Demitri/Victor round from the same
title checkpoint. The unarmed branch retained the stock words. The
armed branch cleared the request and installed all three Training
sequences before character select. They persisted into the loaded fight.

At one vitality the stock branch wrote `01 FF` to the KO bytes on the
first strike. It displayed K.O., credited the round, and opened round two
with Victor back at `0090`. The armed branch registered six lethal strikes
in two repetitions. It showed `3 HIT CHAIN` each time, kept Victor at
`0001`, and ended the sample window with timer `4D` (hex) and KO bytes
`00 00`. The SH-2 executed the on-disc variant's store at `0x060229A2`
once per lethal hit. No code bytes were injected by the debugger.

The cold title checkpoint `check/title.mc0` is 1,714,627 bytes, SHA-256
`18b84573f7533df74bee2f1baaeaf4cabcde7c125480298460e87ccbdd76cf07`.
The activated fight checkpoint `check/on/vs.mc0` is 2,680,205 bytes,
SHA-256 `81425aa2d0b9462f4a5314484dbf097221d6b8cdef221754188e0747bb45359a`.
Both are stored under ignored `local/exp0061/`. The request and hook bytes
are in the `hooks.txt` files. The KO bytes, timer, and vitality readings
are in `reads.txt`; the combat register traces are in `events.log`.

| Capture under `local/exp0061/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `check/title.png` | 14,476 | `dd7ed7d74389a3053470c39b564a7a49544cd175ed59c33470462af9914c529e` |
| `check/off/hit1-after-20.png` | 9,789 | `843c1a722afe136171dd77cfb3f555a3dc6bf458bdc6d477b8a0911fece91081` |
| `check/off/hit2-after-180.png` | 28,707 | `7bb83dda1b583c34e36d20075d268c3c4427e524ffc0c18a6905d68db98d099a` |
| `check/on/hit1-after-90.png` | 29,285 | `c649208e7d1ce91dc2ebde46a4f2b1f464ef678a76b2237718a7c9709b313a4b` |
| `check/on/hit2-after-90.png` | 29,287 | `2cc20cc4592fd005a54d05c5417fc6211735e1e939ea55dadb51b9e9f293b295` |

### Reset to the title

From the activated fight checkpoint, fire a projectile at one vitality,
then use the stock reset chord. The raw pad word is `0F00` and only Start
(`0800`) is newly pressed. The raw and pressed checks are at `0x06013D42`
and `0x06013D4C`. The first reset replay hit the cinematic. Its 3,600-frame
poll limit expired before the title task ran. The corrected replay allowed
the intro to advance and sent Start after 3,600 frames. The title overlay
slot `0x4D7` and its initialized byte were present on return. The request
was `00` and all three combat sites held the stock words again.

`exit-v2/after-reset.png` shows the return to the Deluxe opening title.
It is 15,594 bytes, SHA-256
`9a3f87134c6f3164bd80b8dd172b503beaf6e177996fb9cef721af4817b0b747`.

### Both throw paths in the built image

Two replays from the armed fight state used the attack scripts from
EXP-0058. Demitri's normal throw reached `0x0602B728` twice, leaving
Victor at `0001`. Victor's hold reached `0x0602B8E6` five times across
two holds. Its ticks brought Demitri to zero several times, and the
clamp handled subsequent negative results. Both replays reached the
second throw with clear KO bytes and finished the sample window with the
timer at `4F` (hex). The second hold was still in progress at that sample.

| Capture under `local/exp0061/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `demitri-throw/hit2-after-40.png` | 29,624 | `4339fffda897ed4da9df3b679a58097eb36382df934c2834164c14439805850d` |
| `victor-hold/hit2-after-40.png` | 29,197 | `dc06f9a551d5909bbe57a6acb8bdb12d60ea61abb54dc08431c061f5fcd6ba33` |

## Conclusion and next check

A request from the title selects the tested combat behavior for VS.
The same image supports a stock KO and round transition with a clear
request. The tested reset reaches the Deluxe title with the stock
combat words. This experiment relied on two emulated pads and the
existing VS clock. TRN-003 owns the menu entry, one-controller fighter
selection, untimed practice, quick reset, and the wider move coverage.

## Reproduction

Run from the repository root. Each replay output should be a new directory.

```bash
exp=research/experiments/EXP-0061
build=build/exp0061_training
cue="$build/Night Warriors - Darkstalkers' Revenge (USA).cue"
./invenv.sh python "$exp/build_training.py" "$build"
./invenv.sh python "$exp/check_training.py" "$cue" local/exp0061/check
state=local/exp0061/check/on/vs.mc0
./invenv.sh python "$exp/check_training.py" "$cue" local/exp0061/exit-v2 --exit-state "$state"
probe=research/experiments/EXP-0057/probe.py
./invenv.sh python "$probe" "$cue" local/exp0061/demitri-throw --state "$state" \
  --low-vitality --approach 8000x115 --motion 8010x3,0000x2
./invenv.sh python "$probe" "$cue" local/exp0061/victor-hold --state "$state" \
  --low-vitality --attack-pad 2 --approach 4000x115 --motion 4010x3,0000x2
./invenv.sh python -m tools.disc.iso9660 --check \
  "$build/Night Warriors - Darkstalkers' Revenge (USA) (Track 1).bin" \
  > local/exp0061-sector-check.log
```
