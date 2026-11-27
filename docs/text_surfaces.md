# Saturn Text and UI Surface Audit

The Japanese reference is the T-1202G V1.000 1M image, Redump 3677.
The US reference is T-1208H V1.001, Redump 5836. Their full component
hashes are in [saturn_jp](../references/saturn_jp/README.md) and
[saturn_us](../references/saturn_us/README.md). This audit compares the
ordinary title, menus, Arcade and ending paths. The audio rows cite
earlier matched traces and recordings. Binary captures stay in `local/`.

| Surface | Japanese observation | US observation | Evidence and Deluxe behavior |
| --- | --- | --- | --- |
| BIOS and license | Japanese Saturn logo sequence and local SEGA copyright | US Saturn orb and US SEGA copyright | EXP-0001. Each stock disc selects its region BIOS. Mednafen's stock settings show no game warning on the matched cart-free boots (EXP-0002). Deluxe uses the US image's area. |
| Boot and loading labels | Capcom, NOW LOADING in English | Same labels. One matching NOW LOADING frame is byte-identical | EXP-0001, `emu003/{jp1,us1}/frames/029.png`. Relative text scan finds the loading label in `MAIN.BIN` (EXP-0047). |
| Intro logo card | A red logo beginning VAM is drawn on black | Red DARKSTALKERS logo card | EXP-0001/0002, `emu004/{jp-none,us-none}/frames`. Deluxe uses the US intro in all editions. |
| Title and title menu | VAMPIRE HUNTER, followed by ARCADE, VS and OPTION | NIGHT WARRIORS, with the same three menu entries | `emu003/{jp1,us1}/frames/065.png`, `exp0049/live-{jp,us}/title-menu.png`. Deluxe keeps the US title graphics. |
| Attract demo | Anakaris vs. Aulbath. English fight labels | Anakaris vs. Rikuo. English fight labels | `emu003/{jp1,us1}/frames/092.png`; later moments diverge as play branches. EXP-0040 controls the settings when comparing animation. |
| Option mode and configuration | English labels, including SOUND MODE and CONFIGURATION | Same labels and stock navigation | `exp0042/app-{jp,us}-none/boot1`, EXP-0042, EXP-0047. Deluxe adds EDITION and NAMES. |
| Appendix | Same English menu, including ANIMATION with CUT and FULL | Same menu and unlock code | EXP-0042, `exp0042/app-{jp,us}-none/boot1/07-appendix.png`. Deluxe exposes it by default. |
| Fighter and speed selection | LEI-LEI nameplate, SPEED SELECT, NORMAL and TURBO | HSIEN-KO nameplate, same speed choices | `exp0049/live-{jp,us}/select.png`. The Enhanced names preference was checked on the select screen with US Enhanced showing LEI-LEI. |
| Mode selection | MODE SELECT, NORMAL and AUTO GUARD | MODE SELECT, NORMAL and AUTOMATIC | `exp0049/live-{jp,us}/mode.png`. This is a label difference. Mechanics were outside this comparison. The selection follows EDITION in Deluxe. |
| Match introduction | LEI-LEI and VICTOR | HSIEN-KO and VICTOR | `exp0049/live-{jp,us}/load.png`. Both fighter-name art routes were traced in D-015. |
| Fight and later Arcade stage | English HUD and prompts, Lei-Lei. Victor first, then Bishamon | The same HUD labels and opponents, Hsien-Ko | `exp0049/live-{jp,us}/{first-fight,second-fight}.png`. Actor timings and move effects differ in the sampled frames. These samples do not compare identical attacks. |
| Continue and reselect | CONTINUE? and countdown in English, Victor's quote in Japanese | Same countdown, Victor's quote in English | `exp0049/live-{jp,us}/{continue,reselect,rematch}.png`. Both matched runs accepted Continue and returned to the first matchup. |
| Winner quote | Japanese renderer and stock Japanese quote selector | English renderer and stock US quote selector | `exp0049/live-{jp,us}/quote.png`, EXP-0049. US Enhanced mixes the extra translations with the stock English lines. |
| Main ending | Japanese dialogue and original scripts. Hsien-Ko's original name is Lei-Lei and her sister is Lin-Lin | Rewritten and re-paginated English dialogue. Hsien-Ko's sister is Mei-Ling. Donovan's Anita becomes Amanda | EXP-0030, EXP-0046, matched Hsien-Ko ending captures in `exp0049/main-{jp,us}/ending.png`. The NAMES option operates on fighter labels and art. The scripts retain their edition's wording. |
| Epilogue | Scrolls a Japanese paragraph over the art | Scrolls the art with the text gated off | Matched captures in `exp0049/end-{jp,us}/epilogue.png` and earlier D-010–D-012 comparisons. US Enhanced restores English text from the PSP reference, and both JP editions draw the Japanese text. |
| Credits and cast names | Japanese fighter names in the cast roll | US fighter names in the cast roll | Matched `exp0049/end-{jp,us}/cast-second.png`, GALLON and JON TALBAIN. Cast-route table trace in D-015. The names option reuses the existing paired tables. |
| Voices and sound | Morrigan's four voice cues, two Donovan events and the Sasquatch behaviors were observed in the Japanese source | Those cues or behaviors are suppressed by the US branches under the same conditions | D-007–D-008, D-031–D-033. Shared sound banks are byte-identical. Intro voice and ordinary fight effects were not exhaustively isolated cue by cue. |

The capture manifest and short reproduction commands are in
[EXP-0050](../research/experiments/EXP-0050/README.md). Open register items
are tracked in [coverage exceptions](coverage_exceptions.md).
