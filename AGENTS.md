# Agent Operating Contract

This file is authoritative for every AI-agent session in this repository. The
project is an empirical reverse-engineering investigation of the two Sega
Saturn releases of Capcom's 1996 Darkstalkers sequel, the Japanese *Vampire
Hunter: Darkstalkers' Revenge* (T-1202G) and the US *Night Warriors:
Darkstalkers' Revenge* (T-1208H). Its goal is one "Ultimate" image that combines
them: content one region has and the other lacks, reproduced from evidence and
selectable where the user decides. It is not a speculative implementation
exercise.

Three sibling projects did comparable work first, each on one Japanese
release that it translated:

- Marvel Super Heroes vs. Street Fighter (MSHvSF), the first. Its method is in
  `docs/playbook_from_mshvsf.md`.
- X-Men vs. Street Fighter (XvSF), the second. What carried over is in
  `docs/lessons_from_xvsf.md`.
- Cyberbots: Fullmetal Madness, the third. What carried over is in
  `docs/lessons_from_cyberbots.md`.

Those files are a method, not a map: **nothing in them is a fact about Vampire
Hunter.** This project differs in kind: both regions are on hand, the US
release already has official English, and the work is mostly finding,
explaining and merging regional differences rather than translating a whole
script. The target is one image offering the JP original, the US original and
a US Enhanced edition (`docs/localization_policy.md`). `references/web_research/` holds the user's web research on those
differences; it is a list of leads, not evidence about these discs.

## Before Each Session

1. Read `local_agent_guidance.md` if it exists. It holds this machine's user
   preferences, git identity, and local paths. It is ignored by git and is never
   committed.
2. Read the "Current State" section of `TASKS.md`.

## Required Method

Use this cycle for each investigation:

```text
OBSERVE -> FORM ONE HYPOTHESIS -> DESIGN A DISCRIMINATING EXPERIMENT
        -> RUN IT -> RECORD RESULT -> ACCEPT / REJECT / REFINE
        -> UPDATE DOCUMENTATION
```

Use confidence labels precisely:

- **UNKNOWN**: no meaningful conclusion yet.
- **HYPOTHESIS**: plausible explanation with insufficient experimental evidence.
- **SUPPORTED**: evidence is consistent, but alternatives remain.
- **CONFIRMED**: a controlled experiment produced the predicted result and is
  reproducible.
- **DISPROVEN**: evidence contradicts the hypothesis.

Plausibility, visual similarity, a matching byte sequence, or an analogous game
is not confirmation. A sibling result is an analogous game. A web source, fan
transcript, guide, or arcade observation is a lead.

## Mandatory Rules

1. Never modify original disc images. Derived builds go under `build/` and patch
   commands default to a distinct output path.
2. Record SHA-256, size, filename, and release description for every source-image
   component before research.
3. Never treat a hypothesis as fact or invent missing addresses, offsets, text,
   citations, correspondences, commands, or results.
4. Test one controlled hypothesis at a time when practical. Prefer experiments
   that change exactly one variable.
5. Document every confirmed discovery in `docs/discoveries.md` with evidence and
   reproduction instructions.
6. Record plausible but disproven hypotheses in `research_log.md` so future agents
   do not unknowingly retry them.
7. Do not bypass a blocker or dependency in `TASKS.md`.
8. Do not begin a later milestone because it appears easy. Nothing past M1 begins
   before M1 is confirmed; no generalization begins before M2 works from an
   untouched source image.
9. Preserve exact commands, tool versions, inputs, outputs, and hashes required to
   reproduce results.
10. Prefer reusable scripted extraction and analysis over undocumented manual work.
11. Support visible or audible game modifications with before/after evidence
    (screenshots, recorded audio, or equivalent) and a deterministic checkpoint.
12. For every binary modification, record original bytes, modified bytes, file
    offset or memory address, purpose, expected result, and observed result.
13. Never assume Vampire Hunter shares structures, offsets, encodings, file names,
    compression formats, fonts, functions, memory addresses, selection logic, or
    renderer behavior with MSHvSF, XvSF or Cyberbots. Every sibling fact,
    including each one in `docs/playbook_from_mshvsf.md`,
    `docs/lessons_from_xvsf.md` and `docs/lessons_from_cyberbots.md`, is at most
    a **HYPOTHESIS** here until a Vampire Hunter experiment confirms it.
14. Never assume CPS-II, PlayStation, PSP and Saturn structures are identical, and
    never assume the Japanese and US Saturn releases share a structure, address
    or behaviour beyond what a recorded comparison shows.
15. Use reference releases as evidence and translation oracles, not templates.
16. Use stock Mednafen first. The sibling projects' frontend-only agent-interface
    patch (`vendor/mednafen/patches/`) may be built once stock Mednafen boots
    Vampire Hunter (`EMU-003`), `EMU-020` records why stock Mednafen is
    insufficient, citing the sibling evidence, and the user has confirmed reuse
    (asked in `EMU-020`). Re-run the interface validations V1-V4 on Vampire Hunter
    (`EMU-021`) before using it as evidence.
17. Any Mednafen change beyond that patch is the smallest useful change, with the
    upstream URL, version/revision, patches, rationale, and build steps preserved.
18. Python 3.12+ is the default implementation language. Avoid large dependencies
    without a demonstrated need.
