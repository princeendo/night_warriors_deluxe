# EXP-0060: Keep a three-hit chain intact at lethal vitality

Task: TRN-002

Status: DONE

Confidence: CONFIRMED for Demitri’s crouching three-punch chain versus Victor.

## Observation

The projectile branch in EXP-0057 and EXP-0059 restores one vitality before
KO. The normal strike sequence also needs to sustain subsequent hits and
preserve the game's chain recognition.

## Hypothesis and prediction

Demitri's crouching light punch, medium punch, and heavy punch use that
same vitality branch. At one starting vitality, the stock combat path
will terminate the chain early. With the existing projectile edit,
Victor will take all three hits and the game will report a three-hit
chain in the same round.

## Controlled change

Use the hashed Deluxe US Enhanced VS checkpoint and muted Mednafen 1.32.1
build from [EXP-0057](../EXP-0057/README.md). Run all trials with no cart,
`CUT`, and idle Victor on P2. Demitri walks 115 frames to point-blank
range, then taps the three crouching punches at fixed intervals. First
confirm the chain at healthy vitality. Compare the low-vitality control
and low-vitality RAM variant with the same timing and only the four-byte
edit from EXP-0057 enabled for the variant.

## First result

`chain-healthy` reached the three vitality stores at `0x06022992` on
frames 127, 145 and 164. Victor fell from `0090` to `0074`. The screen
reported `3 HIT CHAIN`. At one vitality, `chain-lethal` reached that
store once, wrote `FFFF`, set the KO bytes to `01 FF`, and showed K.O.

`chain-clamp` reached all three damage stores at the healthy timings
and the four-byte edit restored one vitality after every hit. The KO
bytes stayed clear. Victor stayed upright and the chain banner was absent.
The initial hypothesis about preserving the normal reaction is disproven.

## Refined hypothesis and controlled change

US `MAIN.BIN` compares the defender's `+0x46` and `+0x48` vitality words
at `0x060263D8`. A difference branches at `0x060263DA` to `0x06026438`.
The healthy trace reaches the reaction initialization at `0x060264C4`;
the one-word clamp trace skips it. Restoring vitality to the same value
as the comparison word can therefore bypass hit-reaction setup.

Repeat the lethal trial with a single refinement. Keep the same one-point
clamp, and leave a one-point difference for the reaction code by writing
`0002` to `+0x48` after a negative damage result. The prediction is that
the hit-reaction writes and the visible three-hit chain return.

| RAM address | Original | Trial | Effect |
| --- | --- | --- | --- |
| `0x0602299A`–`0x060229A3` | `9015 04EE E075 044C 2448` | `0EB5 E048 E202 A026 0E25` | Store live vitality 1 at `+0x46`, branch to `0x060229F0`, and store 2 at `+0x48` in the delay slot. |

## Refined result

`chain-delta` reached all six damage stores and all six reaction writes
in two repetitions of the three-hit chain. The damage stores still used
`-1`, `-3`, `-3` as the tentative vitality results. The hook stored one
at `0x0602299A` and two at `0x060229A2` on each hit. In the following
frame, the defender entered the reaction path through `0x060264C4`,
and `0x0602651C` copied its vitality back into `+0x48`. Both repetitions
show `3 HIT CHAIN`. The KO bytes stayed zero through the final sample.

Use the refined edit with the prior projectile and guard scripts as a
regression. `shot-delta` registered two lethal direct hits and `chip-delta`
registered a zero-vitality chip hit followed by a lethal one. The refined
edit kept the KO bytes clear and the timer running across both cases.
Both fighters were idle at each final capture.

| Frame capture under `local/exp0060/` | Bytes | SHA-256 |
| --- | ---: | --- |
| `chain-healthy/hit1-after-90.png` | 29,104 | `f04a3cb8c411b87cb25cfa9bbe7137eee8a93842fcfdc1572cdd62ec32e9fb68` |
| `chain-lethal/hit1-after-20.png` | 9,789 | `843c1a722afe136171dd77cfb3f555a3dc6bf458bdc6d477b8a0911fece91081` |
| `chain-clamp/hit1-after-90.png` | 29,189 | `b06ef4334bb615de64540bc7a5a043bdd7f57831f28b6f482cd33908d7a49cbd` |
| `chain-delta/hit1-after-90.png` | 29,285 | `c649208e7d1ce91dc2ebde46a4f2b1f464ef678a76b2237718a7c9709b313a4b` |
| `chain-delta/hit2-after-90.png` | 29,287 | `2cc20cc4592fd005a54d05c5417fc6211735e1e939ea55dadb51b9e9f293b295` |
| `shot-delta/hit2-after-180.png` | 29,199 | `6ac5d3e24c49ea983e76afea9533a987aec05b86a669d5e635d752c08f4b3bed` |
| `chip-delta/hit2-after-180.png` | 29,254 | `4c1948914ae250fcc1c74abf6eba9c27c7385022de3bac543878f3934b69bc70` |

## Conclusion

A viable hook for this combat path needs the `+0x46` and `+0x48` vitality
words to differ until reaction setup consumes the change. The ten-byte
RAM trial covers the tested chain, direct hit, and chip paths. A future
Training-specific version needs to retain the stock negative path when
Training is disabled and account for other move families.

## Reproduction

Run from the repository root with new output directories as needed.
Use the same saved checkpoint as EXP-0057.

```bash
probe=research/experiments/EXP-0057/probe.py
cue="build/exp0053_deluxe_title/Night Warriors - Darkstalkers' Revenge (USA).cue"
state=local/exp0057/control/vs.mc0
motion=2040x3,2000x9,2020x3,2000x10,2010x3,0000x3
patch=0602299A:0EB5E048E202A0260E25
./invenv.sh python "$probe" "$cue" local/exp0060/chain-healthy --state "$state" \
  --approach 8000x115 --motion "$motion"
./invenv.sh python "$probe" "$cue" local/exp0060/chain-lethal --state "$state" \
  --low-vitality --approach 8000x115 --motion "$motion"
./invenv.sh python "$probe" "$cue" local/exp0060/chain-clamp --state "$state" \
  --low-vitality --approach 8000x115 --motion "$motion" --patch 0602299A:A0290EB5
./invenv.sh python "$probe" "$cue" local/exp0060/chain-delta --state "$state" \
  --low-vitality --approach 8000x115 --motion "$motion" --patch "$patch"
./invenv.sh python "$probe" "$cue" local/exp0060/shot-delta --state "$state" \
  --low-vitality --patch "$patch"
./invenv.sh python "$probe" "$cue" local/exp0060/chip-delta --state "$state" \
  --low-vitality --guard --motion 2000x4,A000x4,8000x2,8020x4,0000x57 --patch "$patch"
./invenv.sh python -m tools.sh2.disasm local/extracted/saturn_us/MAIN.BIN \
  --base 0x06012000 --start 0x060263D0 --end 0x060264C6
```
