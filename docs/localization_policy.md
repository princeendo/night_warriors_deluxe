# Edition Policy

The user's policy decisions for Vampire Hunter Ultimate (`DOC-002`). Each row
quotes the user. These are policy, not facts: whether each one is achievable
on these discs is found by experiment.

## Decisions (2026-11-13)

| Topic | The user's words | Meaning for this project |
| --- | --- | --- |
| Editions in the image | "For this release, my goal is to have the "Ultimate" edition have the option for the user to switch between the JP original, the US original, and the US "Enhanced" which incorporates the missing JP pieces. If there are pieces in the US version which don't exist in the JP version, we can also create an "Enhanced" version for JP." | One image, with an in-game choice of **JP original**, **US original** and **US Enhanced** (US plus the Japanese-only content), and **JP Enhanced** only if the US release turns out to have content the Japanese one lacks. Working interpretation, to confirm in `EDITION-001`: "original" means behaving exactly as that release does. How the choice is offered and stored, and what it costs on disc, is found by `EDITION-001`. |
| Edition switch (2026-11-16, `EDITION-001`) | "No, one code set"; "Options menu, saved"; JP Enhanced "Yes" | One code set, the US release's; "JP original" is the US code in Japanese mode, not the Japanese release byte for byte (this replaces the working interpretation above). The edition is an options entry saved in spare save bytes. Four editions, JP Enhanced included (`EDITION-003`). |
| JP Enhanced content (2026-11-16, `EDITION-003`) | "US-only ending lines"; "Hide until it differs (Recommended)" | JP Enhanced = JP original plus Japanese versions of what the US main endings add (a new translation, `END-005`); not the US pause or win-quote behaviour. Hidden in the menu until it differs. |
| Japanese source image | "If we don't need all the separate JP releases, we can keep just one and work from that." | The three Japanese images share one byte-identical data track, so the project works from the **1M** image only (`local/disc_images/vh_saturn_jp_1m/`). The other two were deleted locally on 2026-11-13; the supplied archives remain in `~/Downloads/vh_nw_saturn/`, and their hashes stay in `references/saturn_jp/README.md`. |
| First investigations | "I definitely want to check the US disc for whether the Morrigan info is present." and "Apparently, there are individual character story epilogue screens in the JP version that don't exist in the US version. We should investigate. Each character has a post-ending artwork accompanied by scrolling Japanese text." | The Morrigan voice leads (`AUD-01` to `AUD-03`, task `AUD-001`) and the epilogue screens (`END-01`, task `END-001`) are the user's first priorities. They set the order for `DIFF-003`. |
| M1 and `GATE-M0` (2026-11-14) | "Count this as M1 reached, with your GO recorded now?" → "Yes, record GO" | `GATE-M0` is passed with Morrigan's epilogue (`END-01`) as the M1 item, though the GO came after the RAM change (`EXP-0012`) and `REF-004` was not done. M2 work may begin. |
| Patched Mednafen (2026-11-14, `EMU-020`) | "Reuse the siblings' Mednafen agent-interface patch here (EMU-020)?" → "Yes, reuse it" | The sibling agent-interface patch is built unchanged on a separate copy of the stock source (`EMU-021`), and validations V1-V4 are re-run on both releases before its output is evidence (`AGENTS.md` rule 16). |
| Epilogue English source (2026-11-15, `GATE-TRANSLATION`, `EXP-0020`) | Asked which English goes into US Enhanced, given that two PSP epilogues change the Japanese meaning (Lord Raptor, Sasquatch) → "PSP for all 14 (Recommended)" | US Enhanced uses the PSP *Chronicle* English epilogue for all 14 characters, provenance "PSP *Chronicle* (official, 2005)". The meanings changed against the Japanese (Lord Raptor, Sasquatch; details in Bishamon and Rikuo) are recorded as known differences, not corrected. |
| Epilogue typos (2026-11-15) | Asked how PSP typos go on disc ("new without speakig", "exaulted", "kindom's", "nothing more a", "lie dormant") → "Fix spelling, log each (Recommended)" | Only spelling and missing-word slips are corrected; each edit is recorded beside the PSP original. Wording is otherwise unchanged. |
| Epilogue names (2026-11-15) | Asked whether to keep the PSP spellings ("Rapter", "Le marta") → "Match the US Saturn (Recommended)" | Where the US Saturn release has a name, the epilogue uses its spelling (Raptor); names the US Saturn lacks stay as the PSP has them. The wider names question in the Enhanced editions stays with `LOC-001`. |
| Epilogue fit (2026-11-15) | Asked what may change if a paragraph does not fit the Saturn layout → "Rewrap, then ask (Recommended)" | Line breaks may change freely; any cut or rewording to fit goes back to the user first. |
| Main endings in US Enhanced (2026-11-16, `END-003`) | Asked which main-ending differences US Enhanced should change → "Morrigan's missing lines (Recommended)"; source → "Check PSP movies first (Recommended)"; extent → "Minimal (Recommended)" | US Enhanced restores only Morrigan's two missing lines and pause page (D-029); all other US main-ending text stays as shipped (rule 30), including the four meaning changes and the renames. English from the PSP *Chronicle* main-ending movie if it has these lines; any new translation is asked first. Only the missing pages change. |

## Deferred To Evidence

| Topic | Deferred to | Why |
| --- | --- | --- |
| Release formats and timing; patches as GitHub Release assets only (rule 21) | `REL-001` | Adding files or growing track 1 may rule out SSP (`docs/lessons_from_cyberbots.md`, section 4). |
| Names in each edition (Gallon/Jon Talbain etc., Amanda/Anita) | `LOC-001` | Probably "as that release" for the originals; to ask for the Enhanced editions. |
| Arcade sets and PSP image as references | `REF-001`, `REF-002` | Asked when an investigation needs them. |
| The carried preferences in `local_agent_guidance.md` | next decision round | Followed as the user's latest known preferences meanwhile. |

## Translation Gates

Any English that is not already on the US disc goes on disc only after
`GATE-TRANSLATION` (`TASKS.md`).

- **2026-11-15, `END-01` epilogues:** the user's decisions above (PSP for all
  14, spelling fixes logged, US Saturn names, rewrap then ask). The gate
  opened on 2026-11-15 with `DOC-003` done; this scope only.
- **2026-11-16, `END-02` Morrigan's main ending:** a second scope (decisions
  above): restore her two missing lines and pause page in US Enhanced, from
  the PSP if it has them; a new translation needs the user's yes.
