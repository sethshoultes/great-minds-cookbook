# Run: Skills as SOPs (Orwell)

| Field | Value |
|---|---|
| Date | 2026-04-29 (post date 2026-05-07) |
| Recipe | [multi-agent-essay-production](../README.md) |
| Author dispatched | Orwell (`great-authors:orwell-persona`) |
| Image briefer | Jony Ive (`great-minds:jony-ive-designer`) |
| Renderer | gpt-image-1 (1536×1024) |
| Wall clock | ~25 minutes (5 min orchestrator briefing, 95s author runtime, 35s Ive runtime, 60s image render, ~3 min integration + commit) |
| Outcome | SHIPPED. Post live at https://sethshoultes.com/blog/skills-as-sops.html |
| Token spend | ~120K input, ~25K output across both sub-agents combined |

---

## The seed

User message in the orchestrator session:

> "save our processes as skills and create standard operating procedures as Ai skills, plugins, and specialized agents"

That sentence carried the claim: **the next layer of the agentic economy is processes made installable.** Everything that followed in the brief carried that claim forward verbatim into Orwell's READ-FIRST list, where he picked it up as the post's thesis.

This is the lesson the recipe doesn't always make obvious: the user's exact phrasing tends to BE the post. The orchestrator's job is to recognize the claim and put it in front of the author intact, not paraphrase it.

---

## What the orchestrator did

