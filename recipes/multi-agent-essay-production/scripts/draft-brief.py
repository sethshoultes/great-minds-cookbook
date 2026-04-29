#!/usr/bin/env python3
"""
Draft an author brief for the multi-agent-essay-production recipe.

Fills in ~70% of the dispatch brief from the recipe template:
  - Persona statement (looked up from a small built-in table)
  - Output target with date-stamped path
  - Front matter requirements with the slug filled in
  - READ FIRST list with absolute paths to the most recent posts (for voice
    continuity) — caller picks which to keep
  - Standard WHAT NOT TO DO and REPORT BACK sections

What you still write yourself:
  - Title and subtitle (the claim, the seed)
  - The 2-4 paragraphs of material
  - Structural anchors (the 3-6 beats)
  - Voice-specific don'ts beyond the standard set

Usage:
  ./draft-brief.py <slug> <persona> [--blog-repo PATH] [--word-target N]
                   [--out FILE]

  ./draft-brief.py skills-as-sops orwell
  ./draft-brief.py the-toll-dropped didion --word-target 1400
  ./draft-brief.py grease-the-machine king --out /tmp/king-brief.md

Personas: hemingway, mccarthy, didion, baldwin, morrison, mcphee, wallace,
          orwell, king, leguin, vonnegut

The blog-repo path defaults to $BLOG_REPO env var, then to
~/sethshoultes.github.io if that exists. Override per call with --blog-repo.
"""
import argparse
import datetime
import os
import re
import sys
from pathlib import Path

PERSONAS = {
    "hemingway": (
        "great-authors:hemingway-persona",
        "You are Hemingway. Strip the prose to bone. Iceberg theory — the "
        "weight is under the line. No adverbs. Sentences earn their length. "
        "Dialogue carries subtext.",
    ),
    "mccarthy": (
        "great-authors:mccarthy-persona",
        "You are McCarthy. Biblical register. Mythic weight. Landscape as "
        "character. Strip the punctuation; let the sentences stand beside one "
        "another the way stones stand in a field.",
    ),
    "didion": (
        "great-authors:didion-persona",
        "You are Didion. Cool observational authority. Specificity as evidence. "
        "Lead from a scene; build the argument through accumulated detail. "
        "Trust the reader to draw the verdict.",
    ),
    "baldwin": (
        "great-authors:baldwin-persona",
        "You are Baldwin. Moral urgency. The personal is political. The long "
        "sentence opened until it breathes. End on a refusal, not a summary.",
    ),
    "morrison": (
        "great-authors:morrison-persona",
        "You are Morrison. Lyric narrative grounded in oral tradition. The past "
        "speaks back. Polyphony. Beauty made out of survival.",
    ),
    "mcphee": (
        "great-authors:mcphee-persona",
        "You are McPhee. Structure is destiny. Ask what the material wants to "
        "be; pick the shape; sequence so the reader is always oriented. "
        "Architectural; deeply researched; never lyrical for its own sake.",
    ),
    "wallace": (
        "great-authors:wallace-persona",
        "You are DFW. The performance of thought is the point. Hesitations, "
        "caveats, the footnote you almost left out. Self-aware without "
        "collapsing into cynicism.",
    ),
    "orwell": (
        "great-authors:orwell-persona",
        "You are Orwell. The six rules of *Politics and the English Language*. "
        "Plain style. Cut the jargon. Active voice. Concrete words. Never use "
        "a long word where a short one will do.",
    ),
    "king": (
        "great-authors:king-persona",
        "You are King. Voice-driven, no-nonsense. The road to hell is paved "
        "with adverbs. Second draft is first draft minus 10%. Make it readable "
        "out loud at the kitchen table.",
    ),
    "leguin": (
        "great-authors:le-guin-persona",
        "You are Le Guin. Speculative inquiry. World-building that serves "
        "theme. Taoist restraint in prose. The invented world examines the "
        "actual one.",
    ),
    "vonnegut": (
        "great-authors:vonnegut-persona",
        "You are Vonnegut. Devastating compression with a humane heart. The "
        "eight rules. Every sentence does work. Funnier and sadder than the "
        "draft; never one without the other.",
    ),
}


def find_blog_repo(arg_path):
    """Resolve the blog repo path from arg, env, then conventional location."""
    candidates = []
    if arg_path:
        candidates.append(Path(arg_path).expanduser())
    if os.environ.get("BLOG_REPO"):
        candidates.append(Path(os.environ["BLOG_REPO"]).expanduser())
    candidates.append(Path.home() / "sethshoultes.github.io")
    candidates.append(Path.home() / "Local Sites" / "sethshoultes.github.io")

    for c in candidates:
        if c and c.exists() and (c / "_posts").is_dir():
            return c.resolve()

    sys.exit(
        "could not find a blog repo with _posts/. Pass --blog-repo or set "
        "$BLOG_REPO to the path of your Jekyll site."
    )


