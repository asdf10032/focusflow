# Roadmap: FocusFlow Intelligent Energy Scheduler

## Milestones

- **v1.0 MVP** - Shipped 2026-04-27. Archive: [v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md)
- **v1.1 Execution Insights** - Shipped 2026-04-30. Archive: [v1.1-ROADMAP.md](milestones/v1.1-ROADMAP.md)
- **v1.2 Learning Duration Suggestions** - Active.

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

## Active Milestone: v1.2 Learning Duration Suggestions

**Goal:** Turn v1.1 execution history into practical duration suggestions that help users estimate new tasks more accurately while keeping the product local, deterministic, explainable, and manually overridable.

| Phase | Name | Goal | Requirements | Status |
|-------|------|------|--------------|--------|
| 10 | Duration Suggestion Backend | Add deterministic suggestion service/API from execution history snapshots. | DSUG-01, DSUG-02, LERN-01, LERN-02, NFR-01 | Complete |
| 11 | Task Suggestion UX | Surface suggestions in task and parse flows with accept/manual override behavior and bilingual copy. | DSUG-03, DSUG-04, UX-01 | Complete |
| 12 | Learning Demo Polish | Seed demonstrable history, document the v1.2 path, and verify the full loop. | LERN-03, NFR-02 | Planned |

## Phase Details

### Phase 10: Duration Suggestion Backend

**Goal:** Add the backend foundation for local duration suggestions.

**Requirements:** DSUG-01, DSUG-02, LERN-01, LERN-02, NFR-01

**Success criteria:**
1. API can return suggested minutes, confidence, sample count, and reason text for a task-like draft.
2. Suggestion logic uses execution log snapshots and does not depend on later task edits.
3. Fallback responses are deterministic and useful when history is sparse.
4. Backend tests cover confident match, fallback, snapshot stability, and response envelope behavior.

**Status:** Complete on 2026-04-30.

### Phase 11: Task Suggestion UX

**Goal:** Make duration suggestions usable inside the existing Tasks workflows.

**Requirements:** DSUG-03, DSUG-04, UX-01

**Success criteria:**
1. Tasks page can request and display a duration suggestion without overwriting the user's estimate automatically.
2. User can accept a suggestion into the estimate field and still edit it manually.
3. Parse-task flow can surface suggestion metadata alongside the draft.
4. Chinese and English UI strings cover all new suggestion states.

**Status:** Complete on 2026-04-30.

### Phase 12: Learning Demo Polish

**Goal:** Make v1.2 repeatable to test and demo locally.

**Requirements:** LERN-03, NFR-02

**Success criteria:**
1. Demo seed data creates enough execution history to demonstrate confident and fallback suggestions.
2. Smoke tests cover seed -> suggestion -> accept/use flow at the API or helper level.
3. README documents the v1.2 demo path and verification commands.
4. Backend tests, compile checks, and frontend build remain clean.

## Traceability Summary

| Requirement | Phase | Status |
|-------------|-------|--------|
| DSUG-01 | Phase 10 | Complete |
| DSUG-02 | Phase 10 | Complete |
| DSUG-03 | Phase 11 | Complete |
| DSUG-04 | Phase 11 | Complete |
| LERN-01 | Phase 10 | Complete |
| LERN-02 | Phase 10 | Complete |
| LERN-03 | Phase 12 | Pending |
| UX-01 | Phase 11 | Complete |
| NFR-01 | Phase 10 | Complete |
| NFR-02 | Phase 12 | Pending |

**Coverage:**
- v1.2 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

## Next Up

```bash
$gsd-plan-phase 12 --skip-research
```
