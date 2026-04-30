# PROJECT.md

## Current State

- **Shipped versions:** v1.0 MVP on 2026-04-27; v1.1 Execution Insights on 2026-04-30; v1.2 Learning Duration Suggestions on 2026-04-30.
- **What this is:** FocusFlow is a local web MVP for turning tasks, energy templates, blocked time, and execution feedback into explainable daily schedules and reviewable execution insight.
- **Core value:** Reduce manual scheduling effort by producing practical daily plans and showing what actually happened after execution.
- **Current focus:** Ready to choose the next milestone.

## Last Completed Milestone: v1.2 Learning Duration Suggestions

**Goal:** Use durable execution history to suggest better task duration estimates while keeping the workflow local, deterministic, explainable, and manually overridable.

**Shipped features:**
- Backend duration suggestion service and API based on execution history snapshots.
- Task creation/editing and parse-task flows can surface suggested minutes with confidence and explanation.
- Demo seed, tests, and README updates show how execution history improves future estimates.

## Shipped Product Loop

Tasks -> Calendar -> Select Plan -> Today -> Feedback -> Daily Review

The app supports task/project CRUD, default energy templates, blocked time, dependency-aware scheduling, three plan variants, selected-plan persistence, calendar viewing, bilingual UI switching, validate-move, reoptimization, Today execution, durable feedback history, progress metrics, Daily Review, deterministic task parsing, deterministic plan explanations, task filters, repeatable demo seed data, and README demo instructions.

## Validated Requirements

### v1.0 MVP

- Project CRUD with priority - v1.0
- Task CRUD with dependencies, deadlines, split settings, and status - v1.0
- Default weekday/weekend energy templates - v1.0
- Blocked time configuration - v1.0
- Three daily schedule variants - v1.0
- Schedule selection and selected-state retrieval - v1.0
- Calendar plan display and variant switching - v1.0
- Bilingual Chinese/English UI toggle - v1.0
- Validate-move conflict detection - v1.0
- Same-day reoptimization - v1.0
- Today execution flow and status feedback - v1.0
- Local deterministic task parsing - v1.0
- Repeatable non-destructive demo data and smoke coverage - v1.0

### v1.1 Execution Insights

- Durable execution feedback history - v1.1
- Feedback status, actual duration, and optional notes - v1.1
- Date-filtered execution history - v1.1
- Today progress metrics and refresh-after-feedback behavior - v1.1
- Estimated-vs-actual duration tracking - v1.1
- Daily Review page and API - v1.1
- Deterministic schedule summaries, risk explanations, and unplaced reasons - v1.1
- Task status and project filters - v1.1
- Repeatable v1.1 demo history and smoke coverage - v1.1

### v1.2 Learning Duration Suggestions

- Duration suggestions from execution history - v1.2
- Suggestion confidence, sample count, source, and reason text - v1.2
- Manual accept/override behavior in task workflows - v1.2
- Parse-task integration with duration suggestions - v1.2
- Repeatable demo and verification for learned estimates - v1.2

## Active Requirements

- None. Run `$gsd-new-milestone` to define the next cycle.

## Future Candidates

- Export tasks, history, and review summaries as JSON/CSV.
- Weekly planning and partial replan.
- Richer task search and filtering.
- Better onboarding and empty states.
- Adaptive priority or schedule scoring beyond duration estimation.

## Out Of Scope

- Login, multi-user support, and cloud sync.
- Third-party calendar/task integrations.
- External LLM dependency for task parsing, explanations, or duration suggestions.
- Automatically rewriting existing task estimates without explicit user action.
- Desktop packaging.

## Architecture

- Frontend: React, TypeScript, Vite, Router, Zustand, Tailwind.
- Backend: FastAPI, SQLAlchemy, Pydantic v2, SQLite, Alembic.
- Scheduling: backend service layer with deterministic slot generation, dependency validation, scoring, placement, persistence, selected-plan state, and deterministic explanations.
- Execution insights: execution logs store task snapshots, status, actual minutes, notes, and date-based review data.
- Duration learning: local deterministic suggestions derive from execution history snapshots and expose explanation metadata rather than calling an external model.
- Demo tooling: local seed services for energy templates, tasks, schedule plans, selected balanced plan, repeatable execution history, and v1.2 suggestion examples.

## Key Decisions

| Decision | Outcome |
|----------|---------|
| Keep V1.0 local-first with SQLite | Good for fast demo and simple setup |
| Use unified `status/data/error/meta` envelopes | Good for consistent API/client handling |
| Persist generated schedule plans before selection | Good for Today execution flow |
| Implement bilingual UI with lightweight local dictionaries | Good enough for MVP without i18n framework overhead |
| Keep AI parse local and deterministic | Good for no-network demo reliability |
| Add durable execution logs in v1.1 | Good foundation for review and future learning |
| Snapshot task title and estimated minutes in history | Preserves historical truth after task edits |
| Keep plan explanations deterministic | Matches local-first/no-network constraint |
| Add non-destructive demo seed instead of reset-by-default | Good for protecting local user data |
| Scope v1.2 learning to duration suggestions | Keeps learning useful, testable, and explainable before changing schedule scoring |

## Known Gaps And Tech Debt

- No export workflow yet.
- No weekly planning or partial replan yet.
- No adaptive scheduler scoring beyond duration suggestions yet.
- Phase audit noted artifact naming drift: recent phases use `VALIDATION` plus summaries/UAT rather than per-phase `VERIFICATION.md`.

## Archives

- v1.0 roadmap: `.planning/milestones/v1.0-ROADMAP.md`
- v1.0 requirements: `.planning/milestones/v1.0-REQUIREMENTS.md`
- v1.1 roadmap: `.planning/milestones/v1.1-ROADMAP.md`
- v1.1 requirements: `.planning/milestones/v1.1-REQUIREMENTS.md`
- v1.1 audit: `.planning/v1.1-MILESTONE-AUDIT.md`
- v1.2 roadmap: `.planning/milestones/v1.2-ROADMAP.md`
- v1.2 requirements: `.planning/milestones/v1.2-REQUIREMENTS.md`

---

*Last updated: 2026-04-30 after archiving v1.2 milestone*
