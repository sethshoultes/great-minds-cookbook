# Recipe: Multi-Agent Essay Production

> **One-line summary:** Ship a long-form blog essay with an original featured image in a single Claude Code session, by dispatching an author persona and a designer persona as parallel sub-agents in fresh context. The orchestrator briefs and integrates; it does not write or design.

| Field | Value |
|---|---|
| Project type | Long-form blog essay (1,000–1,800 words) with one original featured image |
| Plugins exercised | great-authors, great-minds (Jony Ive specifically) |
| Time to ship | ~15–25 min wall clock (5–10 min of operator briefing + parallel agent runtime + image render + integration + commit) |
| Risk level | LOW (worst case: a draft that needs revision; the cost of failure is one re-dispatch) |
| First shipped | 2026-04-29 ([first run notes](runs/2026-05-07-skills-as-sops.md)) |

---

## What you'll have at the end

- A complete blog post at `_posts/YYYY-MM-DD-<slug>.html` with proper Jekyll-style front matter (title, subtitle, date, description, og_*, read_time, related)
- An original 1536×1024 featured image at `blog/images/<slug>-featured.png` matching the existing visual register
- The image embedded at the top of the post body
- The post wired to 2–3 related posts in `related:` front matter for cross-navigation
- A clean git commit ready to push

---

## Prerequisites

### Claude Code

- Claude Code installed and working
- Familiarity with the `Agent` tool — dispatches use `Agent({ subagent_type: "<plugin>:<persona>-<suffix>", prompt: "..." })`
- An OpenAI API key in `~/.config/dev-secrets/secrets.env` as `OPENAI_API_KEY` for image rendering

### Plugins required

| Plugin | What it contributes | Personas you'll dispatch |
|---|---|---|
| `great-authors` | The post body in voice, in fresh context | Pick one of: Hemingway, McCarthy, Didion, Baldwin, Morrison, McPhee, Wallace, Orwell, King, Le Guin, Vonnegut |
| `great-minds` | The image brief — visual direction with continuity to the existing register | Jony Ive (`jony-ive-designer`) |

If any aren't installed:

```bash
/plugin marketplace add sethshoultes/great-minds-constellation
/plugin install great-authors@great-minds-constellation
/plugin install great-minds@great-minds-constellation
```

### Per-project enablement

In `.claude/settings.json` for the blog repo:

```json
{
  "enabledPlugins": {
    "great-authors@great-minds-constellation": true,
    "great-minds@great-minds-constellation": true
  }
}
```

### Substitution table — when a plugin isn't loaded

| Missing | Substitute with | What you lose |
|---|---|---|
| `great-authors` not loaded | The orchestrator drafts in chosen voice | Voice integrity — the *orchestrator-and-writer* learning warns this produces hollow imitation |
| Jony Ive not available | Pick another visual-judgment persona (Rick Rubin from great-minds, or skip the image-brief step and write the gpt-image-1 prompt directly) | Visual continuity with the existing register |

The recipe REQUIRES dispatching the author. If `great-authors` is unavailable, do not run this recipe — you'll save 5 minutes and ship a worse post.

---

## The seed

The recipe doesn't manufacture the argument. It manufactures the post around one. Before dispatching anything, the orchestrator needs a **claim** — not a topic.

- **Topic** (insufficient): "Write about the avatar build."
- **Claim** (the seed): "The next layer of the agentic economy is processes made installable. The factory floor solved this in 1908; we're solving it now with skills."

If you only have a topic, do not dispatch yet. Spend 5 minutes turning the topic into a claim. The author can find the post if there's an argument; if there isn't, the dispatch fails politely.

---

## Step 1 — Pick the voice

Match the material to a voice. Rough heuristics:

| Material | Voice |
|---|---|
| Architecture / structural argument | McPhee, Hemingway |
| Personal arc / observation / inversion | Didion |
| Recursive / meta / self-referential | Wallace |
| Plain-style polemic, anti-jargon | Orwell |
| Compression with humane heart | Vonnegut |
| Working-novelist day-in-the-life | King |
| Anthropological / speculative | Le Guin |
| Black-American oral lyric / generational | Morrison |
| Moral urgency / political | Baldwin |
| Mythic / biblical weight | McCarthy |

**Vary.** Check the last 3–4 author voices used in `_posts/` and pick something different. The blog's range comes from the variety; repeat voices flatten the corpus.

---

