#!/usr/bin/env python3
import re, sys, pathlib
path=pathlib.Path('Unit-01-Non-Chordates.md')
text=path.read_text()
answers=re.findall(r'\*\*Model Answer \((\d+) words\):\*\*\n\n(.+?)(?=\n\n\*\*Key Terms:\*\*)', text, flags=re.S)
errors=[]
if len(answers)!=20: errors.append(f'Expected 20 answers, found {len(answers)}')
for idx,(declared,body) in enumerate(answers,1):
    count=len(re.findall(r"\b[\w-]+\b", body))
    dec=int(declared)
    if count!=dec: errors.append(f'Answer {idx}: declared {dec}, actual {count}')
    if idx<=10 and not (110<=count<=125): errors.append(f'Short answer {idx} out of range: {count}')
    if idx>10 and not (175<=count<=200): errors.append(f'Long answer {idx-10} out of range: {count}')
if text.count('**Key Terms:**')!=20: errors.append('Expected 20 key-term blocks')
if text.count('**Source Validation:**')!=20: errors.append('Expected 20 source-validation blocks')
if errors:
    print('\n'.join(errors)); sys.exit(1)
print('Unit 1 validation passed: 10 short answers, 10 long answers, all word counts in range, key terms and source validation present.')
