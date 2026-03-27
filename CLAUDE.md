# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

---

## 仓库现状

- 本仓库包含规划/方案文档与最小后端骨架（FastAPI + SQLAlchemy + Alembic），前端尚未初始化。
- 根目录存在：
  - README.md（MVP 目标与分阶段任务）
  - FocusFlow技术方案与项目结构.md（技术选型、目标架构、模块边界、数据模型与接口草案、调度引擎方案）
  - backend/（后端代码）
  - alembic/（数据库迁移）
- 结论：当前可启动后端与执行迁移，前端与端到端联调未就绪。

## 重要文档入口

- README.md：阐明 MVP 的业务闭环与优先级，用于把握“先跑通闭环”的范围。
- FocusFlow技术方案与项目结构.md：目标技术栈与清晰的模块边界，是未来落地实现的主参照文件。
- .planning/*：PROJECT/REQUIREMENTS/ROADMAP/STATE/TASKS 统一规划入口。

## 开发命令与运行（后端当前可用）

- Python 环境（建议 3.11+）：
  - 创建虚拟环境：
    - Windows PowerShell（推荐）：`python -m venv .venv; . .venv/Scripts/Activate.ps1`
    - Bash：`python -m venv .venv && . .venv/Scripts/activate`
  - 安装依赖：`pip install fastapi uvicorn sqlalchemy alembic pydantic`
- 初始化数据库（SQLite）：
  - `alembic upgrade head`
- 启动后端：
  - `uvicorn backend.app.main:app --reload`
- 快速联调：
  - 健康检查：GET `http://localhost:8000/api/v1/health`
  - 项目：GET/POST `http://localhost:8000/api/v1/projects`
  - 任务：GET/POST/PUT/DELETE `http://localhost:8000/api/v1/tasks`
  - 模板：GET/PUT `http://localhost:8000/api/v1/energy/templates`
  - 不可排：GET/POST/DELETE `http://localhost:8000/api/v1/blocked-times`
- 可选：写入默认能量模板（幂等）
  - `python -m backend.app.services.seeds.energy_templates`

## 目标架构（规划中，非当前实现）

前后端分离 + 统一后端服务层 + 调度引擎：
- 前端（计划）：React + TypeScript + Vite，路由（React Router），状态（Zustand），UI（日历 FullCalendar、曲线 ECharts），表单（React Hook Form + Zod）。
- 后端（已起步）：FastAPI + SQLAlchemy 2 + Pydantic v2 + SQLite（MVP）+ Alembic；图与数值工具 NetworkX/NumPy（待引入）；服务层调用调度引擎并对外提供 REST API。
- 调度引擎（计划）：
  - 依赖图校验（建图/拓扑/环检测）
  - 时间槽生成（48×30 分钟槽，叠加精力值与 blocked time）
  - 启发式排期与评分（deadline/项目优先级/认知负荷/连续性/惩罚项）
  - 三方案生成（conservative/balanced/aggressive 参数变体）
  - 冲突校验（blocked/依赖/重叠/截止）

业务闭环（规划）：“待办录入 → 生成 3 套今日排期 → 选择方案 → 日历查看 → 执行反馈”。

## 领域模型要点（现状/规划）

- 已建表：projects、tasks、task_dependencies、energy_templates、energy_template_slots、blocked_times、schedule_plans、schedule_items。
- 计划补充：execution_logs。

## 核心接口表面（现状/规划）

- 现状（已提供）：
  - 项目/任务 CRUD：GET/POST/PUT/DELETE /tasks，GET/POST /projects
  - 精力模板与 blocked time：GET/PUT /energy/templates，GET/POST/DELETE /blocked-times
- 规划：
  - 生成排期：POST /schedules/generate（一次返回三方案 + 可牺牲任务建议）
  - 选择方案：POST /schedules/select
  - 拖拽校验：POST /schedules/validate-move
  - 重新优化：POST /schedules/reoptimize
  - 执行反馈：POST /execution/logs，GET /execution/today

## 给未来 Claude 的注意事项

- 区分“已实现”与“规划中”：不要假设调度引擎已就绪。
- 若继续实现：遵循 .planning/ROADMAP 与 TASKS，先补后端 P0 能力（调度核心壳），再前端壳与联调。
- 修改/删除/重构前先给出变更计划，获批后执行。
