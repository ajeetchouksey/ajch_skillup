#!/usr/bin/env node
/**
 * check-option-lengths.mjs
 *
 * Enforces the question-generator skill's length-bias rule on MCQ files:
 *   - per question: correct option length is within 0.7x-1.3x of the mean distractor length
 *   - per file: the correct option is the single longest option in at most 50% of questions
 *
 * Usage: node scripts/check-option-lengths.mjs <questions.json> [...more files]
 * Exits 1 if any file violates either limit.
 */
import { readFileSync } from 'fs';

const MAX_RATIO = 1.3;
const MIN_RATIO = 0.7;
const MAX_LONGEST_SHARE = 0.5;

const files = process.argv.slice(2);
if (files.length === 0) {
  console.error('Usage: node scripts/check-option-lengths.mjs <questions.json> [...]');
  process.exit(2);
}

let failed = false;
for (const file of files) {
  const raw = JSON.parse(readFileSync(file, 'utf-8'));
  const questions = Array.isArray(raw) ? raw : raw.questions;
  if (!Array.isArray(questions)) {
    console.error(`${file}: expected an array of questions (or { questions: [...] })`);
    failed = true;
    continue;
  }

  let longest = 0;
  const violations = [];
  for (const q of questions) {
    const lens = q.options.map((o) => o.length);
    const key = lens[q.correct];
    const others = lens.filter((_, i) => i !== q.correct);
    const mean = others.reduce((a, b) => a + b, 0) / others.length;
    const ratio = key / mean;
    if (key > Math.max(...others)) longest++;
    if (ratio > MAX_RATIO || ratio < MIN_RATIO) {
      violations.push(`  ${q.id}: key is ${ratio.toFixed(2)}x the mean distractor length`);
    }
  }

  const share = longest / questions.length;
  const setOk = share <= MAX_LONGEST_SHARE;
  const ok = violations.length === 0 && setOk;
  console.log(
    `${ok ? 'PASS' : 'FAIL'} ${file}: key is longest in ${longest}/${questions.length} (${Math.round(share * 100)}%), ` +
      `${violations.length} per-question violation(s)`,
  );
  if (violations.length) console.log(violations.join('\n'));
  if (!setOk) console.log(`  set-level: key is longest in more than ${MAX_LONGEST_SHARE * 100}% of questions`);
  if (!ok) failed = true;
}
process.exit(failed ? 1 : 0);
