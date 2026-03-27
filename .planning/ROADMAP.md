# ROADMAP.md

 本文件给出从「底座」到「闭环」的分阶段推进方案，并映射 REQ-IDs。

## Phase 0 — 开工准备（1 天）
- 建仓库、确定目录结构、最小 README（参考仓库已具备）。

## Phase 1 — 底座打通（P0）
- 后端：FastAPI 骨架、SQLAlchemy/SQLite、Alembic、统一响应（NFR-API）
- 数据：projects/tasks/task_dependencies/energy_templates/energy_template_slots/blocked_times/schedule_plans/schedule_items 迁移
- 接口：/projects、/tasks、/energy/templates、/blocked-times
- 对应：REQ-PROJ-CRUD、REQ-TASK-CRUD、REQ-ENERGY、REQ-BLOCKED、REQ-DEFAULT-SEEDS

## Phase 2 — 调度最小闭环（P0）
- 引擎：槽生成、依赖校验、优先级评分、不可拆分放置、三方案生成、风险提示
- 接口：/schedules/generate、/schedules/select
- 对应：REQ-SCHEDULE-3PLANS、REQ-SCHEDULE-SELECT、NFR-TEST（核心单测）

## Phase 3 — 前端主流程（P0）
- 页面：任务列表、日历（FullCalendar）、方案切换/选择
- 对应：REQ-CALENDAR-VIEW、REQ-TASK-CRUD、REQ-SCHEDULE-SELECT

## Phase 4 — 可用性增强（P1）
- 引擎/接口：validate-move、reoptimize、可拆分放置
- 前端：今日执行页、冲突/风险提示、AI 输入组件
- 对应：REQ-SCHEDULE-VALIDATE、REQ-SCHEDULE-REOPT、REQ-EXECUTION、REQ-AI-PARSE

## Phase 5 — 打磨与演示（P1）
- 测试：联调流程覆盖、演示数据、README 补全
- 对应：NFR-TEST、NFR-UX

## 里程碑（Milestones）
- M1：数据层完成（README 验收项）
- M2：排期核心完成（可返回 3 方案）
- M3：前端闭环完成（日历展示 + 方案选择）
- M4：执行反馈完成（今日执行页可提交）
- M5：演示版完成（AI 任务输入 + demo 数据）
