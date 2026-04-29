#!/usr/bin/env python3
"""
List the author persona used in the last N posts so you can pick a different
one for the next dispatch.

Reads voices.json (the manually-maintained slug -> persona map) and the blog
repo's _posts directory; orders posts by date (most recent first); shows the
persona for each. Then suggests the personas that haven't been used in the
recent window.

Usage:
  ./last-voice.py
  ./last-voice.py --window 5             # check more posts
  ./last-voice.py --blog-repo /path

After dispatching a new post, append the slug -> persona mapping to
voices.json so future runs see it.
"""
import argparse
import json
import os
import re
import sys
from pathlib import Path

ALL_PERSONAS = [
    "hemingway", "mccarthy", "didion", "baldwin", "morrison",
    "mcphee", "wallace", "orwell", "king", "leguin", "vonnegut",
]

# Default voices.json sits next to this script (in the cookbook recipe).
SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_VOICES_FILE = SCRIPT_DIR.parent / "voices.json"


def find_blog_repo(arg_path):
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
    sys.exit("could not find a blog repo with _posts/. Pass --blog-repo or set $BLOG_REPO.")


def post_slugs_by_date(blog_repo):
    """Return [(date, slug), ...] sorted most-recent-first."""
    out = []
    for p in (blog_repo / "_posts").glob("*.html"):
        m = re.match(r"(\d{4}-\d{2}-\d{2})-(.+)\.html$", p.name)
        if m:
            out.append((m.group(1), m.group(2)))
    return sorted(out, reverse=True)


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--window", type=int, default=5, help="Posts to look back (default 5)")
    parser.add_argument("--blog-repo", help="Override blog repo path")
    parser.add_argument("--voices-file", help="Override voices.json path")
    args = parser.parse_args()

    blog_repo = find_blog_repo(args.blog_repo)
    voices_path = Path(args.voices_file).expanduser() if args.voices_file else DEFAULT_VOICES_FILE
    if not voices_path.exists():
        sys.exit(f"voices.json not found at {voices_path}")
    voices = json.loads(voices_path.read_text())
    voices = {k: v for k, v in voices.items() if not k.startswith("_")}

    posts = post_slugs_by_date(blog_repo)[: args.window]
    if not posts:
        sys.exit("no posts found")

    print(f"last {len(posts)} posts:\n")
    used_recent = []
    for date, slug in posts:
        persona = voices.get(slug, "?")
        if persona not in {"?", "unknown"}:
            used_recent.append(persona)
        print(f"  {date}  {slug:<55}  {persona}")

    print()
    available = [p for p in ALL_PERSONAS if p not in used_recent]
    overdue = [p for p in available if p not in used_recent]

    print(f"used in window: {', '.join(sorted(set(used_recent))) or '(none confirmed)'}")
    print(f"available:      {', '.join(available)}")

    # Heuristic suggestion: pick personas not used at all in the window
    if available:
        print(f"\nsuggest:        {', '.join(available[:3])}")

    if any(voices.get(slug, "?") in {"?", "unknown"} for _, slug in posts):
        print()
        print("note: some recent posts have unknown persona; backfill voices.json")
        print(f"      ({voices_path}) for sharper rotation tracking.")


if __name__ == "__main__":
    main()
