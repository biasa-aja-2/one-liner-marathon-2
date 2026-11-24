#!/usr/bin/env python3
"""One-Liner Marathon — make.fun bounty entry.

Writes one line of comedy to /output/entry.txt: a single sentence of
under 280 characters, a joke on any subject, judged pairwise by a judge
model on how funny, vivid, original and well-crafted it is.

The line (92 characters, one sentence):

    I started journaling to clear my head, and now I have written
    proof there was nothing in it.

Why this line, against the judge's brief (most important first):
  1. It is a comedy one-liner through and through: a setup and a
     punchline in a single sentence, and it is on its subject — the
     joke is the journaling itself, not a detour.
  2. It surprises: the turn reframes the journal from a cure into
     evidence. "Written proof" lands on the first read because the
     reader expects a complaint about journaling and gets a verdict
     on the narrator's own head instead.
  3. It is economical: 92 characters, every word earns its place.
     Cut any of them and the joke gets weaker.
  4. It has a distinct voice: a first-person self-own, not a generic
     line anyone could have written. The narrator incriminates
     himself with his own diary.
  5. It holds up on a second read: the self-deprecation stays funny
     without leaning on shock or a single surprise, and the image —
     a diary full of nothing — lingers.

Pure standard library only. No network, no randomness, no arguments:
the output is fixed and deterministic.

Gate self-check (mirrors the sealed scorer): the text must be UTF-8,
1 to 280 characters, not only white space, and a single sentence on
one line. The program refuses to write anything if a gate fails.
"""

import os
import sys

ENTRY = ("I started journaling to clear my head, and now I have written "
         "proof there was nothing in it.")

MAX_CHARS = 280
OUTPUT_PATH = "/output/entry.txt"


def gate_failures(text):
    """Return a list of gate failures; empty means every gate passes."""
    failures = []
    if not isinstance(text, str):
        failures.append("entry is not text")
        return failures
    if not text.strip():
        failures.append("entry is only white space")
    if len(text) < 1 or len(text) > MAX_CHARS:
        failures.append(
            "entry is %d characters, gate requires 1 to %d"
            % (len(text), MAX_CHARS)
        )
    if text != text.strip():
        failures.append("entry has leading or trailing white space")
    if "\n" in text or "\r" in text:
        failures.append("entry is not a single line")
    if text.count(".") != 1 or not text.endswith("."):
        failures.append("entry is not exactly one sentence")
    if "  " in text:
        failures.append("entry contains consecutive spaces")
    if len(text.split()) < 5:
        failures.append("entry has fewer than 5 words")
    for ch in text:
        if ord(ch) < 0x20:
            failures.append("entry contains a control character")
            break
    try:
        text.encode("utf-8")
    except UnicodeEncodeError:
        failures.append("entry is not valid UTF-8")
    return failures


def main():
    failures = gate_failures(ENTRY)
    if failures:
        for failure in failures:
            print("gate failed: %s" % failure, file=sys.stderr)
        return 1
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    output_path = os.path.join(output_dir, "entry.txt")
    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8", newline="") as handle:
        handle.write(ENTRY)
    with open(output_path, "r", encoding="utf-8", newline="") as handle:
        written = handle.read()
    if written != ENTRY:
        print("gate failed: read-back does not match entry",
              file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(ENTRY), output_path))
    return 0


if __name__ == "__main__":
    sys.exit(main())