## Step 2 — Write the author brief

Spend the time. ~1,500 words of brief produces 1,300–1,800 words of post. Thin briefs produce thin work.

Structure:

```
You are <persona>. <Voice description in 2–3 sentences.>

THE POST:
Title: <working title>
<Optional subtitle direction>

THE MATERIAL:
<2–4 paragraphs explaining the argument, the facts, the seed phrase verbatim>

THE ARGUMENT THE POST MAKES (do not state as a thesis sentence):
<one paragraph>

READ FIRST (in this order):
1. <related post #1 with absolute path>
2. <related post #2 with absolute path>
3. <reference material — brain learning, runbook, existing artifact>
4. <2–4 more for voice continuity>

WHAT TO DO:
- Output target: /absolute/path/to/_posts/YYYY-MM-DD-<slug>.html
- Length target: <a 300-word window>
- Front matter requirements: title, subtitle, date, description, og_*, og_image (use a placeholder filename for now), read_time, related (list slugs)
- Embed the (forthcoming) featured image at the top of the post body using the existing pattern.

STRUCTURAL ANCHORS (your discretion to reorder; these are the beats):
- Open with <a specific opening direction — concrete, not abstract>
- <3–6 beats, each one sentence>
- Close on <a closing direction>

CRAFT REQUIREMENTS:
- Section breaks via <hr> and <h2>.
- <Specific numbers — e.g., 17 URL documents, 36 hours, ten plugins>
- <Required hyperlinks with anchor text>
- post-bio: <length and tone>

WHAT NOT TO DO:
- <Forbid corporate plural unless you mean a literal team>
- <Forbid exclamation marks>
- <Forbid "I'm excited to announce">
- <Forbid voice-specific anti-patterns — e.g., "do not write in the orchestrator's first-person present-tense">
- <Forbid retreading other posts' arguments>

REPORT BACK:
- Word count
- The single sentence you would defend most strongly if asked to cut it
- One observation about <topic> you noticed during writing that the briefer did not name
```

---

## Step 3 — Write the Ive brief

In parallel with the author brief.

```
One featured image needed for an upcoming blog post on sethshoultes.com.

POST: <title> by <persona>. The argument is <one paragraph>.

The visual should carry <the load-bearing concept>. Possible directions:
- <metaphor 1 — concrete, one sentence>
- <metaphor 2>
- <metaphor 3>
- <metaphor 4>

Pick the strongest — your call.

EXISTING VISUAL REGISTER (must match):
Pen-and-ink, New Yorker editorial. Crosshatch shading. Off-white paper. Black ink. No color (or at most a single muted accent). Subject in the center; ample negative space. The image is a metaphor; no text labels in the image. Wide 16:9 (1536x1024 for gpt-image-1).

REFERENCE IMAGES (read these with the Read tool):
- <path to existing featured image #1>
- <path to existing featured image #2>
- <2–4 more for register continuity>

WHAT I NEED:
1. Read the reference images first.
2. Pick one metaphor. Justify it in one sentence.
3. Write the gpt-image-1 prompt — 2–4 sentences, specific about composition, register, and load-bearing visual.
4. Name the load-bearing visual — the single image element that carries the post's idea.

OUTPUT FORMAT:
Save to <path>/_image-brief-<slug>.txt:

CHOSEN METAPHOR: [1 sentence]

PROMPT (filename: <slug>-featured.png):
[2-4 sentences]
Load-bearing visual: [one sentence]

Do not generate the image yourself.
```

---

## Step 4 — Dispatch in parallel

Both briefs go out in the same orchestrator turn. `run_in_background: true` so they fire-and-forget.

```
Agent({
  subagent_type: "great-authors:vonnegut-persona",
  prompt: "<the full author brief>",
  run_in_background: true
})

Agent({
  subagent_type: "great-minds:jony-ive-designer",
  prompt: "<the full image brief>",
  run_in_background: true
})
```

The author typically returns in 90–180 seconds; Ive in 30–60 seconds. The orchestrator can do other work in between (or just wait).

---

## Step 5 — Render the image

When Ive returns, write a tiny Python script that POSTs to OpenAI's `/v1/images/generations` with `model: "gpt-image-1"`, `size: "1536x1024"`, `quality: "high"`, the prompt verbatim from Ive's brief, and saves the base64-decoded PNG to `blog/images/<slug>-featured.png`. ~30–60 seconds.

