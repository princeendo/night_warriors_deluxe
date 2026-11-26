# EXP-0045: Morrigan's Soul Fist trail is pinned to the left

Task: AUD-005

Status: DONE

Confidence: CONFIRMED on US T-1208H and JP 1M T-1202G (bug) and on Deluxe
(fix, every edition), in Mednafen.

## Observation

Playtester report (`AUD-005`): Morrigan's Soul Fist trail stays panned to one
side.

## Hypothesis

The trail's sound request carries a wrong screen position, so its pan never
follows the fireball.

## Controlled Change

Measurement runs change no disc bytes. VS with forced fighters (`EXP-0044`
`vsmove.py`): Morrigan (5) against an idle Victor (3), Soul Fist as down,
down-forward, forward + medium punch. The control swaps the sides, or keeps
P1 and crosses her over to the right.

The fix changes one instruction at two sites in both copies of Morrigan's
code (`pan_fix.py`), on disc in the Deluxe build, for every edition (user
decision below):

| File | Offset (RAM) | Original | Modified | Purpose | Observed |
| --- | --- | --- | --- | --- | --- |
| `PL05.O` (P1) | `0x3BE2` (`0x06004BE2`), `0x3DBA` (`0x06004DBA`) | `25 49` (`and r4,r5`) | `25 4B` (`or r4,r5`) | keep the screen position in the queued request | the trail follows the fireball |
| `PL05.O2` (P2) | `0x3BE2` (`0x0600CBE2`), `0x3DBA` (`0x0600CDBA`) | `25 49` | `25 4B` | same | same |

Stock `PL05.O` and `PL05.O2` are both 27,540 bytes (SHA-256
`e775efa4…ae18`, `6d7799d8…5caff`).

## Prediction

Retail: the trail voice keeps one pan whatever her position. Fixed: it moves
from her side toward the target, mirrored for P2, centered in mono.

## Inputs and Provenance

- Untouched US `T-1208H` (Track 1 `d0960087…70da`) and JP 1M `T-1202G`.
- Deluxe `build/us_edition`: Track 1
  `4d70df4243fe2af77eafa7c7209aa2bd2f479b4eb9f2ce6d9e9f8c593aad4451`,
  `TITLE.O` `3855d1737010fc3bd40f6692194cfb8edbb9b03ad39e5a91cd4d047041a144bf`,
  `PL05.O` `d41285ae…d3e4`, `PL05.O2` `37813931…f966` (with the flag-literal
  changes of `EXP-0038` and this fix).

## Tools and Environment

As `EXP-0044`: Mednafen 1.32.1 agent build (patches `0001`, `0002`), muted,
no cart, stereo `-soundrecord`; `vsmove.py` (`--patch-fight` added here for
RAM writes after the fight loads), `slots2.py`.

## Procedure

1. Sample the SCSP voices (sample address, pan) after the Soul Fist, Morrigan
   on P1 and on P2.
2. Trace the sound requests (ID, the queued position at `0x0603A29E`), then
   the object, x and camera at the position helper `0x0603AC44`.
3. Read the caller in `PL05.O` and compare it with every character's
   matching call.
4. Patch in RAM; build; repeat on the image with a crossover, mono, and the
   US Original edition; JP retail as a control.

## Actual Result

**The pinned voice.** After the Soul Fist, voice `s13` (sample `546D4` for P1,
`722D4` for P2; TL `0E`) has DIPAN `16` (far left) with Morrigan on either
side. Her voice `s07` (pan `12` on the left, `03` on the right) and the
impact `s21` (`01` / `10`) follow the positions. JP retail gives the same
`16`. Song 3 (the trail) contains no pan command, so the pan comes from the
game.

**The request.** The trail is a shared sound (IDs `0x5F` / `0xCF`, type
`g=2`; variant `0x1FA` / `0x2FA`, `g=5`). Its queued position (the second
long) is `0x00` on both sides, where her voice has `0x0D` / `0x13` and the
impact `0x11` / `0x0F`. The position helper `0x0603AC44` gets her object
(`0x06076C20`, x `0x22B`, camera `0x1C0`) and returns a valid position. The
caller, `PL05.O` `0x06004BD0`, then does:

```
06004BD6  mov r0,r5        ; position (0-0x1F)
06004BD8  mov.l ...,r4     ; 0x00030020, or 0x00040020 when @(9,r13) is set
06004BE2  and r4,r5        ; position & flags = 0
06004BE4  ... jmp 0x0603A4A6 (enqueue)
```

The same `and` is at `0x06004DBA` (same IDs). Every other character's call of
`0x0603AC44` that combines flags uses `or` (`254B` or `253B`), including
Anakaris's call of identical shape (`PL06.O` `0x060048F6`). JP `PL05.O` and
`PL05.O2` have the same `and` at the same four places.

**The fix** (`or r4,r5`), trail pan over time (frames ~7 apart):

