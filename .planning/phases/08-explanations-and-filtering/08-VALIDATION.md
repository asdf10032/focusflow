# Phase 8 Validation: Explanations and Filtering

## Acceptance Checks

- Generated schedule plans include deterministic user-readable summary text.
- Schedule risks and unplaced tasks include clearer deterministic reason text.
- Schedule explanation fields are persisted/reused through existing generate and reoptimize flows without changing the success envelope.
- Calendar or Today displays plan summaries and risk/unplaced explanations.
- Tasks page supports status filtering.
- Tasks page supports project filtering when project data is available.
- New UI text is localized in Chinese and English.
- Phase 8 introduces no external AI calls, login, cloud sync, or third-party calendar integration.

## Verification Commands

- `python -m pytest tests/test_scheduler_engine.py tests/test_phase4_api.py tests/test_phase8_explanations.py -q -p no:cacheprovider`
- `python -m pytest tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py -q -p no:cacheprovider`
- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_demo_flow.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_scheduler_engine.py -q -p no:cacheprovider`
- `python -m compileall backend alembic`
- `npm.cmd run build`
