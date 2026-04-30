# Milestones

## v1.0 MVP (Shipped: 2026-04-27)

**Phases completed:** 6 phases, 9 plans

**Scope:** local web MVP for the complete scheduling loop.

**Key accomplishments:**
- Built the FastAPI/SQLite foundation with unified response envelopes, CRUD APIs, Alembic, and default energy seeds.
- Implemented dependency-aware daily scheduling with conservative, balanced, and aggressive plans.
- Delivered the main frontend flow for tasks, calendar plan viewing, plan switching, and plan selection.
- Added Chinese/English UI switching.
- Added usability APIs and UI flows for validate-move, reoptimization, Today execution, feedback, and deterministic task parsing.
- Added repeatable non-destructive demo data, README startup/demo instructions, and a full demo-flow smoke test.

**Validation:**
- Phase 5 UAT: 4 passed, 0 issues.
- Backend pytest verification: 24 relevant tests passed.
- `python -m compileall backend alembic` passed.
- `npm.cmd run build` passed.

**Known gaps accepted:**
- No formal `v1.0-MILESTONE-AUDIT.md` was created; user approved proceeding after UAT.
- Feedback history, advanced AI parsing, exports, and richer analytics are deferred to later milestones.

**Archives:**
- Roadmap: `.planning/milestones/v1.0-ROADMAP.md`
- Requirements: `.planning/milestones/v1.0-REQUIREMENTS.md`

---

## v1.1 Execution Insights (Shipped: 2026-04-30)

**Phases completed:** 4 phases, 7 plans

**Scope:** durable execution history and reviewable daily execution insights on top of the v1.0 scheduling loop.

**Key accomplishments:**
- Added execution logs with snapshot fields and date-filtered history APIs.
- Added Today progress metrics and a Daily Review page/API with actual duration and estimate variance.
- Added deterministic plan summaries, risk explanations, unplaced task reason text, and task status/project filters.
- Added repeatable v1.1 demo seed data with reviewable execution history.
- Expanded smoke coverage and README instructions for the full v1.1 demo path.

**Validation:**
- Milestone audit: passed, 21/21 requirements satisfied.
- Phase 9 UAT: 4 passed, 0 issues.
- Backend/frontend verification: 39 relevant tests passed.
- `python -m compileall backend alembic` passed.
- `npm.cmd run build` passed.

**Known gaps accepted:**
- Learning-based duration suggestions, export, weekly planning, and partial replan remain future work.
- Phase artifacts use `VALIDATION` plus summaries/UAT rather than per-phase `VERIFICATION.md`; audit evidence is recorded in `.planning/v1.1-MILESTONE-AUDIT.md`.

**Archives:**
- Roadmap: `.planning/milestones/v1.1-ROADMAP.md`
- Requirements: `.planning/milestones/v1.1-REQUIREMENTS.md`
- Audit: `.planning/v1.1-MILESTONE-AUDIT.md`

---

## v1.2 Learning Duration Suggestions (Shipped: 2026-04-30)

**Phases completed:** 3 phases, 6 plans

**Scope:** local, deterministic, explainable duration suggestions based on durable execution history snapshots.

**Key accomplishments:**
- Added execution log context snapshots for project and cognitive load.
- Added a deterministic duration suggestion API using completed execution history with actual durations.
- Added confidence, sample count, source, reason code, and fallback metadata for suggestions.
- Surfaced suggestions in Tasks and Quick Parse flows with explicit accept and manual override behavior.
- Added bilingual UI copy for suggestion controls, metadata, states, and reason codes.
- Expanded repeatable demo seed data and smoke coverage to show both learned and fallback suggestions.
- Updated README demo instructions for the v1.2 learning loop.

**Validation:**
- Phase 12 UAT: 6 passed, 0 issues.
- Focused demo and suggestion tests: 7 passed.
- v1.0-v1.2 regression suite: 46 passed.
- `python -m compileall backend alembic` passed.
- `npm.cmd run build` passed.

**Known gaps accepted:**
- Suggestions are advisory only and do not automatically rewrite estimates.
- Scheduler scoring does not yet adapt from learned duration history.
- Browser sanity remains optional after starting local services.

**Archives:**
- Roadmap: `.planning/milestones/v1.2-ROADMAP.md`
- Requirements: `.planning/milestones/v1.2-REQUIREMENTS.md`

---
