# Recipe: regex-explainer

> **One-line summary:** A single-page static tool that takes a regex and returns a plain-English explanation, with a test panel for sample strings. Built end-to-end through the Great Minds constellation as the cookbook's first recipe.

| Field | Value |
|---|---|
| Status | In progress — phases 1-3 captured (session 1); 4-7 to be run in session 2 with real Carmack + Norman dispatchable |
| Date | 2026-04-28 (started); session 2 to follow |
| Operator | Seth Shoultes (with Claude Opus 4.7 as the operator's hands) |
| Project repo | `/Users/sethshoultes/Local Sites/regex-explainer/` (local) |
| Plugins exercised | great-minds, great-authors, great-engineers, great-designers |
| Substitutions in session 1 | **Sara Blakely** (great-minds) substituted for **Marty Cagan** (great-designers) on discovery — great-designers wasn't loaded in session 1's agent registry. The recipe records this honestly. Sessions 2+ have great-designers and great-engineers loaded, so the build phase (Carmack, Norman) runs without substitution. |
| Time to ship | TBD (recipe live as build progresses) |

---

## Why this recipe matters

This is the cookbook's load-bearing first recipe. It demonstrates:

1. **Cross-plugin dispatch on a small, real project.** Not a hypothetical, not a self-referential demo — a tool a developer would actually use.
2. **What happens when not every plugin is loaded.** The operator's Claude Code session has 3 plugins (`great-minds`, `great-authors`, `great-filmmakers`) live, not all 10. The recipe shows the substitution pattern (Sara for Cagan, Elon for Carmack, Jony for Norman) and the trade-offs.
3. **A complete pipeline run** — PRD → Discovery → Debate → Plan → Build (parallel) → Assembly → QA → Ship — captured with each phase's actual dispatch and output, not a sanitized version.
4. **The constellation's claim that real disagreement happens** — Sara surfaced a structure-vs-intent tension Steve had to resolve. That's the kind of friction that makes the agency real.

The next recipe will exercise the full constellation (no substitutes) for comparison.

---

## The brief

The customer is **Sam Lopez, a senior dev at Bowline Software**. Operator wrote the PRD as Sam — a fictional but specific customer, real constraints, real opinions. PRD lives at `regex-explainer/PRD.md`.

```
# PRD — Regex Explainer

**From:** Sam Lopez, Senior Engineer, Bowline Software
**To:** Great Minds
**Date:** 2026-04-28

## What I want

A tool that takes a regex and explains it in plain English. I paste
`^([a-z]+)@([a-z]+\.[a-z]{2,})$` and I get back something a human can read —
what each part does, how the parts connect, what would and wouldn't match.

I also want a small "test it" panel: paste a string, see if the regex
matches, see which capture group caught what.

One page. Local file or localhost. No accounts, no SaaS, no signup.

## Why I'm asking

Five-person dev team at a small SaaS company. Half my team reads regex like
a foreign language. The other half writes regex and can't explain it three
weeks later. Tired of being the bottleneck for "what does this pattern do?"
in PR reviews.

Existing tools don't fit:
- regex101 explains *structure* not *intent* — juniors bounce off it
- regexper draws railroad diagrams — pretty but not the right register
- Stack Overflow answers are never about the regex you actually have

## Constraints

- Single static page (HTML/CSS/JS)
- JS regex flavor only for v0
- Readable, modifiable code (no 200KB webpack bundle)
- Done in a few hours, not a sprint
- Differentiated from regex101: simpler, forgiving, explanation-first

## What the customer admits he's NOT sure about

The agency should push back on these:
- Flavor scope (JS-only vs. Python/PCRE in v0)
- How to handle very long regex (collapse, paginate, refuse?)
- Naming ("Regex Explainer" vs. something cleverer)
- Whether test panel belongs in v0 or v1
```

**What's load-bearing:** "no backend" + "reads like a human wrote it" — these constraints fight each other, and discovery surfaced that fight. "Push back on these" is the explicit invitation for the constellation to disagree with the customer where it counts.

---

## Phase 1 — Discovery

**Persona dispatched:** `great-minds:sara-blakely-growth` (substituting for `great-designers:marty-cagan-designer`)

**Why the substitution:** great-designers wasn't loaded in this session. Sara's founder-empathy lens covers the same Cagan four-risks ground (value/usability/feasibility/viability) but in her register: *"would Sam actually pay for this and stick around?"*

**Brief sent (excerpt):**

> "...Don't try to *be* Cagan — bring your own founder's lens. The four risks are still the spine, but you frame them how YOU would: through the question 'would Sam actually pay for this and stick around?'..."

**Output (load-bearing excerpt):**

> *"The honest answer is: Sam would use this every day for a month, maybe two. Whether he sticks around past that depends entirely on one thing — whether the explanations are actually right. Wrong explanations, confidently delivered, are worse than no explanation. His junior devs will trust them. That trust is the whole product, and it is also the whole risk."*
>
> *"The feasibility risk is this: the tool Sam described and the tool that is actually buildable in 'a few hours' with 'no backend' are not the same tool. The agency needs to be honest about that before it commits."*
>
> **Recommendation in one sentence:** *"Before the agency writes a line of code, Sam needs to answer one question on record: does he want a tool that explains structure in plain English (buildable in a few hours, no backend, correct 95% of the time), or a tool that explains intent in human-sounding prose (requires an LLM call, requires a backend, correct far more often on complex patterns) — because those are two different builds, and the one he described in the PRD is the second one, but the constraints he set only permit the first."*

Full output: `regex-explainer/discovery.md`

**What discovery surfaced:**

- The **structure-vs-intent tension** — the customer's stated success criteria ("reads like a human wrote it") and stated constraints ("no backend") are mutually incompatible. The build can satisfy one, not both. *This is the kind of finding that justifies the discovery phase existing at all.*
- **Test panel as trust mechanism, not feature** — Sara argued test panel ships in v0 (was customer-marked "maybe v1"), because without it juniors have no way to catch wrong explanations.
- **Flavor warning as trust mechanism, not scope** — silent wrong explanations of Python regex pasted into a JS-only explainer would be worse than rejecting them.
- **Limitations callout addition** — Sara recommended adding a "what this tool won't do well" note to protect junior devs.

**Operator's customer-side decision** (recorded in discovery.md):
- **Build the rule-based, no-backend version.** Sam's "no backend" was emphatic — accept the structure-explained-in-prose ceiling.
- Adopt Sara's test-panel-in-v0 + flavor-warning-in-v0 + limitations-callout additions.

---

## Phase 2 — Debate

**Persona dispatched:** `great-minds:steve-jobs-visionary`

**The tension being debated:** *Given the no-backend, rule-based constraint settled in Phase 1, what's the right v0 scope?* Specifically: minimal annotator (paste regex → prose + test panel + flavor warning + limitations callout) vs. full playground (annotator + inline highlighting + live updates + pattern library + simplification suggestions + cross-engine quirks panel).

**Output (verdict excerpt):**

> *"Ship Camp A [minimal annotator]."*
>
> *"The inline highlighting argument is seductive and wrong. It sounds like it closes the loop, but it requires a level of structural mapping — bidirectional, real-time, accurate between prose tokens and regex tokens — that a rule-based engine will get wrong on nested groups and lookaheads, which is precisely where Sam needs it most. A broken highlighting connection is worse than no connection. It tells Sam 'I mapped this' and then maps it wrong."*
>
> *"What I'm giving up by picking Camp A: the second user. The junior Sam shares it with is going to have a worse experience than they would have in Camp B. ... I'm choosing Sam's job over the junior's education, and I'm choosing the tool being right over the tool being impressive. That's the call I'd make every time."*

Full output: `regex-explainer/debate.md`

**The scope decision** (the bullet list the build phase will execute against):

**IN v0:**
- Single-page static app (HTML/CSS/JS), no backend
- Regex input field + flags field + multiline toggle + flavor selector (JS / Python / PCRE)
- Plain-English structural explanation rendered as prose paragraph
- Flavor warning banner — appears only when the selected flavor affects interpretation
- Test panel — paste sample string, see pass/fail + capture groups, static (not live)
- Limitations callout — persistent, non-dismissible note about structure-vs-intent
- Copy-to-clipboard button

**NOT IN v0:** Inline highlighting, live updates, pattern simplification, quirks panel, common-patterns library, shareable URLs, mobile-first, persistence/analytics.

---

## Phase 3 — Plan

**Persona dispatched:** `great-minds:phil-jackson-orchestrator`

**The dispatch graph Phil produced:**

> *"All three [build dispatches] can run in parallel with one honest caveat. ... The one seam to watch: Elon's prose output format (a single paragraph? a structured list of sentences?) must match what Jony leaves room for. The briefs align them on 'a prose paragraph' as the output unit. If Elon returns a bullet list instead, the operator reconciles before assembly, not after.*
>
> ***Run all three in parallel. Reconcile at the seams before touching HTML.***"

**The three build briefs:** Phil produced fully self-contained dispatch briefs for each of the three build personas:

- **Engineer (Elon, substituting for Carmack):** Write `regex-engine.js` exposing `window.RegexExplainer = { explainRegex, testRegex, validatePattern, flavorWarning }`. Specific edge-case behavior defined: empty pattern → empty string, invalid regex → null, unknown flavor warnings handled separately.
- **UX (Jony, substituting for Norman):** Written design spec, not code. Specific page regions, color palette of ≤5 values, typography stack (system fonts), all empty/error/active states defined. Critical: explanation region must handle variable-length prose from 1 sentence to 15 lines.
- **Copy (Hemingway):** Every word on the page — page title, hero descriptor, all input placeholders, button labels, empty states, error states, flavor warning text (one each for Python and PCRE), limitations callout text. *"LOTR rhythm — plain, confident, no jargon."*

**Phil's bet** (the highest-stakes assumption in the plan):

> *"The highest-stakes assumption is that Elon's prose paragraph and Jony's explanation region are the same kind of thing. Elon will optimize for completeness — a paragraph that mentions every token. Jony will design for a region that looks right when the explanation is three sentences and also when it's eight. If Elon returns fifteen lines for a moderately complex regex, and Jony has designed for four, the page breaks visually."*

Full plan: `regex-explainer/plan.md`

---

## Phase 4 — Build (parallel dispatch)

*To run in session 2 with Carmack and Norman dispatchable. Phil's three briefs (in `regex-explainer/plan.md`) are ready to send.*

### Dispatch 1: John Carmack (great-engineers) — engineering

*Pending. Brief specified by Phil: write `regex-engine.js` exposing `window.RegexExplainer = { explainRegex, testRegex, validatePattern, flavorWarning }`.*

### Dispatch 2: Don Norman (great-designers) — UX spec

*Pending. Brief specified by Phil: written design spec (not code) covering page regions, color palette, type stack, all states. Variable-length prose handling is the load-bearing requirement.*

### Dispatch 3: Hemingway (great-authors) — copy

*Pending. Brief specified by Phil: every word on the page in LOTR-rhythm register. Word counts specified for the load-bearing slots (header descriptor, flavor warnings, limitations callout).*

---

## Phase 5 — Assembly

*To come.*

---

## Phase 6 — QA

*To come — Margaret Hamilton dispatch.*

---

## Phase 7 — Review

*To come — Steve Jobs final review.*

---

## Ship

*To come — local file:// open + verify.*

---

## Retro — what worked, what broke

*To come.*

---

## Source materials

- PRD: `regex-explainer/PRD.md`
- Discovery: `regex-explainer/discovery.md` (Sara Blakely)
- Debate: `regex-explainer/debate.md` (Steve Jobs)
- Plan: `regex-explainer/plan.md` (Phil Jackson)
- Build artifacts: `regex-explainer/build/` (TBD)
- Final ship: `regex-explainer/index.html` (TBD)
