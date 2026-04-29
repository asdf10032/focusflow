# Phase 10 Validation: Duration Suggestion Backend

## Scope

Phase 10 adds the backend foundation for local deterministic duration suggestions. It should use durable execution history snapshots, expose an advisory API, and avoid frontend UI changes.

## Acceptance Checks

- Execution logs snapshot task project and cognitive load when feedback is submitted.
- `POST /api/v1/ai/suggest-duration` returns the standard success envelope.
- Suggestions include `suggested_minutes`, `confidence`, `sample_count`, `source`, `reason_code`, and `reason`.
- Completed execution logs with actual minutes drive history-based suggestions.
- Non-done logs and logs without actual minutes are ignored.
- Suggestions remain stable after source tasks are later edited.
- Sparse history falls back deterministically to current estimate or cognitive-load bands.
- No external LLM, network dependency, frontend UI, or scheduler scoring change is added.

## Required Verification

Run from the repository root:

```powershell
python -m pytest tests/test_phase6_execution_history.py tests/test_phase10_duration_suggestions.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase10_duration_suggestions.py -q -p no:cacheprovider
python -m compileall backend alembic
```

## Manual API Sanity

1. Create a task and submit done feedback with actual minutes.
2. Call `POST /api/v1/ai/suggest-duration` with a similar title.
3. Confirm the suggestion is history-based and advisory only.
