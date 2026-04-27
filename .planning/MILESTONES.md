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

