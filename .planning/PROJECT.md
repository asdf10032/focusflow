# PROJECT.md

## Current State

- **Shipped version:** v1.0 MVP on 2026-04-27.
- **What this is:** FocusFlow is a local web MVP for turning tasks, energy templates, and blocked time into executable daily schedules.
- **Core value:** Reduce manual scheduling effort by producing three practical, explainable daily plans that account for time constraints and cognitive load.
- **Current focus:** V1.1 Execution Insights is being defined.

## Current Milestone: v1.1 Execution Insights

**Goal:** Turn FocusFlow from a one-day scheduling demo into a tool that records execution history, shows completion/estimation patterns, and helps users understand what happened after following a plan.

**Target features:**
- Execution feedback history instead of status-only feedback.
- Today progress and completion metrics.
- Estimated-vs-actual duration tracking.
- Daily review page with completed, missed, skipped, and delayed work.
- Human-readable schedule risk and plan rationale.
- Basic task filtering so growing history remains usable.

## Shipped V1.0 Loop

Tasks -> Calendar -> Select Plan -> Today -> Feedback

The MVP supports task/project CRUD, default energy templates, blocked time, dependency-aware scheduling, three plan variants, selected-plan persistence, calendar viewing, bilingual UI switching, validate-move, reoptimization, Today execution, task feedback, deterministic task parsing, repeatable demo seed data, and README demo instructions.

## Validated Requirements

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

## Active Requirements

- [ ] V1.1 captures execution feedback as historical records.
- [ ] V1.1 summarizes daily progress and completion outcomes.
- [ ] V1.1 compares estimated and actual task duration.
- [ ] V1.1 explains schedule risk and plan tradeoffs in user-facing language.
- [ ] V1.1 adds basic filtering for task/history-heavy workflows.

## Out Of Scope

- Login, multi-user support, and cloud sync.
- Third-party calendar/task integrations.
- Learning-based scheduling and advanced optimization algorithms.
- Desktop packaging.
- External LLM dependency for task parsing.

## Architecture

- Frontend: React, TypeScript, Vite, Router, Zustand, Tailwind.
- Backend: FastAPI, SQLAlchemy, Pydantic v2, SQLite, Alembic.
- Scheduling: backend service layer with deterministic slot generation, dependency validation, scoring, placement, persistence, and selected-plan state.
- Demo tooling: local seed services for energy templates and repeatable demo data.

## Key Decisions

| Decision | Outcome |
|----------|---------|
| Keep V1.0 local-first with SQLite | ✓ Good for fast demo and simple setup |
| Use unified `status/data/error/meta` envelopes | ✓ Good for consistent API/client handling |
| Persist generated schedule plans before selection | ✓ Good for Today execution flow |
| Implement bilingual UI with lightweight local dictionaries | ✓ Good enough for MVP without i18n framework overhead |
| Keep AI parse local and deterministic | ✓ Good for no-network demo reliability |
| Treat feedback as task status updates in v1.0 | ✓ Good MVP tradeoff; history can be v1.1+ |
| Add non-destructive demo seed instead of reset-by-default | ✓ Good for protecting local user data |

## Known Gaps And Tech Debt

- No formal `v1.0-MILESTONE-AUDIT.md` was produced before completion; Phase 5 UAT passed 4/4 and the user approved proceeding.
- Execution feedback has no history table yet.
- Task parsing is heuristic, not a real AI integration.
- Advanced task filtering, history views, export, weekly planning, and learning-based optimization remain future work.

## Next Milestone Candidates

- Better onboarding and empty states.
- Search/filter and richer task management.
- Execution history and completion analytics.
- Risk explanation text and schedule rationale.
- JSON/CSV export.
- Weekly planning or partial replan.

---

*Last updated: 2026-04-28 after starting v1.1 milestone*
