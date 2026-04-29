# Phase 11 Summary: Task Suggestion UX

**Completed:** 2026-04-30

## Outcome

Phase 11 made duration suggestions usable from the Tasks page while keeping the Phase 10 backend behavior unchanged.

## Implemented

- Added a typed frontend client for `POST /api/v1/ai/suggest-duration`.
- Added Chinese and English copy for duration suggestion controls, metadata, errors, and deterministic reason codes.
- Added a localized reason-label helper with backend-reason fallback for unknown future codes.
- Added a Tasks page suggestion panel showing suggested minutes, confidence, sample count, source, and reason.
- Added explicit accept behavior that writes the suggested minutes into the form only when the user chooses it.
- Kept manual override behavior intact by allowing the minutes field to be edited after accepting a suggestion.
- Extended Quick Parse so parsed drafts also request and display duration suggestion metadata.

## Verification

- `python -m pytest tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py -q -p no:cacheprovider`
- `npm.cmd run build` from `frontend/`

## Notes

- No migrations, scheduler scoring changes, external LLM calls, or backend learning changes were added in Phase 11.
- The task form does not currently expose `project_id`, so the frontend sends title, cognitive load, and estimated minutes for suggestions.
