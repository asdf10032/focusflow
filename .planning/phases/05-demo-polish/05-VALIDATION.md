# Phase 5 Validation: Demo Polish

## Acceptance Checks

- Demo data can be seeded repeatably with `python -m backend.app.services.seeds.demo_data`.
- Demo seeding accepts `--date YYYY-MM-DD` and does not wipe existing user data.
- Demo seed creates default energy templates, one demo project, realistic tasks, a blocked time, three generated schedule plans, and selects the balanced plan.
- `/api/v1/execution/today` shows selected demo work immediately after seeding.
- Smoke test covers demo seed, selected schedule retrieval, feedback submission, and deterministic task parsing.
- README startup, seeding, verification, and demo path instructions are easy to find near the top.
- Existing API response shapes remain unchanged.

## Verification Commands

- `python -m pytest tests/test_demo_flow.py -q -p no:cacheprovider`
- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_demo_flow.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider`
- `python -m compileall backend alembic`
- `npm.cmd run build`

