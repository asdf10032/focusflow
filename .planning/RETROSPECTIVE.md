# Project Retrospective

*A living document updated after each milestone. Lessons feed forward into future planning.*

## Milestone: v1.0 — MVP

**Shipped:** 2026-04-27
**Phases:** 6 | **Plans:** 9 | **Sessions:** 1

### What Was Built

- Local FastAPI + React MVP for the full task-to-schedule-to-feedback loop.
- Deterministic scheduling engine with three daily plan variants.
- Task, project, energy template, blocked time, schedule, Today, feedback, and parse-task APIs.
- Frontend task, calendar, Today, bilingual UI, reoptimization, validation, and parse flows.
- Repeatable demo data seed, README demo guide, smoke test, and UAT record.

### What Worked

- Keeping the MVP local-first avoided auth/cloud complexity and made demo reliability easier.
- GSD phase boundaries kept backend, scheduler, frontend, usability, and polish work understandable.
- Adding the demo seed late gave the project a repeatable presentation path without changing product scope.

### What Was Inefficient

- Phase 5 summaries were missing until milestone completion, so readiness analysis initially showed 78%.
- No formal milestone audit was run before completion; UAT reduced risk but did not replace a full requirement audit.
- Several unrelated dirty files remained in the worktree, which made staging require extra care.

### Patterns Established

- API responses use `status/data/error/meta` envelopes.
- Schedule persistence is shared through a scheduler service instead of endpoint-local helpers.
- Demo/support tooling must be non-destructive by default.
- Lightweight i18n lives in frontend dictionaries until a larger product need appears.

### Key Lessons

1. Every executed plan should get a SUMMARY before moving to milestone completion.
2. Demo seeds should be added before final README work so docs can be verified against real commands.
3. Keep milestone completion separate from feature implementation to avoid mixing product changes with archive changes.

### Cost Observations

- Model mix: not recorded.
- Sessions: 1 visible completion session after Phase 5 implementation.
- Notable: the final GSD archive required manual curation because automatic accomplishment extraction found no summary metadata fields.

---

## Milestone: v1.3 - Export & Planning Utilities

**Shipped:** 2026-05-01
**Phases:** 3 | **Plans:** 7 | **Sessions:** 1

### What Was Built

- Local export APIs and UI controls for tasks, execution history, and Daily Review data.
- Selected-plan-based partial replan that preserves execution logs and excludes already-feedbacked work.
- Task notes and title/notes search that composes with existing project/status filters.
- Localized empty states for filtered tasks, selected Today plans without items, and no-data exports.
- Repeatable v1.3 demo smoke flow covering seed, search, export, partial replan, Today feedback, and Daily Review.

### What Worked

- Keeping exports read-only avoided risky restore/import behavior while still improving portability.
- Basing partial replan on the selected plan kept the behavior narrow and understandable.
- Adding task notes gave search a useful second field without opening a broader search index.
- UAT caught the user-facing path after automated tests already covered the API and helper behavior.

### What Was Inefficient

- Phase 13 and 14 needed summary backfill during milestone completion before readiness reached 100%.
- No formal v1.3 audit file was created; the milestone relied on verification files plus Phase 15 UAT.
- The worktree still contains unrelated dirty files, so selective staging remains important.

### Patterns Established

- Export endpoints should be read-only and return deterministic filenames, content types, content, and record counts.
- Replan flows should preserve execution history as the source of truth for what already happened.
- Empty-state polish belongs in the same milestone as demo readiness, because it makes local demos easier to trust.

### Key Lessons

1. Every plan should get a matching SUMMARY immediately after execution.
2. Local-first portability can ship safely as export before import.
3. Remaining-work flows should start from the user-selected plan, not the whole task database.

### Cost Observations

- Model mix: not recorded.
- Sessions: 1 visible completion session after Phase 15 implementation and UAT.
- Notable: documentation and planning artifacts needed more manual curation than code verification.

---

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 1 | 6 | Established phase-based MVP delivery with UAT before milestone archival |
| v1.1 | 1 | 4 | Added durable execution insight and milestone audit before archival |
| v1.2 | 1 | 3 | Converted execution history into local duration learning and demo proof |
| v1.3 | 1 | 3 | Added local portability, partial replan, task search, and demo empty-state polish |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 24 relevant pytest checks + frontend build + UAT | Not measured | Local deterministic parse and non-destructive demo seed |
| v1.1 | 39 relevant pytest checks + frontend build + UAT | Not measured | Local deterministic review and explanation APIs |
| v1.2 | 46 relevant pytest checks + frontend build + UAT | Not measured | Local deterministic duration suggestions |
| v1.3 | 62 relevant pytest checks + frontend build + UAT | Not measured | Local exports, partial replan, and task notes/search |

### Top Lessons (Verified Across Milestones)

1. Phase summaries and UAT files are essential planning artifacts, not afterthoughts.
2. Demo-ready local data makes manual verification and presentation much less fragile.
3. Milestone completion is smoother when summaries, verification, and UAT are updated before archival.

---

---

## Milestone: v1.2 - Learning Duration Suggestions

**Shipped:** 2026-04-30
**Phases:** 3 | **Plans:** 6 | **Sessions:** 1

### What Was Built

- Execution log context snapshots for project and cognitive load.
- Deterministic duration suggestion backend using done history with actual minutes.
- Confidence, sample count, source, reason code, and reason text metadata.
- Tasks and Quick Parse UI flows for viewing and accepting suggestions.
- Bilingual Chinese/English suggestion copy and reason labels.
- Repeatable v1.2 demo history and smoke coverage for learned and fallback suggestions.

### What Worked

- Reusing execution history snapshots kept learning deterministic and stable after task edits.
- Keeping suggestions advisory avoided surprising estimate rewrites.
- Demo seed coverage made the learning behavior easy to verify without external services.

### What Was Inefficient

- No formal v1.2 audit file was created before milestone completion; Phase 12 verification and UAT provided the completion evidence.
- Existing unrelated dirty files required careful selective staging.
- Roadmap analysis still reports recent phases as partial because summaries are grouped per phase rather than per plan.

### Patterns Established

- Learning APIs should return explainable metadata, not just a number.
- UI suggestion flows should require explicit accept and preserve manual override.
- Demo data should include both confident-history and sparse-history examples.

### Key Lessons

1. Snapshot fields are the right boundary for local learning features.
2. Suggestion UX is safer when it stays transparent and optional.
3. Future milestones should create a milestone audit before completion when practical.
