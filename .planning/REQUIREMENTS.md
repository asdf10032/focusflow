# Requirements: FocusFlow v1.1 Execution Insights

**Defined:** 2026-04-28
**Core Value:** Reduce manual scheduling effort with practical, explainable daily plans, then use execution history to make future planning more accurate.

## v1.1 Requirements

### Execution History

- [x] **HIST-01**: User feedback creates an execution history record instead of only updating task status.
- [x] **HIST-02**: User can record feedback status, actual duration, and an optional note.
- [x] **HIST-03**: User can query execution history for a selected date.

### Today Progress

- [ ] **PROG-01**: User can see total planned items, completed count, skipped/incomplete count, and completion rate on Today.
- [ ] **PROG-02**: Today progress metrics refresh after feedback submission.
- [ ] **PROG-03**: Today shows a clear empty state when no plan is selected.

### Estimate Accuracy

- [ ] **EST-01**: User can compare estimated task duration with actual duration.
- [ ] **EST-02**: User can see daily estimate variance summary.
- [x] **EST-03**: Execution history stores the estimated duration at feedback time so later task edits do not rewrite historical review data.

### Daily Review

- [ ] **REV-01**: User can open a daily review page for a selected date.
- [ ] **REV-02**: Daily review shows completed, incomplete, skipped work, completion rate, planned duration, actual duration, and estimate variance.
- [ ] **REV-03**: Daily review can be demonstrated from seeded/demo data and covered by a smoke test.

### Schedule Explanation

- [ ] **EXPL-01**: Generated schedules include a user-readable plan summary.
- [ ] **EXPL-02**: Risks and unplaced tasks include clearer reason text.
- [ ] **EXPL-03**: Calendar or Today displays plan summaries and risk explanations without requiring an external AI service.

### Filtering

- [ ] **FILT-01**: User can filter tasks by status.
- [ ] **FILT-02**: User can filter tasks by project.
- [ ] **FILT-03**: User can filter history/review records by date.

### Nonfunctional

- [x] **NFR-01**: Existing API success envelope remains unchanged.
- [ ] **NFR-02**: Backend API, frontend helper/i18n, build, and smoke tests cover v1.1 behavior.
- [ ] **NFR-03**: v1.1 does not introduce login, cloud sync, external LLM, or third-party calendar integration.

## Future Requirements

### Learning Scheduler

- **LEARN-01**: System suggests future duration estimates based on execution history.
- **LEARN-02**: System adapts scheduling preferences from repeated user feedback.

### Export

- **EXP-01**: User can export tasks and execution history as JSON.
- **EXP-02**: User can export review summaries as CSV.

### Weekly Planning

- **WEEK-01**: User can generate a weekly plan from tasks and availability.
- **WEEK-02**: User can partially replan remaining work after a day changes.

## Out of Scope

| Feature | Reason |
|---------|--------|
| User accounts and cloud sync | V1.1 remains local-first and single-user. |
| External AI parsing or explanation | Deterministic explanations are enough for this milestone. |
| Third-party calendar sync | Integration complexity would distract from execution insights. |
| Full learning-based scheduler | Execution history must exist before meaningful learning can be built. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| HIST-01 | Phase 6 | Complete |
| HIST-02 | Phase 6 | Complete |
| HIST-03 | Phase 6 | Complete |
| PROG-01 | Phase 7 | Pending |
| PROG-02 | Phase 7 | Pending |
| PROG-03 | Phase 7 | Pending |
| EST-01 | Phase 7 | Pending |
| EST-02 | Phase 7 | Pending |
| EST-03 | Phase 6 | Complete |
| REV-01 | Phase 7 | Pending |
| REV-02 | Phase 7 | Pending |
| REV-03 | Phase 9 | Pending |
| EXPL-01 | Phase 8 | Pending |
| EXPL-02 | Phase 8 | Pending |
| EXPL-03 | Phase 8 | Pending |
| FILT-01 | Phase 8 | Pending |
| FILT-02 | Phase 8 | Pending |
| FILT-03 | Phase 7 | Pending |
| NFR-01 | Phase 6 | Complete |
| NFR-02 | Phase 9 | Pending |
| NFR-03 | Phase 8 | Pending |

**Coverage:**
- v1.1 requirements: 21 total
- Mapped to phases: 21
- Unmapped: 0

---
*Requirements defined: 2026-04-28*
*Last updated: 2026-04-28 after Phase 6 completion*