1. Recognized the seed as a publishable claim, not just a status update.
2. Wrote the author brief — ~1,500 words, structured per the recipe template:
   - Persona statement (Orwell's six rules, plain style)
   - The post material (the SOP analogy, the agent-substrate, the kitchen card)
   - The argument (do not state as thesis sentence — let it surface)
   - READ FIRST list with absolute paths to 5 reference posts
   - Output target, length window, front matter requirements
   - Structural anchors (8 beats, each 1–2 sentences)
   - WHAT NOT TO DO (corporate plural, exclamation marks, "I'm excited to announce", padding, summary closings)
   - REPORT BACK format (word count, defended sentence, observation the briefer didn't name)
3. Wrote the Ive brief in parallel — 4 candidate metaphors (cork board with two cards, factory line, clipboard with silhouette, pinned card next to laptop), with reference images and instructions to "pick the strongest — your call."
4. Dispatched both with `run_in_background: true`.

Total briefing time: ~7 minutes of typing.

---

## What Orwell delivered

1,350-word post body, structured in 6 sections via `<hr>` and `<h2>`. Front matter complete. Image embed at top. Related posts wired to two prior pieces.

The opening was the kitchen card (literal, working-class, sensory) — exactly the SOP analogy the brief asked for, executed in the voice the persona file specifies.

The closing, unprompted, made the analogy load-bearing for an honest caveat: **a wrong skill executes the wrong thing in every session that calls it, without complaint, at full speed.** That sentence was not in the brief. It came from the REPORT BACK prompt asking the author for "one observation about the topic you noticed during writing that the briefer did not name." Orwell, in fresh context, extended the SOP analogy to its sharpest edge — the same property that makes SOPs valuable also makes wrong SOPs dangerous. The brief had asked for an honest caveat; Orwell discovered what the caveat actually was.

This is the line of the post. Everything else in the post is structure; this sentence is the argument.

---

## What Ive delivered

Picked the cork-board metaphor over the other three. Justified the choice in one sentence: *"The two-cards direction wins because it is the most legible at thumbnail scale — the single cork board is an immediately readable field, and the contrast between aged and fresh reads in under one second."*

Three specific load-bearing details in his prompt:

1. **"Only the format is legible"** — the cards carry no readable text, only the silhouette of a numbered list versus markdown frontmatter dashes. Enough to carry the 1908/2026 argument without spelling it out.
2. **"The thumbtack above it leaving a rust-colored ghost ring"** — that single detail does more aging work than any amount of yellowing.
3. **"No human figures"** — consistent with the empty-chair register of the Agentic Economy series. The work proceeds. Nobody is there.

gpt-image-1 rendered the prompt accurately on the first attempt. No re-render needed.

---

## What the orchestrator did with the outputs

1. Reviewed both deliverables. No revisions requested.
2. Wired the image embed (Orwell had already added the `<img>` tag with the placeholder filename; just needed the actual file in place).
3. Built the site (`bundle exec jekyll build`), verified `_site/blog/skills-as-sops.html` rendered.
4. Committed as part of the larger "Open the educational layer" commit (commit `a2f21dc`).
5. Pushed. The GitHub Action picked up the new post and synced its URL to the avatar's RAG knowledge base on the `page_build` event.

Total integration time: ~3 minutes.

---

## What surprised the operator

Three things specifically:

1. **Orwell's caveat sentence.** The brief asked for "an honest caveat about correctness." Orwell delivered: *"a wrong skill executes the wrong thing in every session that calls it, without complaint, at full speed."* That's an extension of the analogy, not a paraphrase of the brief. The recipe's REPORT BACK prompt is what surfaced it — without the explicit ask for an unnamed observation, this sentence wouldn't exist in the post.

2. **Ive's "rust-colored ghost ring."** The brief listed four candidate metaphors. Ive picked one and added detail the briefer didn't think to specify. The ghost ring does more aging work than any amount of yellowing — it's a load-bearing visual element the orchestrator wouldn't have specified. This is the value of dispatching to a designer rather than writing the prompt yourself: the designer sees details the briefer misses.

3. **The integration was small.** The bulk of the work (briefing) is upstream of the dispatch. After the agents return, integration is ~3 minutes. The recipe's economic shape is "front-load the briefing; back-end is fast."

---

## Reader response (subsequent session)

The user's message after reading the published post was the highest-signal feedback this recipe has gotten:

> *"the blog post turned out really well and is one of the best so far this week. Who all was involved in the writing?"*

The "who all was involved" framing is the right reaction — the post reads as a single voice (Orwell's), but the credits include Orwell, Ive, gpt-image-1, the user (whose exact phrasing IS the thesis), the orchestrator (briefer + integrator), and HeyGen's `liveavatar-agent-skills` (the structural format reference).

Six contributors for ~1,350 words. The recipe scales because no single contributor has to do everything — and because the contract between layers is the dispatch protocol, not personal judgment about what to include.

---

## Token economics

- Author dispatch (Orwell): ~75K input (READ-FIRST files + brief), ~14K output (post)
- Image briefer (Ive): ~22K input (brief + reference image reads), ~3K output (gpt-image-1 prompt)
- Orchestrator (this session): ~25K typing the briefs, ~3K integration
- gpt-image-1: 1 standard 1536×1024 high-quality render

Total cost in actual API spend (Claude + OpenAI): under $1 for the post. The cookbook recipe pays back the operator's briefing time roughly the second time it runs — once you have the brief template, the next run is template-substitution rather than from-scratch authoring.

---

## What the recipe needs (improvements queued)

- **Voice rotation tracker.** The recipe says "vary voices" but the operator currently checks `_posts/` manually. A small `scripts/last-voice.py` that reads the last 3–4 posts and lists which voices are due would prevent repetition.
- **Brief template generator.** The current brief is hand-written every time. A `scripts/draft-brief.py <slug> <persona>` that fills in 70% of the structure (READ FIRST paths, target path, front matter format, REPORT BACK section) would shave ~3 minutes off the briefing step.
- **Slug-to-image-filename helper.** The image filename has to match `<slug>-featured.png`. Currently the orchestrator manually keeps these in sync. A small utility would prevent drift.

These are queued for the next run, not blockers.

---

## Cross-references

- Recipe README: [`../README.md`](../README.md)
- The post: [Skills as SOPs](https://sethshoultes.com/blog/skills-as-sops.html)
- Brain learning that captures the recipe: [`multi-agent-essay-production-recipe.md`](https://github.com/sethshoultes/building-with-ai-brain/blob/main/learnings/multi-agent-essay-production-recipe.md)
- Foundational learnings:
  - [`orchestrator-and-writer-are-different-ai-roles`](https://github.com/sethshoultes/building-with-ai-brain/blob/main/learnings/orchestrator-and-writer-are-different-ai-roles.md)
  - [`distinct-editor-personas-converge-on-real-craft-problems`](https://github.com/sethshoultes/building-with-ai-brain/blob/main/learnings/distinct-editor-personas-converge-on-real-craft-problems.md)
  - [`sub-agent-briefs-must-be-self-contained`](https://github.com/sethshoultes/building-with-ai-brain/blob/main/learnings/sub-agent-briefs-must-be-self-contained.md)
- Visual-direction reference: HeyGen's [`liveavatar-agent-skills`](https://github.com/heygen-com/liveavatar-agent-skills) — pattern source for the SKILL.md format the post is announcing.
