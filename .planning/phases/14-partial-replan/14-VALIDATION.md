# Phase 14 Validation: Partial Replan

## Scope

Phase 14 adds remaining-work replanning for a selected day. It should regenerate selectable schedule variants from unfinished selected-plan tasks while preserving execution logs. It should not add weekly planning, side-by-side original-vs-replanned comparison, migrations, or new execution-history semantics.

## Acceptance Checks

- Partial replan requires a selected plan for the requested date.
- Remaining-work candidates come only from the selected plan.
- Tasks with same-day execution feedback are excluded regardless of feedback status.
- Tasks currently marked `done` or `canceled` are excluded even without same-day feedback.
- A successful partial replan returns the existing schedule generation payload shape inside the success envelope.
- A successful partial replan replaces same-day generated plan variants, clears selected state, and leaves execution logs untouched.
- No selected plan, no remaining work, and no schedulable time return clear error envelopes.
- Calendar exposes a localized partial replan action and reuses the existing plan review/selection flow.

## Required Verification

Run from repository root unless noted:

```powershell
python -m pytest tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase14_partial_replan.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual Demo Sanity

1. Seed or create tasks for a date.
2. Generate and select a Calendar plan.
3. Submit feedback for one or more selected tasks from Today.
4. Return to Calendar and run partial replan.
5. Confirm feedbacked work is absent from new plans, execution history remains visible, and a new plan can be selected.
