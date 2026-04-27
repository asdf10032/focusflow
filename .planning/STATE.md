# STATE.md

- Current goal: V1.0 (complete the demoable scheduling loop).
- Current position: Phase 5 (Demo Polish) is next.
- Last completed: Phase 4 / Plans 01-02 on 2026-04-26.
- Focus: prepare demo data, docs, smoke tests, and presentation-ready flow.
- Next action: run `$gsd-discuss-phase 5` or `$gsd-plan-phase 5 --skip-research`.

## Recent Decisions

- Foundation endpoints return the documented `status/data/error/meta` envelope.
- Phase work is tracked under `.planning/phases/*` using GSD PLAN/SUMMARY artifacts.
- Schedule generation persists same-day plans and `/schedules/select` maintains one selected plan per date.
- Scheduler orders dependencies, rejects dependency cycles, and reports unplaced tasks with warnings/risk/score.
- Frontend uses a typed API client for task CRUD and schedule generate/select calls.
- Task and calendar pages form the MVP loop: manage tasks, generate three variants, switch variants, inspect items, and select a plan.
- Vite uses `postcss.config.cjs` so Tailwind utilities are emitted in production builds.
- UI localization is intentionally lightweight: `frontend/src/lib/i18n.ts` owns `zh-CN` and `en` dictionaries, Zustand owns current language state, and `localStorage` persists the selected language.
- Phase 4 added backend APIs for validate-move, reoptimize, today execution, execution feedback, and local deterministic task parsing.
- Phase 4 frontend added a Today page, task draft parser, calendar reoptimization, and calendar move-validation controls.

## Accumulated Context

### Roadmap Evolution

- Phase 03.1 inserted after Phase 3: Bilingual UI Toggle (URGENT).
- Phase 4 completed the usability enhancement loop without adding a database migration.

## Blockers

- None known.

## Verification Baseline

- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider`
- `python -m compileall backend alembic`
- `npm.cmd run build`
