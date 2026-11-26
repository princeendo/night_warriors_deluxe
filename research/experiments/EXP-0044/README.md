# EXP-0044: Opponent sound effects play Anakaris's copies when he is P1

Task: AUD-004

Status: IN_PROGRESS (fix built and verified; Donovan's ice attack not yet
triggered live)

Confidence: CONFIRMED on US T-1208H and JP 1M T-1202G (bug) and on Deluxe
US Enhanced (fix), in Mednafen.

## Observation

Playtester report (relayed by the user, 2026-11-26): whenever Anakaris is
played from the 1P side, several of the 2P opponent's sound effects are
"loaded in strangely": Demitri's forward-forward dash and fireball, Pyron's
fireball, and the ice attacks of Sasquatch, Donovan and Huitzil. This
happens in Arcade (CPU opponent) and with two controllers, but never with
Anakaris on P2.

## Hypothesis

First: P1's oversized sequence file (`ANAKA1.SEQ`, 1,624 bytes, the largest)
overruns P2's data in sound RAM. Disproven (below). Then: the game, not the
sound driver, requests P2's sounds from P1's bank.

## Controlled Change

Measurement runs change no disc bytes. The fighters are forced in RAM after
the picks (nothing writes the ID bytes between the picks and the load).
Moves are injected frame by frame as held pad words (`vsmove.py`). The
control changes only P1's fighter (Victor instead of Anakaris) or swaps the
sides.

The fix replaces the 78-byte shared-sound lookup in US `MAIN.BIN` RAM
(`0x0603A1C8`-`0x0603A215`) through the Deluxe edition patch list, US
Enhanced only (`sound_fix.py`):

| Address | Original (start) | Modified (start) | Purpose | Expected | Observed |
| --- | --- | --- | --- | --- | --- |
| `0x0603A1C8`-`0x0603A215` | `DE2E 65E3 9258 66E3 3420 8F20 7601 84D4 6350 …` | `DE2E 9259 65E3 66E3 3420 8F20 7601 6050 8806 8B01 6563 66E3 …` | with Anakaris (6) on P1, try P2's character first; the first character with an entry plays its song from its own bank | P2's own shared sounds | as expected (below) |

## Prediction

