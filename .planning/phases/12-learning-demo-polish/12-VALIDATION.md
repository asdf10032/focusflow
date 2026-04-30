# Phase 12 Validation: Learning Demo Polish

## Scope

Phase 12 finishes the v1.2 milestone by making duration suggestions demonstrable and repeatable. It should improve demo seed data, smoke coverage, and README instructions. It should not add new product features, migrations, external LLM calls, or scheduler-learning behavior.

## Acceptance Checks

- Demo seed data remains repeatable and non-destructive.
- Demo seed data creates execution history with `done` actual-minute records that include project and cognitive-load snapshots.
- Seeded data can demonstrate a history-based duration suggestion with nonzero sample count and high confidence through the local API.
- Seeded data can also demonstrate fallback duration suggestion behavior for a novel task.
- Existing demo flow still creates tasks, blocked time, three schedule plans, selected balanced plan, Today work, progress, review, and history records.
- Smoke tests cover seed -> today/review -> duration suggestion history -> duration suggestion fallback -> parse-task flow.
- README startup and demo instructions are easy to find near the top and mention v1.2 duration suggestions.
- Verification commands include backend smoke tests, wider regression tests, compile checks, and frontend build.
- Phase 12 updates GSD requirements, roadmap, and state after implementation.

## Required Verification

Run from the repository root unless noted:

```powershell
python -m pytest tests/test_demo_flow.py tests/test_phase10_duration_suggestions.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_demo_flow.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase10_duration_suggestions.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual Demo Sanity

1. Run `alembic upgrade head`.
2. Run `python -m backend.app.services.seeds.demo_data --date 2026-04-30`.
3. Start backend and frontend.
4. Open Tasks and request a duration suggestion for a seeded task-like title.
5. Confirm a history-based suggestion appears and can be accepted, then manually edited.
6. Try a novel title and confirm fallback behavior is explainable.
7. Continue the documented path through Calendar, selected plan, Today feedback, and Daily Review.