Reference renderer is at `recipes/multi-agent-essay-production/runs/2026-05-07-skills-as-sops.md` (see the run notes). Idempotent script template — drop in, change the prompt, run.

---

## Step 6 — Integrate

The author's output is on disk with a placeholder image filename in the front matter. Verify:

1. The slug in the filename matches the slug in the related-posts of OTHER posts pointing at this one (if any).
2. The image embed at the top of the post body uses the right `<img>` style: `width:100%;max-width:780px;display:block;margin:0 auto 2rem;border-radius:6px`.
3. The `related:` front matter has 2–3 entries, each `{ slug, note }`.
4. `bundle exec jekyll build` succeeds; the post lands at `_site/blog/<slug>.html`.

---

## Step 7 — Commit

```bash
git add -A
git commit -m "Publish '<title>' (<persona>)
<one-paragraph commit body summarizing the post + the agent dispatches>
"
git push
```

If the blog repo has a GitHub Action that syncs new posts to a RAG knowledge base (per the `add-rag-to-elevenlabs-agent` skill), the post auto-attaches to the avatar's corpus on `page_build`. No manual step.

---

## Pitfalls

### The seed is a topic, not a claim

If the brief doesn't carry an argument, the author has to invent one — and that's where dispatches go wrong. State the claim explicitly in THE MATERIAL section. The user's exact words are usually the claim.

### Sequenced dispatch instead of parallel

Don't wait for the author to return before dispatching Ive. They're independent. Parallelize.

### Voice repetition

Three Didions in a row will flatten the corpus. Track the last 3–4 voices used; pick something else.

### `expects_response: true` on the LiveAvatar SDK + ElevenLabs Plugin path

(Unrelated to this recipe but a foot-gun in the broader stack — see `register-elevenlabs-client-tool` skill.)

### Skipping WHAT NOT TO DO

The negative space defines the voice as much as the positive guidance. Forbidding "I'm excited to announce" matters; forbidding exclamation marks matters; forbidding corporate plural matters. Each one matters.

### The orchestrator drafts "to save a dispatch"

The voice flattens. Per `[orchestrator-and-writer-are-different-ai-roles]` in the brain learnings — every time. Always dispatch.

---

## Variations

- **Two parallel authors** — when the right voice is genuinely uncertain, dispatch two authors with the same brief and pick the better draft. Costs 2× agent runtime; produces real signal.
- **Cross-model orchestrator** — the recipe's dispatch contract is portable. The same brief structure works whether the orchestrator session is on Claude, Kimi K2.6, or another model. See `[cross-model-persona-portability]`.
- **Skip the image** — for speed, reuse an existing featured image (e.g., a thematic predecessor) instead of dispatching Ive. Saves 5 minutes; loses visual lineage.
- **Series posts** — when shipping a multi-part series, dispatch all parts in parallel with explicit "stay in your lane; Part X covers ABC" notes in each brief. See the Agentic Economy series for the pattern.

---

## Companion artifacts

- **Skill (Agent Skill format):** [`set-up-claude-code-with-brain-vault`](https://github.com/sethshoultes/building-with-ai-skills/blob/main/skills/set-up-claude-code-with-brain-vault/SKILL.md) — sister skill (the brain vault is where the source learnings for this recipe live).
- **Brain learning:** [`multi-agent-essay-production-recipe.md`](https://github.com/sethshoultes/brain/blob/main/learnings/multi-agent-essay-production-recipe.md) — the source pattern.
- **Reference posts (the recipe's own outputs):**
  - [Skills as SOPs](https://sethshoultes.com/blog/skills-as-sops.html) (Orwell)
  - [The Recipe That Wrote Itself](https://sethshoultes.com/blog/the-recipe-that-wrote-itself.html) (Vonnegut — the recipe blogging itself)
  - [Stars Aligned](https://sethshoultes.com/blog/stars-aligned.html) (Le Guin)
  - [Three Sessions Running](https://sethshoultes.com/blog/agentic-economy-three-sessions-running.html) (McPhee)
  - [The Bible Reads First](https://sethshoultes.com/blog/the-bible-reads-first.html) (Didion)

---

## Run history

| Date | Post | Author | Plugins | Notes |
|---|---|---|---|---|
| [2026-05-07](runs/2026-05-07-skills-as-sops.md) | Skills as SOPs | Orwell | great-authors, great-minds | First documented run; canonical reference |

Future runs append here.
