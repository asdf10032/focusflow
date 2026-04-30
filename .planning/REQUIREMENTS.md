# Requirements: FocusFlow v1.3 Export & Planning Utilities

**Defined:** 2026-04-30
**Core Value:** Reduce manual scheduling effort by producing practical daily plans and showing what actually happened after execution.

## v1.3 Requirements

### Export

- [x] **EXP-01**: User can export tasks as local JSON including project, scheduling, status, and estimate fields.
- [x] **EXP-02**: User can export execution history as local JSON filtered by date or date range.
- [x] **EXP-03**: User can export Daily Review summary data as CSV for a selected date or date range.
- [x] **EXP-04**: User can trigger exports from the UI with Chinese and English copy, clear filenames, and visible error states.

### Partial Replan

- [ ] **PLAN-01**: User can regenerate plans for the remaining work on a selected date without deleting completed execution history.
- [ ] **PLAN-02**: User can keep completed, skipped, canceled, or already-feedbacked work out of remaining-work replan candidates.
- [ ] **PLAN-03**: User can review and select the newly generated remaining-work plan using the existing calendar selection flow.
- [ ] **PLAN-04**: User sees a clear message when partial replan cannot run because there is no selected plan, no remaining work, or no schedulable time.

### Search And Empty States

- [ ] **SRCH-01**: User can search tasks by title and notes from the Tasks page.
- [ ] **SRCH-02**: User can combine task search with existing status and project filters.
- [ ] **ONBD-01**: User sees helpful empty states for Tasks, Calendar, Today, Daily Review, and export flows when no local data exists.

### Quality

- [x] **NFR-01**: Export APIs use the existing success envelope and are covered by focused backend tests.
- [ ] **NFR-02**: Partial replan APIs use the existing success envelope and are covered by focused backend tests.
- [ ] **NFR-03**: Frontend export, partial replan, search, and empty-state copy are covered by i18n/helper tests and production build verification.
- [ ] **NFR-04**: v1.3 demo documentation and smoke coverage show the export and partial replan loop without requiring network access.

## Future Requirements

### Export

- **EXP-05**: User can import a previously exported JSON backup.
- **EXP-06**: User can export all app data as a single portable archive.

### Planning

- **PLAN-05**: User can generate a weekly plan from daily scheduling primitives.
- **PLAN-06**: User can compare original and partial-replanned schedules side by side.

### Search And Onboarding

- **SRCH-03**: User can search across execution notes and Daily Review summaries.
- **ONBD-02**: User can follow a guided first-run checklist.

## Out of Scope

| Feature | Reason |
|---------|--------|
| Data import/restore | Export is lower risk and should be proven before restore behavior mutates local data. |
| Cloud sync or hosted backups | Conflicts with the local-first project boundary. |
| Third-party calendar export formats | CSV/JSON are enough for v1.3 portability and verification. |
| Weekly planning | Useful, but partial daily replan is a smaller step on the same path. |
| Adaptive scheduler scoring | Still deferred until duration suggestions and replan behavior are proven in use. |

## Traceability

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

---
*Requirements defined: 2026-04-30*
*Last updated: 2026-05-01 after Phase 13 completion*
