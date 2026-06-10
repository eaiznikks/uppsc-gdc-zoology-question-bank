#!/usr/bin/env python3
from __future__ import annotations
import re, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
UNIT_FILE=ROOT/"Unit-08-Mammalian-Physiology.md"
REQUIRED_SECTIONS=["Introduction","Diagram / Flowchart","Core Answer","Significance","Conclusion","Key Terms","Source Validation"]
MIN_WORDS=250; MAX_WORDS=300; EXPECTED_ANSWERS=20

def word_count(text):
    return len(re.findall(r"\b[\w-]+\b", re.sub(r"<[^>]+>", " ", text)))
def extract_answers(text):
    return [(m.group(1).strip(),m.group(2).strip()) for m in re.finditer(r"(?ms)^###\s+(Q\d+\.\s+.+?)\n\n(.*?)(?=^###\s+Q\d+\.|^---\s*$|\Z)", text)]
def main():
    text=UNIT_FILE.read_text(encoding='utf-8'); answers=extract_answers(text); errors=[]
    if len(answers)!=EXPECTED_ANSWERS: errors.append(f"Expected {EXPECTED_ANSWERS} answers, found {len(answers)}.")
    for h,b in answers:
        for s in REQUIRED_SECTIONS:
            if not re.search(rf"\*\*{re.escape(s)}:\*\*", b): errors.append(f"{h}: missing section '{s}'.")
        body=re.split(r"\n\*\*Key Terms:\*\*", b, maxsplit=1)[0]
        wc=word_count(body)
        if not(MIN_WORDS<=wc<=MAX_WORDS): errors.append(f"{h}: answer word count {wc}, expected {MIN_WORDS}-{MAX_WORDS}.")
        if "```" not in b and "→" not in b and "↓" not in b: errors.append(f"{h}: no visible diagram/flowchart block or arrows found.")
    if errors:
        print('Unit 8 validation failed:'); [print('- '+e) for e in errors]; return 1
    print(f"Unit 8 validation passed: {len(answers)} answers, all {MIN_WORDS}-{MAX_WORDS} words, required sections present."); return 0
if __name__=='__main__': raise SystemExit(main())
