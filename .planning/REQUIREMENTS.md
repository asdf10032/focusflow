# Requirements: FocusFlow v1.2 Learning Duration Suggestions

**Defined:** 2026-04-30
**Core Value:** Reduce manual scheduling effort by producing practical daily plans and showing what actually happened after execution.

## v1.2 Requirements

### Duration Suggestions

- [x] **DSUG-01**: User can request a suggested duration for a task draft using title, project, cognitive load, and optional current estimate.
- [x] **DSUG-02**: User can see suggested minutes, confidence, sample count, and reason text for a duration suggestion.
- [x] **DSUG-03**: User can accept a duration suggestion in the task form without losing the ability to manually override the estimate.
- [x] **DSUG-04**: User can receive duration suggestion metadata when parsing plain task text into a draft.

### Learning Data

- [x] **LERN-01**: User duration suggestions are derived from durable execution history snapshots rather than mutable current task fields.
- [x] **LERN-02**: User receives safe fallback behavior when there is not enough relevant execution history.
- [ ] **LERN-03**: Demo data includes enough execution history to show both confident and fallback duration suggestions.

### Usability And Quality

- [x] **UX-01**: User can use duration suggestions from the Tasks page in both Chinese and English.
- [x] **NFR-01**: Backend duration suggestion behavior is local, deterministic, and covered by focused tests.
- [ ] **NFR-02**: The v1.2 demo path, README, smoke tests, compile checks, and frontend build remain repeatable.

## Future Requirements

### Export

- **EXP-01**: User can export tasks and execution history as JSON.
- **EXP-02**: User can export review summaries as CSV.

### Planning

- **PLAN-01**: User can generate a weekly plan from daily scheduling primitives.
- **PLAN-02**: User can partially replan remaining work without discarding completed feedback.

### Search And Onboarding

- **SRCH-01**: User can search tasks by text across title and notes.
- **ONBD-01**: New user sees helpful empty states and first-run guidance.

## Out of Scope

| Feature | Reason |
|---------|--------|
| External LLM duration estimation | Conflicts with local-first, deterministic demo goals. |
| Automatic rewriting of existing estimates | v1.2 suggestions should require explicit user acceptance. |
| Adaptive schedule scoring | Duration suggestion should be proven before changing planner scoring. |
| Cloud/shared learning | Authentication and sync are outside the local MVP scope. |
| Bulk historical data import | Demo seed data is enough for v1.2 verification. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| DSUG-01 | Phase 10 | Complete |
| DSUG-02 | Phase 10 | Complete |
| LERN-01 | Phase 10 | Complete |
| LERN-02 | Phase 10 | Complete |
| NFR-01 | Phase 10 | Complete |
| DSUG-03 | Phase 11 | Complete |
| DSUG-04 | Phase 11 | Complete |
| UX-01 | Phase 11 | Complete |
| LERN-03 | Phase 12 | Pending |
| NFR-02 | Phase 12 | Pending |

**Coverage:**
- v1.2 requirements: 10 total
- Mapped to phases: 10
- Unmapped: 0

---
*Requirements defined: 2026-04-30*
*Last updated: 2026-04-30 after Phase 11 completion*
