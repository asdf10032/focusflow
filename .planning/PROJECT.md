# PROJECT.md

## Current State

- **Shipped versions:** v1.0 MVP on 2026-04-27; v1.1 Execution Insights on 2026-04-30.
- **What this is:** FocusFlow is a local web MVP for turning tasks, energy templates, blocked time, and execution feedback into explainable daily schedules and reviewable execution insight.
- **Core value:** Reduce manual scheduling effort by producing practical daily plans and showing what actually happened after execution.
- **Current focus:** No active milestone; next milestone requirements should be defined fresh.

## Shipped Product Loop

Tasks -> Calendar -> Select Plan -> Today -> Feedback -> Daily Review

The app supports task/project CRUD, default energy templates, blocked time, dependency-aware scheduling, three plan variants, selected-plan persistence, calendar viewing, bilingual UI switching, validate-move, reoptimization, Today execution, durable feedback history, progress metrics, Daily Review, deterministic task parsing, deterministic plan explanations, task filters, repeatable demo seed data, and README demo instructions.

## Validated Requirements

### v1.0 MVP

- ✓ Project CRUD with priority — v1.0
- ✓ Task CRUD with dependencies, deadlines, split settings, and status — v1.0
- ✓ Default weekday/weekend energy templates — v1.0
- ✓ Blocked time configuration — v1.0
- ✓ Three daily schedule variants — v1.0
- ✓ Schedule selection and selected-state retrieval — v1.0
- ✓ Calendar plan display and variant switching — v1.0
- ✓ Bilingual Chinese/English UI toggle — v1.0
- ✓ Validate-move conflict detection — v1.0
- ✓ Same-day reoptimization — v1.0
- ✓ Today execution flow and status feedback — v1.0
- ✓ Local deterministic task parsing — v1.0
- ✓ Repeatable non-destructive demo data and smoke coverage — v1.0

### v1.1 Execution Insights

- ✓ Durable execution feedback history — v1.1
- ✓ Feedback status, actual duration, and optional notes — v1.1
- ✓ Date-filtered execution history — v1.1
- ✓ Today progress metrics and refresh-after-feedback behavior — v1.1
- ✓ Estimated-vs-actual duration tracking — v1.1
- ✓ Daily Review page and API — v1.1
- ✓ Deterministic schedule summaries, risk explanations, and unplaced reasons — v1.1
- ✓ Task status and project filters — v1.1
- ✓ Repeatable v1.1 demo history and smoke coverage — v1.1

## Active Requirements

- None. Run `$gsd-new-milestone` to define the next milestone.

## Future Candidates

- Learning-based duration suggestions from execution history.
- Export tasks, history, and review summaries as JSON/CSV.
- Weekly planning and partial replan.
- Richer task search and filtering.
- Better onboarding and empty states.

## Out Of Scope

- Login, multi-user support, and cloud sync.
- Third-party calendar/task integrations.
- External LLM dependency for task parsing or explanations.
- Desktop packaging.

## Architecture

- Frontend: React, TypeScript, Vite, Router, Zustand, Tailwind.
- Backend: FastAPI, SQLAlchemy, Pydantic v2, SQLite, Alembic.
- Scheduling: backend service layer with deterministic slot generation, dependency validation, scoring, placement, persistence, selected-plan state, and deterministic explanations.
- Execution insights: execution logs store task snapshots, status, actual minutes, notes, and date-based review data.
- Demo tooling: local seed services for energy templates, tasks, schedule plans, selected balanced plan, and repeatable execution history.

## Key Decisions

| Decision | Outcome |
|----------|---------|
| Keep V1.0 local-first with SQLite | ✓ Good for fast demo and simple setup |
| Use unified `status/data/error/meta` envelopes | ✓ Good for consistent API/client handling |
| Persist generated schedule plans before selection | ✓ Good for Today execution flow |
| Implement bilingual UI with lightweight local dictionaries | ✓ Good enough for MVP without i18n framework overhead |
| Keep AI parse local and deterministic | ✓ Good for no-network demo reliability |
| Add durable execution logs in v1.1 | ✓ Good foundation for review and future learning |
| Snapshot task title and estimated minutes in history | ✓ Preserves historical truth after task edits |
| Keep plan explanations deterministic | ✓ Matches local-first/no-network constraint |
| Add non-destructive demo seed instead of reset-by-default | ✓ Good for protecting local user data |

## Known Gaps And Tech Debt

- No learning-based scheduler yet.
- No export workflow yet.
- No weekly planning or partial replan yet.
- Phase audit noted artifact naming drift: recent phases use `VALIDATION` plus summaries/UAT rather than per-phase `VERIFICATION.md`.

## Archives

- v1.0 roadmap: `.planning/milestones/v1.0-ROADMAP.md`
- v1.0 requirements: `.planning/milestones/v1.0-REQUIREMENTS.md`
- v1.1 roadmap: `.planning/milestones/v1.1-ROADMAP.md`
- v1.1 requirements: `.planning/milestones/v1.1-REQUIREMENTS.md`
- v1.1 audit: `.planning/v1.1-MILESTONE-AUDIT.md`

---

*Last updated: 2026-04-30 after v1.1 milestone*