With Anakaris on P1, P2's shared-sound requests resolve to bank 1 (P1's) on
retail and to bank 2 (P2's) with the fix. Nothing else changes.

## Inputs and Provenance

- Untouched US `T-1208H` (Track 1 `d0960087…70da`) and JP 1M `T-1202G`.
- Deluxe `build/us_edition` with the fix: Track 1
  `33768e2970bac6ee3abfbea07580f79f60af2c1be80414234ba93e631490a2a4`,
  `TITLE.O` 35,488 bytes,
  `251d50e8efb906a38c71ead09f14af22f47dcff2e51dab96377346e8853c4a4c`.
- Sound files: every character sound file and sequence file is
  byte-identical between the releases (`references/*/iso_listing.json`).

## Tools and Environment

Mednafen 1.32.1 agent build (patches `0001`, `0002`), muted, no cart, stereo
`-soundrecord` per run. Scripts: `sndram.py` (sound RAM after a forced
attract load), `vsmove.py` (VS or Arcade with forced fighters, held-input
motions, PC traces, SH-2 writes to the driver command area, SCSP slot
sampling), `slots2.py` (slot SA, pitch, level, pan; extended from
`EXP-0008/slots.py`), `cmds.py` (driver commands from the write log),
`battery.py` (a fixed set of motions and a per-request summary),
`sound_fix.py` (the replacement).

## Procedure

1. Dump sound RAM after Anakaris vs. Demitri and Victor vs. Demitri load.
2. In VS, play Demitri's fireball (down, down-forward, forward + punch) and
   dash (forward, forward) with Anakaris and with Victor on the other side,
   in both side orders; sample the SCSP slots after each move.
3. Log the game's driver commands and trace the sequence-start routine
   `0x0603B270` (channel r4, bank r5, song r6) back to its caller.
4. Patch in RAM and repeat; build; repeat on the image; run the motion
   battery for Pyron, Sasquatch, Donovan and Huitzil; Arcade; JP.

## Actual Result

**Sound RAM is intact (overrun disproven).** P1's sequence slot is at
`0x77350` and P2's at `0x779A8` in both runs, exactly `0x658` = 1,624 bytes
apart: the game reserves room for Anakaris's file. `ANAKARIS.BIN` or
`VICTOR.BIN` sits at `0x3B2C0`, `DEMITRI.BIN` at `0x58EC0`, `ALWAYS.BIN` at
`0x0B000`, all whole. Every static area matches; only the driver's work
tables differ.

**The wrong voices.** Sample start (SA) of the voices after each move:

| Sound | Victor P1, Demitri P2 | Anakaris P1, Demitri P2 | Demitri P1 vs. Anakaris or Victor |
| --- | --- | --- | --- |
| Fireball, part 1 | `5FAAE` (P2 bank) | `5FAAE` | `41EAE` (P1 bank) |
| Fireball, part 2 | `61228` (P2), FNS `2BA` | **`462CA` (P1, Anakaris), FNS `07D`** | `43628` (P1) |
| Dash | `68C46` (P2), oct -2 FNS `1A8` | **`4B172` (P1, Anakaris), oct -3 FNS `2BA`** | `4B046` (P1) |

JP 1M gives the same addresses: `462CA` and `4B172` with Anakaris on P1,
`61228` and `68C46` with Victor.

**The game requests them.** Each sequence start (`0x0603B270`, called from
`0x0603A324`) carries a bank: 1 = P1's files, 2 = P2's, 0 = common. Demitri
P2's fireball is bank 2 song 0 against Victor but bank 1 song 1 against
Anakaris. His dash is bank 2 song 2 against Victor and bank 1 song 8
against Anakaris.

**Why.** Sound records `0x0605C45C + 6 * (ID - 0x30)`. Type `0xFE` is a
shared sound with type number g in byte 4. For these, `0x0603A1C8` looks
in the per-character table `0x0606C10C[g]` (14 flag/song pairs). It
checks P1's character (`0x0607663B`) first and plays P1's song from bank 1
whenever P1's character has an entry. Only otherwise does it try P2
(`0x0607663C`, bank 2). The requesting player is never considered.
Anakaris has entries for 17 of the 27 types, and each of them is also owned
by another character (`g=13`: Demitri 0, Anakaris 1; `g=14`: Demitri 2,
Anakaris 8; `g=6`: Pyron 7, Anakaris 15; `g=18`: Sasquatch 4, Huitzil 11,
Hsien-Ko 4, Donovan 1, Anakaris 10). The requester cannot be recovered at
the lookup. The queue holds only the ID (the dash uses ID `0x75` from
either side) and a screen position.

**The fix.** With Anakaris on P1, P2's character is tried first. Otherwise
the order is stock. This is the behaviour stock already has with Anakaris
on P2. When he throws back an opponent's projectile, the opponent's
original plays, as it does with him on P2.

**Verification** (shared-sound requests resolved, bank and song):

| Case | Retail US | Deluxe US Enhanced |
| --- | --- | --- |
| Demitri P2 fireball, dash (vs. Anakaris P1) | bank 1 songs 1, 8 | bank 2 songs 0, 2 |
| Pyron P2 fireball `g=6` (×3) | bank 1 song 15 | bank 2 song 7 |
| Sasquatch P2 `g=15`, ice `g=18` (×3 each) | bank 1 songs 4, 10 | bank 2 songs 1, 4 |
| Huitzil P2 ice `g=18` (×2) | bank 1 song 10 | bank 2 song 11 |
| `g=21` (Sasquatch, Huitzil; not Anakaris) | bank 2 | bank 2 (unchanged) |
| Arcade, Anakaris P1 vs. CPU Victor, `g=0` | bank 1 song 9 (`arc-us-long`) | bank 2 song 0 (`arc-dx`) |
| Victor P1 vs. Demitri P2 battery | `g=13`, `g=14` bank 2 | identical file |
| Deluxe edition US Original (`E=1`) | — | bank 1 songs 1, 8 (stock, as intended) |

The `EXP-0042` Appendix check on the final image (`app-regress`, no cart)
gives the same values as before in both boots.

The RAM patch on the retail image alone leaves every sequence start
unchanged in two control batteries: Anakaris P1 running the battery against
Demitri (18 starts) and Victor vs. Demitri (25 starts). The edition switch
puts the fix bytes at `0x0603A1D6` for US Enhanced (`60508806`) and stock
bytes for US Original and JP Original (`84D46350`).

**Not covered.** The motion battery produced no shared sound for Donovan
(normal attacks only), so his ice attack was not triggered live. His `g=18`
entry goes through the same lookup and table as Sasquatch's and Huitzil's,
which are confirmed. Anakaris's own battery made no shared-sound requests.

**Side observation, not this task.** With identical VS inputs, the Deluxe
image and retail differ in two or three common-bank sequence starts (bank 0,
e.g. song 8 against `0x1D`), even in Victor vs. Demitri. The RAM fix alone
does not cause this (identical control). Cause UNKNOWN; recorded in
`docs/known_unknowns.md`.

| Evidence under `local/exp0044/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `us-6-1/scspram.bin` | 524,288 | `22d869b0399d542b4c2dc993c2b0cb30e321a05a63110665eba309b5c6a561c4` |
| `us-3-1/scspram.bin` | 524,288 | `ce7a64a4a01eb4550384fe13eaebaf0a36bb3381b6ad43949daa015f2687d255` |
| `cmp-a-6-1/slots.jsonl` | 25,004 | `34730c02ddf2e81618b07cd98e2562edc1ad28e4baf84b746b28feef686abb5e` |
| `cmp-b-3-1/slots.jsonl` | 25,312 | `2e8157f51979ec82373eda517ecdb090ce9601f72ade9a5fa5f4f07c9098657d` |
| `cmp-c-1-6/slots.jsonl` | 25,315 | `40d64a5a151f49064eb4f4dcd8687d18d68c764768817a0ee6d2d868f5962abe` |
| `cmp-d-1-3/slots.jsonl` | 25,146 | `4f929e815adc00b40f32133a382605b61f46281ecafc596bf4750717026d72b8` |
| `cmp-a-6-1/sound.wav` (stereo) | 23,828,220 | `4fedc2a2340cbe17e60c3928173b4714d058e35e742280f5b4069795e7ccbc47` |
| `cmp-b-3-1/sound.wav` (stereo) | 23,792,916 | `35ff763465a0bf563ffec25ba4ea7bebb44ae563e2e8b9a33bf6d0e8e84a91bc` |
| `cmd-a-6-1/cmds.txt` | 3,186 | `62adf1cdaa9af2ab6f348838be8a0166f68dd624ed071da4b3de0234a323324d` |
| `cmd-b-3-1/cmds.txt` | 3,132 | `52f52b3d3ac7aca8f55babe7644ace19cc8697966ec6378ccab38d83f292c471` |
| `tr-a/events.log`, `tr-b/events.log` | 65,337 each | `7d946776…4614`, `48ed6fd3…ef80` |
| `jp-a-6-1/slots.jsonl` | 24,849 | `752055d3b61fbf683914c55ab30baa675720ea329b341977abbad283169ff4ad` |
| `jp-b-3-1/slots.jsonl` | 25,157 | `dd65095954afb7df6def29a45108f0a5f21f5902db69f9319ff87b816cfe6566` |
| `fix-a/events.log`, `fix-c/events.log` (RAM fix) | 65,337 each | `f4fbbc12…85e8`, `ed6a5db3…2358` |
| `bat-us-6-12/shared.txt`, `bat-dx-6-12/shared.txt` | 141; 138 | `96cd416a…b202`, `42342590…8467` |
| `bat-us-6-10/shared.txt`, `bat-dx-6-10/shared.txt` | 549; 546 | `d35d8273…ad7f`, `50eb5407…3f06` |
| `bat-us-6-11/shared.txt`, `bat-dx-6-11/shared.txt` | 268 each | `04ca4505…d0a7`, `3dd4317c…a316` |
| `bat-us-3-1/shared.txt`, `bat-dx-3-1/shared.txt` (identical) | 192 | `261bec5bdf13212c78e8d4b6ec25235bf6caf2c3e2abad4925a775db0b0ab5a7` |
| `arc-us-long/shared.txt`, `arc-dx/shared.txt` | 295; 115 | `fdcf2538…656f`, `691ebecd…668f` |
| `dx-e00/events.log`, `dx-e01/events.log` | 65,337 each | `44a4f1d3…fcdc9`, `a1870201…843e` |

## Conclusion

The report is a stock bug in both retail releases. The shared-sound lookup
always prefers P1's character, and Anakaris carries copies of 17 shared
types, so with him on P1 the opponent's fireballs, dashes and ice attacks
play his copies (different samples and pitch). Deluxe US Enhanced now tries
P2's character first when P1 is Anakaris. That gives every tested opponent
its own sounds in VS and Arcade, and leaves all other matchups and the
original editions unchanged.

## Uncertainty and Alternatives

- Donovan's ice attack was not triggered live (motion not found).
- Overlaps among other characters keep the stock P1-first order (for
  example `g=21` Sasquatch/Huitzil/Donovan, `g=0` Victor/Raptor/Huitzil/
  Donovan). None was reported. Whether those copies sound different is
  UNKNOWN.
- Heard on real hardware: not yet (Mednafen only).

## Reproduction

```bash
US="local/disc_images/nw_saturn_us/Night Warriors - Darkstalkers' Revenge (USA).cue"
JP="local/disc_images/vh_saturn_jp_1m/Vampire Hunter - Darkstalkers' Revenge (Japan) (1M).cue"
DX="build/us_edition/Night Warriors - Darkstalkers' Revenge (USA).cue"
E=research/experiments/EXP-0044
./invenv.sh python $E/sndram.py "$US" local/exp0044/us-6-1 --ids 6 1
FB2="2:2000x4,6000x4,4000x2,4020x4,0000x2"; DS2="2:wait:120,4000x3,0000x3,4000x10,0000x2"
./invenv.sh python $E/vsmove.py "$US" local/exp0044/cmp-a-6-1 --ids 6 1 --fight-wait 2400 \
  --slot-frames 60 --moves "$FB2" "$DS2"
./invenv.sh python $E/vsmove.py "$US" local/exp0044/tr-a --ids 6 1 --fight-wait 2400 \
  --trace 0603B270 --moves "$FB2" "$DS2"
./invenv.sh python $E/vsmove.py "$JP" local/exp0044/jp-a-6-1 --region jp --ids 6 1 \
  --fight-wait 2400 --slot-frames 60 --moves "$FB2" "$DS2"
./invenv.sh python research/experiments/EXP-0038/build_edition.py build/us_edition
./invenv.sh python $E/battery.py run "$US" local/exp0044/bat-us-6-12 --ids 6 12 --pad 2
./invenv.sh python $E/battery.py run "$DX" local/exp0044/bat-dx-6-12 --ids 6 12 --pad 2
./invenv.sh python $E/vsmove.py "$DX" local/exp0044/arc-dx --arcade --ids 6 0 \
  --fight-wait 2400 --trace 0603A1D6 0603B270 --moves "1:wait:2400"
./invenv.sh python $E/battery.py summary local/exp0044/arc-dx
```
