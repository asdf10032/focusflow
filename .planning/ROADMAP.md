# Roadmap: FocusFlow Intelligent Energy Scheduler

## Milestones

- **v1.0 MVP** - Shipped 2026-04-27. Archive: [v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md)
- **v1.1 Execution Insights** - Shipped 2026-04-30. Archive: [v1.1-ROADMAP.md](milestones/v1.1-ROADMAP.md)
- **v1.2 Learning Duration Suggestions** - Shipped 2026-04-30. Archive: [v1.2-ROADMAP.md](milestones/v1.2-ROADMAP.md)
- **v1.3 Export & Planning Utilities** - Active.

## Completed

<details>
<summary>v1.0 MVP (Phases 1-5) - SHIPPED 2026-04-27</summary>

- [x] Phase 1: Foundation - backend/API/database foundation
- [x] Phase 2: Scheduling MVP - deterministic daily plans and persistence
- [x] Phase 3: Frontend Main Flow - Tasks and Calendar workflow
- [x] Phase 03.1: Bilingual UI Toggle - Chinese/English UI switching
- [x] Phase 4: Usability Enhancements - validate move, reoptimize, Today, deterministic parse
- [x] Phase 5: Demo Polish - repeatable demo seed, README, smoke coverage

</details>

<details>
<summary>v1.1 Execution Insights (Phases 6-9) - SHIPPED 2026-04-30</summary>

- [x] Phase 6: Execution History Foundation - durable feedback history and date-filtered history API
- [x] Phase 7: Today Progress and Daily Review - progress metrics, estimate variance, Daily Review UI/API
- [x] Phase 8: Explanations and Filtering - deterministic plan/risk explanations and task filters
- [x] Phase 9: Execution Insights Demo Polish - seeded review history, v1.1 smoke coverage, README demo path

</details>

<details>
<summary>v1.2 Learning Duration Suggestions (Phases 10-12) - SHIPPED 2026-04-30</summary>

- [x] Phase 10: Duration Suggestion Backend - deterministic suggestion service/API from execution history snapshots
- [x] Phase 11: Task Suggestion UX - task and parse flows with accept/manual override behavior and bilingual copy
- [x] Phase 12: Learning Demo Polish - seeded history, smoke coverage, README demo path, and UAT

</details>

## Active Milestone: v1.3 Export & Planning Utilities

**Goal:** Make FocusFlow easier to use with real data by adding local exports, remaining-work replanning, task search, and clearer empty states.

| Phase | Name | Goal | Requirements | Status |
|-------|------|------|--------------|--------|
| 13 | Export Data Utilities | Add local JSON/CSV exports and UI entry points for tasks, history, and review data. | EXP-01, EXP-02, EXP-03, EXP-04, NFR-01 | Complete |
| 14 | Partial Replan | Add remaining-work replan behavior that preserves completed feedback/history. | PLAN-01, PLAN-02, PLAN-03, PLAN-04, NFR-02 | Planned |
| 15 | Search And Demo Polish | Add task search, empty states, final i18n/tests/docs, and v1.3 smoke coverage. | SRCH-01, SRCH-02, ONBD-01, NFR-03, NFR-04 | Planned |

## Phase Details

### Phase 13: Export Data Utilities

**Goal:** Make core FocusFlow data portable through local export APIs and UI controls.

**Requirements:** EXP-01, EXP-02, EXP-03, EXP-04, NFR-01

**Success criteria:**
1. Export endpoints return tasks, execution history, and review summaries in deterministic JSON/CSV formats.
2. History and review exports support date or date-range filtering.
3. Frontend exposes localized export controls with clear filenames and error states.
4. Backend export tests and frontend i18n/helper checks cover the new behavior.

**Status:** Complete on 2026-05-01.

### Phase 14: Partial Replan

**Goal:** Let users regenerate the rest of a day while preserving already completed execution evidence.

**Requirements:** PLAN-01, PLAN-02, PLAN-03, PLAN-04, NFR-02

**Success criteria:**
1. Partial replan excludes work that already has completed, skipped, canceled, or same-day feedback state.
2. Partial replan returns selectable generated plans without deleting existing execution logs.
3. Calendar flow can show and select newly generated remaining-work plans.
4. Empty/error states clearly explain no selected plan, no remaining work, or no schedulable time.

**Status:** Planned.

### Phase 15: Search And Demo Polish

**Goal:** Polish the v1.3 user path with task search, empty states, documentation, and repeatable smoke coverage.

**Requirements:** SRCH-01, SRCH-02, ONBD-01, NFR-03, NFR-04

**Success criteria:**
1. Task search matches title and notes and composes with existing project/status filters.
2. Empty states guide users on Tasks, Calendar, Today, Daily Review, and export surfaces.
3. README documents the v1.3 demo path and verification commands.
4. Smoke coverage verifies seed -> export -> partial replan -> selected plan -> review loop.
5. Frontend i18n/helper tests, backend focused tests, compile checks, and frontend build pass.

**Status:** Planned.

## Traceability Summary

| Requirement | Phase | Status |
|-------------|-------|--------|
| EXP-01 | Phase 13 | Complete |
| EXP-02 | Phase 13 | Complete |
| EXP-03 | Phase 13 | Complete |
| EXP-04 | Phase 13 | Complete |
| PLAN-01 | Phase 14 | Pending |
| PLAN-02 | Phase 14 | Pending |
| PLAN-03 | Phase 14 | Pending |
| PLAN-04 | Phase 14 | Pending |
| SRCH-01 | Phase 15 | Pending |
| SRCH-02 | Phase 15 | Pending |
| ONBD-01 | Phase 15 | Pending |
| NFR-01 | Phase 13 | Complete |
| NFR-02 | Phase 14 | Pending |
| NFR-03 | Phase 15 | Pending |
| NFR-04 | Phase 15 | Pending |

**Coverage:**
- v1.3 requirements: 15 total
- Mapped to phases: 15
- Unmapped: 0

## Next Up

```bash
$gsd-plan-phase 14 --skip-research
```
