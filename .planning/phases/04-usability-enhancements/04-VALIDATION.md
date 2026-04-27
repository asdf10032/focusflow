# Phase 4 Validation: Usability Enhancements

## Acceptance Criteria

- Validate-move returns a clear `valid` flag and conflict list without mutating schedule data.
- Reoptimize regenerates same-day plans and clears stale selected-plan state.
- Today execution returns the selected plan's work items and supports status feedback.
- AI task parse returns a structured draft using local deterministic parsing only.
- Frontend exposes the Phase 4 flows in Chinese and English.

## Verification Commands

- `python -m pytest tests/test_phase4_api.py -q -p no:cacheprovider`
- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider`
- `python -m compileall backend alembic`
- `npm.cmd run build`
