# PROJECT.md

> 本文件基于仓库现有两份文档（README.md、FocusFlow技术方案与项目结构.md）进行归纳，作为后续规划与实施的统一入口。

## 1. 项目是什么（What This Is）
- 面向单人效率的「智能精力排期系统」（FocusFlow）。
- 目标：在 1–2 周内实现 V1.0 可演示的完整闭环。
- 闭环：待办录入 → 生成 3 套今日排期方案 → 选择方案 → 日历查看 → 执行反馈。

## 2. 核心价值（Core Value）
- 在有限时间与精力曲线下，给出今日最可执行且可解释的安排，显著降低手动排期成本。

## 3. 范围与优先级（Scope & Priorities）
- 以 README 的 P0/P1 列表为裁剪依据：
  - P0：底座初始化、数据模型、基础 CRUD、调度核心（槽生成/依赖/评分/不可拆分放置/三方案/风险）、前端（任务列表/日历/方案选择）、精力模板与 blocked time。
  - P1：可拆分放置、重新优化、冲突校验、执行反馈、AI 任务输入、基础测试与演示数据。
  - P2+：延后。

## 4. 目标架构（Target Architecture）
- 前端：React + TypeScript + Vite + Router + Zustand + Tailwind + FullCalendar + ECharts + RHF/Zod。
- 后端：FastAPI + SQLAlchemy 2 + Pydantic v2 + SQLite（MVP）+ Alembic；NetworkX、NumPy 用于调度。
- 服务边界：后端提供 REST API；调度引擎作为后端的独立模块由服务层编排。

## 5. 核心数据模型（Domain Models）
- projects、tasks、task_dependencies、energy_templates、energy_template_slots、blocked_times、schedule_plans、schedule_items、execution_logs。
- 关键字段见 README：任务时长、认知负荷、截止时间、依赖、是否可拆、最早开始/固定开始等。

## 6. 关键接口（APIs 概览）
- CRUD：/projects、/tasks、/energy/templates、/blocked-times。
- 排期：/schedules/generate（一次 3 方案）、/schedules/select、/schedules/reoptimize、/schedules/validate-move。
- 执行：/execution/logs、/execution/today。

## 7. 调度引擎（概要）
- 输入：待办、能量曲线、blocked、day type。
- 步骤：依赖校验 → 48 槽生成 → 任务优先级排序 → 放置（先不可拆，后可拆 ≤3 段）→ 风险/warnings → 三方案（conservative/balanced/aggressive）。
- 评分：匹配度 + 紧迫度 + 连续性 − 超时与碎片化惩罚。

## 8. 成功标准（Success Criteria）
- 通过 README 的 M1–M5 里程碑验收标准。
- 本地可运行、能生成 3 方案并选择、前端能展示并提交执行反馈。

## 9. 非目标（Out of Scope for V1）
- 登录/多用户/云同步、第三方日历与任务同步、复杂学习型算法、桌面端。

## 10. 风险与约束（Risks & Constraints）
- 单人/短周期：避免过早优化与复杂算法；先跑通闭环。
- 可视化依赖：FullCalendar/ECharts 的集成复杂度需预留缓冲。

## 11. 下一步（Next）
- 依据 ROADMAP 分阶段推进：先完成 P0 底座与核心闭环，再做 P1 提升。
