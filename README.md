# TLA design guide

How Arcforma materials for **The Last Agency** should look and sound. TLA is a brand strategy and PR firm in New York and Paris, working with creative businesses across design, architecture and lifestyle. Their own identity (by Cotton Design) is black, image-first and restrained, so ours is too.

## Sources

- **thelast.agency**: black theme color (`#000000`), a two-line wordmark ("The Last / Agency"), full-bleed image galleries, very little copy, and services named without descriptions.
- **Session decks from Oct 1 and Oct 7, 2026**: the type, color and layout system below. `templates/tla-session-template.pptx` is the Oct 7 deck.

Not captured yet: the exact web fonts and any hex values beyond black. The site's stylesheet couldn't be fetched from the build environment. If you have it open in a browser, add the font names here.

## Color

| Token | Hex | Use |
|---|---|---|
| background | `#000000` | Every slide and page. No light mode. |
| text | `#FFFFFF` | Titles, labels, body. |
| accent | `#F8FFD8` | Pale lime. Only **one** emphasis per slide, always the last row or column (the step that matters most, or the call to action). As a fill it takes black text. |
| muted | `#8E8E8E` | Subtitles, column headers, closing notes. |
| mutedLight | `#BBBBBB` | Quotes and example prompts. |
| rule | `#4A4A4A` | Row dividers. White rules are for the footer and column tops. |

## Type

- **Helvetica Neue Medium**, all caps, everywhere. No bold, no italics, no second typeface.
- Hierarchy comes from size and color, not weight. Sizes are in `tokens.json`. The display words on the title slide run at 143pt with tight tracking and are allowed to bleed off the edge.
- Short lines. A row value should fit on one line (about 45 characters). Break longer thoughts with `|` instead of letting them wrap.

## Layout

- 16:9, 0.44" side margins, left aligned.
- Footer on every slide: a thin white rule, `TLA / TOPIC` on the left and `ARCFORMA AI INC.      NN / NN` on the right, at 9.5pt.
- Title slide: three huge words ("THE / THIRD / SESSION"), client and date lines, and a lime line of today's topics.
- Content layouts, in `scripts/tla_deck.py`:
  - `rows4`: a label and a one-line value, four rows. Use for check-ins and wrap-ups.
  - `rows4quote`: the same, plus a grey example prompt at the bottom.
  - `rows6`: six tighter rows with a subtitle and note. Use for checklists.
  - `numbered4`: `01  LABEL` rows with dividers, and the last row in a lime band. Use for agendas and processes.
  - `big4`: four oversized words with short explanations. Use for the parts of a brief.
  - `columns4`: four columns with stacked short lines, and the last column in lime. Use for builds and proposals.

## Voice

Taken from TLA's own copy: "clarify their vision, sharpen their narrative, and amplify their reach."

- Use imperatives and plain verbs: CHECK THE FACTS. SHIP A FIRST DRAFT TODAY.
- Use their words for their work: coverage, pods, reports, clients, launches, "daily media coverage grids."
- Don't use AI hype or tool jargon on slides. Name what the thing does for the agency.

## Making a deck

```bash
pip install python-pptx
python scripts/tla_deck.py examples/2026-10-27-session-3.json out.pptx
```

Each slide in the spec gives a `layout`, its slots (see `LAYOUTS` in the script) and an optional `footer` label. The full Oct 27 deck is in `examples/2026-10-27-session-3.pdf`.
