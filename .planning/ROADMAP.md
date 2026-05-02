# Roadmap: FocusFlow Intelligent Energy Scheduler

## Milestones

- **v1.0 MVP** - Shipped 2026-04-27. Archive: [v1.0-ROADMAP.md](milestones/v1.0-ROADMAP.md)
- **v1.1 Execution Insights** - Shipped 2026-04-30. Archive: [v1.1-ROADMAP.md](milestones/v1.1-ROADMAP.md)
- **v1.2 Learning Duration Suggestions** - Shipped 2026-04-30. Archive: [v1.2-ROADMAP.md](milestones/v1.2-ROADMAP.md)
- **v1.3 Export & Planning Utilities** - Shipped 2026-05-01. Archive: [v1.3-ROADMAP.md](milestones/v1.3-ROADMAP.md)
- **v1.4 Weekly Review Insights** - Active.

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

<details>
<summary>v1.3 Export & Planning Utilities (Phases 13-15) - SHIPPED 2026-05-01</summary>

- [x] Phase 13: Export Data Utilities - local task/history/review exports and UI controls
- [x] Phase 14: Partial Replan - selected-plan-based remaining-work replanning
- [x] Phase 15: Search And Demo Polish - task notes/search, empty states, demo docs, smoke coverage, and UAT

</details>

## Active Milestone: v1.4 Weekly Review Insights

**Goal:** Turn daily execution history into a useful weekly review view with core trend metrics inside Daily Review.

| Phase | Name | Goal | Requirements | Status |
|-------|------|------|--------------|--------|
| 16 | Weekly Review Backend | Add deterministic weekly review aggregation and previous-week comparison APIs. | WREV-01, WREV-02, WREV-03, WREV-04, WREV-05, TRND-01, TRND-02, TRND-03, TRND-04, NFR-01, NFR-02 | Complete |
| 17 | Weekly Review UI | Add a Daily Review weekly view with week controls, metric cards, daily breakdown, and bilingual copy. | DRUX-01, DRUX-02, DRUX-03, DRUX-04, NFR-03 | Complete |
| 18 | Weekly Review Demo Polish | Seed meaningful weekly review data, extend smoke coverage, update README, and prepare UAT. | NFR-04 | Planned |

## Phase Details

### Phase 16: Weekly Review Backend

**Goal:** Add deterministic weekly review aggregation and previous-week comparison APIs.

**Requirements:** WREV-01, WREV-02, WREV-03, WREV-04, WREV-05, TRND-01, TRND-02, TRND-03, TRND-04, NFR-01, NFR-02

**Success criteria:**
1. Backend returns selected-week start/end dates and aggregated metrics from execution logs.
2. Completion rate, actual minutes, and estimate variance are calculated deterministically.
3. Response includes day-by-day breakdown for the selected week.
4. Previous-week comparison is returned when data exists and clear empty metadata is returned when it does not.
5. Focused backend tests cover aggregation, comparison, empty week, and success-envelope behavior.

**Status:** Complete.

### Phase 17: Weekly Review UI

**Goal:** Add a Daily Review weekly view with week controls, metric cards, daily breakdown, and bilingual copy.

**Requirements:** DRUX-01, DRUX-02, DRUX-03, DRUX-04, NFR-03

**Success criteria:**
1. Daily Review lets the user switch between daily and weekly views without leaving the page.
2. Weekly view exposes previous/next week controls and loads the selected week.
3. Weekly completion rate, actual minutes, estimate variance, previous-week deltas, and daily breakdown are visible.
4. Existing Daily Review history and export controls still work.
5. i18n/helper tests and frontend production build pass.

**Status:** Complete.

### Phase 18: Weekly Review Demo Polish

**Goal:** Make v1.4 repeatable and demo-ready with seeded weekly data, smoke coverage, README updates, and UAT readiness.

**Requirements:** NFR-04

**Success criteria:**
1. Demo seed creates enough history across at least two weeks to show weekly metrics and previous-week comparison.
2. Smoke tests cover seed -> weekly review API -> Daily Review compatibility.
3. README documents the v1.4 weekly review demo path.
4. Phase verification and UAT artifacts are ready for milestone completion.

**Status:** Planned.

## Traceability Summary

| Requirement | Phase | Status |
|-------------|-------|--------|
| WREV-01 | Phase 16 | Complete |
| WREV-02 | Phase 16 | Complete |
| WREV-03 | Phase 16 | Complete |
| WREV-04 | Phase 16 | Complete |
| WREV-05 | Phase 16 | Complete |
| TRND-01 | Phase 16 | Complete |
| TRND-02 | Phase 16 | Complete |
| TRND-03 | Phase 16 | Complete |
| TRND-04 | Phase 16 | Complete |
| DRUX-01 | Phase 17 | Complete |
| DRUX-02 | Phase 17 | Complete |
| DRUX-03 | Phase 17 | Complete |
| DRUX-04 | Phase 17 | Complete |
| NFR-01 | Phase 16 | Complete |
| NFR-02 | Phase 16 | Complete |
| NFR-03 | Phase 17 | Complete |
| NFR-04 | Phase 18 | Pending |

**Coverage:**
- v1.4 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0

## Next Up

```bash
$gsd-plan-phase 18 --skip-research
```
