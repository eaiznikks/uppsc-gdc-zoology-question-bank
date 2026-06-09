#!/usr/bin/env python3
"""Validate Unit 2 UPSC topper-style Zoology mains answers.

Checks:
- 20 answers total if both short and long sections are complete.
- Each model answer is 250–300 words.
- Each answer has required topper-style sections.
- Key Terms and Source Validation are present for every answer.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
UNIT_FILE = ROOT / "Unit-02-Chordates.md"

REQUIRED_SECTIONS = [
    "Introduction",
    "Diagram / Flowchart",
    "Core Answer",
    "Conclusion",
    "Key Terms",
    "Source Validation",
]

MIN_WORDS = 250
MAX_WORDS = 300
EXPECTED_ANSWERS = 20


def word_count(text: str) -> int:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\w-]+\b", cleaned))


def extract_answers(text: str) -> list[tuple[str, str]]:
    """Return list of (question_heading, answer_block)."""
    pattern = re.compile(
        r"(?ms)^###\s+(Q\d+\.\s+.+?)\n\n(.*?)(?=^###\s+Q\d+\.|\Z)"
    )
    return [(m.group(1).strip(), m.group(2).strip()) for m in pattern.finditer(text)]


def section_present(block: str, section: str) -> bool:
    escaped = re.escape(section)
    return bool(re.search(rf"\*\*{escaped}:\*\*", block))


def answer_body_for_word_count(block: str) -> str:
    """Count the model answer only, excluding Key Terms and Source Validation."""
    block = re.split(r"\n\*\*Key Terms:\*\*", block, maxsplit=1)[0]
    return block.strip()


def main() -> int:
    if not UNIT_FILE.exists():
        print(f"Missing file: {UNIT_FILE}", file=sys.stderr)
        return 1

    text = UNIT_FILE.read_text(encoding="utf-8")
    answers = extract_answers(text)
    errors: list[str] = []

    if len(answers) != EXPECTED_ANSWERS:
        errors.append(
            f"Expected {EXPECTED_ANSWERS} answers, found {len(answers)}. "
            "This is okay only while Unit 2 is still in draft."
        )

    for heading, block in answers:
        for section in REQUIRED_SECTIONS:
            if not section_present(block, section):
                errors.append(f"{heading}: missing section '{section}'.")

        wc = word_count(answer_body_for_word_count(block))
        if not (MIN_WORDS <= wc <= MAX_WORDS):
            errors.append(
                f"{heading}: answer word count {wc}, expected {MIN_WORDS}-{MAX_WORDS}."
            )

        if "```" not in block and "→" not in block and "↓" not in block:
            errors.append(f"{heading}: no visible diagram/flowchart block or arrows found.")

    if errors:
        print("Unit 2 validation failed:")
        for err in errors:
            print(f"- {err}")
        return 1

    print(
        f"Unit 2 validation passed: {len(answers)} answers, "
        f"all {MIN_WORDS}-{MAX_WORDS} words, required sections present."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
