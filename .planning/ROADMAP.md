# Roadmap: FocusFlow Intelligent Energy Scheduler

## Overview

V1.0 delivers a local web MVP for turning tasks, energy templates, and blocked time into executable daily schedules. The roadmap keeps the scope tight: first stabilize the foundation, then complete the scheduling loop, then wire the user-facing flow.

## Phases

**Phase Numbering:**
- Integer phases (1, 2, 3): Planned milestone work
- Decimal phases (2.1, 2.2): Urgent insertions

- [x] **Phase 1: Foundation** - FastAPI, database, CRUD, seeds, frontend shell, and verification baseline
- [x] **Phase 2: Scheduling MVP** - Slot generation, dependency checks, scoring, placement, and selectable three-plan output
- [x] **Phase 3: Frontend Main Flow** - Task creation/editing, calendar display, plan switching, and plan selection
- [x] **Phase 03.1: Bilingual UI Toggle (INSERTED)** - Add Chinese/English UI language switching before Phase 4 expands the frontend
- [x] **Phase 4: Usability Enhancements** - Validate move, reoptimize, execution feedback, and AI task parse shell
- [x] **Phase 5: Demo Polish** - Demo data, docs, smoke tests, and presentation-ready flow

## Phase Details

### Phase 1: Foundation
**Goal**: Backend and frontend foundations are runnable, tested, and consistent with the Phase 1 API contract.
**Depends on**: Nothing (first phase)
**Requirements**: [REQ-PROJ-CRUD, REQ-TASK-CRUD, REQ-ENERGY, REQ-BLOCKED, REQ-DEFAULT-SEEDS, NFR-API, NFR-VALIDATION]
**Success Criteria** (what must be TRUE):
  1. Backend app imports and health returns a success envelope.
  2. Projects, tasks, energy templates, and blocked times use the unified response envelope.
  3. Alembic reports the initial migration at head.
  4. Default energy templates can be seeded with 48 slots for weekday/weekend variants.
  5. Frontend production build succeeds.
**Plans**: 1 plan

Plans:
- [x] 01-01: Stabilize Phase 1 API contract and verification baseline

### Phase 2: Scheduling MVP
**Goal**: Users can request three daily schedule variants from real task, energy, and blocked-time data.
**Depends on**: Phase 1
**Requirements**: [REQ-SCHEDULE-3PLANS, REQ-SCHEDULE-SELECT, NFR-TEST]
**Success Criteria** (what must be TRUE):
  1. Generate returns conservative, balanced, and aggressive plans.
  2. Plans respect blocked slots and task duration.
  3. Unplaced tasks are reported explicitly.
  4. Selecting a plan persists selected state for later frontend reads.
**Plans**: 2 plans

Plans:
- [x] 02-01: Persist generated plans and selected state
- [x] 02-02: Add dependency validation, scoring checks, and risk/unplaced coverage

### Phase 3: Frontend Main Flow
**Goal**: Users can manage tasks and view/select generated plans through the web UI.
**Depends on**: Phase 2
**Requirements**: [REQ-CALENDAR-VIEW, REQ-TASK-CRUD, REQ-SCHEDULE-SELECT]
**Success Criteria** (what must be TRUE):
  1. Task list supports create, edit, delete, and status visibility.
  2. Calendar page renders generated plan items.
  3. User can switch among three plan variants.
  4. User can select a plan from the frontend.
**Plans**: 1 plan

Plans:
- [x] 03-01: Implement task management and calendar plan selection UI

### Phase 03.1: Bilingual UI Toggle (INSERTED)

**Goal:** Users can switch the web UI between Chinese and English without changing backend behavior.
**Requirements**: [NFR-UX]
**Depends on:** Phase 3
**Plans:** 1 plan

Plans:
- [x] 03.1-01: Add lightweight Chinese/English UI toggle

### Phase 4: Usability Enhancements
**Goal**: The MVP becomes usable for live demos through feedback, conflict handling, and AI-assisted input shells.
**Depends on**: Phase 03.1
**Requirements**: [REQ-SCHEDULE-VALIDATE, REQ-SCHEDULE-REOPT, REQ-EXECUTION, REQ-AI-PARSE]
**Success Criteria** (what must be TRUE):
  1. Validate-move reports conflicts clearly.
  2. Reoptimize can regenerate plans after changes.
  3. Today execution flow can display selected work and submit feedback.
  4. AI parse endpoint returns structured task draft data.
**Plans**: 2 plans

Plans:
- [x] 04-01: Backend usability APIs
- [x] 04-02: Frontend usability flows

### Phase 5: Demo Polish
**Goal**: The project is ready for a local demo or review session.
**Depends on**: Phase 4
**Requirements**: [NFR-TEST, NFR-UX]
**Success Criteria** (what must be TRUE):
  1. Demo data can be loaded repeatably.
  2. README startup and smoke-test instructions are accurate.
  3. Core backend tests and frontend build pass from clean commands.
  4. Demo path is documented end to end.
**Plans**: 2 plans

Plans:
- [x] 05-01: Demo data and smoke test
- [x] 05-02: README and final verification

## Progress

**Execution Order:**
Phases execute in numeric order: 1 -> 2 -> 3 -> 03.1 -> 4 -> 5

| Phase | Plans Complete | Status | Completed |
|-------|----------------|--------|-----------|
| 1. Foundation | 1/1 | Complete | 2026-04-26 |
| 2. Scheduling MVP | 2/2 | Complete | 2026-04-26 |
| 3. Frontend Main Flow | 1/1 | Complete | 2026-04-26 |
| 03.1 Bilingual UI Toggle | 1/1 | Complete | 2026-04-26 |
| 4. Usability Enhancements | 2/2 | Complete | 2026-04-26 |
| 5. Demo Polish | 2/2 | Complete | 2026-04-27 |
