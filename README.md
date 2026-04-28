# Great Minds Cookbook

Recipes for working with the [Great Minds constellation](https://github.com/sethshoultes/great-minds-constellation) — concrete walkthroughs of using named-figure personas to do real work.

Each recipe answers one question: **how would the constellation actually build this?**

## What's a recipe

A recipe is a documented walkthrough of a real project built using the constellation. Not a tutorial, not a marketing piece — a retro of an actual run. Each recipe captures:

- **The brief** — what was asked for, in customer voice
- **Discovery** — what risks the constellation surfaced before building (Cagan in `great-designers`, or Sara Blakely in `great-minds` if discovery is led founder-style)
- **Debate** — where Steve Jobs / Elon Musk / Phil Jackson stake positions on scope and approach
- **Plan** — Phil Jackson's dispatch list: who builds what, in what order
- **Build** — the parallel dispatches, with each persona's actual output captured verbatim
- **Assembly** — what the operator (the human) did to integrate the parallel outputs
- **QA** — Margaret Hamilton's verdict + the fixes
- **Review** — Steve Jobs's final ship/no-ship call
- **Retro** — what worked, what broke, what the recipe taught us about the dispatch pattern for next time

Recipes are real. Not idealized. If a dispatch returned slop, the recipe says so. If a persona was substituted for an unavailable one, the recipe explains why and what was lost.

## Why a cookbook

The constellation is ~111 personas across 10 plugins. Knowing *which* personas to dispatch for *which* phase of work is the operator's job — and a hard one if you're new. Recipes show the patterns:

- Which plugins compose well for which kinds of project
- What a *self-contained brief* looks like for each persona
- Where parallel dispatch saves time vs. where serial review is required
- What happens when you swap one persona for another (Hemingway vs. Vonnegut for copy; Cagan vs. Sara Blakely for discovery)

The cookbook is the constellation's manual for using itself.

## Recipes

*(None shipped yet — first recipe in progress)*

| Recipe | Project type | Plugins exercised | Status |
|---|---|---|---|
| [regex-explainer](recipes/regex-explainer.md) | Single-page static tool | great-minds, great-engineers, great-designers, great-authors | In progress |

## Recipe template

When writing a new recipe, start from [`recipes/_template.md`](recipes/_template.md). It enforces the section structure so recipes are comparable.

## Testing recipes

A recipe isn't done until it's been **run end-to-end**. The build the recipe describes must actually ship. Recipes that haven't been tested are marked clearly. Untested recipes are aspirational; tested recipes are evidence.

## Contributing

The cookbook is curated. To propose a recipe:

1. Run a real project through the constellation
2. Capture each phase's dispatch + output as you go (this is the bulk of the work)
3. Write up the retro using the template
4. Open a PR

What makes a recipe useful is the honesty about what broke, not the polish on what worked.

## Related

- [Great Minds Constellation](https://github.com/sethshoultes/great-minds-constellation) — the marketplace + plugins
- The brain learning [`agency-operator-must-redirect-not-pinch-hit`](https://github.com/sethshoultes/brain/blob/main/learnings/agency-operator-must-redirect-not-pinch-hit.md) — when to file a recipe issue vs. when to fix it inline

## License

MIT — see [LICENSE](./LICENSE).
