# Recipe: Regex Explainer

> **One-line summary:** Build a single-page static tool that takes a regex and returns a plain-English explanation, with a test panel for sample strings. Reusable playbook for any small developer-tool project where the deliverable is HTML/JS that opens locally in a browser.

| Field | Value |
|---|---|
| Project type | Single-page static developer tool (HTML + vanilla JS, no backend) |
| Plugins exercised | great-minds, great-engineers, great-designers, great-authors |
| Time to ship | ~3-5 hours (1.5 hours of operator work + dispatch + assembly) |
| Risk level | MEDIUM (engine correctness is load-bearing) |
| First shipped | 2026-04-28 ([run notes](runs/2026-04-28.md)) |

---

## What you'll have at the end

- A standalone `index.html` (~20-25 KB) that opens in any browser via `file://`
- A `regex-engine.js` module (~40 KB) — hand-rolled recursive-descent regex parser plus a prose explanation generator
- A working "test panel" UI: paste a sample string, see match result + capture groups
- A flavor selector (JS / Python / PCRE) with warnings when the selected flavor would interpret the pattern differently than JS
- A persistent "limitations" callout protecting the user from over-trusting the explanation

---

## Prerequisites

### Claude Code

- Claude Code installed and working
- Familiarity with the `Agent` tool — dispatches use `Agent({ subagent_type: "<plugin>:<persona>-<suffix>", prompt: "..." })`

### Plugins required

| Plugin | What it contributes | Personas you'll dispatch |
|---|---|---|
| `great-minds` | Discovery (founder lens), debate, planning, QA, review | Sara Blakely OR Marty Cagan, Steve Jobs, Phil Jackson, Margaret Hamilton |
| `great-engineers` | The regex parser + prose generator JS | John Carmack |
| `great-designers` | UX / layout spec | Don Norman |
| `great-authors` | Every word on the page | Hemingway |

If any aren't installed:

```
/plugin marketplace add sethshoultes/great-minds-constellation
/plugin install great-minds@great-minds-constellation
/plugin install great-engineers@great-minds-constellation
/plugin install great-designers@great-minds-constellation
/plugin install great-authors@great-minds-constellation
```

### Per-project enablement

Create `.claude/settings.json` in your project root:

```json
{
  "enabledPlugins": {
    "great-minds@great-minds-constellation": true,
    "great-engineers@great-minds-constellation": true,
    "great-designers@great-minds-constellation": true,
    "great-authors@great-minds-constellation": true
  }
}
```

**Restart Claude Code in this directory** so the project's plugin set takes effect. Verify by checking that subagent_types like `great-engineers:john-carmack-engineer` resolve.

### Substitution table — when a plugin isn't loaded

If `great-designers` and/or `great-engineers` aren't loaded in your session:

| Missing | Substitute with | What you lose |
|---|---|---|
| Cagan (great-designers) on discovery | Sara Blakely (great-minds) | Cagan's structured four-risks framework; gain founder-empathy lens |
| Carmack (great-engineers) on build | Elon Musk (great-minds) | Carmack's specific systems craft; gain first-principles instead |
| Norman (great-designers) on UX | Jony Ive (great-minds) | Norman's usability-engineering academic register; gain Apple-aesthetic discipline |

The recipe still works with substitutes. The first run shipped this way — see [runs/2026-04-28.md](runs/2026-04-28.md). Fewer substitutes = closer to the canonical recipe.

---

## The pattern

```
PRD (you write)
  ↓
Discovery — Cagan or Sara
  ↓ [Decision point: structure-vs-intent tension]
Debate — Steve Jobs (scope: minimal vs. full playground)
  ↓
Plan — Phil Jackson (parallel build dispatch list)
  ↓
Build (PARALLEL):
  ├─ Engine — Carmack (regex-engine.js)
  ├─ UX spec — Norman (written design spec, not code)
  └─ Copy — Hemingway (every word on the page)
  ↓
Assembly — you (stitch the three outputs into index.html)
  ↓
QA — Margaret Hamilton (edge cases, ship verdict)
  ↓
Review — Steve Jobs (final ship/no-ship)
  ↓
Ship — open file://, verify smell test
```

