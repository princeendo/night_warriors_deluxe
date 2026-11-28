# EXP-0030: What Each Main Ending Says in Each Release

Follow-up (2026-11-28, D-056): Demitri and Pyron draw from the
startup-loaded `P00.BIN` pages. The rendered retail JP and US page
bodies match the corresponding `ST2JPN.BIN` and `ST2USA.BIN` entries
compared here. The selector and self-relative page indexing are recorded
in [EXP-0056](../EXP-0056/README.md).

Task: END-003 (criteria 2-4)
Status: DONE
Confidence: CONFIRMED (records, page mapping); SUPPORTED (each comparison is
a reading by meaning)

## Observation

`EXP-0029`: the two regions' ending scripts differ in page count for 12 of
14 characters; what each page says was open.

## Method

Static, on the files; game text stays in ignored files and is not quoted
here beyond a few words.

1. `research/experiments/EXP-0029/st2_text.py` decodes every `ST2USA.BIN`
   entry to `local/end003/st2usa.txt`. Records of the line kind use the
   win-quote Latin codes (D-021); records whose fourth word is `0x01xx`
   (`0x00`-`0x08`, `0x60`-`0x65`, `0x68`-`0x6A`, `0xE0`-`0xE7`, and the
   placeholder entries) hold byte-level ASCII lines. The file's unused
   entries repeat one Pyron record or point past the file.
2. `research/experiments/EXP-0029/draw_st2jpn.py` draws `ST2JPN.BIN` entries
   from `MOJI.CHR` (some kanji fall outside the base font and draw blank;
   every page stayed readable).
3. Page id → entry (both regions): the id itself, except Demitri (+`0x10`:
   ids `00`-`07` → entries `10`-`17`) and Pyron (+`0x60`: ids `08`-`0D` →
   `68`-`6D`). Found by content: every US page id led to the right
   character's text and every Japanese one to a page of that character's
   story; Japanese entries `00`-`0F` are a placeholder line. How the code
   applies the offset is UNKNOWN.
4. The Japanese forced runs (`EXP-0029`) were checked to show the intended
   character (one frame each at 40 % and 58 % of the run, agent-reviewed).

## Result

| Roster | Pages JP → US | Content (reading by meaning) | Change type |
| --- | --- | --- | --- |
| 1 Demitri | 8 → 8 | same pages; wording rewritten (Earth's ruler → "true lord of the night"; the sun → "the day dwellers") | rewritten (wording) |
| 2 Jon Talbain | 6 → 4 | same story; short exclamations merged; the close ("the morning sun is dazzling") becomes "I will remember this day" | merged, rewritten |
| 3 Victor | 6 → 6 | Japanese: Emily introduces herself; they live happily as brother and sister. US: the villagers were unkind; carry on father's dream; celebrate today | rewritten (meaning) |
| 4 Lord Raptor | 8 → 9 | same scenes re-paginated (US `A0` is the second half of the last page); tone rewritten | re-paginated, rewritten (tone) |
| 5 Morrigan | 11 → 9 | US lacks her request for bed (`36`), the butler's reply (`37`) and a blank pause page (`B1`); US adds a new line ("You worry too much…"); order changed | **omitted** (2 lines, 1 pause), added (1 line), reordered |
| 6 Anakaris | 10 → 12 | same scenes; two pages split into four; "I had to leave this land for battle" → "returned in my land's darkest hour" | re-paginated, rewritten |
| 7 Felicia | 6 → 7 | Japanese: a victory interview and her musical stardom. US: a talent scout signs her; films about the Darkstalkers; a Blanka joke | **rewritten (different content)** |
| 8 Bishamon | 7 → 8 | Japanese: he remembers being a murderer under the curse and vows to atone by serving others. US: his oath was not enough; he must battle darkness wherever it is; new closing line | **rewritten (meaning)**, added (1 line) |
| 9 Rikuo | 8 → 9 | same scenes; names dropped (Aulbath, Aquaria); new lines (others with no homeland; build our future); "a new guardian of the holy land" → "an heir to a budding empire" | rewritten, added (lines) |
| 10 Sasquatch | 8 → 11 | same scenes split into more pages; "the opponents were weak" → "the humans are weak" | re-paginated, rewritten |
| 11 Huitzil | 5 → 6 | Japanese: auto-repair, standby mode. US: the continents are "infested with non-aboriginals"; their removal begins (new page) | **rewritten (meaning)**, added (1 page) |
| 12 Pyron (`END-03`) | 6 → 3 | merged; the planet joins his collection → he consumes it, leaving a cinder; the Earth is pulled by a great force → the Earth is burning up | merged, **rewritten (meaning)** |
| 13 Hsien-Ko | 12 → 9 | same story merged; Lei-Lei and Lin-Lin → Hsien-Ko and Mei-Ling; lines rewritten | merged, renamed, rewritten |
| 14 Donovan | 11 → 8 | same story merged; Anita → Amanda; the close ("will he lose even his heart of sorrow?") → the darkness is patient, "Soon" | merged, renamed, rewritten |

Pictures and scenes were not compared asset by asset; the Japanese runs and
`EXP-0019`'s US controls show the same artwork for each character in the
frames reviewed.

## Conclusion

**CONFIRMED (structure) / SUPPORTED (meaning):** the US main endings are a
free rewrite of the Japanese ones, re-paginated for English. Text missing
from the US is limited to Morrigan's two lines and pause page; four endings
change in meaning (Felicia, Bishamon, Huitzil, Pyron), Victor's resolution
differs, and three US endings add lines or a page that the Japanese lacks
(Bishamon, Rikuo, Huitzil). Two renames occur inside endings (Lei-Lei/Lin-
Lin, Anita). No Japanese scene is absent from the US (D-029).

## Uncertainty and Alternatives

- Every comparison is the agent's reading of the Japanese against the
  English, not an official translation (none exists for these screens; the
  PSP *Chronicle* main-ending movies `HmovieNN_1` are a possible official
  English donor, not examined).
- The page-id offset for Demitri and Pyron is inferred from content.
- Timing (US pages are mostly shown longer, D-028) is a separate change not
  analysed further.