| Run | Trail pan | Result |
| --- | --- | --- |
| Retail US, P1 / P2 | `16` throughout / `16` throughout | pinned left |
| Retail JP, P1 | `16` throughout | pinned left |
| Deluxe, P1 (left, firing right) | `12`, `10`, `00`, `03`, `04`, `06` | left to right |
| Deluxe, P2 (right, firing left) | `02`, `00`, `11`, `13`, `15` | right to left |
| Deluxe, P1 crossed to the right (voice `04`) | `02` | starts on her side |
| Deluxe, mono (`0x060808C0` = `0x200`, set in the fight) | `00` | centered, as every voice |
| Deluxe, US Original (`E=1`), P1 | `11`, `01`, `04` | follows (every edition) |

Her voice, the impact and Victor's sounds keep their pans in every run.
SOUND MODE MONO in OPTION MODE writes `0x200` to `0x060808C0` (STEREO: 0).
The mono run set it after the fight loaded, because VS reloads it from the
save. In the same US Original run with Anakaris on P1, Demitri's fireball
requests bank 2 song 0: the `EXP-0044` fix now applies in every edition.

The `EXP-0042` Appendix check on the final image (`app-regress`, no cart)
gives the same values as before in both boots.

**User decision** (multiple choice, verbatim): asked which editions get the
fix → "All, plus Anakaris fix" (`docs/localization_policy.md`).

| Evidence under `local/exp0045/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `sf-p1/slots.jsonl`, `sf-p2/slots.jsonl` (retail) | 24,524; 24,214 | `6446707f…d2f3`, `4b0ef109…aa80` |
| `sf-p1/sound.wav` (stereo) | 23,356,456 | `15c32bb1bf9a191ff9ab97a7f28b1cd7fa2aa403e2f10f744266bf49cc00bb45` |
| `pos-p1/events.log`, `pos-p2/events.log` | 58,670 each | `697bce14…c864`, `6a5279fa…404b` |
| `obj-p1/events.log` | 59,926 | `cf32600d7eeaefec648f274b2499a690fba2d12961c39ccbc9ba45a676102adc` |
| `or-p1/slots.jsonl`, `or-p2/slots.jsonl` (RAM fix) | 14,104; 13,794 | `3974a666…5b05f`, `79eb497d…1c1c` |
| `dx-p1/slots.jsonl`, `dx-p2/slots.jsonl` | 14,566; 14,103 | `9f198709…b38d`, `4af25108…93d7` |
| `dx-cross/slots.jsonl` | 25,278 | `68b929a6e29174599de95f5a841bc78369fd9b5197977e8c03566c3a1acdc53e` |
| `dx-mono/slots.jsonl` | 14,090 | `ab870641ab84b98e811bd0268c8d41908149d7d9243ad4a6c98cd90b0fadf0a4` |
| `dx-e1-p1/slots.jsonl`, `dx-e1-ana/events.log` | 14,100; 32,916 | `691ffb76…654d`, `1608f3b4…b6d` |
| `jp-p1/slots.jsonl` | 13,800 | `7cf6f962cd1fea5b694062b226aec83a62df0c676bd0e4ddcf01ef7bb7c2da8d` |

## Conclusion

A typo in Morrigan's code (`and` for `or`), present in both retail releases,
wipes the screen position from her Soul Fist trail request, so the trail
always plays from the far left. With `or`, the trail moves with the fireball
on either side, stays centered in mono, and leaves her other sounds
unchanged. The fix is in every edition.

## Uncertainty and Alternatives

- The crossover run sampled the trail only once before it ended (`02`, her
  side). The full sweep was seen from the normal positions.
- The `g=5` variant at the second site (IDs `0x1FA` / `0x2FA`) was not
  triggered; it goes through the same corrected instruction.
- Heard on real hardware: not yet.

## Reproduction

```bash
US="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
JP="local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
DX="build/us_edition/Night Warriors - Darkstalkers' Revenge (USA).cue"
V=research/experiments/EXP-0044/vsmove.py
SF1="1:2000x4,A000x4,8000x2,8020x4,0000x2"; SF2="2:2000x4,6000x4,4000x2,4020x4,0000x2"
./invenv.sh python $V "$US" local/exp0045/sf-p1 --ids 5 3 --fight-wait 2400 --slot-frames 120 --moves "$SF1"
./invenv.sh python $V "$US" local/exp0045/pos-p1 --ids 5 3 --fight-wait 2400 \
  --trace 0603A13E 0603A29E 0603B270 --moves "$SF1"
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/us_edition
./invenv.sh python $V "$DX" local/exp0045/dx-p1 --ids 5 3 --fight-wait 2400 --slot-frames 60 --moves "$SF1"
./invenv.sh python $V "$DX" local/exp0045/dx-p2 --ids 3 5 --fight-wait 2400 --slot-frames 60 --moves "$SF2"
./invenv.sh python $V "$DX" local/exp0045/dx-cross --ids 5 3 --fight-wait 2400 --slot-frames 60 \
  --moves "1:8000x40,9000x3,0000x70" "1:2000x4,6000x4,4000x2,4020x4,0000x2"
./invenv.sh python $V "$DX" local/exp0045/dx-mono --ids 5 3 --fight-wait 2400 --slot-frames 60 \
  --patch-fight 060808C0:00000200 --moves "$SF1"
./invenv.sh python $V "$JP" local/exp0045/jp-p1 --region jp --ids 5 3 --fight-wait 2400 \
  --slot-frames 60 --moves "$SF1"
```