The operator (you) is doing real work in **PRD**, **Decision point**, **Assembly**, **Ship verification**. Everything else is dispatched.

---

## Step 1 — Write the brief

What this step produces: a customer-style PRD at `PRD.md` in your project root.

Create `PRD.md`. Use this template — adapt to your actual or fictional customer:

```markdown
# PRD — Regex Explainer

**From:** [customer name, role, company]
**To:** Great Minds
**Date:** YYYY-MM-DD

## What I want

A tool that takes a regex and explains it in plain English. I paste
`^([a-z]+)@([a-z]+\.[a-z]{2,})$` and I get back something a human can
read — what each part does, how the parts connect, what would and
wouldn't match.

I also want a small "test it" panel: paste a string, see if the regex
matches, see which capture group caught what.

One page. Local file or localhost. No accounts, no SaaS, no signup.

## Why I'm asking

[Specific scenario — e.g., team that inherits regex they didn't write,
PR review bottleneck, etc. The brief is more useful when the scenario is
specific.]

## Constraints

- Single static page (HTML/CSS/JS)
- JS regex flavor only for v0
- Readable, modifiable code (no 200KB webpack bundle)
- Done in a few hours, not a sprint
- Differentiated from regex101: simpler, forgiving, explanation-first

## What I'm NOT sure about

The agency should push back on these:
- Flavor scope (JS-only vs. Python/PCRE in v0)
- How to handle very long regex (collapse, paginate, refuse?)
- Naming
- Whether test panel belongs in v0 or v1
```

**Operator notes:**
- The "What I'm NOT sure about" section is load-bearing. It's the explicit invitation for the constellation to disagree with the customer where it counts.
- Specific customers produce specific output. *"Sam Lopez, senior dev at a 5-person SaaS"* gets you better discovery than *"a developer who needs a tool."*

---

## Step 2 — Discovery

What this step produces: `discovery.md` with the four risks (value, usability, feasibility, viability) surfaced before any code is written.

**Dispatch:**

```js
Agent({
  subagent_type: "great-designers:marty-cagan-designer",  // or great-minds:sara-blakely-growth if great-designers not loaded
  prompt: `[paste the discovery brief below]`
})
```

**Discovery brief template:**

```
You're being dispatched for discovery on a regex-explainer tool. The
customer's PRD is below. Surface the four risks (value, usability,
feasibility, viability) before the agency commits to a build plan.

## The PRD
[paste your PRD here]

## What you deliver

A discovery doc with these sections:

### The customer in one breath
Who they are, what they actually do at 4pm on a Tuesday, what they'd
actually replace with this tool.

### Would [customer] pay for this and stick around?

#### Value — would they pay?
The honest take, not the optimistic one. Where they pick the tool up;
where they bounce back to alternatives.

#### Usability — will their team adopt it?
Smallest UI that delivers. The failure mode where a junior gets a wrong
explanation and trusts it.

#### Feasibility — can we build this correctly?
Where rule-based parsing breaks. Whether "explanation correctness" is
testable. The sharpest engineering risk.

#### Viability — what's the business shape?
Maintenance liability if this gets indexed. Whose responsibility for v1.

### Three pushback questions for the customer
Specific pushbacks with stakes — not "have you considered."

### Recommended cuts and additions
What's IN v0, what's CUT to v1, what's ADDED that the customer didn't ask
for but the constellation should insist on.

### My recommendation in one sentence
The single thing the agency must get right or this whole project is a
waste.
```

**Expected output:** a discovery doc that surfaces the **structure-vs-intent tension** (the customer wants "reads like a human wrote it" but constraints to "no backend" — those fight). Discovery should also recommend test panel + flavor warning + limitations callout into v0 (NOT v1 — these are trust mechanisms, not features).

**Save** the output to `discovery.md`.

---

## Step 3 — Operator decision point

This is where you (the human) make a customer-side call. Discovery surfaced the structure-vs-intent tension. Now the operator decides on the customer's behalf:

> **Build the rule-based, no-backend version.** Accept that the tool will be sharper than regex101 (better register, progressive disclosure) but won't reach "intent in human prose" quality. That's the only build buildable in a few hours with no backend.

