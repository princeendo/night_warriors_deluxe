# Coverage Exceptions

The [surface audit](text_surfaces.md) covers matched ordinary play on the two
retail discs. The [regional difference register](difference_register.md)
tracks the disposition and evidence for each row.

| Item | Current disposition | Remaining evidence or decision |
| --- | --- | --- |
| Japanese/US branding, boot art and license lines | The US base defines the Deluxe logo and intro in every edition. The BIOS follows that image's area. See EDITION-001. | Physical boot behavior remains part of the console check. |
| Regional menu wording, fighter labels and narrative names | Edition selects MODE SELECT wording. The names preference can override fighter labels in Enhanced. The original script controls supporting names and names inside dialogue. | Live names-preference checks covered selection, HUD and the quote language. The loading/results/cast behavior is supported by the traced readers and merits console verification. |
| Victory quotes | Retail selection is mapped for both discs. US Enhanced adds one Japanese translation for each of the four conditions for each fighter, retaining the official US lines. | Additional Japanese entries outside this 56-translation set remain in the Japanese quote inventory. |
| Appendix and animation | Stock Appendix code and setting were checked. Deluxe makes the menu available by default and enables full mixed-matchup animation with 4 MiB. | Real Saturn timing, sprites and stability with 4 MiB remain open (ANI-003). |
| Shared sound effects | Both sound fixes are on the build. | Donovan's ice-attack sound remains an open live check (AUD-004). |
| Track 2, manuals and other media | Track 2 audio data differs on the two retail discs, and the manuals are an optional reference. | Track 2's precise content and BIO-01 remain open. No manual pair was supplied. |
| Other program/data differences | Same-action comparisons exist for the surfaces named in the register. | FILE-05 and the remaining OTHER-01 behaviors need separate tracing or comparative play before M8 closure. |

These entries keep COV-001 open for the full regional merge. They describe
the bounds of the current audit and hardware candidate.
