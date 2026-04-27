# STATE.md

- Current goal: V1.0 (complete the demoable scheduling loop).
- Current position: Phase 5 (Demo Polish) is complete.
- Last completed: Phase 5 / Plans 01-02 on 2026-04-27.
- Focus: verify the local demo, then decide whether to complete the V1.0 milestone or plan V1.1.
- Next action: run `$gsd-verify-work` or `$gsd-complete-milestone`.

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
- Phase 5 added repeatable non-destructive demo data seeding, a full demo-flow smoke test, and README startup/demo instructions.

## Accumulated Context

### Roadmap Evolution

- Phase 03.1 inserted after Phase 3: Bilingual UI Toggle (URGENT).
- Phase 4 completed the usability enhancement loop without adding a database migration.
- Phase 5 completed the V1.0 demo polish without adding a database migration or destructive reset.

## Blockers

- None known.

## Verification Baseline

- `python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider`
- `python -m pytest tests/test_demo_flow.py -q -p no:cacheprovider`
- `python -m compileall backend alembic`
- `npm.cmd run build`
