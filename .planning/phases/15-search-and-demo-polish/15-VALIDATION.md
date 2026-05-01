# Phase 15 Validation: Search And Demo Polish

## Scope

Phase 15 closes v1.3 by adding task search, useful empty states, v1.3 demo documentation, and repeatable smoke coverage. It should not add import/restore, cloud sync, weekly planning, side-by-side replan comparison, adaptive scheduler scoring, or cross-history search.

## Acceptance Checks

- Tasks can store optional notes and existing local databases can migrate safely.
- Task search matches title and notes case-insensitively from the Tasks page.
- Task search composes with existing status and project filters.
- Empty states are localized and helpful for Tasks, Calendar, Today, Daily Review, and export flows.
- Export controls show a clear empty result when there is no local data to export.
- Demo seed data supports the v1.3 path: tasks with notes, exports, selected plan, partial replan, Today feedback, and Daily Review.
- Smoke coverage verifies seed -> export -> partial replan -> selected plan -> review loop.
- README surfaces v1.3 setup, seed, verification, and demo path near the top.
- Frontend i18n/helper tests, backend focused tests, compile checks, and frontend production build pass.

## Required Verification

Run from repository root unless noted:

```powershell
python -m pytest tests/test_phase15_task_search.py tests/test_demo_flow.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_phase15_task_search.py tests/test_demo_flow.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual Demo Sanity

1. Run demo seed for a fixed date.
2. Open Tasks, search by task title, then search by task notes, and combine search with status/project filters.
3. Export tasks from Tasks and export history/review from Daily Review.
4. Open Calendar, run partial replan after seeded or submitted feedback, select a newly generated plan.
5. Open Today and submit feedback.
6. Open Daily Review and confirm history/review content is visible.
