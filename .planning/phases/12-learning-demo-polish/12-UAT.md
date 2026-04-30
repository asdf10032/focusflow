---
status: complete
phase: 12-learning-demo-polish
source: 12-01-SUMMARY.md, 12-VERIFICATION.md
started: 2026-04-30T03:15:00+08:00
updated: 2026-04-30T03:30:00+08:00
---

## Current Test

[testing complete]

## Tests

### 1. Cold Start v1.2 Demo
expected: From a fresh local start, `alembic upgrade head` succeeds, `python -m backend.app.services.seeds.demo_data --date 2026-04-30` completes without deleting user data, the backend starts, and the frontend can load the app.
result: pass

### 2. History and Fallback Duration Suggestions
expected: After seeding demo data, a seeded task-like title such as `Prepare slide talking points` produces a history-based duration suggestion with sample count and confidence, while a novel title such as `Plan a new workshop` produces an explainable fallback suggestion.
result: pass

### 3. Tasks Suggestion Acceptance and Override
expected: On the Tasks page, requesting a duration suggestion shows suggested minutes, confidence, sample count, source, and reason without changing the minutes field. Clicking the accept/use button updates minutes, and typing afterward can still manually override it.
result: pass

### 4. Quick Parse Suggestion Flow
expected: Entering `Polish demo script 45min medium` in Quick Parse fills the task form and shows duration suggestion metadata in the same suggestion area.
result: pass

### 5. Calendar to Today to Daily Review Loop
expected: The documented path continues to work: Calendar shows/generates plans, selecting balanced makes Today show work, submitting feedback records actual minutes/note, and Daily Review shows history, completion metrics, and estimate variance.
result: pass

### 6. README v1.2 Demo Instructions
expected: README starts with v1.2 local demo instructions, including backend setup, demo seed command, frontend commands, verification commands, and the exact Tasks -> Calendar -> Today -> Review demo path.
result: pass

## Summary

total: 6
passed: 6
issues: 0
pending: 0
skipped: 0

## Gaps

[none yet]
