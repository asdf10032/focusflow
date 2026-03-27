# TASKS.md

> Phase 1（底座打通）任务分解与验收清单；映射 REQUIREMENTS 与里程碑。

## 1. 后端骨架（FastAPI）
- 目标：可本地启动的最小后端；统一响应封装；基础异常处理。
- 产出：backend/ 目录与最小 app；uvicorn 启动脚本（文档占位，暂不实现）。
- 映射：NFR-API、REQ-PROJ-CRUD/REQ-TASK-CRUD 的接口承载层。
- 验收：本地可启动，GET /health 返回 { status: 'ok' }。

## 2. 数据模型与迁移（SQLite + SQLAlchemy + Alembic）
- 表：projects、tasks、task_dependencies、energy_templates、energy_template_slots、blocked_times、schedule_plans、schedule_items。
- 产出：迁移脚手架与首批迁移脚本（文档占位，暂不实现）。
- 映射：REQ-PROJ-CRUD、REQ-TASK-CRUD、REQ-ENERGY、REQ-BLOCKED、REQ-SCHEDULE-3PLANS。
- 验收：迁移可执行，表结构与 README 对齐。

## 3. 默认数据种子（能量模板）
- 模板：early_bird、normal、night_owl（48 槽）。
- 产出：种子脚本与调用入口（文档占位，暂不实现）。
- 映射：REQ-DEFAULT-SEEDS、REQ-ENERGY。
- 验收：初始化后模板数据存在。

## 4. 基础 CRUD 接口
- Projects：GET /projects、POST /projects。
- Tasks：GET/POST/PUT/DELETE /tasks。
- Energy Templates：GET /energy/templates、PUT /energy/templates/{id}。
- Blocked Times：GET/POST/DELETE /blocked-times。
- 产出：路由定义、DTO/校验模型（Pydantic v2），统一响应。
- 映射：REQ-PROJ-CRUD、REQ-TASK-CRUD、REQ-ENERGY、REQ-BLOCKED、NFR-VALIDATION。
- 验收：Postman/HTTPie 联调清单通过；错误返回不泄漏内部细节。

## 5. 调度引擎壳（占位）
- 模块：slots、graph、score、place（不可拆）。
- 产出：纯函数接口定义与 TODO（中文注释说明设计意图）。
- 映射：REQ-SCHEDULE-3PLANS 的先决条件。
- 验收：单元测试可导入模块并调用空实现（后续补逻辑）。

## 6. 前端最小骨架（占位）
- tech：React+TS+Vite、Router、Zustand、Tailwind。
- 页面：任务列表（空壳）、日历页（挂载点）。
- 映射：REQ-CALENDAR-VIEW、REQ-TASK-CRUD 的承载层。
- 验收：npm run dev 可打开空页面（后续补组件与 API）。

## 7. 质量与文档
- 更新仓库 CLAUDE.md 的“开发命令与运行”在骨架建立后补全。
- 为关键模块添加中文注释与错误处理约定（按 coding-style）。
- 初始测试清单草案（后端核心 + 联调路径）。

## 检查清单（Phase 1 完成判定）
- [ ] 后端可启动（/health ok）
- [ ] Alembic 首迁移执行成功
- [ ] 基础 CRUD 全部可用
- [ ] 默认能量模板写入成功
- [ ] 前端可启动并可访问 API
- [ ] 统一响应与输入校验生效
- [ ] 文档更新（CLAUDE.md 命令区）
