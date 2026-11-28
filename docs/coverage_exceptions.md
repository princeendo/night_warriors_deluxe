# Coverage Exceptions

The [surface audit](text_surfaces.md) covers matched ordinary play on the two
retail discs. The [regional difference register](difference_register.md)
tracks the disposition and evidence for each row.

| Item | Current disposition | Remaining evidence or decision |
| --- | --- | --- |
| Japanese/US branding, boot art and license lines | The v0.2.0 candidate uses the US title and intro. The later UI-002 build draws the saved edition's regional wordmark at the title. The BIOS follows the US base image's area. | Physical boot and title behavior remain part of the console check. |
| Regional menu wording, fighter labels and narrative names | Edition selects MODE SELECT wording. The names preference can override fighter labels in Enhanced. The original script controls supporting names and names inside dialogue. | Live names-preference checks covered selection, HUD and the quote language. The loading/results/cast behavior is supported by the traced readers and merits console verification. |
| Victory quotes | Retail selection is mapped for both discs. US Enhanced adds one Japanese translation for each of the four conditions for each fighter, retaining the official US lines. | Additional Japanese entries outside this 56-translation set remain in the Japanese quote inventory. |
| Appendix and animation | Stock Appendix code and setting were checked. Deluxe makes the menu available by default and enables full mixed-matchup animation with 4 MiB. ANI-003 closed by user decision on emulator evidence. | Real Saturn timing, sprites and stability with 4 MiB remain unverified. |
| Shared sound effects | Both sound fixes are on the build; `AUD-004` closed by user decision (2026-11-27) on emulator evidence. | None. |
| Track 2 and ISO descriptive files | JP Track 2 has a spoken data-disc warning. US Track 2 is silent (D-054). Both discs name the same ISO descriptive files. The JP files contain metadata and the US files are empty (D-055). | The comparison covers disc content. The Track 1-only patch uses the US audio track. |
| Manuals | The paired manuals are an optional reference (REF-003). | BIO-01 awaits a scope decision and a manual pair. |
| Other program/data differences | FILE-05 identifies the shared ending pages and Victor's reduced animation set (D-056). Same-action comparisons exist for the surfaces named in the register. | Victor's altered reduced records and the remaining OTHER-01 behaviors need tracing or comparative play before M8 closure. |

These entries keep COV-001 open for the full regional merge. They describe
the bounds of the current audit and hardware candidate.
