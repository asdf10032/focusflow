---
status: complete
phase: 15-search-and-demo-polish
source: [15-01-SUMMARY.md, 15-02-SUMMARY.md, 15-03-SUMMARY.md]
started: 2026-05-01T21:09:18.5082054+08:00
updated: 2026-05-01T21:15:14.4496219+08:00
---

## Current Test

[testing complete]

## Tests

### 1. Cold Start Smoke Test
expected: From a clean local start, `alembic upgrade head` succeeds, demo seeding for a chosen date completes without deleting user data, the backend can start, and the frontend build completes.
result: pass

### 2. Task Notes Entry And Display
expected: On the Tasks page, the task form includes a Notes field. Creating or editing a task saves notes, and the notes text appears on the task card after save.
result: pass

### 3. Task Search With Filters
expected: On the Tasks page, searching by title or notes narrows the task list, and the search still works when combined with status and project filters.
result: pass

### 4. Empty States And No-Data Exports
expected: When filters match no tasks, Today has a selected plan with no items, or an export has no records, the UI shows localized empty-state text instead of a confusing blank area or empty download.
result: pass

### 5. v1.3 Demo Guide
expected: Near the top of README, the v1.3 local demo section shows backend setup, migration, demo seed, backend/frontend commands, verification commands, and the Tasks -> Calendar -> Today -> Daily Review demo path.
result: pass

### 6. v1.3 Demo Loop
expected: The documented demo path can be followed end to end: seed demo data, search a demo task, export data, run partial replan, select the new plan, submit Today feedback, and review/export Daily Review data.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0

## Gaps

[none yet]
