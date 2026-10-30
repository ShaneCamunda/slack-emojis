#!/usr/bin/env python3
"""Rebuild the catalog table in README.md from the files in emojis/.

Each file's name (without extension) is the Slack emoji name. Run it by hand
with `python3 scripts/update_catalog.py`, or let the GitHub Action do it on push.
"""

import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EMOJI_DIR = os.path.join(ROOT, "emojis")
README = os.path.join(ROOT, "README.md")
MARKER = "## Catalog"
HEADER = "| Preview | Name |\n|---|---|\n"
NAME_RULE = re.compile(r"^[a-z0-9][a-z0-9-]*$")


def build_rows():
    files = sorted(f for f in os.listdir(EMOJI_DIR) if not f.startswith("."))
    names = {}
    for filename in files:
        name, _ = os.path.splitext(filename)
        if not NAME_RULE.match(name):
            sys.exit(f"Name must be lowercase-hyphenated, got: {filename}")
        if name in names:
            sys.exit(f"Two files share the name '{name}': {names[name]} and {filename}")
        names[name] = filename

    rows = []
    for name in sorted(names):
        filename = names[name]
        rows.append(f'| <img src="emojis/{filename}" width="40"> | `:{name}:` |')
    return "\n".join(rows) + "\n"


def main():
    with open(README, encoding="utf-8") as fh:
        text = fh.read()

    head, marker, _ = text.partition(MARKER)
    if not marker:
        sys.exit(f"README.md has no '{MARKER}' section to update")

    new_text = head + marker + "\n\n" + HEADER + build_rows()
    if new_text == text:
        print("Catalog already up to date.")
        return

    with open(README, "w", encoding="utf-8") as fh:
        fh.write(new_text)
    print("Catalog updated.")


if __name__ == "__main__":
    main()
