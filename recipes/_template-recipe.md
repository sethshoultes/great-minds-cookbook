# Recipe: [name]

> **One-line summary:** what this recipe builds and why someone would run it.

| Field | Value |
|---|---|
| Project type | (e.g., single-page tool / long-form prose / decision memo) |
| Plugins exercised | great-X, great-Y, great-Z |
| Time to ship | ~X hours |
| Risk level | LOW / MEDIUM / HIGH |
| First shipped | YYYY-MM-DD ([link to first run](runs/YYYY-MM-DD.md)) |

---

## What you'll have at the end

A bulleted list of the concrete deliverables. Be specific. *"A working tool"* is not specific. *"A 4-6K word document at `<filename>`, including X / Y / Z"* is.

---

## Prerequisites

### Claude Code

- Claude Code installed and working
- Familiarity with the `Agent` tool and dispatch syntax `Agent({subagent_type: "<plugin>:<persona>-<suffix>", prompt: "..."})`

### Plugins

Required for this recipe:

- `great-minds@great-minds-constellation` — orchestration personas
- `great-X@great-minds-constellation` — what this plugin contributes
- (etc.)

If any of the above aren't installed:

```
/plugin marketplace add sethshoultes/great-minds-constellation
/plugin install great-X@great-minds-constellation
```

### Per-project enablement

Create `.claude/settings.json` in your project root:

```json
{
  "enabledPlugins": {
    "great-minds@great-minds-constellation": true,
    "great-X@great-minds-constellation": true
  }
}
```

Then **restart Claude Code in this directory** so the project's plugin set takes effect.

### Anything else

(Local tools, API keys via `~/.config/dev-secrets/secrets.env`, files that need to exist at the project root, etc.)

---

## The pattern

A high-level diagram of what happens, in order. Use ASCII or a numbered list — keep it readable.

```
PRD (you) → Discovery (Persona A) → Debate (Persona B) → Plan (Phil) → Build (parallel: C, D, E) → Assembly (you) → QA (Margaret) → Review (Persona F) → Ship
```

Note where parallel dispatches happen, where decision points live, where the operator (the human) is doing the work vs. dispatching.

---

## Step 1 — Write the brief

What this step produces: a customer-style PRD at `PRD.md` in the project root.

The brief format the recipe expects (template):

```markdown
# PRD — [project name]

**From:** [customer name, role, company]
**To:** Great Minds
**Date:** YYYY-MM-DD

## What I want
(1-2 paragraphs — what the customer is asking for, in their voice)

## Why I'm asking
(1-2 paragraphs — what's broken, what they've tried)

## Constraints
- (bullet)
- (bullet)

## What I'm NOT sure about
- (the agency should push back on these)
```

**Operator note:** if you're the customer, write as the customer. If you're role-playing a fictional customer, make them specific (named, with a real job title, with real opinions). Generic briefs produce generic constellation output.

---

## Step 2 — Discovery

Dispatch:

```js
Agent({
  subagent_type: "great-X:persona-Y",
  prompt: `<the discovery brief — see template below>`
})
```

**The discovery brief template:**

```
You're being dispatched as part of a real run of the constellation. A
customer ([name]) handed in a PRD for [project type]. Your job is
discovery — surface the risks before the agency commits to a build plan.

## The PRD
[paste PRD]

## What you deliver
A discovery doc with these sections... (specific to this recipe's domain)
```

**Expected output shape:** [what the recipe expects to come back — file path + structure]

**Decision point:** [where the operator has to make a customer-side decision based on discovery output]

---

## Step 3 — [next phase]

(Same shape — what happens, dispatch template, expected output, decision points.)

---

## Step N — Ship verification

How the operator confirms the build works. Be concrete: smell-test commands, browser steps, sample inputs/outputs.

---

## Variations

If your project shape differs from the canonical recipe in [way X], swap [persona A] for [persona B]. Why: [register difference / domain coverage].

| Variation | Swap this | For this | Trade-off |
|---|---|---|---|
| ... | ... | ... | ... |

---

## Common pitfalls

The mistakes operators make running this recipe, in priority order. Each item should be specific enough that a reader avoids the mistake on their first run.

- **[Pitfall name]** — what goes wrong, why, and the fix.
- ...

---

## Run history

Each run of this recipe is a case study under `runs/`. Read them in date order; the patterns get clearer.

| Date | Operator | Variations | Result |
|---|---|---|---|
| YYYY-MM-DD | name | (any swaps) | [link to run](runs/YYYY-MM-DD.md) |

---

## When this recipe is the wrong choice

Be honest. If the project shape doesn't match this recipe, name where the operator should look instead.
