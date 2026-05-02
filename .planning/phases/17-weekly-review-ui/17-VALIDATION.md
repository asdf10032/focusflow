# Phase 17 Validation: Weekly Review UI

## Scope

Phase 17 adds a weekly review view inside the existing Daily Review page. It should not add a new navigation item, weekly planning, monthly analytics, coaching recommendations, backend migrations, or weekly export behavior.

## Acceptance Checks

- Daily Review exposes a compact daily/weekly view switch without leaving the page.
- Daily mode keeps the existing date picker, summary metrics, history list, refresh, and export controls working.
- Weekly mode loads `GET /api/v1/execution/weekly-review?date=YYYY-MM-DD` through the typed API client.
- Weekly mode exposes previous-week and next-week controls.
- Weekly mode shows week start/end, completion rate, actual minutes, estimate variance, and previous-week deltas when available.
- Weekly mode shows clear comparison-unavailable copy when previous-week data is missing.
- Weekly mode renders a seven-day breakdown, including empty days.
- All new labels, buttons, metric names, comparison messages, and empty states have Chinese and English i18n keys.
- Frontend helper/i18n tests and production build pass.

## Required Verification

Run from repository root:

```powershell
python -m pytest tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py -q -p no:cacheprovider
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual Sanity

1. Open Daily Review.
2. Confirm daily mode still loads the selected date, exports history/review, and shows the existing empty state.
3. Switch to weekly mode.
4. Move to previous and next week.
5. Confirm weekly metrics, comparison state, and seven-day breakdown render without layout overlap.
