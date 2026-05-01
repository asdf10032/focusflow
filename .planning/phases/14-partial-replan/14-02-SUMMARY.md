# Phase 14-02 Summary: Calendar Partial Replan UI

## Completed

- Added a typed API client method for partial replan.
- Added a localized Calendar action near Reoptimize for remaining-work replanning.
- On success, Calendar refreshes generated plans, defaults the active view to balanced when present, clears selected-plan state, and clears move validation state.
- Added localized success and backend-error messages for missing selected plan, no remaining work, no schedulable time, and generic failure.
- Extended frontend i18n coverage for partial replan labels and messages.
- Updated v1.3 GSD roadmap and state after verification.

## Verification

- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider` - 53 passed.
- `npm.cmd run build` from `frontend/` - passed.

