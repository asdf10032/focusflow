# REQUIREMENTS.md

> 本文件将 README 中的任务拆分为可跟踪需求（REQ-IDs），用于路线图与测试覆盖映射。

## 版本范围
- V1.0（当前目标）：跑通完整闭环，可演示。

## 功能需求
- REQ-PROJ-CRUD: 用户可创建/查询项目，支持优先级字段。
- REQ-TASK-CRUD: 用户可增删改查任务，含依赖、截止、是否可拆分等字段。
- REQ-ENERGY: 系统提供能量模板（weekday/weekend）与 48 槽曲线读写。
- REQ-BLOCKED: 用户可配置 blocked time（上课/睡觉/自定义）。
- REQ-SCHEDULE-3PLANS: 一次生成 conservative/balanced/aggressive 三套今日方案。
- REQ-SCHEDULE-SELECT: 可选择方案并标记 selected，前端可读取。
- REQ-SCHEDULE-VALIDATE: 拖拽后支持 validate-move 冲突检测（P1）。
- REQ-SCHEDULE-REOPT: 支持重新优化的接口（P1）。
- REQ-EXECUTION: 今日执行页展示与反馈提交（P1）。
- REQ-AI-PARSE: 自然语言解析任务字段（P1）。
- REQ-CALENDAR-VIEW: 日历页展示任务块并可切换方案。
- REQ-DEFAULT-SEEDS: 初始化后存在默认能量模板（early_bird/normal/night_owl）。

## 非功能需求
- NFR-API: 统一响应格式（status/data/error/meta）。
- NFR-VALIDATION: 严格的输入校验（Pydantic v2 / Zod）。
- NFR-TEST: 后端核心单测 + 基础联调，80% 覆盖为目标（逐步达成）。
- NFR-UX: 前端交互清晰，冲突提示明确。

## 验收与溯源
- 每个接口在 E2E 清单中有可见验证步骤。
- 关键需求映射至 ROADMAP 阶段与里程碑。
