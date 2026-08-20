# ajch_skillup

This repository is the canonical content source for Aarya's SkillUp exam-prep tracks — study notes, MCQ question banks, scenarios, and task-statement mappings for every certification exam the platform offers. The platform consumes this repository via a pinned Git SHA through `content-manifest.json` in the main app repo (`ajeetchouksey/ajch_platform`), so content is versioned and reviewable before it goes live.

## What this repo contains

- `content/skillup/{examId}/` — one directory per exam:
  - `index.json` — exam registry: domains, weights, `questionFiles[]`, `scenarioFiles[]`, `taskStatementsFile`
  - `questions/` — MCQ question bank, one file per domain
  - `notes/` — domain study notes (markdown, with Mermaid diagrams and exam-trap callouts)
  - `scenarios/` — multi-step applied scenarios
  - `task-statements.json` — maps official study-guide task statements to question IDs
  - `images/` — diagrams referenced from notes (as `/content/skillup/{examId}/images/{file}`)
- `content/skillup/catalog.json` — **auto-generated**, aggregates every exam's `index.json`. Never hand-edit; regenerate with `scripts/generate-catalog.py`.
- `.claude/agents/` — the 4 content-authoring agents for this vertical
- `.claude/skills/exam-registry/`, `.claude/skills/content-analysis/` — schema reference skills these agents load
- `.github/workflows/validate-content.yml` — automated schema validation on PR/push
- `scripts/validate-content.mjs` — schema validator (canonical copy, synced from `ajch_platform`)
- `scripts/generate-catalog.py` — regenerates `catalog.json` from each exam's `index.json`, recounting questions from the actual question files
- `scripts/new-exam.mjs`, `optimize-images.mjs`, `render-diagrams.mjs`, `swap-mermaid-to-png.mjs`, `check-exam-completeness.mjs`, `check-mermaid.mjs`, `backfill-task-statements.mjs` — authoring/maintenance tooling

## Publishing model

Content authoring here is agent-driven, not a free-form editing sandbox.

1. **Curriculum Engineer** (L1 orchestrator) receives a content request — a new exam, a domain gap, a stale note — and classifies concepts against the exam's registry (`index.json`).
2. It delegates to the relevant specialist:
   - **Assessment Engineer** — writes schema-validated MCQ question JSON to `content/skillup/{examId}/questions/`
   - **Docs Engineer** — writes/updates domain study notes to `content/skillup/{examId}/notes/`
   - **Scenario Engineer** — writes RichScenario JSON to `content/skillup/{examId}/scenarios/`
3. Each specialist updates the exam's `index.json` after writing (question counts, `notesFile`/`scenarioFiles` references, `contentVersion` bump).
4. Run `scripts/generate-catalog.py` to regenerate `catalog.json` from the updated registries.
5. Validate locally, open a PR, get it reviewed and merged.
6. After merge to `main`, `ajch_platform` can promote the new SHA into its `content-manifest.json` (via its `promote-content.yml` workflow or `scripts/sync-vertical-repo.mjs`).

## How the content agents work

### Curriculum Engineer (`.claude/agents/curriculum-engineer.md`)

L1 orchestrator. Registry-first: always reads an exam's `index.json` (and `catalog.json` for the full exam list) before classifying concepts or delegating — never assumes a fixed domain structure. Delegates MCQ generation to Assessment Engineer and notes writing to Docs Engineer.

### Assessment Engineer (`.claude/agents/assessment-engineer.md`)

Writes schema-validated question JSON to `content/skillup/{examId}/questions/` only. Never writes outside that path. Confirms the exam's `index.json` `questionFiles[]` includes any new file.

### Docs Engineer (`.claude/agents/docs-engineer.md`)

Writes domain study notes to `content/skillup/{examId}/notes/` only. Every note requires a `## Deep Dive` section (connective narrative, worked scenario, memory aid, exam strategy) — pointer-only notes are rejected in review.

### Scenario Engineer (`.claude/agents/scenario-engineer.md`)

Writes RichScenario JSON to `content/skillup/{examId}/scenarios/` only. Bumps `contentVersion` in the exam's `index.json` after every write.

## Validation

CI runs `scripts/validate-content.mjs` against every exam's `index.json`, `task-statements.json`, question files, and notes files on PR/push. It checks JSON validity, MCQ schema (domain, id, question, options, correct, explanation, tags), and that every file reference in an `index.json`/`task-statements.json` actually resolves.

Local validation:

```bash
shopt -s globstar nullglob
node scripts/validate-content.mjs \
  content/skillup/catalog.json \
  content/skillup/**/index.json \
  content/skillup/**/task-statements.json \
  content/skillup/**/questions/*.json \
  content/skillup/**/notes/*.md
```

Regenerate the catalog after any registry change:

```bash
python3 scripts/generate-catalog.py
```

## Publishing process

1. **Create a branch**: `git checkout -b skillup/<exam-or-domain-slug>`
2. **Author content** via the relevant agent (Assessment/Docs/Scenario Engineer), or by hand following the schema in `.claude/skills/exam-registry/SKILL.md`
3. **Update the exam's `index.json`** — question counts, file references, `contentVersion`
4. **Regenerate the catalog**: `python3 scripts/generate-catalog.py`
5. **Validate locally** (command above) — fix any reported errors
6. **Open a PR** — include exam/domain, content summary, and rationale
7. **Review and merge**
8. **Post-merge promotion**: from `ajch_platform`, run `node scripts/sync-vertical-repo.mjs skillup ajeetchouksey/ajch_skillup <sha>` (or dispatch `promote-content.yml`), then merge the resulting `content-manifest.json` update.

## File ownership and scope

- SkillUp content lives in this repo only.
- `ajch_platform` tracks the published version through a manifest pin (`content-manifest.json`) — never edits exam content directly.
- `catalog.json` is generated, never hand-edited.
- Don't bypass validation before merge; don't promote a SHA that hasn't passed CI.

## Related references

- `.claude/agents/curriculum-engineer.md`, `assessment-engineer.md`, `docs-engineer.md`, `scenario-engineer.md`
- `.claude/skills/exam-registry/SKILL.md` — full schema reference
- `.github/workflows/validate-content.yml`
- `scripts/validate-content.mjs`, `scripts/generate-catalog.py`
