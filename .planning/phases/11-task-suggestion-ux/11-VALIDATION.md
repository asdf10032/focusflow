# Phase 11 Validation: Task Suggestion UX

## Scope

Phase 11 makes the Phase 10 duration suggestion backend usable in the existing Tasks page. It should add frontend API typing, suggestion display, accept/manual override behavior, parse-task suggestion metadata, and Chinese/English copy. It should not add new backend learning behavior or demo seed changes.

## Acceptance Checks

- Tasks page can request a duration suggestion for the current form title, project, cognitive load, and estimate.
- Suggestions display suggested minutes, confidence, sample count, source, and localized reason text.
- Suggestions never overwrite `estimated_minutes` automatically.
- User can explicitly accept a suggestion into the minutes field and then edit the value manually.
- Parse-task flow fills the task form and also fetches/displays duration suggestion metadata for the parsed draft.
- Existing create/edit/delete task behavior remains compatible.
- All new UI text is covered in Chinese and English translation dictionaries.
- Phase 11 does not add migrations, external LLM calls, network dependencies beyond the local API, or scheduler scoring changes.

## Required Verification

Run from the repository root unless noted:

```powershell
python -m pytest tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py -q -p no:cacheprovider
```

Run from `frontend/`:

```powershell
npm.cmd run build
```

## Manual UI Sanity

1. Start backend and frontend with Phase 10 available.
2. Open Tasks.
3. Enter a task title/load/estimate and request a duration suggestion.
4. Confirm the suggestion appears without changing the minutes field.
5. Accept the suggestion and confirm minutes updates.
6. Edit minutes manually afterward.
7. Use Quick Parse and confirm a suggestion appears for the parsed draft.
