---
phase: 02-scheduling-mvp
plan: 02
subsystem: scheduler-engine
tags: [scheduler, dependencies, risk, scoring, tdd]
provides:
  - Dependency-aware task ordering
  - Dependency cycle detection
  - Stable unplaced task warnings
  - Plan risk level and quality scoring
affects: [scheduling-mvp, frontend-main-flow]
tech-stack:
  added: []
  patterns: [topological-sort, warning-list, score-by-placed-tasks]
key-files:
  created:
    - tests/test_scheduler_engine.py
  modified:
    - backend/app/services/scheduler/engine.py
    - backend/app/schemas/schedule.py
    - backend/app/api/v1/endpoints/schedules.py
    - tests/test_phase1_api.py
key-decisions:
  - "Scheduler returns warnings as a stable response field alongside unplaced task IDs."
  - "Cyclic candidate-task dependencies are treated as invalid schedule input and returned as a 400 envelope from the API."
duration: 35min
completed: 2026-04-26
---

# Phase 2: Scheduling MVP Summary

**Completed the scheduler correctness slice with dependency ordering, cycle detection, unplaced warnings, risk levels, and scoring.**

## Performance
- **Duration:** 35min
- **Tasks:** 3 completed
- **Files modified:** 4 code/test files plus GSD planning artifacts

## Accomplishments
- Added direct scheduler unit tests for dependency ordering, dependency cycles, and fully blocked days.
- Reworked the scheduler engine to order candidate tasks with a topological pass before placement.
- Added `warnings` to schedule generation output and mapped cyclic dependencies to a 400 `invalid_schedule_input` API error.
- Replaced item-count-only scoring with placed-task scoring plus penalties for fragmentation and unplaced tasks.

## Task Commits
1. **Task 1: Add scheduler unit tests** - not committed in this session
2. **Task 2: Harden scheduler dependency and warning behavior** - not committed in this session
3. **Task 3: Improve scoring and API exposure** - not committed in this session

## Files Created/Modified
- `tests/test_scheduler_engine.py` - Focused scheduler unit tests using in-memory SQLite.
- `backend/app/services/scheduler/engine.py` - Dependency-aware scheduling, warnings, risk, and scoring.
- `backend/app/schemas/schedule.py` - `GenerateResponse.warnings`.
- `backend/app/api/v1/endpoints/schedules.py` - Error mapping for invalid scheduler input.
- `tests/test_phase1_api.py` - API regression for dependency-cycle error envelope.

## Verification
- `python -m pytest tests/test_scheduler_engine.py tests/test_phase1_api.py -q -p no:cacheprovider` -> 10 passed

## Decisions & Deviations
No external graph library was added; the dependency pass uses a small local topological sort to keep the MVP dependency footprint unchanged.

## Next Phase Readiness
Phase 3 can consume generated plans with persisted selected state, stable unplaced IDs, warning text, score, and risk level.
