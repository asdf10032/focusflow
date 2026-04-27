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

## Cross-Milestone Trends

### Process Evolution

| Milestone | Sessions | Phases | Key Change |
|-----------|----------|--------|------------|
| v1.0 | 1 | 6 | Established phase-based MVP delivery with UAT before milestone archival |

### Cumulative Quality

| Milestone | Tests | Coverage | Zero-Dep Additions |
|-----------|-------|----------|-------------------|
| v1.0 | 24 relevant pytest checks + frontend build + UAT | Not measured | Local deterministic parse and non-destructive demo seed |

### Top Lessons (Verified Across Milestones)

1. Phase summaries and UAT files are essential planning artifacts, not afterthoughts.
2. Demo-ready local data makes manual verification and presentation much less fragile.

