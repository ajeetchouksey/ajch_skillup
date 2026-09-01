# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

`ajch_skillup` is a **content-only** repository — the canonical source for Aarya's SkillUp exam-prep tracks (study notes, MCQ banks, scenarios, task-statement mappings) for every certification exam the platform offers. There is no `src/`, no app code, and no build step here. The consuming app, `ajeetchouksey/ajch_platform`, pulls this content via a pinned Git SHA in its `content-manifest.json` — it never edits exam content directly, and this repo never contains app/TypeScript/routing code.

Content lives at `content/skillup/{examId}/`: `index.json` (per-exam registry — the single source of truth for that exam), `questions/{examId}-domain{N}.json`, `notes/*.md`, `scenarios/*.json`, `task-statements.json`, `images/`. `content/skillup/catalog.json` aggregates every exam's `index.json` and is **auto-generated** — never hand-edit it.

## Commands

```bash
# Validate all content against schema (JSON validity, MCQ schema, file-reference resolution)
npm run validate
# equivalent to:
shopt -s globstar nullglob
node scripts/validate-content.mjs \
  content/skillup/catalog.json \
  content/skillup/**/index.json \
  content/skillup/**/task-statements.json \
  content/skillup/**/questions/*.json \
  content/skillup/**/notes/*.md

# Regenerate catalog.json from each exam's index.json (recounts questions from actual files)
npm run catalog          # python3 scripts/generate-catalog.py
```

There is no lint, test, or build command — `validate` (schema/reference checks) is the only gate, and it is exactly what CI runs (`.github/workflows/validate-content.yml`) on any PR/push touching `content/skillup/**` or `scripts/validate-content.mjs`. To check a single exam or file, pass narrower globs to `validate-content.mjs` directly, e.g. `node scripts/validate-content.mjs content/skillup/ccaf/questions/*.json`.

### Other scripts (`scripts/`)

| Script | Purpose |
|---|---|
| `new-exam.mjs --id <id> --code <CODE> --title <t> --level 101\|201\|301 --domains "A,B,C" [--provider --fee --duration --pass --color]` | Scaffolds a brand-new exam directory with all required files from templates |
| `check-exam-completeness.mjs [--exam <id>] [--strict]` | Completeness dashboard for one/all exams; `--strict` exits 1 on issues |
| `domain-content-audit.mjs [--exam <id>]` | Per-domain readiness (question count, difficulty coverage, notes present, task-statement coverage, tag distribution) against the minimums in the content-standard skill |
| `backfill-task-statements.mjs [--dry-run] [--exam <id>]` | Assigns unmapped questions into `task-statements.json` |
| `check-mermaid.mjs` | Validates mermaid block syntax in AB-731 notes (hardcoded file list) |
| `render-diagrams.mjs [--exam <id>]` → `swap-mermaid-to-png.mjs --exam <id>` | Two-step pipeline: render mermaid blocks to PNG via mermaid.ink into `images/`, then swap the markdown mermaid blocks for image references |
| `optimize-images.mjs [--exam <id>] [--max-kb 300]` | Compresses oversized PNGs in exam `images/` dirs (uses `sharp`) |
| `generate-catalog.py` | Regenerates `catalog.json`; also self-corrects drifted question counts in each `index.json` |

Run `check-exam-completeness.mjs` and/or `domain-content-audit.mjs` after any content change, and always regenerate the catalog (`npm run catalog`) before opening a PR when an `index.json` changed.

**Caveat**: some `.claude/skills/*/SKILL.md` files (synced platform-wide) reference `scripts/content-health-report.mjs`, `src/types/content.ts`, and `src/lib/content-loader.ts`. None of these exist in this repo — they're part of `ajch_platform`. In this repo, use `check-exam-completeness.mjs` / `domain-content-audit.mjs` as the equivalent health checks, and treat the registry schema (below) as authoritative over any TS interface mentioned in the skill docs.

## Architecture: registry-driven exams

Adding or growing an exam never requires app code changes — everything is data-driven off `index.json`:

