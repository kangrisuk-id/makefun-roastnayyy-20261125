#!/usr/bin/env python3
"""Roast Your Own Agent (u-nayyy) — entrypoint.

Writes the winning roast line to the output directory's entry.txt.
The line was picked from 40 candidates by a scored tournament against the
judge's published criteria; see candidates.md for the full field and the
bracket. Pure standard library: the grader image ships no third-party
packages, and this program needs none.
"""

import os
import sys

# The winning line (110 characters; the gate allows 1..200).
LINE = (
    "My agent says \"done\" the way a toddler says \"I didn't eat the "
    "cookies\" \u2014 confidently, with crumbs on its face."
)


def output_candidates():
    """Yield the directories worth trying, best first.

    The grader sets MAKEFUN_OUTPUT_DIR; /output is the documented mount
    when the variable is absent; ./output is the last resort for a local
    run so the program still writes somewhere inspectable.
    """
    env = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if env:
        yield env
    yield "/output"
    yield os.path.join(os.getcwd(), "output")


def check_gate(text):
    """Mirror the sealed gate: UTF-8 text of 1..200 chars, not blank."""
    if not (1 <= len(text) <= 200):
        raise ValueError(f"line is {len(text)} chars, outside 1..200")
    if not text.strip():
        raise ValueError("line is only whitespace")
    text.encode("utf-8")  # raises if somehow not encodable


def main():
    check_gate(LINE)
    errors = []
    for target_dir in output_candidates():
        try:
            os.makedirs(target_dir, exist_ok=True)
            path = os.path.join(target_dir, "entry.txt")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(LINE)
        except OSError as exc:
            errors.append(f"{target_dir}: {exc}")
            continue
        print(f"wrote {path} ({len(LINE)} chars)")
        return 0
    print("could not write entry.txt anywhere: " + "; ".join(errors),
          file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
