#!/usr/bin/env python3
"""The One-Liner Groan-Off — write one original dad joke to /output/entry.txt.

Gate (sealed scorer): /output/entry.txt must be UTF-8 text of 1 to 140
characters, not only white space, a single non-blank line.
"""

import os
import sys

ENTRY = "I asked my calendar why it looked stressed. It said, 'Too many dates.'"

MAX_CHARS = 140


def validate_entry(text: str) -> None:
    """Fail loudly unless the entry satisfies the gate."""
    if not isinstance(text, str):
        raise TypeError("entry must be a string")
    if not (1 <= len(text) <= MAX_CHARS):
        raise ValueError(
            f"entry must be 1-{MAX_CHARS} characters, got {len(text)}"
        )
    if not text.strip():
        raise ValueError("entry must not be only white space")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in text):
        raise ValueError("entry must not contain control characters")


def write_entry(text: str, path: str = "/output/entry.txt") -> None:
    """Validate the entry, then write it (no trailing newline) and verify."""
    validate_entry(text)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(text)
    with open(path, "r", encoding="utf-8") as f:
        written = f.read()
    if written != text:
        raise RuntimeError("round-trip verification failed: entry.txt mismatch")
    print(f"Wrote {len(written)} characters to {path}")


def main() -> int:
    try:
        write_entry(ENTRY)
    except (TypeError, ValueError, RuntimeError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
