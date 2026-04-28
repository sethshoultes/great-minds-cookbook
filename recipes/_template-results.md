# Run: [project name] — YYYY-MM-DD

> **One-line summary:** what was built in this run, by whom, with what variations from the canonical recipe.

This is a **case study** — a single run of a recipe. The reusable playbook lives in the parent recipe directory's `README.md`. This file is the falsifiable evidence that the recipe ran end-to-end on a specific date with a specific operator.

| Field | Value |
|---|---|
| Recipe | [recipe name](../README.md) |
| Status | Shipped / Failed / Aborted |
| Date | YYYY-MM-DD |
| Operator | [name] |
| Project repo | (link if public; otherwise local path) |
| Plugins loaded in session | great-X, great-Y, great-Z |
| Substitutions | (e.g., "Sara Blakely substituted for Cagan when great-designers wasn't installed") |
| Time to ship | ~X hours |
| Final artifacts | (paths or links) |

---

## Why this run mattered

What did this specific run demonstrate that previous runs didn't (if it's not the first run)? Be specific to *this* run — the recipe-level reusable patterns belong in the parent README.md, not here.

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

## Patterns to fold back into the recipe

If this run surfaced patterns that should make the recipe better — pitfalls to add, variations to document, common mistakes to warn about — list them here. After this run is filed, update the parent `README.md` (the recipe playbook) to reflect the lessons. The recipe gets sharper run by run.

---

## Source materials

Links to the project's PRD, the per-phase artifacts, the actual git commits. Every run is falsifiable — a reader should be able to inspect the actual evidence, not just trust the narrative.

Suggested layout:
- `screenshots/` — visual proof of the ship
- `artifacts/` — copies or links to PRD.md, discovery.md, debate.md, plan.md, etc.
