# claude-design-tla

Design system for anything Arcforma makes for The Last Agency (TLA): session decks, one-pagers, briefs.

- Read README.md for the rules before designing anything.
- Decks: write a JSON spec and run `python scripts/tla_deck.py <spec.json> <out.pptx>`. Do not hand-build slides; the script clones layouts from `templates/tla-session-template.pptx` so styling stays exact.
- `tokens.json` holds colors, type and sizes for non-deck outputs (HTML, docs).
- Client-facing outputs only: keep internal notes (pricing, coaching feedback) out of anything Bradley sees.
