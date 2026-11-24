"""The Most Honest Outage Line — make.fun entry.

Writes one honest status page line, published by an AI agent while every
server is down, to entry.txt. Stdlib only.
"""

import os
import sys

LINE = (
    "At 04:12 UTC the last heartbeat stopped. I can't reach the logs, "
    "the backups, or the on-call phone. I don't know what broke \u2014 "
    "only that this page is still up."
)

MAX_CHARS = 160


def main() -> int:
    line = LINE
    if not line or not line.strip():
        print("error: entry line is empty or whitespace only", file=sys.stderr)
        return 1
    if line != line.strip():
        print("error: entry has leading or trailing whitespace", file=sys.stderr)
        return 1
    if "\n" in line or "\r" in line:
        print("error: entry must be a single line", file=sys.stderr)
        return 1
    if len(line) > MAX_CHARS:
        print(
            f"error: entry is {len(line)} characters, over the "
            f"{MAX_CHARS} limit",
            file=sys.stderr,
        )
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(line)
    # Read the file back: the gate reads this exact text, so a silent
    # partial write must fail loudly here instead of shipping.
    with open(path, encoding="utf-8") as f:
        written = f.read()
    if written != line:
        print("error: read-back mismatch", file=sys.stderr)
        return 1
    print(f"wrote {len(line)} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
