#!/usr/bin/env python3
"""Score a lifecycle email: three notes, each with a subject, a time, and a body.

Welcome, then the bargain, then nurture on the pain. Refuses a generic drip
and a cold email. A non-empty draft still fails when the notes are not three,
the welcome is not for someone who opted in, the nurture subject drops the
pain, the timing is not three times, or a timing number is not labeled example.

Stdlib only. No network. Does not send.

  python3 scripts/score.py --file draft.json
  python3 scripts/score.py --stdin
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MAX_INPUT_BYTES = 2_000_000
REFUSAL = "a generic drip and a cold email"

DRIP_RE = re.compile(
    r"generic drip|\bday\s*1\b|\bday\s*3\b|\bday\s*7\b|tip series",
    re.IGNORECASE,
)
COLD_RE = re.compile(
    r"cold email|never opted|stranger|\bintroduce our\b|first touch",
    re.IGNORECASE,
)


def fail_input(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(2)


def read_text(path: Path) -> str:
    try:
        if not path.exists():
            fail_input("file not found")
        if not path.is_file():
            fail_input("not a file")
        if path.stat().st_size > MAX_INPUT_BYTES:
            fail_input("file is too large")
        raw = path.read_bytes()
    except SystemExit:
        raise
    except OSError:
        fail_input("cannot read file")
    if raw.startswith(b"\xef\xbb\xbf"):
        raw = raw[3:]
    try:
        return raw.decode("utf-8")
    except UnicodeDecodeError:
        fail_input("file is not UTF-8 text")


def load_payload(args: argparse.Namespace) -> object:
    if args.file and args.stdin:
        fail_input("pass --file or --stdin, not both")
    if args.stdin:
        raw = sys.stdin.buffer.read(MAX_INPUT_BYTES + 1)
        if len(raw) > MAX_INPUT_BYTES:
            fail_input("input is too large")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            fail_input("input is not UTF-8 text")
    elif args.file:
        text = read_text(Path(args.file))
    else:
        fail_input("pass --file or --stdin")
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        fail_input("invalid JSON")


def nonempty_text(value: object) -> str:
    if isinstance(value, str) and value.strip():
        return value.strip()
    return ""


def refused(blob: str) -> bool:
    return DRIP_RE.search(blob) is not None or COLD_RE.search(blob) is not None


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a lifecycle email draft")
    parser.add_argument("--file", help="Path to a JSON object")
    parser.add_argument("--stdin", action="store_true", help="Read a JSON object from stdin")
    args = parser.parse_args()
    data = load_payload(args)
    if not isinstance(data, dict):
        fail_input("JSON must be an object")

    pain = nonempty_text(data.get("pain"))
    welcome_subject = nonempty_text(data.get("welcome_subject"))
    welcome_when = nonempty_text(data.get("welcome_when"))
    welcome = nonempty_text(data.get("welcome"))
    bargain_subject = nonempty_text(data.get("bargain_subject"))
    bargain_when = nonempty_text(data.get("bargain_when"))
    bargain = nonempty_text(data.get("bargain"))
    nurture_subject = nonempty_text(data.get("nurture_subject"))
    nurture_when = nonempty_text(data.get("nurture_when"))
    nurture = nonempty_text(data.get("nurture"))
    fields = (
        pain,
        welcome_subject,
        welcome_when,
        welcome,
        bargain_subject,
        bargain_when,
        bargain,
        nurture_subject,
        nurture_when,
        nurture,
    )
    blob = "\n".join(fields)

    if refused(blob):
        print(REFUSAL)
        return 1

    if any(not value for value in fields):
        print("draft is incomplete")
        return 1

    if pain.lower() not in nurture.lower():
        print(REFUSAL)
        return 1
    if len({welcome, bargain, nurture}) < 3:
        print("the notes are not three")
        return 1
    if len({welcome_subject.lower(), bargain_subject.lower(), nurture_subject.lower()}) < 3:
        print("subjects are not three notes")
        return 1
    if not re.search(r"\b(asked|opted|opt-in|opt in)\b", welcome, re.IGNORECASE):
        print("welcome is not for someone who opted in")
        return 1
    if pain.lower() not in nurture_subject.lower():
        print("nurture does not name the pain")
        return 1
    timing_ok = (
        re.search(r"opt", welcome_when, re.IGNORECASE)
        and re.search(r"\bnext\b", bargain_when, re.IGNORECASE)
        and re.search(r"\bafter\b", nurture_when, re.IGNORECASE)
    )
    if not timing_ok:
        print("timing is not three notes")
        return 1
    for when in (welcome_when, bargain_when, nurture_when):
        if re.search(r"\d", when) and "example" not in when.lower():
            print("timing number is not labeled example")
            return 1

    print(f"pain: {pain}")
    print(f"welcome subject: {welcome_subject}")
    print(f"welcome when: {welcome_when}")
    print(f"welcome: {welcome}")
    print(f"bargain subject: {bargain_subject}")
    print(f"bargain when: {bargain_when}")
    print(f"bargain: {bargain}")
    print(f"nurture subject: {nurture_subject}")
    print(f"nurture when: {nurture_when}")
    print(f"nurture: {nurture}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
