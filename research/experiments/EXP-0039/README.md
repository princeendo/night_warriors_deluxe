# EXP-0039: Donovan's Second Region Guard

Task: AUD-003 follow-up (`docs/known_unknowns.md`: "What does Donovan's
second region guard play?")
Status: DONE
Confidence: CONFIRMED (Japanese release, live and replayed); SUPPORTED for
the US release (identical code, flag control)

## Observation

`EXP-0033`: `PL14` skips a call through `0x0603A76E` (code `0x1B2`) at
`0x060033C4` when the region flag is non-zero; no session or replay had
reached it.

## Static Reading (`PL14.O`, base `0x06001000`; the same in both releases)

The call ends `0x06003356`, a routine that starts an action from table
`0x06001268`. Its only caller is `0x060033D4`, which returns early unless
the object's byte `+0x228` is 1, then checks `0x0602D160`. In the session
below every call came from `0x0600369E` (return `0x060036A2`), right after
`0x060034CA`, which keeps the newly pressed buttons (word `+0x39C` xor
`+0x39E`, mask `0x0770`) and passes only when a punch and the kick of the
same strength are pressed together (bits `0x070` and `0x700 >> 4`).

## Live Session (with the user, Japanese 1M)

`research/experiments/EXP-0036/options_watch.py local/aud005/donovan-jp
<JP cue> pc:060033C6 pc:0600B3C6 pc:060033D4 pc:0600B3D4` (the script now
takes `pc:` arguments). The user played Donovan against Victor trying
every motion. `0x060033D4` ran 48 times; the guarded call `0x060033C6` 4
times (frames 8,430, 8,668, 9,307, 9,798), each from `0x0600369E` with
action 0 and table `0x06001268`. Donovan's `+0x228` (object `0x06076C70`),
read from the one-second states: 1 at `0131`-`0132`, `0142`-`0145`, `0153`,
when the screenshots show his sword stuck upright in the floor after a
special move; 0 or 2 otherwise.

## Replays (no user)

1. Injecting light punch + light kick (on-hit write `0x0607700C` =
   `0x0110` when `0x060034D2` runs) into states `0126`-`0174`: `0x060033D4`
   runs in every one; the guarded call follows exactly in `0132`, `0144`
   and `0153`, the states with `+0x228` = 1.
2. `EXP-0008/dense.py` (now takes `PC:ADDRESS=HEX` on-hit writes) from
   `0132`, 240 frames: with the press, flag 0, sample **`0x4F2EA`** (8-bit,
   `0xD00` bytes) starts 5 frames after the press; with the Japanese flag
   written to 2 (`060808EA=02`), it never does, and every other sample is
   the same. Without the press, `0x4F2EA` and six other samples (the
   action's own) are absent.
3. `PL14.O` of the two releases differs over `0x060032A0`-`0x06003740` only
   in literal-pool words (relocated variables and routines; the flag
   `0x060808EA`/`0x0608089A`): the code is the same, so the US release,
   whose flag is 2, skips the call as the flag-2 control does.

## Conclusion

**CONFIRMED (Japanese):** with Donovan's sword planted in the floor,
pressing a punch with the same-strength kick plays sample `0x4F2EA`
through the second guard; with the region flag non-zero it does not.
**SUPPORTED (US):** identical code. In the edition build (D-034) this guard
reads the content byte C like the first, so US Enhanced and JP original
play it and US original does not (not played on that build).

## Uncertainty

- The move that plants the sword and the action's name are not
  identified; the screenshots show the sword in the floor.
- The sample was identified by address, not listened to.
