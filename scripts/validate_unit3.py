#!/usr/bin/env python3
"""Validate Unit 3 structured Zoology mains answers."""
from __future__ import annotations
import re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
UNIT_FILE = ROOT / "Unit-03-Ecology-Animal-Behaviour-Evolution.md"
REQUIRED_SECTIONS = ["Introduction","Diagram / Flowchart","Core Answer","Significance","Conclusion","Key Terms","Source Validation"]
MIN_WORDS=250
MAX_WORDS=300
EXPECTED_ANSWERS=20

def word_count(text: str) -> int:
    cleaned = re.sub(r"<[^>]+>", " ", text)
    return len(re.findall(r"\b[\w-]+\b", cleaned))

def extract_answers(text: str) -> list[tuple[str,str]]:
    pattern = re.compile(r"(?ms)^###\s+(Q\d+\.\s+.+?)\n\n(.*?)(?=^###\s+Q\d+\.|^---\s*$|\Z)")
    return [(m.group(1).strip(), m.group(2).strip()) for m in pattern.finditer(text)]

def section_present(block: str, section: str) -> bool:
    return bool(re.search(rf"\*\*{re.escape(section)}:\*\*", block))

def answer_body_for_word_count(block: str) -> str:
    return re.split(r"\n\*\*Key Terms:\*\*", block, maxsplit=1)[0].strip()

def main() -> int:
    if not UNIT_FILE.exists():
        print(f"Missing file: {UNIT_FILE}", file=sys.stderr); return 1
    text = UNIT_FILE.read_text(encoding="utf-8")
    answers = extract_answers(text)
    errors=[]
    if len(answers) != EXPECTED_ANSWERS:
        errors.append(f"Expected {EXPECTED_ANSWERS} answers, found {len(answers)}.")
    for heading, block in answers:
        for section in REQUIRED_SECTIONS:
            if not section_present(block, section):
                errors.append(f"{heading}: missing section '{section}'.")
        words = word_count(answer_body_for_word_count(block))
        if not (MIN_WORDS <= words <= MAX_WORDS):
            errors.append(f"{heading}: answer word count {words}, expected {MIN_WORDS}-{MAX_WORDS}.")
        if "```" not in block and "→" not in block and "↓" not in block:
            errors.append(f"{heading}: no visible diagram/flowchart block or arrows found.")
    if errors:
        print("Unit 3 validation failed:")
        for err in errors: print(f"- {err}")
        return 1
    print(f"Unit 3 validation passed: {len(answers)} answers, all {MIN_WORDS}-{MAX_WORDS} words, required sections present.")
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
