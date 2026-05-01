# Phase 15 Verification: Search And Demo Polish

## Result

Passed on 2026-05-01.

## Acceptance Checks

- Task notes are stored, returned by APIs, and included in task exports.
- Task search matches title and notes case-insensitively.
- Task search composes with status and project filters.
- Blank task search is ignored.
- Tasks page exposes localized search and notes UI.
- Empty states are localized for filtered tasks, selected-plan-without-items, and no-data exports.
- Demo flow covers seed data, task search, task export, execution-history export, daily-review export, partial replan, plan reselection, Today feedback, and Daily Review data.
- README documents the v1.3 local demo path and verification commands.

## Commands

```powershell
python -m pytest tests/test_phase15_task_search.py tests/test_demo_flow.py -q -p no:cacheprovider
```

Result: `7 passed in 1.10s`

```powershell
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_phase15_task_search.py tests/test_demo_flow.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
```

Result: `62 passed in 6.46s`

```powershell
python -m compileall backend alembic
```

Result: passed.

```powershell
npm.cmd run build
```

Result: passed.

