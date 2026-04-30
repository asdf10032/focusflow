# Phase 13 Validation: Export Data Utilities

## Scope

Phase 13 adds local export utilities for the data users already create in FocusFlow. It should expose deterministic export APIs for tasks, execution history, and Daily Review summaries, then add localized UI controls to download those exports. It should not add import/restore behavior, cloud sync, hosted backups, third-party calendar formats, migrations, or partial replan behavior.

## Acceptance Checks

- Task export returns local JSON with task fields plus enough project context for the data to be understandable outside the app.
- Execution history export returns local JSON filtered by a selected date or inclusive date range.
- Daily Review export returns deterministic CSV content for a selected date or inclusive date range.
- All export APIs use the existing `status/data/error/meta` envelope rather than raw file responses.
- CSV export data has a stable header order and stable row ordering.
- Export filenames are deterministic and include the export kind and selected date/range.
- Frontend export controls are localized in Chinese and English.
- Frontend export controls create downloadable files in the browser from API payloads.
- Frontend export errors are visible and do not break existing Tasks, Calendar, Today, or Daily Review flows.
- No user data is mutated by any export endpoint.

## Required Verification

Run from repository root unless noted:

```powershell
python -m pytest tests/test_phase13_exports.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase13_exports.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py -q -p no:cacheprovider
python -m compileall backend alembic
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual Demo Sanity

1. Seed demo data for a date.
2. Start backend and frontend.
3. Open Tasks and export tasks as JSON.
4. Open Daily Review, choose a date with history, and export review CSV.
5. Trigger execution history export for the same date or range.
6. Confirm downloaded filenames are clear and the file content is readable.

