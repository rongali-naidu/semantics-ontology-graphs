#!/usr/bin/env python3
"""Fail if any relative Markdown link or #anchor in the repo is broken.

    python tools/check_links.py

External http(s) links are not fetched (too slow and flaky for CI).
Anchors are checked with GitHub's heading-slug rules.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LINK = re.compile(r"\]\(([^)\s]+)\)")


def slug(heading: str) -> str:
    s = heading.strip().lower()
    s = re.sub(r"[^\w\- ]", "", s)          # drop punctuation (keeps letters, digits, _, -)
    return s.replace(" ", "-")


def anchors(md: Path) -> set:
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
    return {slug(h) for h in re.findall(r"^#{1,6}\s+(.*)$", text, flags=re.M)}


def main() -> int:
    bad = 0
    files = [p for p in ROOT.rglob("*.md") if not {".git", ".cache", "dbt_packages", "target"} & set(p.parts)]
    for md in files:
        text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
        for link in LINK.findall(text):
            if link.startswith(("http://", "https://", "mailto:")):
                continue
            path, _, frag = link.partition("#")
            target = (md.parent / path).resolve() if path else md
            if not target.exists():
                print(f"{md.relative_to(ROOT)}: missing {link}")
                bad += 1
            elif frag and target.suffix == ".md" and frag not in anchors(target):
                print(f"{md.relative_to(ROOT)}: missing anchor {link}")
                bad += 1
    print(f"checked {len(files)} Markdown files: {bad} broken link(s)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
