# EXP-0033: Donovan's Region-Gated Sound

Task: AUD-003
Status: IN_PROGRESS
Confidence: CONFIRMED (`PL14` is Donovan; the Japanese release makes the
guarded call at his win in the session played); UNKNOWN (why the US never
reaches it)

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

## Status

Opening Donovan's guards cannot be judged from this pair: the US match
never reached the code they guard. Clearing the flag at the state does not
change that, so the cause is in the match itself (HYPOTHESIS: which win
pose or result the game chose), or set before the state. Next: more US wins
as Donovan, or find what enters the block (the object's state value at
`+70` is `0x90` there in the Japanese run).

## Uncertainty and Alternatives

- Sample addresses were compared across the two regions; that the sound RAM
  layout for Donovan's bank is the same in both was not checked.
- The second guard (`0x060033C4`, code `0x1B2`) was not reached in either
  replay.