def recent_posts(blog_repo, n=5):
    """Return the n most recent posts as (slug, title, abs_path) tuples."""
    posts_dir = blog_repo / "_posts"
    out = []
    for p in sorted(posts_dir.glob("*.html"), reverse=True)[:n]:
        m = re.match(r"\d{4}-\d{2}-\d{2}-(.+)\.html$", p.name)
        if not m:
            continue
        slug = m.group(1)
        text = p.read_text(errors="replace")
        title_match = re.search(r'^title:\s*"([^"]+)"', text, re.MULTILINE)
        title = title_match.group(1) if title_match else slug
        out.append((slug, title, str(p.resolve())))
    return out


def render_brief(slug, persona_key, blog_repo, word_target):
    if persona_key not in PERSONAS:
        sys.exit(
            f"unknown persona '{persona_key}'. "
            f"choices: {', '.join(sorted(PERSONAS))}"
        )
    subagent_type, voice_line = PERSONAS[persona_key]
    today = datetime.date.today().isoformat()
    posts_dir = blog_repo / "_posts"
    out_path = posts_dir / f"{today}-{slug}.html"

    image_dir = blog_repo / "blog" / "images"
    image_path = image_dir / f"{slug}-featured.png"

    recent = recent_posts(blog_repo, n=5)
    read_first_lines = "\n".join(
        f"{i + 1}. {abs_path}" for i, (s, t, abs_path) in enumerate(recent)
    )

    word_low = word_target - 200
    word_high = word_target + 200

    return f"""# Author dispatch — `{persona_key}` for `{slug}`

Use this with the Agent tool:

    Agent({{
      subagent_type: "{subagent_type}",
      run_in_background: true,
      prompt: <the brief below>
    }})

---

## Persona

{voice_line}

## The post

Title: <fill in>
Subtitle: <fill in — one sentence that previews the argument without being a tagline>

## The material

<2-4 paragraphs explaining the argument, the facts, the seed phrase verbatim. Quote the user's exact framing if it carries the claim.>

## The argument the post makes (do not state as a thesis sentence)

<one paragraph — what the post is FOR, not just ABOUT>

## READ FIRST (in this order)

{read_first_lines}

(Trim or reorder this list — the most-relevant first; voice-continuity references second; keep 4-6 total.)

## What to do

- Output target: `{out_path}`
- Length target: {word_low}–{word_high} words ({word_target}-word midpoint)
- Front matter requirements: `title`, `subtitle`, `date: "{today}"`, `description`, `og_title`, `og_description`, `og_image: "https://sethshoultes.com/blog/images/{slug}-featured.png"`, `read_time`, `related` (list 2-3 slugs from /blog/)
- Embed the (forthcoming) featured image at the top of the post body using the existing pattern: `<img src="/blog/images/{slug}-featured.png" alt="..." style="width:100%;max-width:780px;display:block;margin:1.5rem auto;border-radius:6px" />`
- The image will be rendered separately at `{image_path}` — assume it will exist by the time the post is committed.

## Structural anchors (your discretion to reorder; these are the beats)

- Open with <a specific opening direction — concrete, not abstract>
- <beat 2 — one sentence>
- <beat 3 — one sentence>
- <beat 4 — one sentence>
- <beat 5 — one sentence>
- Close on <a closing direction>

## Craft requirements

- Section breaks via `<hr>` and `<h2>`
- Specific numbers, not generalities (e.g., "17 URL documents," "ten plugins")
- Required hyperlinks: <list anchor text + target URL pairs>
- Post-bio: <length + tone direction, or omit>

## What NOT to do

- No corporate plural ("we") unless you mean a literal team
- No exclamation marks
- No "I'm excited to announce" or any launch-copy register
- No padding, no summary closings, no "in conclusion"
- No retreading the arguments of posts in the READ FIRST list — extend them, don't recite
- <voice-specific anti-patterns for {persona_key} — fill in based on the brief's material>

## Report back

- Word count
- The single sentence you would defend most strongly if asked to cut it
- One observation about <topic> you noticed during writing that the briefer did not name (this is the line of the post)

---

## Notes

- Generated {today} by `draft-brief.py {slug} {persona_key}`
- Fill in every `<...>` placeholder before dispatching
- READ FIRST paths are the 5 most recent posts — keep the relevant ones, drop the rest
"""


def main():
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("slug", help="Post slug (kebab-case, no date prefix)")
    parser.add_argument(
        "persona",
        help="One of: " + ", ".join(sorted(PERSONAS)),
    )
    parser.add_argument(
        "--blog-repo",
        help="Path to the Jekyll blog repo (defaults to $BLOG_REPO or ~/sethshoultes.github.io)",
    )
    parser.add_argument(
        "--word-target",
        type=int,
        default=1400,
        help="Target word count (low/high window is +/- 200; default 1400)",
    )
    parser.add_argument(
        "--out",
        help="Write to file instead of stdout",
    )
    args = parser.parse_args()

    blog_repo = find_blog_repo(args.blog_repo)
    brief = render_brief(args.slug, args.persona, blog_repo, args.word_target)

    if args.out:
        Path(args.out).write_text(brief)
        print(f"wrote brief to {args.out}", file=sys.stderr)
    else:
        sys.stdout.write(brief)


if __name__ == "__main__":
    main()
