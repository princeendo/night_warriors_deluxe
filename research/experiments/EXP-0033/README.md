# EXP-0033: Donovan's Region-Gated Sound

Task: AUD-003
Status: DONE
Confidence: CONFIRMED (`PL14` is Donovan; the first guard holds back one
sample at his win, and opening it plays that sample in US, from post-KO
states, then a cold boot)

## Observation

`EXP-0014`: `PL14.O` makes two sound calls (through `0x0603A76E`, codes
`0x1B4` and `0x1B2`) only when the region flag is 0; the guards' `bf` are at
file `0x111C` and `0x23C4` (P1 `0x0600211C`, `0x060033C4`).

## Build

`research/experiments/EXP-0033/build_donovan.py`: the `EXP-0032` image plus
both guards made `nop` in `PL14.O` and `PL14.O2` (Track 1
`64344d5875bd47e9e3f186b20dd64672803d43fe52a425ac6fbf30b1316c984e`).

## Sessions (with the user, sound recorded)

`EXP-0018/session.sh` (now takes the image and records sound):

| Session | Image | Play |
| --- | --- | --- |
| `local/aud003/jp-session` | Japanese 1M | Donovan beat Victor; win pose; Japanese win quote |
| `local/aud003/us-session` | `build/us_en_donovan` | Donovan beat Victor; win pose; English win quote |

At a pre-KO state of each (`jp` `f00010037`, `us` `f00007677`), `PL14.O`
matches WRAM-H at `0x06001000`: **`PL14` is Donovan's code** (player 1).

## Replays From Those States

1. `EXP-0008/dense.py` (extended here with an optional image and RAM writes)
   over 900 frames: the patched US run and the same run with both guards
   restored in RAM (`0600211C=8B08`, `060033C4=8B03`) start **the same 15
   samples**; the Japanese run starts samples the US runs do not, among them
   a looping 8-bit sample at `0x1B4B2` (loop `0x1845`-`0x2150`) from frame
   169 through the win pose.
2. PC logs (`EXP-0010/force.py --log-pc`): in the Japanese replay the block
   that holds the first guard (`0x060020A0`-`0x0600212A`, a per-object state
   machine) runs at frame 180, and the guarded call follows (`0x0600211E`);
   in the patched US replay **the block is never entered**, with the flag at
   2 or written to 0 at the state.
3. The block's inputs (`PL14` literals; every Japanese one is the US one +
   `0x50`, so the code is the same): the variable it tests second
   (`0x0608097B` US / `0x060809CB` JP) is `00` in the US state and `01` in
   the Japanese one; nearby bytes differ widely between the two states.

## Why the First US Replay Never Reached the Block

The US state `f00007677` is about 80 frames before the KO, and a replay sends
no input. Without the user's final attack the replayed round never ends:
the shots (`local/aud003/pc-us4/shots`, every 6th of 60) show the fight going
on, the timer 58 → 38, Victor standing. The Japanese state happened to
reach the KO without input. So the earlier "the US never enters the block"
was a test that never reached the win, not a regional difference.

## Replays From Post-KO US States

Same patched image, logging `0x06002088` (the state routine), `0x0600211E`
(the first guarded call) and `0x060033C6` (the second), 60 × 15 frames:

| State | `0x06002088` | `0x0600211E` | `0x060033C6` |
| --- | --- | --- | --- |
| `f00007737` | 8 (from frame 183) | 1 | 0 |
| `f00007794` | 8 (from frame 126) | 1 | 0 |
| `f00007851` | 8 (from frame 69) | 1 | 0 |

The same 8 + 1 as the Japanese replay. Then `dense.py` over 400 frames from
`f00007737`, one variable changed (the two guards restored in RAM:
`0600211C=8B08 060033C4=8B03`):

| Sample (start, loop, 8-bit) | Japanese (`dense-jp`) | US patched (`dense-ko-patched`) | US guards restored (`dense-ko-closed2`) |
| --- | --- | --- | --- |
| `0x1B4B2`, loop `0x1845`-`0x2150` | frame 169 | 177 | 177 |
| `0x5687A`, `0x0`-`0x2474` | 177 (8 later) | 189 (12 later) | **never** |

Every other sample starts in both US runs. `0x5687A` is the only
difference, and its bytes (`0x2475`) are at the same sound-RAM address in
both regions (and so is `0x1B4B2`'s data), so the sample is on the US disc
and loaded; only the call is skipped. The looping `0x1B4B2` plays in both
regions; it is not the regional difference.

## Status

**CONFIRMED (replay from post-KO states):** Donovan's first guard
(`0x111C`, code `0x1B4`) holds back one sample, `0x5687A`, which follows his
win sound in the Japanese release; with the guard a `nop` the US build plays
it at the same point; with the guard restored it does not (D-032). The
second guard (`0x23C4`, code `0x1B2`) was not reached in any replay; its
event is UNKNOWN. Confirmed from a cold boot (below). Open: what the second guard's sound
is.

## Which Win Pose Has the Sound

The block at `0x06002088` is Donovan's win-pose chooser. The guarded call
follows only pose 0: pose 1 when the round counter `0x0608096A` (US) is 0,
that is a first-round win; pose 0 for a later round (pose 4/5 under a
`+0x46 = 0x90` test, not met here). So his first-round win never makes the
call in either region.

## Cold Boot

In `EXP-0034`'s cold boot of `build/us_en_sasquatch` (which includes this
change) the user won 2-0 as Donovan; both guards read `0009` in RAM. Round
1 took pose 1, and a replay from its post-KO state (`f00005029`) runs the
chooser 8 times without the call, as expected. Round 2 took pose 0; from
its post-KO state `f00007017`, `dense.py` on the build: `0x1B4B2` at frame
193, **`0x5687A` at 201** (8 frames later, as in Japanese); with the two
guards restored in RAM, `0x5687A` never. Donovan's English win quote is
unchanged.

## Uncertainty and Alternatives

- The sample was identified by address and bytes, not listened to.
- The second guard (`0x060033C4`, code `0x1B2`) was not reached in either
  replay.
