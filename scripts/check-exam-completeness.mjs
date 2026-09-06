#!/usr/bin/env node
/**
 * check-exam-completeness.mjs
 * Audits every exam in content/skillup/ and prints a completeness
 * dashboard to stdout.
 *
 * Usage:
 *   node scripts/check-exam-completeness.mjs
 *   node scripts/check-exam-completeness.mjs --strict      (exit 1 if any issues found)
 *   node scripts/check-exam-completeness.mjs --exam ab731  (single exam)
 */

import { readFileSync, existsSync, readdirSync, statSync } from 'fs';
import { resolve, dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = resolve(__dirname, '..');
// Pre-split (ajch_platform) layout nested content under public/; ajch_skillup
// has content/ at the repo root directly — support both.
const CONTENT_BASE = existsSync(join(ROOT, 'public')) ? join(ROOT, 'public') : ROOT;
const SKILLUP_DIR = join(ROOT, 'content', 'skillup');

const args = process.argv.slice(2);
const STRICT = args.includes('--strict');
const FILTER_EXAM = (() => {
  const i = args.indexOf('--exam');
  return i !== -1 ? args[i + 1] : null;
})();

// ANSI colours
const RESET  = '\x1b[0m';
const BOLD   = '\x1b[1m';
const GREEN  = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED    = '\x1b[31m';
const DIM    = '\x1b[2m';

// ── Helpers ───────────────────────────────────────────────────────────────────

function readJson(absPath) {
  try { return JSON.parse(readFileSync(absPath, 'utf8')); }
  catch { return null; }
}

/** Resolve a content-relative path (e.g. "content/skillup/...") to absolute. */
function absContent(relativePath) {
  if (relativePath.startsWith('content/')) return join(CONTENT_BASE, relativePath);
  return join(ROOT, relativePath);
}

function pct(score, total) {
  if (total === 0) return 100;
  return Math.round((score / total) * 100);
}

function bar(score, total) {
  const p = pct(score, total);
  const filled = Math.round(p / 5);
  return '[' + '█'.repeat(filled) + '░'.repeat(20 - filled) + `] ${p}%`;
}

function colorFor(p) {
  if (p === 100) return GREEN;
  if (p >= 80)   return YELLOW;
  return RED;
}

// ── Canonical required fields for index.json ──────────────────────────────────

const INDEX_REQUIRED = [
  'schemaVersion', 'id', 'examCode', 'title', 'shortTitle',
  'contentLevel', 'description', 'questions', 'duration',
  'passScore', 'passThreshold', 'examFee',
  'available', 'accentColor', 'colorScheme',
  'domains', 'questionFiles', 'taskStatementsFile', 'resources',
];

// Skill tracks (IDEA-0016) are deliberately exam-metadata-free — no
// examCode/duration/passScore/passThreshold/examFee, and modules[] instead
// of domains[]/questionFiles[]. A skill-track entry that DOES carry any of
// EXAM_ONLY_FIELDS is a defect (NFR-6), not just a missing-field warning.
const SKILL_TRACK_REQUIRED = [
  'schemaVersion', 'id', 'title', 'shortTitle',
  'contentLevel', 'description', 'available',
  'accentColor', 'colorScheme', 'modules', 'resources',
];
const EXAM_ONLY_FIELDS = ['examCode', 'duration', 'passScore', 'passThreshold', 'examFee'];

// ── Check functions ───────────────────────────────────────────────────────────

function checkIndex(idx) {
  if (idx.kind === 'skill-track') return checkSkillTrackIndex(idx);

  const issues = [];
  const warnings = [];

  for (const f of INDEX_REQUIRED) {
    if (!(f in idx)) issues.push(`missing required field: "${f}"`);
  }

  if (Array.isArray(idx.domains)) {
    for (const d of idx.domains) {
      if (!d.notesFile) {
        warnings.push(`domain ${d.id} ("${d.title}"): missing notesFile`);
      } else if (!existsSync(absContent(d.notesFile))) {
        issues.push(`domain ${d.id}: notesFile not found → ${d.notesFile}`);
      }
    }
  }

  if (Array.isArray(idx.questionFiles)) {
    for (const qf of idx.questionFiles) {
      if (!existsSync(absContent(qf))) issues.push(`questionFile not found → ${qf}`);
    }
  }

  if (idx.taskStatementsFile && !existsSync(absContent(idx.taskStatementsFile))) {
    issues.push(`taskStatementsFile not found → ${idx.taskStatementsFile}`);
  }

  if (Array.isArray(idx.scenarioFiles)) {
    for (const sf of idx.scenarioFiles) {
      if (!existsSync(absContent(sf))) issues.push(`scenarioFile not found → ${sf}`);
    }
  }

  // Actual question count vs declared
  if (Array.isArray(idx.questionFiles)) {
    let actual = 0;
    for (const qf of idx.questionFiles) {
      const data = readJson(absContent(qf));
      if (Array.isArray(data)) actual += data.length;
    }
    if (actual > 0 && actual !== idx.questions) {
      issues.push(`question count mismatch: index.json says ${idx.questions}, files contain ${actual}`);
    }
  }

  return { issues, warnings };
}

function checkSkillTrackIndex(idx) {
  const issues = [];
  const warnings = [];

  for (const f of SKILL_TRACK_REQUIRED) {
    if (!(f in idx)) issues.push(`missing required field: "${f}"`);
  }

  for (const f of EXAM_ONLY_FIELDS) {
    if (f in idx) issues.push(`kind: "skill-track" must not carry exam-only field "${f}" (fabricated-exam-metadata risk — IDEA-0016 NFR-6)`);
  }

  if (Array.isArray(idx.modules)) {
    for (const m of idx.modules) {
      if (!Array.isArray(m.lessons) || m.lessons.length === 0) {
        issues.push(`module ${m.id} ("${m.title}"): no lessons`);
        continue;
      }
      for (const l of m.lessons) {
        if (!l.notesFile) {
          warnings.push(`lesson ${l.id} ("${l.title}"): missing notesFile`);
        } else if (!existsSync(absContent(l.notesFile))) {
          issues.push(`lesson ${l.id}: notesFile not found → ${l.notesFile}`);
        }
        if (!Array.isArray(l.knowledgeCheck) || l.knowledgeCheck.length === 0) {
          warnings.push(`lesson ${l.id}: no knowledgeCheck questions`);
        } else if (l.knowledgeCheck.length < 3 || l.knowledgeCheck.length > 5) {
          warnings.push(`lesson ${l.id}: knowledgeCheck has ${l.knowledgeCheck.length} questions (expected 3-5)`);
        }
      }
    }
  }

  if (idx.practiceBank) {
    if (!Array.isArray(idx.practiceBank.questionFiles)) {
      issues.push('practiceBank present but questionFiles is not an array');
    } else {
      for (const qf of idx.practiceBank.questionFiles) {
        if (!existsSync(absContent(qf))) issues.push(`practiceBank questionFile not found → ${qf}`);
      }
      let actual = 0;
      for (const qf of idx.practiceBank.questionFiles) {
        const data = readJson(absContent(qf));
        if (Array.isArray(data)) actual += data.length;
      }
      if (actual > 0 && actual !== idx.practiceBank.questions) {
        issues.push(`practiceBank question count mismatch: index.json says ${idx.practiceBank.questions}, files contain ${actual}`);
      }
    }
  }

  return { issues, warnings };
}

function checkTaskStatements(idx) {
  const issues = [];
  const warnings = [];

  if (!idx.taskStatementsFile) return { issues, warnings };
  const tsPath = absContent(idx.taskStatementsFile);
  if (!existsSync(tsPath)) return { issues, warnings };

  const ts = readJson(tsPath);
  if (!ts) { issues.push('task-statements.json is invalid JSON'); return { issues, warnings }; }

  const allIds = new Set();
  if (Array.isArray(idx.questionFiles)) {
    for (const qf of idx.questionFiles) {
      const data = readJson(absContent(qf));
      if (Array.isArray(data)) data.forEach(q => { if (q.id) allIds.add(q.id); });
    }
  }

  const mappedIds = new Set();
  if (Array.isArray(ts.domains)) {
    for (const domain of ts.domains) {
      if (!Array.isArray(domain.tasks)) continue;
      for (const task of domain.tasks) {
        if (!Array.isArray(task.questionIds) || task.questionIds.length === 0) {
          warnings.push(`task ${task.id}: no questionIds — consider adding coverage`);
          continue;
        }
        if (task.questionIds.length < 3) {
          warnings.push(`task ${task.id}: only ${task.questionIds.length} question(s) — low coverage`);
        }
        for (const qid of task.questionIds) {
          mappedIds.add(qid);
          if (!allIds.has(qid)) {
            issues.push(`task ${task.id}: questionId "${qid}" not found in question files`);
          }
        }
      }
    }
  }

  for (const id of allIds) {
    if (!mappedIds.has(id)) warnings.push(`orphaned question: "${id}" not mapped to any task`);
  }

  return { issues, warnings };
}

function checkNotesCoverage(idx) {
  const warnings = [];
  const notesFiles = idx.kind === 'skill-track'
    ? (idx.modules ?? []).flatMap((m) => (m.lessons ?? []).map((l) => ({ id: l.id, notesFile: l.notesFile })))
    : (idx.domains ?? []).map((d) => ({ id: d.id, notesFile: d.notesFile }));
  const unit = idx.kind === 'skill-track' ? 'lesson' : 'domain';

  for (const { id, notesFile } of notesFiles) {
    if (!notesFile) continue;
    const p = absContent(notesFile);
    if (!existsSync(p)) continue;
    const content = readFileSync(p, 'utf8');
    if ((content.match(/^#{1,3} /gm) || []).length === 0) {
      warnings.push(`${unit} ${id}: notes file has no headings`);
    }
  }
  return warnings;
}

// ── Audit one exam ────────────────────────────────────────────────────────────

function auditExam(examId) {
  const idxPath = join(SKILLUP_DIR, examId, 'index.json');
  if (!existsSync(idxPath)) return null;

  const idx = readJson(idxPath);
  if (!idx) {
    return { examId, examCode: examId, title: examId, score: 0, totalChecks: 1,
             issues: ['index.json is invalid JSON'], warnings: [] };
  }

  const { issues: i1, warnings: w1 } = checkIndex(idx);
  const { issues: i2, warnings: w2 } = checkTaskStatements(idx);
  const w3 = checkNotesCoverage(idx);

  const allIssues   = [...i1, ...i2];
  const allWarnings = [...w1, ...w2, ...w3];

  const totalChecks = idx.kind === 'skill-track'
    ? SKILL_TRACK_REQUIRED.length +
      (idx.modules ?? []).reduce((n, m) => n + (m.lessons?.length ?? 0), 0) +
      (idx.practiceBank?.questionFiles?.length ?? 0)
    : INDEX_REQUIRED.length +
      (idx.domains?.length ?? 0) +
      (idx.questionFiles?.length ?? 0) +
      (idx.taskStatementsFile ? 1 : 0);

  return {
    examId,
    examCode: idx.examCode ?? (idx.kind === 'skill-track' ? 'SKILL-TRACK' : examId),
    title: idx.title ?? examId,
    score: Math.max(0, totalChecks - allIssues.length),
    totalChecks,
    issues: allIssues,
    warnings: allWarnings,
  };
}

// ── Discover exams ─────────────────────────────────────────────────────────────

if (!existsSync(SKILLUP_DIR)) {
  console.error(`SkillUp directory not found: ${SKILLUP_DIR}`);
  process.exit(1);
}

const examIds = readdirSync(SKILLUP_DIR)
  .filter(d => statSync(join(SKILLUP_DIR, d)).isDirectory())
  .filter(d => existsSync(join(SKILLUP_DIR, d, 'index.json')))
  .filter(d => !FILTER_EXAM || d === FILTER_EXAM);

if (examIds.length === 0) {
  console.error(FILTER_EXAM
    ? `Exam "${FILTER_EXAM}" not found in ${SKILLUP_DIR}`
    : `No exams found in ${SKILLUP_DIR}`);
  process.exit(1);
}

// ── Render ─────────────────────────────────────────────────────────────────────

console.log(`\n${BOLD}╔════════════════════════════════════════════════════╗${RESET}`);
console.log(`${BOLD}║       SkillUp — Exam Completeness Audit             ║${RESET}`);
console.log(`${BOLD}╚════════════════════════════════════════════════════╝${RESET}\n`);

let totalIssues = 0;

for (const examId of examIds) {
  const r = auditExam(examId);
  if (!r) continue;

  const p = pct(r.score, r.totalChecks);
  const c = colorFor(p);

  console.log(`${BOLD}${c}${r.examCode}${RESET}  ${DIM}${r.title}${RESET}`);
  console.log(`  ${c}${bar(r.score, r.totalChecks)}${RESET}  ${DIM}(${r.score}/${r.totalChecks} checks)${RESET}`);

  for (const issue of r.issues) {
    console.log(`  ${RED}✗${RESET} ${issue}`);
    totalIssues++;
  }
  for (const warn of r.warnings) {
    console.log(`  ${YELLOW}⚠${RESET} ${warn}`);
  }
  if (r.issues.length === 0 && r.warnings.length === 0) {
    console.log(`  ${GREEN}✓ All checks passed${RESET}`);
  }
  console.log();
}

if (totalIssues === 0) {
  console.log(`${GREEN}${BOLD}All ${examIds.length} exam(s) passed all checks ✓${RESET}\n`);
} else {
  console.log(`${RED}${BOLD}${totalIssues} issue(s) found. Fix before adding new content.${RESET}`);
  console.log(`${DIM}Tip: node scripts/check-exam-completeness.mjs --exam <id> to focus on one exam.${RESET}\n`);
}

if (STRICT && totalIssues > 0) process.exit(1);