19. Run Python tooling through `./invenv.sh`; do not rely on an activated shell.
20. Update `TASKS.md` and `research_log.md` before ending a substantial session.
21. Never commit copyrighted game images, BIOS files, extracted game contents,
    save states, memory dumps, screenshots, audio captures, or emulator
    binaries. The siblings' exception (release patch files, xdelta and SSP and
    zips of them, published as GitHub Release assets and never committed) is to
    be confirmed for this project in `REL-001`.
22. Keep binary evidence locally under ignored paths. Commit hashes, addresses,
    scripts, schemas, small synthetic fixtures, and derived factual metadata.
23. Do not start a second difference class (`docs/difference_register.md`)
    before the first one chosen in `DIFF-003` is proven through M5, unless a
    task explicitly permits it.
24. Do not work on special cases (unused or unreachable assets, hidden content,
    debug features, content in neither release's normal play) before the
    ordinary pipeline is mature and a task explicitly permits it.
25. Do not modify the MSHvSF, XvSF or Cyberbots repositories, their source images,
    or their tools from this repository. Copy a tool here, with its provenance,
    before changing it.
26. Code copied from a sibling keeps a provenance note (source repository, path,
    and commit). Anything that hard-codes a sibling address, offset, file name,
    or format is parameterized or rewritten, then re-validated on Vampire Hunter
    before its output is evidence.

## Rules For Merging Two Releases

27. A regional difference is established only by the same action under the same
    settings on both releases producing different content, or by a data
    comparison that explains the difference. Record it in
    `docs/difference_register.md` with both regions' evidence. A web-research
    item starts there as a lead and stays UNKNOWN until such a comparison.
28. "Missing" describes presentation (what is seen or heard) unless a data
    comparison proves the asset is absent from a disc. Keep distinct change
    types: **omitted**, **rewritten**, **renamed**, **reordered**, **retimed**,
    **conditionally suppressed**, and **asset absent**. Separate a regional
    difference from a Saturn conversion change (both Saturn releases differ from
    the arcade) and from an optional setting (Appendix, animation options).
29. Every English line that goes into a build carries its provenance: the US
    Saturn release, another official release (PSP *Darkstalkers Chronicle*,
    arcade *Night Warriors*), or a new translation marked as such. Fan
    transcripts and guides locate content; they are never the source of a line
    without a recorded user decision.
30. Keep the original US wording where it exists unless the user decides
    otherwise (`DOC-002`). Do not silently modernize names (Amanda, Anita) or
    wording.
31. The three Japanese pressings share one byte-identical data track
    (`references/saturn_jp/README.md`); the project works from the 1M image
    (user decision 2026-11-13). Name the exact image a patch applies to in
    every build and release.

## Task Discipline

Allowed statuses are `BACKLOG`, `BLOCKED`, `READY`, `IN_PROGRESS`, `DONE`, and
`REJECTED`. Keep at most one reverse-engineering experiment `IN_PROGRESS`. Code or
notes alone do not make a task `DONE`; all acceptance criteria must be supported by
evidence. If prerequisites change, update dependencies and blockers before work.

When blocked, state the unknown, available evidence, competing explanations, and
the smallest discriminating experiment. Do not respond with speculative systems or
premature abstractions.

## Artifact Discipline

Significant experiments use `research/experiments/EXP-NNNN/`, based on the template
in `research/experiments/README.md`. Do not create empty evidence files. Every
experiment records the observation, hypothesis, single change, prediction, actual
result, conclusion, and uncertainty. An experiment that compares the regions
names the image of each side.

Save states are checkpoints, not analyzable RAM snapshots. Dump identical Saturn
memory regions from each checkpoint into stable raw files before differential
analysis. There are two sources for those raw files:

- stock debugger dumps;
- the save-state extractor (`tools/memory/mcs_extract.py`, copied from
  Cyberbots).

Use extracted data for a region only after that region's extraction has matched,
byte for byte, a stock debugger dump of the same paused instant **on Vampire
Hunter**, as recorded in `docs/discoveries.md`. Unvalidated regions remain
`HYPOTHESIS` evidence. Never analyze the compressed state file directly. A state
from one release is not loaded into the other.

Begin with WRAM-L `0x00200000-0x002FFFFF` and WRAM-H `0x06000000-0x060FFFFF`.
Expand to cartridge RAM, sound RAM, or VDP VRAM only with the rationale recorded
in the experiment.

`docs/discoveries.md` contains only durable `CONFIRMED` findings. Put hypotheses and
failures in `research_log.md`; put unresolved questions in
`docs/known_unknowns.md`; keep the regional difference inventory in
`docs/difference_register.md`.

## Session Closeout

Before ending substantial work:

1. Run relevant tests, lint, formatting, and typing checks.
2. Record commands and outcomes in `research_log.md`.
3. Update task status only when acceptance criteria are met.
4. Identify the next unblocked task without beginning a gated milestone.
5. Check that no copyrighted or machine-local artifact is staged for commit,
   including `local_agent_guidance.md`.
6. After each successfully completed user-requested task, run the relevant
   verification, inspect the status and diff, stage only intended files, create
   a concise commit, and push it to the configured upstream branch. Never force-
   push or commit prohibited artifacts or secrets; report an unavailable
   upstream or failed push as a blocker.
