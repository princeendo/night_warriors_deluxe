# EXP-0006: Validate the Save-State Extractor Against Stock Debugger Dumps

Task: DBG-001
Status: DONE
Confidence: CONFIRMED

## Observation

`tools/memory/mcs_extract.py` (copied from Cyberbots) reads WRAM-L, WRAM-H,
VDP1 VRAM and VDP2 VRAM from a Mednafen 1.32.1 state, by default swapping
each stored 16-bit element into Saturn (big-endian) order. Every sibling
found the swap necessary. `EXP-0005` showed the extractor equals the agent's
reads; `AGENTS.md` asks for a match with **stock** debugger dumps of the same
instant before extracted regions are evidence.

## Hypothesis

For both releases, `mcs_extract` with `--byte-order saturn` reproduces stock
debugger dumps of the same paused instant exactly for all four regions, and
`--byte-order state` (no swap) does not.

## Controlled Change

None to the extractor or the games. The comparison varies only the byte order.
Instant A reuses `EXP-0004` (work RAM only). Instant H is one new key-driven
run per release, with the user present and hands-off ("Yes, run it now",
2026-11-14).

## Prediction

`saturn` output equals the dumps for every region at both instants; `state`
output differs from every dump.

## Inputs and Provenance

- Instant A (`EXP-0004` run A): states `local/emu007/<r>-a-state/*.mc0`
  (Japanese `f945cb51…91a0`, US `2eb7dbd0…49db`) and dumps
  `research/memory_dumps/emu007/<r>/wraml-1.bin`, `wramh-1.bin`.
- Instant H (this experiment): states `local/dbg001/<r>-h-state/*.mc0`
  (Japanese 1,633,750 bytes,
  `bba2647a6e33e90e2dd22f0385a93f74fda7b6dfb051d6f4f890e3b025f777b3`; US
  1,630,691 bytes,
  `0698b56a2e0f694919db5422c9309f436c92563e4929c62443a9254e6277a4f6`) and the
  four dumps per release in `research/memory_dumps/dbg001/` (below).
- Stock Mednafen `de542817…582a`, quiet home, images and BIOS as `EXP-0001`.

## Tools and Environment

`tools/memory/mcs_extract.py`; `tools/mednafen/hotkeys.py --keep-focus
--script`; Python byte comparison.

## Procedure

Instant A (no emulator run), per release:

```bash
S=local/emu007/$r-a-state/*.mc0
./invenv.sh python -m tools.memory.mcs_extract $S --region wram_l --region wram_h \
  --out-dir research/memory_dumps/dbg001/$r-a-saturn
./invenv.sh python -m tools.memory.mcs_extract $S --region wram_l --region wram_h \
  --byte-order state --out-dir research/memory_dumps/dbg001/$r-a-state
```

Instant H, per release: [`steps/<r>-h.steps`](steps/) are Cyberbots' `EXP-0005`
`run-h.steps` (`bac6fde`) with the same actions, the freeze moved from 63 s to
65 s, and the paths split by release: freeze (`option+a`), save a state,
open the debugger and memory editor one second apart, then dump WRAM-L,
WRAM-H, VDP1 VRAM (the ninth space) and VDP2 VRAM (the twelfth), with a window
capture before each dump.

```bash
./invenv.sh python -m tools.mednafen.hotkeys "$CUE" local/dbg001/$r-h.log \
  --script research/experiments/EXP-0006/steps/$r-h.steps --keep-focus
./invenv.sh python -m tools.memory.mcs_extract local/dbg001/$r-h-state/*.mc0 \
  --region wram_l --region wram_h --region vdp1_vram --region vdp2_vram \
  --byte-order saturn --out-dir research/memory_dumps/dbg001/$r-h-saturn
# and --byte-order state into $r-h-state (files named <region>.state-order.bin)
```

## Actual Result

Runs H: Japanese 2026-11-14 07:52:35 UTC, US 07:54:11; both exit 0 with all
47 keys sent; all eight dump files written; sources unchanged; no Mednafen
left; configs unchanged.

| Release | Instant | Region | Stock dump SHA-256 | `saturn` | `state` |
| --- | --- | --- | --- | --- | --- |
| Japanese | A | WRAM-L | `b7caad6501ed9f80…18bb` | equal | differs |
| Japanese | A | WRAM-H | `a6c4aaa36dfad499…3db0` | equal | differs |
| Japanese | H | WRAM-L | `b7caad6501ed9f8094cd39f50e2177dca4f68dfb7d45c1673566b66e052218bb` | equal | differs |
| Japanese | H | WRAM-H | `85116ad0ec6569495676184dedb70320905e2170371f6a60dd5949baa703dd80` | equal | differs |
| Japanese | H | VDP1 VRAM | `808ce01753f145be71650ca8ab0d3e1e675a142a52629b3c5288db94abbd9e6e` | equal | differs |
| Japanese | H | VDP2 VRAM | `84881efaed32188e5614d242013ab327bfadd1ba9611d28f51bd2802b6955ca3` | equal | differs |
| US | A | WRAM-L | `914d4e2bd5888530…ec43` | equal | differs |
| US | A | WRAM-H | `78715324e8ce10df…0702` | equal | differs |
| US | H | WRAM-L | `914d4e2bd58885303a941c18af07aac29add728052c67278138dad874d84ec43` | equal | differs |
| US | H | WRAM-H | `c73ca4b8f5fcd9ce81dd4f84175933e1da212f355bf0808e6bb518359d265ce8` | equal | differs |
| US | H | VDP1 VRAM | `cc4352e073b63b448348a10d2af928fac408df64f7d1b7f20a8cc755592ae1ce` | equal | differs |
| US | H | VDP2 VRAM | `84881efaed32188e5614d242013ab327bfadd1ba9611d28f51bd2802b6955ca3` | equal | differs |

- WRAM-L, VDP1 VRAM and VDP2 VRAM at instant H equal the same regions read by
  the agent in `EXP-0005` (another title instant): they do not change on the
  title. VDP2 VRAM is the same in both releases at the title.
- **A comparison error, corrected.** The first comparison of the `state`
  output named `<region>.bin`, but that byte order writes
  `<region>.state-order.bin`, so it compared against missing files and
  "differs" proved nothing; a shell loop also failed (zsh does not split
  `set -- $p`). Both comparisons were redone in Python against the right file
  names; the table above is the redone result. Nothing else depended on the
  first attempt.

## Conclusion

**CONFIRMED** for both releases: `mcs_extract` with the default `saturn` byte
order reproduces stock debugger dumps exactly for WRAM-L and WRAM-H (two
instants) and VDP1 and VDP2 VRAM (one instant), and the swap is required.
These regions extracted from states may be used as evidence (D-006). Cart
RAM (`CART_BACKUP`: a 512 KiB backup cart here) and sound RAM stay
**HYPOTHESIS**; the extractor reads neither.

## Uncertainty and Alternatives

- VDP1 and VDP2 VRAM were checked at one instant, on the title.
- Sound RAM, needed for `AUD-001`, is not covered; the agent can read
  `scspram` directly, which `EXP-0005` did not test against anything.

## Reproduction

Run the procedure above from the repository root; instant H needs the user
present and hands-off for about 3 minutes. Evidence stays in the ignored
`local/dbg001/` and `research/memory_dumps/dbg001/`.
