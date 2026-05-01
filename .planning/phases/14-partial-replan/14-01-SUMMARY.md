# Phase 14-01 Summary: Backend Partial Replan

## Completed

- Added `POST /api/v1/schedules/partial-replan`.
- Required an existing selected plan for the date and returned `missing_selected_plan` when absent.
- Built remaining-work candidates from unique selected-plan tasks that still exist, are open, and have no same-day execution log.
- Excluded completed, canceled, skipped, and otherwise feedbacked work while preserving execution logs.
- Reused blocked-time and energy-template scheduling rules.
- Returned clear `no_remaining_work` and `no_schedulable_time` errors without replacing plans.
- On success, replaced same-day generated plans and cleared selected-plan state for explicit reselection.
- Added focused backend tests for success and error paths.

## Verification

- `python -m pytest tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase14_partial_replan.py -q -p no:cacheprovider` - 20 passed.
- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider` - 53 passed.
- `python -m compileall backend alembic` - passed.

