# Recipe: [project name]

> **One-line summary:** what was built and why anyone would want it.

| Field | Value |
|---|---|
| Status | Draft / Tested / Shipped |
| Date | YYYY-MM-DD |
| Operator | [name] |
| Project repo | (link if public) |
| Plugins exercised | great-X, great-Y, great-Z |
| Substitutions | (e.g., "Sara Blakely substituted for Cagan when great-designers wasn't installed") |
| Time to ship | ~X hours |

---

## Why this recipe matters

What pattern does this recipe demonstrate? What would someone NOT learn by skipping it? Be specific to *this* project — generic claims about the constellation belong in the constellation README, not in a recipe.

---

## The brief

Drop in the customer-style PRD here. If you wrote it as the operator role-playing the customer, say so. If a real customer wrote it, link to it.

```
[paste the PRD]
```

**What's load-bearing:** which constraints in the brief actually drove later decisions? Which were soft preferences the constellation pushed back on?

---

## Phase 1 — Discovery

**Persona dispatched:** `great-X:Y-persona`

**Brief sent (verbatim):**

```
[the actual prompt sent to the persona]
```

**Output (verbatim or summarized — note which):**

```
[what came back]
```

**What discovery surfaced:** the load-bearing risks the constellation flagged. Did the operator agree? Where did the operator push back? Did the discovery output change scope?

---

## Phase 2 — Debate

**Persona dispatched:** `great-minds:steve-jobs-visionary` (or whoever)

**The tension being debated:** state it in one sentence.

**Brief, output, verdict** — same shape as Phase 1.

**The scope decision** the build phase will execute against (bullet list).

---

## Phase 3 — Plan

**Persona dispatched:** `great-minds:phil-jackson-orchestrator`

The dispatch graph Phil produced — who builds what, in parallel or serial. Include Phil's "what I'm betting on" call: the highest-stakes assumption in the plan.

---

## Phase 4 — Build

For each parallel build dispatch:

### Dispatch 1: [persona]

**Brief, output, time to return.** What did the operator have to follow up on? Was the output ready to integrate, or did seams need reconciling?

### Dispatch 2: [persona]
(same shape)

### Dispatch 3: [persona]
(same shape)

**Integration notes:** how did the operator stitch the parallel outputs together? What broke at the seams? What had to be rewritten by hand?

---

## Phase 5 — QA

**Persona dispatched:** `great-minds:margaret-hamilton-qa`

The P0/P1/P2 list Margaret returned. What was fixed before ship; what was deferred to v1.

---

## Phase 6 — Review

**Persona dispatched:** `great-minds:steve-jobs-visionary`

Steve's ship/no-ship verdict. Anything sent back for rework.

---

## Ship

Where the artifact lives (URL, file path). What runtime / hosting. How a reader can verify it works.

---

## Retro — what worked, what broke

The honest pass. Each item should be specific enough that the next operator avoids the same mistake or repeats the same win.

### What worked
- (specific patterns that delivered)

### What broke
- (specific failure modes)

### What I'd do differently
- (one or two changes to the dispatch pattern for next time)

### What I'd file as a constellation issue
- (anything that's a pipeline gap, not a one-off)

---

## Reusable patterns

Distill 1-3 patterns from this recipe that generalize. These are the takeaways for someone running a different project tomorrow.

---

## Source materials

Links to the project's PRD, the per-phase artifacts, the actual git commits. The recipe should be falsifiable — a reader should be able to inspect the actual evidence, not just trust the narrative.