**Adopt the discovery additions:**
- Test panel ships in v0 (trust mechanism)
- Flavor warning ships in v0 (trust mechanism)
- Limitations callout ships in v0 (protects junior devs)

**Append your decision** to `discovery.md` under `## OPERATOR DECISION`. The build phase will execute against this.

---

## Step 4 — Debate

What this step produces: `debate.md` resolving the v0 scope question.

**The tension to debate** (given the architecture is settled): *minimal annotator* (paste → prose + test panel + flavor warning + limitations callout, ship in 2 hours) vs. *full playground* (annotator + inline highlighting + live updates + pattern library + simplification suggestions + quirks panel, ship in 6-8 hours).

**Dispatch:**

```js
Agent({
  subagent_type: "great-minds:steve-jobs-visionary",
  prompt: `[paste the debate brief below]`
})
```

**Debate brief template:**

```
You're being dispatched as Steve Jobs to debate the v0 scope of a
regex-explainer tool. The architectural decision (rule-based, no backend)
is settled — your debate is: minimal annotator vs. full playground.

[Include the 5-feature minimal scope and the 5-feature playground scope
list — see runs/2026-04-28.md for the canonical version.]

## What you deliver
- "The case for minimal" (full argument)
- "The case for full" (full argument)
- "My verdict" (pick a side, defend in 2-3 paragraphs)
- "Scope decision" (clean IN/NOT-IN-v0 bullet list the build phase executes against)
```

**Save** the output to `debate.md`.

---

## Step 5 — Plan

What this step produces: `plan.md` with three self-contained build briefs Phil produces for the parallel build phase.

**Dispatch:**

```js
Agent({
  subagent_type: "great-minds:phil-jackson-orchestrator",
  prompt: `[paste the planning brief below]`
})
```

**Planning brief template:**

```
You're Phil Jackson, planning the parallel build phase of a regex-explainer
project. The scope is settled (minimal annotator). Three personas will run
in parallel. Produce a self-contained dispatch brief for each.

[Include the IN-v0 / NOT-IN-v0 lists from debate.md.]

## Build team
1. Engineer: great-engineers:john-carmack-engineer (or great-minds:elon-musk-persona)
2. UX/Design: great-designers:don-norman-designer (or great-minds:jony-ive-designer)
3. Copy: great-authors:hemingway-persona

## What you deliver
- Dependency graph (parallel-safe? where's the seam to watch?)
- Brief for engineer (the regex engine spec — function signatures, edge cases, output format)
- Brief for design (a written design spec, not code — page regions, type, color, states)
- Brief for copy (every copy slot on the page — hero, labels, errors, callouts)
- Assembly notes for the operator
- "What I'm betting on" (the highest-stakes assumption in the plan)
```

**Save** the output to `plan.md`.

---

## Step 6 — Build (parallel)

What this step produces: three artifacts saved to disk by each persona — the JS engine, the design spec, and the copy.

**Dispatch all three in parallel** (single message with three Agent tool calls):

```js
// Dispatch 1
Agent({
  subagent_type: "great-engineers:john-carmack-engineer",
  prompt: `[paste Phil's engineering brief verbatim from plan.md]`
})

// Dispatch 2 (same message, parallel)
Agent({
  subagent_type: "great-designers:don-norman-designer",
  prompt: `[paste Phil's UX brief verbatim from plan.md]`
})

