# Roadmap: FocusFlow Intelligent Energy Scheduler

## Milestones

- ✅ **v1.0 MVP** — Phases 1-5 shipped on 2026-04-27. Full archive: [v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md)
- 🚧 **v1.1 Execution Insights** — Phases 6-9 planned.

## Completed

<details>
<summary>✅ v1.0 MVP (Phases 1-5) — SHIPPED 2026-04-27</summary>

- [x] Phase 1: Foundation — 1/1 plan complete on 2026-04-26
- [x] Phase 2: Scheduling MVP — 2/2 plans complete on 2026-04-26
- [x] Phase 3: Frontend Main Flow — 1/1 plan complete on 2026-04-26
- [x] Phase 03.1: Bilingual UI Toggle (INSERTED) — 1/1 plan complete on 2026-04-26
- [x] Phase 4: Usability Enhancements — 2/2 plans complete on 2026-04-26
- [x] Phase 5: Demo Polish — 2/2 plans complete on 2026-04-27

</details>

## Active Milestone: v1.1 Execution Insights

V1.1 turns the MVP feedback loop into durable execution insight: history records, progress metrics, daily review, plan explanations, filters, and demo verification.

- [x] **Phase 6: Execution History Foundation** - Persist feedback history and expose date-based history APIs.
- [x] **Phase 7: Today Progress and Daily Review** - Add progress metrics, estimate variance, and daily review UI/API.
- [ ] **Phase 8: Explanations and Filtering** - Add plan/risk explanations and task/history filters.
- [ ] **Phase 9: Execution Insights Demo Polish** - Seed reviewable history, document the v1.1 demo path, and add smoke coverage.

## Phase Details

### Phase 6: Execution History Foundation

**Goal**: Feedback becomes durable execution history instead of status-only updates.
**Depends on**: v1.0
**Requirements**: [HIST-01, HIST-02, HIST-03, EST-03, NFR-01]
**Success Criteria**:
  1. Feedback submission creates an execution history record.
  2. History records store status, actual duration, optional note, task id, date, and estimated duration snapshot.
  3. History can be queried by date.
  4. Existing success envelope remains unchanged.
**Plans**: 2 plans

Plans:
- [x] 06-01: Add execution history model, schema, migration, and persistence
- [x] 06-02: Update feedback/history APIs and backend tests

### Phase 7: Today Progress and Daily Review

**Goal**: Users can see what happened today and review a selected day.
**Depends on**: Phase 6
**Requirements**: [PROG-01, PROG-02, PROG-03, EST-01, EST-02, REV-01, REV-02, FILT-03]
**Success Criteria**:
  1. Today shows planned count, completed count, skipped/incomplete count, and completion rate.
  2. Metrics refresh after feedback submission.
  3. Empty selected-plan state remains clear.
  4. Daily review shows work outcomes, planned duration, actual duration, and estimate variance for a selected date.
**Plans**: 2 plans

Plans:
- [x] 07-01: Add progress/review backend aggregation APIs
- [x] 07-02: Add Today metrics and Daily Review frontend flow

### Phase 8: Explanations and Filtering

**Goal**: Schedules and growing task/history data become easier to understand and navigate.
**Depends on**: Phase 7
**Requirements**: [EXPL-01, EXPL-02, EXPL-03, FILT-01, FILT-02, NFR-03]
**Success Criteria**:
  1. Generated schedules include user-readable plan summaries.
  2. Risks and unplaced tasks include clearer reason text.
  3. Calendar or Today displays summaries and explanations.
  4. Task list supports status and project filters.
  5. No external AI, login, cloud sync, or third-party calendar integration is introduced.
**Plans**: 2 plans

Plans:
- [ ] 08-01: Add deterministic schedule explanation fields and tests
- [ ] 08-02: Add frontend explanations and task filters

### Phase 9: Execution Insights Demo Polish

**Goal**: V1.1 is easy to verify and demo end to end.
**Depends on**: Phase 8
**Requirements**: [REV-03, NFR-02]
**Success Criteria**:
  1. Demo seed can create reviewable execution history.
  2. Smoke test covers feedback history, Today metrics, daily review, explanations, and filters.
  3. README documents the v1.1 demo path.
  4. Backend tests, frontend helper/i18n tests, compileall, and frontend build pass.
**Plans**: 1 plan

Plans:
- [ ] 09-01: Add v1.1 demo data, docs, smoke tests, and final verification

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|----------------|--------|-----------|
| 1. Foundation | v1.0 | 1/1 | Complete | 2026-04-26 |
| 2. Scheduling MVP | v1.0 | 2/2 | Complete | 2026-04-26 |
| 3. Frontend Main Flow | v1.0 | 1/1 | Complete | 2026-04-26 |
| 03.1 Bilingual UI Toggle | v1.0 | 1/1 | Complete | 2026-04-26 |
| 4. Usability Enhancements | v1.0 | 2/2 | Complete | 2026-04-26 |
| 5. Demo Polish | v1.0 | 2/2 | Complete | 2026-04-27 |
| 6. Execution History Foundation | v1.1 | 2/2 | Complete | 2026-04-28 |
| 7. Today Progress and Daily Review | v1.1 | 2/2 | Complete | 2026-04-28 |
| 8. Explanations and Filtering | v1.1 | 0/2 | Not started | - |
| 9. Execution Insights Demo Polish | v1.1 | 0/1 | Not started | - |
