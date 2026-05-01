# Requirements: FocusFlow v1.4 Weekly Review Insights

**Defined:** 2026-05-01
**Core Value:** Reduce manual scheduling effort by producing practical daily plans and showing what actually happened after execution.

## v1.4 Requirements

### Weekly Review

- [ ] **WREV-01**: User can view a weekly review for the selected week from the Daily Review workflow.
- [ ] **WREV-02**: User can see weekly completion rate based on execution history statuses.
- [ ] **WREV-03**: User can see total actual minutes for the selected week.
- [ ] **WREV-04**: User can see weekly estimate variance using estimated-minute snapshots and actual minutes.
- [ ] **WREV-05**: User can see a day-by-day breakdown for the selected week.

### Trend Comparison

- [ ] **TRND-01**: User can compare the selected week's completion rate with the previous week when previous-week data exists.
- [ ] **TRND-02**: User can compare the selected week's actual minutes with the previous week when previous-week data exists.
- [ ] **TRND-03**: User can compare the selected week's estimate variance with the previous week when previous-week data exists.
- [ ] **TRND-04**: User sees a clear empty or insufficient-data state when comparison data is unavailable.

### Daily Review UX

- [ ] **DRUX-01**: User can switch between daily review and weekly review views without leaving Daily Review.
- [ ] **DRUX-02**: User can change the selected week using simple previous/next week controls.
- [ ] **DRUX-03**: User sees Chinese and English copy for all weekly review labels, messages, and empty states.
- [ ] **DRUX-04**: User can still use existing Daily Review history and export flows after weekly review is added.

### Quality

- [ ] **NFR-01**: Weekly review APIs use the existing success envelope and deterministic local calculations.
- [ ] **NFR-02**: Weekly review backend behavior is covered by focused tests for aggregation, comparison, and empty states.
- [ ] **NFR-03**: Weekly review UI helpers and i18n copy are covered by frontend helper/i18n tests and production build verification.
- [ ] **NFR-04**: Demo seed and smoke coverage show a selected week with meaningful completion, minutes, and variance data.

## Future Requirements

### Review Insights

- **RINS-01**: User can search across execution notes and Daily Review summaries.
- **RINS-02**: User can view monthly review trends.
- **RINS-03**: User can receive deterministic local recommendations based on weekly patterns.
- **RINS-04**: User can export weekly review data.

### Planning

- **PLAN-05**: User can generate a weekly plan from daily scheduling primitives.
- **PLAN-06**: User can compare original and partial-replanned schedules side by side.

### Data Portability

- **DATA-01**: User can import a previously exported JSON backup.
- **DATA-02**: User can export all app data as a single portable archive.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Weekly planning | v1.4 is review-only; planning is a larger scheduling feature. |
| Monthly analytics | Weekly review is the smallest useful trend surface. |
| Prescriptive coaching | Transparent metrics should ship before recommendation logic. |
| Cloud sync or accounts | Conflicts with the current local-first boundary. |
| Import/restore | Data mutation is higher risk than read-only review metrics. |

## Traceability

| Requirement | Phase | Status |
|-------------|-------|--------|
| WREV-01 | Phase 16 | Pending |
| WREV-02 | Phase 16 | Pending |
| WREV-03 | Phase 16 | Pending |
| WREV-04 | Phase 16 | Pending |
| WREV-05 | Phase 16 | Pending |
| TRND-01 | Phase 16 | Pending |
| TRND-02 | Phase 16 | Pending |
| TRND-03 | Phase 16 | Pending |
| TRND-04 | Phase 16 | Pending |
| DRUX-01 | Phase 17 | Pending |
| DRUX-02 | Phase 17 | Pending |
| DRUX-03 | Phase 17 | Pending |
| DRUX-04 | Phase 17 | Pending |
| NFR-01 | Phase 16 | Pending |
| NFR-02 | Phase 16 | Pending |
| NFR-03 | Phase 17 | Pending |
| NFR-04 | Phase 18 | Pending |

**Coverage:**
- v1.4 requirements: 17 total
- Mapped to phases: 17
- Unmapped: 0

---
*Requirements defined: 2026-05-01*
*Last updated: 2026-05-01 after v1.4 roadmap creation*