// Dispatch 3 (same message, parallel)
Agent({
  subagent_type: "great-authors:hemingway-persona",
  prompt: `[paste Phil's copy brief verbatim from plan.md]`
})
```

**Expected outputs:**
- Carmack: a complete `regex-engine.js` (~900-1000 lines) with the four functions Phil's brief specified. Carmack will likely save the file directly to `regex-engine.js`.
- Norman: a written design spec (markdown) with every spacing, color, and typography decision named. Save the spec to `design-spec.md`.
- Hemingway: every copy slot filled (page title through limitations callout) in his characteristic register. Save to `copy.md`.

**The seam to watch** (Phil flagged this): Carmack's prose paragraph length vs. Norman's explanation region size. If Carmack returns 15 lines for a moderately complex regex and Norman designed for 4 lines, the page breaks visually. Check the output shapes match.

---

## Step 7 — Assembly

What this step produces: `index.html` integrating all three build outputs.

This is operator work. Per Phil's assembly notes:

1. **Read Carmack's `regex-engine.js`** and verify it exposes the four functions (`explainRegex`, `testRegex`, `validatePattern`, `flavorWarning`) on `window.RegexExplainer`. Verify `explainRegex` returns a prose paragraph (not a list, not an object).
2. **Read Norman's design spec** in full before writing HTML.
3. **Build the HTML skeleton** matching every region Norman specified. Leave copy slots as comments (`<!-- COPY: explanation_empty_state -->`).
4. **Drop Hemingway's copy** into the slots one-for-one.
5. **Wire the JS** — explain button → `explainRegex`, test button → `testRegex`, input change → `validatePattern`, flavor change → `flavorWarning`.
6. **Smell-test before QA:**
   - Paste `^([a-z]+)\d{2,4}$`, select Python flavor, submit, paste `hello42` as test string
   - Explanation reads naturally; test returns match + 1 capture group with value `hello`
   - **Note:** the flavor warning DOES fire in this configuration (Python's `\d` is Unicode-aware; JS's is ASCII). The original recipe predicted no warning; that prediction was wrong. The warning firing is correct behavior — verify the *prose* and the *match*, not the warning state.
   - If the explanation reads cleanly and the match shape is right → ready for Margaret's QA

---

## Step 8 — QA

What this step produces: a P0/P1/P2 list from Margaret with a ship verdict, then a fixed `index.html` if any P0s were caught.

**Dispatch:**

```js
Agent({
  subagent_type: "great-minds:margaret-hamilton-qa",
  prompt: `[paste the QA brief — see template]`
})
```

**QA brief template:**

```
You're Margaret Hamilton. The regex-explainer build at
[absolute path to index.html] is assembled and ready for QA.

## Read these before testing
- discovery.md — the load-bearing concerns from Sara Blakely's discovery
- debate.md — the scope Steve settled on
- index.html and regex-engine.js

## Your QA gate
Discovery's load-bearing concern was: "wrong explanations confidently
delivered are worse than no explanation." Test through that lens. The
trust layer is the whole product.

Specifically test:
- Anchors (^, $, \b)
- Character classes (literal, ranges, [^...], \d, \w, \s)
- Quantifiers (*, +, ?, {n}, {n,m}, greedy vs. lazy)
- Capturing vs. non-capturing groups (numbered AND named — verify named-group labels survive duplicate captured values, e.g. `(?<a>[a-z]+)-(?<b>[a-z]+)` against `foo-foo`)
- Alternation (|)
- Quantified zero-width assertions (e.g. `(?=foo)+`) — the engine must not claim repetition; lookarounds are zero-width
- Flags (g, i, m, s, u, y)
- Edge cases: empty pattern, invalid pattern, very long pattern
- The flavor warning logic (lookbehinds + Python flavor)
- The test panel for non-matching inputs and zero-capture-group regexes
- Mobile widths

