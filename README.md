# Great Minds Cookbook

Recipes for working with the [Great Minds constellation](https://github.com/sethshoultes/great-minds-constellation) — reusable playbooks for using named-figure personas to do real work.

Each recipe answers one question: **how would the constellation actually build this kind of thing?**

## Recipes vs. runs — the distinction that matters

This cookbook separates two different artifacts:

| | Recipe | Run |
|---|---|---|
| **What it is** | A reusable playbook. Step-by-step instructions you (the reader) follow in your own Claude Code session. | A case study. The actual outputs, screenshots, and retro from one specific time the recipe was run. |
| **Lives at** | `recipes/<name>/README.md` | `recipes/<name>/runs/YYYY-MM-DD.md` |
| **Updated when** | The recipe pattern itself improves (better dispatch templates, new pitfalls surfaced, variations documented). | A new run of the recipe is captured. |
| **Read this when** | You want to *build* something using the constellation. | You want *evidence* the recipe works, or to learn from a specific run's failures and wins. |

The recipe is the playbook. The run is the proof.

This pattern is modeled on [Anthropic's claude-cookbooks](https://github.com/anthropics/claude-cookbooks) — instructions you can walk through and execute, not retrospectives you read about.

## Recipes

### Shipped (read these — runs prove they work)

| Recipe | Project type | Plugins exercised | First shipped |
|---|---|---|---|
| [regex-explainer](recipes/regex-explainer/) | Single-page static developer tool | great-minds, great-engineers, great-designers, great-authors | [2026-04-28](recipes/regex-explainer/runs/2026-04-28.md) |
| [multi-agent-essay-production](recipes/multi-agent-essay-production/) | Long-form blog essay (1,000–1,800 words) with original featured image | great-authors, great-minds (Jony Ive) | [2026-04-29](recipes/multi-agent-essay-production/runs/2026-05-07-skills-as-sops.md) |

### Queued

These recipes are committed for the next phase. Each tests a different shape — not another small static tool.

| # | Recipe | Project type | Plugins to exercise | Why this recipe |
|---|---|---|---|---|
| 2 | Book Proposal | Publisher-ready 4-6K word nonfiction proposal incl. sample chapter | great-minds, great-authors, great-publishers, great-marketers, great-researchers | Tests great-publishers in *editorial-judgment* mode (not just design); stresses great-authors at production prose quality |
| 3 | Decision Memo | 2-3K word memo with three perspectives + dissent on a real business decision | great-minds, great-counsels, great-researchers, great-operators, great-marketers | Tests *integrative* multi-plugin synthesis (recipe #1 was additive); reconciles disagreement into one coherent doc |
| 4 | OKR Set | Quarterly OKR document from a fuzzy annual goal | great-minds, great-operators, great-researchers, great-counsels | Tests structured constraint satisfaction; broadly applicable; LOW risk |

### Backlog

| # | Recipe | Why deferred |
|---|---|---|
| 5 | Film Treatment | great-filmmakers as primary creative engine — interesting but not the highest-leverage next test |
| 6 | Research Brief | Universal upstream artifact — useful, but quality is hard to evaluate without domain expertise |

### Considered and rejected

| Recipe | Why rejected |
|---|---|
| Launch Plan | Would just confirm great-marketers works for copy — doesn't surface new failure modes in the constellation's coordination layer |
| Philosophical Inquiry | The "appears rigorous while being shallow" failure mode is unverifiable without a domain expert. The cookbook's load-bearing claim is recipes ship and are evaluable; this one isn't. |

## Templates

When writing a new recipe or capturing a new run, start from the templates:

- [`recipes/_template-recipe.md`](recipes/_template-recipe.md) — the playbook template (one of these per recipe folder)
- [`recipes/_template-results.md`](recipes/_template-results.md) — the run / case study template (one of these per run, in `runs/`)

Both enforce structure so recipes are comparable.

## Testing recipes

A recipe isn't done until it's been **run end-to-end**. The build the recipe describes must actually ship.

- **Recipes that have at least one shipped run** are evidence — the playbook works.
- **Recipes with no runs yet** are aspirational — they're documented intent, not yet validated.
- **Failed runs are valuable** — file them under `runs/` with `Status: Failed`. The patterns of failure are what make the recipe sharper.

Every shipped run should include screenshots or another concrete artifact in `runs/<date>/screenshots/` so the proof is inspectable, not just narrated.

## Recipe folder layout

```
recipes/
├── README.md                                # this file (or one level up)
├── _template-recipe.md                      # playbook template
├── _template-results.md                     # case study template
└── <recipe-name>/
    ├── README.md                            # THE RECIPE — the playbook
    └── runs/
        ├── YYYY-MM-DD.md                    # one case study per run
        └── YYYY-MM-DD/
            └── screenshots/                 # visual proof
```

A recipe folder always has its own `README.md` (the playbook) and a `runs/` directory.

## Contributing

The cookbook is curated. To propose a recipe:

1. Pick a project shape that exercises the constellation in a way no existing recipe does
2. Run the project end-to-end through the constellation, capturing each phase's dispatch + output
3. Write the **recipe** (`recipes/<name>/README.md`) using the template — that's the playbook
4. Write the **run** (`recipes/<name>/runs/YYYY-MM-DD.md`) using the run template — that's the case study from your specific build
5. Open a PR

What makes a recipe useful is the honesty about what broke and the specificity of the dispatch templates, not the polish of the prose.

## Related

- [Great Minds Constellation](https://github.com/sethshoultes/great-minds-constellation) — the marketplace + plugins this cookbook documents
- The brain learning [`agency-operator-must-redirect-not-pinch-hit`](https://github.com/sethshoultes/building-with-ai-brain/blob/main/learnings/agency-operator-must-redirect-not-pinch-hit.md) — when the constellation fails, file an issue, don't pinch-hit

## License

MIT — see [LICENSE](./LICENSE).
