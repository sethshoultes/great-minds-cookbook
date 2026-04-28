# Recipe: regex-explainer

> **One-line summary:** A single-page static tool that takes a regex and returns a plain-English explanation, with a test panel for sample strings. Built end-to-end through the Great Minds constellation as the cookbook's first recipe.

| Field | Value |
|---|---|
| Status | Shipped (2026-04-28). All 7 phases run end-to-end. |
| Date | 2026-04-28 (sessions 1 + 2 same day) |
| Operator | Seth Shoultes (with Claude Opus 4.7 as the operator's hands) |
| Project repo | `/Users/sethshoultes/Local Sites/regex-explainer/` (local) |
| Plugins exercised | great-minds, great-authors, great-engineers (loaded in session 2 — gave us real Carmack instead of Elon-as-substitute) |
| Substitutions in session 1 | **Sara Blakely** (great-minds) substituted for **Marty Cagan** (great-designers) on discovery — great-designers wasn't loaded in session 1's agent registry. |
| Substitutions in session 2 | **John Carmack** (great-engineers) was AVAILABLE — used real Carmack instead of Elon-as-substitute. **Jony Ive** (great-minds) substituted for **Don Norman** (great-designers) on UX spec — great-designers still not loaded. Hemingway (great-authors) was real both sessions. Net: 1 of 2 session-1 substitutions cleared in session 2. |
| Time to ship | ~50 minutes wall time in session 2 (build → assembly → QA → fix → review → ship) |
| Final artifacts | `regex-explainer/index.html` (~22KB), `regex-engine.js` (~38KB, ~970 lines, hand-rolled recursive-descent regex parser + prose generator + test driver) |

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

Plan.md described three briefs but didn't include their full text — they lived in session 1's conversation, which is gone in session 2. The operator reconstructed each brief from the scope decision (debate.md), the design spec requirements, and Phil's seam notes. Each brief had to be self-contained because dispatched sub-agents start with empty conversation context.

**Three Agent({}) calls fired in parallel in a single message** — the constellation's claim about parallel execution actually works.

### Dispatch 1: John Carmack (great-engineers:john-carmack-engineer) — engineering

**Real Carmack was available** in session 2 (great-engineers loaded). Session 1 had planned to substitute Elon. We used the real one.

**Brief shape (excerpts):**

> "YOUR DELIVERABLE: a single file at `/Users/sethshoultes/Local Sites/regex-explainer/build/regex-engine.js` — pure vanilla JS, no dependencies, no build step, no framework... Use the Write tool."
>
> "EXPLANATION QUALITY BAR: ... Bad output (regex101-in-English — DO NOT SHIP THIS): 'Anchor: start of line. Group 1: character class, one or more. Literal @. ...' Good output (target register): 'Starts at the beginning of the string and captures one or more characters from the set lowercase letters, digits, dots, underscores ...'"
>
> "CONSTRUCTS YOU MAY DECLINE: if you encounter atomic groups, conditionals (?(1)...), recursion (?R), or any construct you can't honestly explain — say so in one sentence: 'this pattern uses [construct] which this tool doesn't currently explain in detail.' Better than guessing."

**Output (Carmack's summary, verbatim):**

> *"Hand-rolled recursive descent over the pattern string. Five recursive entry points: parseAlternation → parseSequence → parseAtom → (parseGroup | parseCharClass | parseEscape) with parseQuantifier attached to the atom that owns it. Output is a plain-object tree (`{ type: 'sequence', children: [...] }`); no class hierarchy. The prose pass is one switch over node.type."*
>
> *"Decisions worth knowing: Top-level ^...$ is hoisted out into framing sentences ('Starts at the beginning...' + 'The whole pattern must consume the entire string'). The PRD's good example does this and it matters for readability. Quantified character classes get a special 'characters from the set X, Y, or Z' rendering instead of 'one or more of any of...'. Quantified groups read as '..., repeated N times' instead of 'one or more of group 1 captures...' — same motivation: avoid stuttering."*
>
> *"Performance: 5000 explanations of typical patterns in 52ms (~0.01ms per call), well under the 50ms-per-call ceiling."*

640 lines, fully commented. Bonus: also exports for Node, which let the operator smoke-test from the CLI before assembly.

### Dispatch 2: Jony Ive (great-minds:jony-ive-designer, substituting for Don Norman) — UX spec

great-designers still not loaded in session 2. Jony substituted with explicit framing in the brief: *"Where Norman would lead with cognitive load and signifiers, you lead with material honesty, hierarchy, and inevitability."*

**Brief shape (excerpts):**

> "YOUR DELIVERABLE: a written design spec (NOT code) at `/Users/sethshoultes/Local Sites/regex-explainer/build/design-spec.md`. The operator will translate your spec into HTML/CSS at assembly time."
>
> "REQUIRED OUTPUT — your spec must include all of these: A. Page layout. B. Type stack. C. Color palette (≤5 values). D. Spacing scale. E. The explanation region in detail [the load-bearing section]. F. The flavor warning banner. G. The test panel. H. Button styling. I. States for all interactive elements. J. Responsive behavior."

**Output (Jony's four "decisions to honor", verbatim):**

> *"1. The explanation region has no fixed height and no internal scrollbar. It grows with its content. The page scrolls. An internal scrollbar demotes the primary output to a sidebar widget. That is not acceptable."*
>
> *"2. The copy button is absolutely positioned at the top-right of the explanation region — not anchored to the bottom of the prose. If it floats below the prose, it moves on every explanation. Sam will copy constantly. It must be findable in a fixed, predictable location."*
>
> *"3. The flavor warning banner uses max-height toggling instead of display:none/block. Set transition-duration to 0ms per the no-animation directive. The explanation region must not jump 80px when the banner appears or disappears. This is the difference between a tool that feels built and one that feels assembled."*
>
> *"4. Matched and no-match results carry identical visual weight — same color, same size, same weight. Do not color 'Matched' green or 'No match' red. The tool reports. It does not judge. A no-match result is often the correct and expected outcome."*

484-line spec with specific px/hex/font-stack values throughout. The operator implemented all four "honor" decisions.

### Dispatch 3: Hemingway (great-authors:hemingway-persona) — copy

Real Hemingway both sessions. The brief asked for every on-page string in 29 numbered slots.

**Brief shape (excerpts):**

> "YOUR DELIVERABLE: every word that appears on the page, written out as a single document at `/Users/sethshoultes/Local Sites/regex-explainer/build/copy.md`."
>
> "WRITE COPY FOR EVERY SLOT BELOW. Keep within the word counts. Don't add slots; don't merge slots."
>
> "CONSTRAINTS: No emoji. No exclamation points. No 'Welcome!' No 'Awesome!' No 'Let's get started.' ... The hero descriptor (slot 2) and the limitations callout (slot 4) are the two slots the whole tone of the page hangs on."

**Output (the load-bearing slots, verbatim):**

> Slot 2 (hero descriptor): *"Paste a pattern. Get a plain-English account of what it does."*
>
> Slot 3 (limitations callout heading): *"Before you trust this"*
>
> Slot 4 (callout body): *"This tool reads regex structure and describes it in plain English. It doesn't know what the pattern was written to do — only what the syntax says. Rule-based parsing can misread unusual constructions, especially nested groups or uncommon syntax combinations. Treat the output as a starting point, not a verdict. Run it against real test cases before you rely on it for anything that matters."*

**Hemingway's note on what he held the line on, verbatim:**

> *"The hero descriptor went through four versions. The one I kept — Paste a pattern. Get a plain-English account of what it does. — earns its rhythm from the period between two short declarative sentences. 'Account' is doing work: it's precise without being clinical, it implies no more than the tool actually delivers."*
>
> *"The one thing I'd push back on: if the operator softens slot 3 ('Before you trust this') to something like 'A note on accuracy,' the whole limitation section loses its edge. The heading has to carry weight the body can't repeat."*

### Phil's seam check at assembly time

Phil's plan flagged one seam: Carmack's prose output length (1 to 15 sentences) had to match what Jony designed for. The seam held: Carmack returned single-paragraph prose, Jony's region was specifically specced to flex 1–15 sentences without an internal scrollbar. **No reconciliation needed.**

---

## Phase 5 — Assembly

The operator integrated the three artifacts into a single `index.html` following Phil's assembly order: read Carmack's API shape first, read Jony's spec in full, drop Hemingway's copy into named slots, wire engine functions to button events.

**File structure shipped:**
```
regex-explainer/
  index.html           ← entry point (single file Sam can read in VS Code)
  regex-engine.js      ← Carmack's engine (sibling, not bundled)
  build/               ← per-persona artifacts kept for the recipe
    regex-engine.js    (mirror)
    design-spec.md     (Jony)
    copy.md            (Hemingway)
```

**One operator-side spec-vs-copy reconciliation:** Hemingway's copy.md slot 7 ("Multi-line mode") and Jony's spec ("expand to multiline" / "collapse to single line" two-state label) disagreed. The operator went with Jony's stateful labels because a toggle without an active-state distinction is a worse UX than the spec drift. Documented here, surfaced again in QA, accepted as a deliberate call.

**One security-hook collision worth recording:** the operator's first pass at the test-result rendering used `innerHTML` with `escapeHtml` — properly sanitized but the security hook objected on principle. The refactor used `createElement` / `textContent` exclusively, which is unambiguously safe and prevents a future maintainer from accidentally introducing XSS. The hook fired again later on a comment containing the word "exec" (about `RegExp.prototype.exec`, not shell `exec`). Reworded the comment. **Lesson for the cookbook:** security hooks pattern-match on word-level signals; defensive code that's safe in context can still trip them. Cleaner code is the right response, not annotations.

**Smell test (Phil's exact sequence):**

Pattern `^([a-z]+)\d{2,4}$`, Python flavor, test string `hello42`. Result: explanation reads naturally, flavor warning fires (correctly: Python's `\d` is Unicode-aware vs JS's ASCII-only — Phil's smell-test description in plan.md said no warning would fire, but the warning is the correct behavior; this is logged as a Phil-was-wrong-on-the-spec, not an engine bug), Test panel reports `Match found / hello42 / Position 0 / Group 1: hello`. Smell test PASS.

Screenshot: `regex-explainer/smell-test-result.png` (assembled state) and `final-ship-state.png` (post-QA-fixes).

---

## Phase 6 — QA

**Persona dispatched:** `great-minds:margaret-hamilton-qa`

The brief gave Margaret the live URL and the Playwright tools. She used them to actually exercise the tool, not just read source.

**Margaret's findings (verbatim verdict):**

> *"Fix-then-ship. Two issues block: P0-1 (named group name lookup produces wrong group names on any pattern where two groups capture the same value — exactly the kind of confident wrong explanation Sara said would kill trust) and P0-2 (quantified lookahead produces prose that actively misinforms about how the pattern executes). Both are engine-level bugs in regex-engine.js, both are small fixes. P1-1 (the 'and finally' ambiguity in Sam's exact PRD test case) should be fixed in the same pass. The rest can wait for v1."*

**The five flagged issues:**

| ID | Severity | What | Outcome |
|---|---|---|---|
| P0-1 | Block | `testRegex` matched named-group names by *value* equality against `m.groups`, so two groups capturing identical strings (`foo-foo`) silently mislabeled the second group with the first group's name. Exactly Sara's "confident wrong explanation kills trust" failure mode. | **FIXED.** Engine now walks the parser AST to build an authoritative `{captureIndex: name}` map. |
| P0-2 | Block | `(?=foo)+` produced prose claiming "repeated one or more times" — but lookarounds are zero-width; quantifiers on them are practically meaningless. Actively misinformed the reader. | **FIXED.** Quantifier on a lookaround is captured separately as `quantifierIgnored` and surfaced in prose: *"a quantifier '+' follows this lookaround but is ignored — lookarounds are zero-width."* |
| P1-1 | Block | Sam's email regex — the load-bearing PRD test case — produced *two* `and finally` connectives in the same sentence (one for the top-level closure, one inside group 2's inner sequence). Group 2's scope became ambiguous to a careful reader. | **FIXED.** Added an `embedded` flag to the prose-walking env. Outer connective stays `and finally`; embedded sub-phrases use `ending with`. First fix overshot (broke the smell test) before threading both flags correctly. |
| P1-2 | Note | Multi-line toggle copy drift (Hemingway's "Multi-line mode" vs. Jony's "expand to multiline / collapse to single line"). | **Documented, not changed.** A stateful toggle needs distinct idle/active labels; Jony's spec is the right call here, and the recipe records the explicit reconciliation. |
| P1-3 | Block | Flavor `<select>` was missing its keyboard-focus outline (the general `select:focus { outline: none }` rule overrode the spec'd 2px solid #2D6BE4). | **FIXED.** Added a more-specific `.flavor-select:focus` rule. Sam's team uses keyboards. |

P2 issues (deprecated `execCommand` clipboard fallback, dead code branch in error path, awkward "2 to 4 of literal 'a'" plural) were noted for v1 and not fixed.

**The recipe-level lesson** is that Margaret didn't catch *typos* — she caught two confidently-wrong-prose failure modes that the operator's smoke tests would never have surfaced. The question her brief asked her to focus on — *"any pattern where the prose is technically wrong is a P0"* — is the same question Sara raised in discovery. The pipeline carried Sara's discovery concern all the way to QA, and QA caught it. **That is the constellation working.**

---

## Phase 7 — Review

**Persona dispatched:** `great-minds:steve-jobs-visionary`

Steve had already weighed in at the scope-debate phase (he picked Camp A, the minimal annotator). The operator asked him for a single ship/no-ship verdict on the assembled tool, with the same Playwright access Margaret had.

**Steve's verdict, verbatim:**

> *"Ship. The PRD's 'Done means' bar is cleared on every point — the email pattern explains correctly, the test panel matches and labels groups accurately, the page is calm and readable by a junior without a guide."*

**Steve's three v1 cuts, verbatim:**

> *"The prose phrasing 'Matches a group named X captures...' is grammatically broken — it reads 'Matches a group named year captures' instead of 'in which group year captures.' Fix the sentence construction before v1."*
>
> *"The test string textarea is disproportionately tall for a single-line string — a junior might wonder if they're supposed to paste multiple strings. Shrink it to 2-3 rows."*
>
> *"The one console error deserves a look before anything called v1 goes to a second customer."*

**Two of three fixed in this session before declaring ship:**

- The grammar bug ("Matches a group named X captures...") was real and affected both named and unnamed group leads. Fixed by detecting phrases that begin with their own subject-verb construction (`group N captures`, `a group named X captures`, `a check that...`) and skipping the leading `matches` framing in those cases. Verified across 11 pattern shapes.
- The console error (a missing-favicon 404) was a one-line fix: `<link rel="icon" href="data:,">`. Removed.
- The textarea height was Steve disagreeing with Jony's spec'd `min-height: 80px`. The operator left it as Jony specified for v0 and noted Steve's concern in this retro for v1.

---

## Ship

The tool is shipped at `/Users/sethshoultes/Local Sites/regex-explainer/index.html`. Opens via `file://` (clipboard falls back to `execCommand` outside secure contexts) or `python3 -m http.server`. No accounts, no signup, no telemetry, no build step, no external dependencies.

Final smell test: green. Console: clean. PRD's "Done means" bar: cleared.

---

## Retro — what worked, what broke

**What worked:**

- **Parallel dispatch is real.** Three Agent calls in a single message, three artifacts on disk in ~10 minutes. The seam Phil flagged (Carmack's prose length vs. Jony's region design) held — the brief alignment ("a prose paragraph as the output unit") prevented the reconciliation drift.
- **The discovery concern carried all the way to QA.** Sara surfaced "wrong-but-confident explanations are the worst failure mode." That exact concern showed up in Margaret's brief, and Margaret caught two engine-level bugs that match the failure mode (P0-1 named-group lookup, P0-2 quantified lookarounds). The pipeline transmitted concern, not just artifacts.
- **Fewer substitutions than session 1 = real Carmack instead of Elon.** Loading great-engineers in session 2 changed the build register. Carmack's instinct ("Top-level `^...$` is hoisted into framing sentences") is exactly what made Sam's email regex readable. A substitute might not have made that call.
- **Ship-with-fixes-after-QA, not ship-without-QA.** Margaret's two P0s were both engine-level prose bugs that would have shipped silently. The smoke test would never have caught them — they only show up on patterns the smell test didn't cover. QA earned its slot.

**What broke (or almost did):**

- **Plan.md's claim that the briefs were "in this conversation" was a load-bearing handoff failure.** Session 1 is gone in session 2. The operator reconstructed each brief from scope, spec, and seam notes. **Lesson for future cookbook recipes: Phil's plan output should include the actual brief text, not a reference to it.** A brief that requires a live conversation to find isn't a brief.
- **First P1-1 fix overshot and broke the smell test** because `top` and `embedded` are different concerns and the operator initially conflated them. Caught immediately by re-running smoke tests; second fix landed cleanly. **Lesson:** when a fix involves a flag, write down what each flag means before changing call sites.
- **Hemingway-vs-Jony copy disagreement on the multiline toggle** had no Phil-style mediator. The operator made the call. The right call is documented in this recipe; an operator who reflexively defers to the copy spec would have shipped a worse UX. **Lesson:** the cookbook recipe is where this kind of operator judgment becomes legible.
- **Phil's smell test specified "no flavor warning fires" for the `\d` + Python combo. Carmack's engine fires the warning correctly** (Python's `\d` is Unicode-aware; JS's is ASCII). Phil was wrong on his own smell test. The engine call was right. **Lesson:** smell tests can be wrong; treat their expectations as a starting hypothesis, not a verdict.
- **One security-hook false positive on a comment containing the word "exec"** about `RegExp.prototype.exec`. Reworded the comment. **Lesson:** security hooks pattern-match on tokens, not semantics. Don't rely on hooks for review; use them as a prompt to look harder.

**For the next recipe:**

- Have Phil's plan include literal brief text, not references.
- Run the smoke test BEFORE assembly when the engine has a Node export. Caught Carmack's engine working correctly without ever opening a browser.
- Margaret should always be dispatched with live tool access, not just source-read access. Two of her P0s required actually running the tool.
- A persona's "v1 cut" is sometimes a v0 fix that costs ten lines (the favicon). Don't reflexively defer.

---

## Source materials

- PRD: `regex-explainer/PRD.md`
- Discovery: `regex-explainer/discovery.md` (Sara Blakely, substituting for Cagan)
- Debate: `regex-explainer/debate.md` (Steve Jobs)
- Plan: `regex-explainer/plan.md` (Phil Jackson)
- Build artifacts: `regex-explainer/build/regex-engine.js` (Carmack), `build/design-spec.md` (Jony), `build/copy.md` (Hemingway)
- QA report: in this recipe (the operator captured Margaret's P0/P1/P2 list inline)
- Final ship: `regex-explainer/index.html` + `regex-engine.js`
- Smell-test screenshot: `regex-explainer/smell-test-result.png`
- Final-state screenshot: `regex-explainer/final-ship-state.png`