## What you deliver
- A P0/P1/P2 list (P0 = ship-blocking, P1 = should fix in v0, P2 = v1)
- A ship verdict (SHIP / FIX-AND-SHIP / DO-NOT-SHIP)
- For each P0, the specific fix instruction
```

**Save** Margaret's report to `qa-report.md`. **Fix all P0s** before moving on. Re-test the smell test after fixes.

---

## Step 9 — Review

What this step produces: a final creative sign-off from Steve.

**Dispatch:**

```js
Agent({
  subagent_type: "great-minds:steve-jobs-visionary",
  prompt: `[paste the review brief]`
})
```

**Review brief:** "The regex-explainer build is at [absolute path]. Margaret cleared the P0s. Final review: ship or send back? Anything that fails the 'is this insanely great?' test?"

**Save** to `review.md`. If Steve says ship, ship.

---

## Step 10 — Ship verification

```bash
# Open in your default browser
open "/path/to/your/index.html"
```

Run the smell test from Step 7 — if it works, the recipe is done.

Optionally take screenshots — the canonical run captured `final-ship-state.png` and `smell-test-result.png` (see [runs/2026-04-28/screenshots/](runs/2026-04-28/screenshots/)).

---

## Variations

| Variation | Swap this | For this | Trade-off |
|---|---|---|---|
| Customer is a non-developer (e.g., compliance officer learning regex from policy docs) | Cagan | Maya Angelou (great-minds) | Lose Cagan's structured framework; gain warmth + dignity in user-facing copy. Build phase unchanged. |
| Want regex to be syntax-highlighted in the input field | (add a step) | Tinker Hatfield (great-designers) | Adds 1-2 hours; tests great-designers in interaction-design mode. |
| Want a CLI version too | (add a parallel build) | Linus Torvalds (great-engineers) | Bigger scope; Linus would write the Node CLI alongside Carmack's browser engine. |

---

## Common pitfalls

- **Skipping the operator decision point (Step 3).** Discovery surfaces a real tension; if you don't resolve it explicitly, the build phase will silently pick a side and you'll discover the wrong choice in QA. **Fix:** always append the operator decision to `discovery.md` before dispatching debate.
- **Sending Phil's plan to the build personas as references instead of verbatim text.** Sub-agents can't "see" your conversation. They need the literal brief in the prompt. **Fix:** copy-paste from `plan.md` into each Agent dispatch. If `plan.md` itself says "see the conversation above" instead of including the brief text, that's a bug in Phil's output — re-prompt for the literal text before dispatching.
- **Doing assembly before reading Carmack's output shape.** If Carmack's prose paragraph is 15 lines and Norman's design assumes 4, the page breaks. **Fix:** Phil's assembly notes are in priority order — read Carmack's output FIRST, reconcile shape mismatches, then touch HTML.
- **Dispatching Margaret with source-only access.** Margaret should be able to actually run the tool to find runtime bugs, not just read code. **Fix:** include the absolute path to `index.html` in the QA brief; have Margaret run smoke tests via her dispatched session if she has a Bash tool.
- **Not capturing screenshots.** A working build is the proof point of the recipe. Screenshots take 30 seconds and make the run inspectable for anyone.
- **Reflexively deferring persona disagreements to "the spec".** Hemingway's copy and Norman's UX spec disagreed on the multi-line toggle (single label vs. stateful idle/active labels). The right call was operator judgment, not blind deference. **Fix:** when two personas disagree at assembly time and there's no Phil-style mediator, name the trade-off in the run notes and pick deliberately. Don't pick by default-to-spec.
- **Suppressing security-hook warnings instead of rewriting.** When the security hook warns about `innerHTML` or pattern-matched words like `exec`, treat it as a prompt to use unambiguously safe DOM methods (`createElement`/`textContent`) — not as a false positive to silence. The hook can't see your sanitization; the rewrite documents safety in the code itself. **Fix:** rewrite, don't annotate.
- **Treating Phil's smell-test predictions as load-bearing.** Phil sometimes predicts subsidiary behaviors (e.g., "no flavor warning fires") that turn out to be wrong on his own terms. The smell test exists to verify the *core* outcome (explanation reads naturally, match shape is correct). Subsidiary behaviors are evidence to interpret, not assertions to confirm. **Fix:** verify the procedure works; don't fail the test because a side-state didn't match Phil's prediction.

---

## Run history

| Date | Operator | Variations | Result |
|---|---|---|---|
| [2026-04-28](runs/2026-04-28.md) | Seth Shoultes | Sara substituted for Cagan in session 1; Carmack real in session 2; Jony substituted for Norman | ✅ Shipped — `index.html` + `regex-engine.js` (~970 lines), 2 P0s caught and fixed in QA |

---

## When this recipe is the wrong choice

- **The deliverable isn't a single static page.** If you need a backend, a database, or runtime AI calls, this isn't the recipe. Consider [Decision Memo](../decision-memo/) (when nothing concrete needs to ship) or wait for a future server-side recipe.
- **The customer isn't a developer or developer-adjacent.** The flavor selector and limitations callout are developer-register language. For non-technical end users, swap copy persona to Maya Angelou.
- **You need real "intent" prose, not "structure" prose.** That requires an LLM call, which requires a backend. If "no backend" is non-negotiable, accept the structure-prose ceiling. If "human-quality intent prose" is non-negotiable, this isn't the recipe — you'll need to add a backend.