- **`content/skillup/{examId}/index.json`** — per-exam registry: `domains[]` (id, title, weight, notesFile), `questionFiles[]`, `scenarioFiles[]`, `taskStatementsFile`, `contentVersion`/`contentUpdatedAt`/`changelog`, `colorScheme`/`palette` (CSS values, not Tailwind — Tailwind scheme mapping lives in `ajch_platform`'s `EXAM_SCHEMES`).
- **`content/skillup/catalog.json`** — generated rollup of every exam's `index.json`, read by the platform to build the exam list. Regenerate with `generate-catalog.py`; never edit by hand.
- **`task-statements.json`** — maps official study-guide task IDs to the `questionIds` that cover them; every exam must have one.
- File path conventions (v3.x): questions at `questions/{examId}-domain{N}.json`, notes at `notes/{examId}-d{N}-{slug}.md` (or `d{N}-{slug}.md` for some older exams — check `domains[].notesFile` for the exact name), scenarios at `scenarios/{examId}-{slug}.json`.

Full schema reference: `.claude/skills/exam-registry/SKILL.md`. Quality bar for all three content types (MCQ schema, tag taxonomy, notes structure, scenario schema, versioning protocol, per-domain minimums): `.claude/skills/content-standard/SKILL.md`.

### Content-versioning protocol (required on every content write)

After any write to questions/notes/scenarios, bump the exam's `index.json`: increment `contentVersion` (patch for small edits, minor for new domain coverage or ≥6 new questions), update `contentUpdatedAt` to today's date, and append a `changelog` entry describing what changed. This applies whether the write comes from an agent or a manual edit.

## Architecture: the agent-driven authoring pipeline

Content authoring here is agent-orchestrated, not free-form editing. **`.claude/agents/` and `.claude/skills/` are synced copies from `ajch_platform`'s canonical definitions (via `sync-vertical-agents.mjs`) — hand-edits here get overwritten on the next sync**, so treat changes to agent/skill files as rare and expect them to originate upstream.

```
Curriculum Engineer (L1 orchestrator, "Exam Commander")
  — fetches source material, extracts concepts, classifies against the target
    exam's index.json domains (registry-first: never assumes a fixed domain
    structure like CCA-F's D1–D5), dedupes against existing question tags
    ↓ delegates
  ├─ Assessment Engineer  → writes MCQ JSON to questions/{examId}/*.json only
  ├─ Docs Engineer        → writes/updates markdown to notes/*.md only
  └─ Scenario Engineer    → writes RichScenario JSON to scenarios/*.json only
```

Each specialist agent is scoped to write to exactly one subdirectory and stops/reports if asked to write elsewhere. Each bumps `contentVersion` in `index.json` after writing (see protocol above), and confirms the relevant registry array (`questionFiles[]`/`scenarioFiles[]`/`domains[].notesFile`) references the file it just wrote.

- **Docs Engineer** notes have a strict required shape (see `.claude/agents/docs-engineer.md` and the sibling `docs-engineer-writing-framework.md`): every domain note needs a `## Deep Dive` section (connective narrative + worked scenario + memory aid + exam strategy — pointer-only notes fail review), every `### Key Concept` block follows a one-line-claim-then-two-paragraphs shape ending in a bolded analogy, and every topic section needs an `### In Practice` block (what breaks without this / decision trigger / when you'd choose differently) before the Exam Trap callout.
- **Assessment Engineer** and **Scenario Engineer** IDs are sequential and zero-padded (`{examId}-d{N}-{NNN}`, `{examId}-scenario-{NNN}`); always read the existing file to find the highest ID before appending — never overwrite the array wholesale.
- Distractors must be plausible (exploit real misconceptions, not nonsense), explanations must cover why the correct answer wins *and* why each distractor fails, and scenarios must span ≥2 domains with ≥2 characters creating decision tension.

## Publishing flow

1. Branch: `git checkout -b skillup/<exam-or-domain-slug>`
2. Author via the relevant agent (or by hand, following `.claude/skills/exam-registry/SKILL.md`)
3. Update the exam's `index.json` (counts, file references, `contentVersion`)
4. `npm run catalog` to regenerate `catalog.json`
5. `npm run validate` — fix any errors
6. Open a PR (CODEOWNERS requires `@ajeetchouksey`/`@ajchava` approval on every path, with `.github/workflows/`, `.github/CODEOWNERS`, and `scripts/validate-content.mjs` under the strictest review)
7. After merge, promotion into `ajch_platform` happens from that repo (`node scripts/sync-vertical-repo.mjs skillup ajeetchouksey/ajch_skillup <sha>` or the `promote-content.yml` dispatch) — not from here.
