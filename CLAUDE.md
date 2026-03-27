# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 仓库现状

- 本仓库当前仅包含规划/方案文档，尚未有可运行的前后端代码或依赖配置。
- 根目录存在：
  - README.md（MVP 目标与分阶段任务）
  - FocusFlow技术方案与项目结构.md（技术选型、目标架构、模块边界、数据模型与接口草案、调度引擎方案）
- 未发现 package.json、pyproject.toml、requirements.txt、go.mod、.cursor/.cursorrules 或现有 CLAUDE.md。
- 结论：暂时没有可验证的“构建/启动/测试”命令。

## 重要文档入口

- README.md：阐明 MVP 的业务闭环与优先级，用于把握“先跑通闭环”的范围。
- FocusFlow技术方案与项目结构.md：给出目标技术栈与清晰的模块边界，是未来落地实现的主参照文件。

## 目标架构（规划中，非当前实现）

前后端分离 + 统一后端服务层 + 调度引擎：
- 前端（计划）：React + TypeScript + Vite，路由（React Router），状态（Zustand），UI（日历 FullCalendar、曲线 ECharts），表单（React Hook Form + Zod）。
- 后端（计划）：FastAPI + SQLAlchemy 2 + Pydantic v2 + SQLite（MVP）+ Alembic；图与数值工具 NetworkX/NumPy；服务层调用调度引擎并对外提供 REST API。
- 调度引擎（计划）：
  - 依赖图校验（建图/拓扑/环检测）
  - 时间槽生成（48×30 分钟槽，叠加精力值与 blocked time）
  - 启发式排期与评分（deadline/项目优先级/认知负荷/连续性/惩罚项）
  - 三方案生成（conservative/balanced/aggressive 参数变体）
  - 冲突校验（blocked/依赖/重叠/截止）

业务闭环（规划）：“待办录入 → 生成 3 套今日排期 → 选择方案 → 今日执行反馈”。

## 领域模型要点（规划中）

- 项目 projects（含优先级）
- 任务 tasks（时长、认知负荷、截止时间、可拆分、最早开始、固定开始、状态等）
- 任务依赖 task_dependencies（前置关系）
- 精力模板 energy_templates + energy_template_slots（工作日/周末 + 48 槽能量值）
- 不可排时间段 blocked_times（sleep/class/custom）
- 排期方案 schedule_plans + schedule_items（方案类型/得分/风险/是否 selected）
- 执行日志 execution_logs（实际开始/结束/用时/状态/主观状态）

## 核心接口表面（规划中）

- 任务/项目 CRUD：GET/POST/PUT/DELETE /tasks，GET/POST /projects
- 精力模板与 blocked time：GET/PUT /energy/templates，GET/POST/DELETE /blocked-times
- 生成排期：POST /schedules/generate（一次返回三方案 + 可牺牲任务建议）
- 选择方案：POST /schedules/select
- 拖拽校验：POST /schedules/validate-move
- 重新优化：POST /schedules/reoptimize
- 执行反馈：POST /execution/logs，GET /execution/today

以上为“目标接口”，当前尚未实现。

## 调度引擎方法（规划中）

- 输入：候选任务、blocked time、能量曲线、day type
- 流程：过滤 → 依赖校验建图 → 生成时间槽 → 任务优先级排序 → 放置（不可拆/可拆 ≤3 段）→ 输出 warnings → 依据不同参数生成三方案
- 评分：匹配度 + 紧迫度 + 连续性 − 超时惩罚 − 碎片化惩罚

## 开发命令与运行（当前状态）

- 现状：仓库暂无可执行的构建/运行/测试命令。
- 待补充清单（完成初始化后请回填具体命令）：
  - 前端：开发/构建/单测/单测过滤（例如 dev/build/test/test:one）
  - 后端：启动（本地 uvicorn）、依赖安装、数据库迁移（Alembic）、单测
  - 端到端：本地前后端联调方式与环境变量说明

建议：当创建 frontend/ 与 backend/ 目录并完成最小可运行骨架后，立刻在本节补充真实命令与关键环境变量。

## 给未来 Claude 的注意事项（与本仓库强相关）

- 区分“规划”与“现状”：当前只有文档，不要假设任一模块已存在。
- 若需要开始实现：按方案文档的模块边界落地最小可运行骨架（前/后端与调度引擎壳），再逐步补全。
- 任何脚手架/初始化完成后，请更新本文件“开发命令与运行”一节，便于后续实例快速介入。
