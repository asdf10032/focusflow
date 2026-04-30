## FocusFlow v1.2 本地演示

FocusFlow 是一个本地优先的智能精力排期 MVP：录入任务，生成三套日程方案，选择今日计划，提交执行反馈，并用执行历史为新任务提供可解释的时长建议。下面命令默认从仓库根目录运行。

### 后端启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings pytest
alembic upgrade head
python -m backend.app.services.seeds.demo_data --date 2026-04-30
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

`demo_data` 是可重复、非破坏性的演示种子：它会补齐默认精力模板，upsert 演示项目和任务，创建 blocked time，生成三套排期，选择 balanced 方案，并写入带项目/认知负荷快照的执行历史。省略 `--date` 时默认使用今天。

### 前端启动

```powershell
cd frontend
npm install
npm.cmd run dev
npm.cmd run build
```

开发服务默认访问 `http://127.0.0.1:5173/`。

### v1.2 演示路径

1. Tasks：输入类似 `Prepare slide talking points` 的标题，点击时长建议，确认出现 history 来源、高置信度和样本数。
2. Tasks：点击使用建议，确认分钟数字段更新；再手动改分钟数，确认仍可覆盖。
3. Tasks：输入一个全新标题，例如 `Plan a new workshop`，确认 fallback 建议可解释。
4. Quick Parse：输入 `Polish demo script 45min medium`，确认表单填充并出现建议区域。
5. Calendar：生成或重新优化计划，查看三套方案与说明，选择 balanced 方案。
6. Today：查看选中的今日工作，提交反馈、实际分钟数和备注。
7. Daily Review：选择同一日期，确认执行历史、完成率、实际用时和估算偏差可见。

### 验证

```powershell
python -m pytest tests/test_demo_flow.py tests/test_phase10_duration_suggestions.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_demo_flow.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase10_duration_suggestions.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
cd frontend
npm.cmd run build
```

---

## 快速启动与 v1.1 本地演示

FocusFlow 是一个本地 Web MVP：录入任务，生成三套今日排期方案，选择方案，在 Today 提交反馈，并在 Daily Review 查看执行历史、进度和估算偏差。下面命令默认从仓库根目录运行。

### 后端启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings pytest
alembic upgrade head
python -m backend.app.services.seeds.demo_data --date 2026-04-27
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

`demo_data` 是可重复、非破坏性的演示种子：它会补齐默认精力模板、创建或更新一个演示项目和任务、写入演示日期的 blocked time、生成三套排期、默认选择 balanced 方案，并写入可复盘的执行历史。它不会清空已有数据。省略 `--date` 时默认使用今天。

### 前端启动

```powershell
cd frontend
npm install
npm.cmd run dev
```

开发服务默认访问 `http://127.0.0.1:5173/`。

### v1.1 演示路径

1. Tasks：查看演示任务，使用状态/项目筛选，也可以用文本解析填充任务表单。
2. Calendar：生成排期，查看 conservative / balanced / aggressive 三套方案、方案说明和风险说明。
3. Select Plan：选择 balanced 或当前想演示的方案。
4. Today：查看今日选中工作流和进度指标。
5. Feedback：把一项任务标记为完成或其他状态，填写实际用时/备注后提交。
6. Daily Review：选择同一日期，确认 seeded execution history、完成率、实际用时和估算偏差已经可见。

### 验证

```powershell
python -m pytest tests/test_demo_flow.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_demo_flow.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
cd frontend
npm.cmd run build
```

---

**可执行的开发任务清单 + 优先级表**，按你的项目现状拆成：

1. **第一版 MVP 开发任务清单**
2. **优先级表**
3. **建议开发顺序**
4. **后续版本路线图**
5. **里程碑与验收标准**

我会按你当前目标来定基线：

* **单人开发**
* **1–2 周完成第一版**
* **Web 优先**
* **先做完整闭环，不先堆高级算法**

---

# 一、优先级定义

为了方便你排期，我统一用这套优先级：

* **P0**：必须做，不做项目不能成立
* **P1**：强烈建议做，会显著提升可用性/演示效果
* **P2**：增强项，第一版时间够再做
* **P3**：后续规划项，第一版不要碰

---

# 二、第一版 MVP 总目标

## MVP 闭环

**待办录入 → 生成 3 个今日排期方案 → 选择方案 → 日历查看 → 执行反馈**

## 第一版必须交付的页面

* 任务列表页
* 日历页
* 今日执行页

## 第一版必须交付的能力

* 系统内部待办池
* 精力模板与微调
* blocked time（上课 / 睡觉）
* 3 套今日排期方案
* 方案选择
* 拖拽冲突检测
* 手动重新优化
* AI 自然语言录入任务
* 执行反馈记录

---

# 三、第一版开发任务清单（按模块拆解）

---

## 模块 A：项目基础设施

### A1. 初始化前端项目

* 内容：

  * 创建 React + TypeScript + Vite 项目
  * 配置 Tailwind CSS
  * 配置 Router
  * 配置 Zustand
  * 配置 API 请求层
* 优先级：**P0**
* 依赖：无
* 验收：

  * 项目可启动
  * 有基础路由
  * 可正常请求后端接口

### A2. 初始化后端项目

* 内容：

  * 创建 FastAPI 项目
  * 配置 SQLAlchemy
  * 配置 SQLite
  * 配置 Alembic
  * 配置基础 settings / env
* 优先级：**P0**
* 依赖：无
* 验收：

  * 后端可启动
  * 数据库连接正常
  * Alembic 可迁移

### A3. 建立基础目录结构与规范

* 内容：

  * 前后端目录拆分
  * 命名规范
  * 通用响应格式
  * 错误处理规范
* 优先级：**P1**
* 验收：

  * 项目结构清晰
  * API 风格统一

---

## 模块 B：数据库与数据模型

### B1. 项目表设计与迁移

* 表：

  * `projects`
* 优先级：**P0**
* 验收：

  * 可创建项目
  * 支持项目优先级字段

### B2. 任务表设计与迁移

* 表：

  * `tasks`
* 字段：

  * title
  * estimated_minutes
  * cognitive_load
  * due_at
  * earliest_start_at
  * fixed_start_at
  * is_splittable
  * max_split_count
  * status
  * project_id
* 优先级：**P0**
* 验收：

  * 任务模型支持核心字段
  * 可正常增删改查

### B3. 任务依赖表设计与迁移

* 表：

  * `task_dependencies`
* 优先级：**P0**
* 验收：

  * 一个任务可绑定多个依赖
  * 数据能正确关联

### B4. 精力模板表设计与迁移

* 表：

  * `energy_templates`
  * `energy_template_slots`
* 优先级：**P0**
* 验收：

  * 支持 weekday / weekend
  * 支持 48 个 slot

### B5. blocked time 表设计与迁移

* 表：

  * `blocked_times`
* 优先级：**P0**
* 验收：

  * 可记录上课 / 睡觉时间段

### B6. 排期结果表设计与迁移

* 表：

  * `schedule_plans`
  * `schedule_items`
* 优先级：**P0**
* 验收：

  * 能存 3 套方案
  * 能标记 selected

### B7. 执行反馈表设计与迁移

* 表：

  * `execution_logs`
* 优先级：**P1**
* 验收：

  * 能记录完成状态、用时、主观状态

---

## 模块 C：后端基础 CRUD 接口

### C1. 项目 CRUD

* 接口：

  * `GET /projects`
  * `POST /projects`
* 优先级：**P0**
* 验收：

  * 可创建和查询项目

### C2. 任务 CRUD

* 接口：

  * `GET /tasks`
  * `POST /tasks`
  * `PUT /tasks/{id}`
  * `DELETE /tasks/{id}`
* 优先级：**P0**
* 验收：

  * 可维护待办池
  * 支持依赖、截止时间、可拆分等字段

### C3. 精力模板接口

* 接口：

  * `GET /energy/templates`
  * `PUT /energy/templates/{id}`
* 优先级：**P0**
* 验收：

  * 可读写精力曲线数据

### C4. blocked time 接口

* 接口：

  * `GET /blocked-times`
  * `POST /blocked-times`
  * `DELETE /blocked-times/{id}`
* 优先级：**P0**
* 验收：

  * 可配置当天不可安排时段

### C5. 执行反馈接口

* 接口：

  * `POST /execution/logs`
  * `GET /execution/today`
* 优先级：**P1**
* 验收：

  * 可提交和查询今日反馈

---

## 模块 D：调度引擎（第一版核心）

### D1. 时间槽生成器

* 内容：

  * 将一天切成 48 个 30 分钟 slot
  * 写入精力值
  * 标记 blocked slots
* 优先级：**P0**
* 验收：

  * 给定日期后能正确生成可用槽位数组

### D2. 依赖图构建与环检测

* 内容：

  * 用 NetworkX 构建任务图
  * 检测循环依赖
  * 支持多个依赖
* 优先级：**P0**
* 验收：

  * 有环时返回错误
  * 无环时能获得合法顺序

### D3. 任务优先级评分函数

* 内容：

  * 基于 deadline、project priority、cognitive load、split penalty 计算 priority
* 优先级：**P0**
* 验收：

  * 评分函数可输出稳定排序结果

### D4. 任务放置器（不可拆分）

* 内容：

  * 找连续可用区间
  * 匹配精力与认知负荷
  * 放入最优区间
* 优先级：**P0**
* 验收：

  * 不可拆分任务能被安排到合法连续时间段

### D5. 任务放置器（可拆分）

* 内容：

  * 支持按 30 分钟拆分
  * 最多 3 段
  * 优先连续安排
  * 允许跨天，但第一版“今日排期”里建议只给出今日部分并标风险
* 优先级：**P1**
* 验收：

  * 可拆分任务能分成不超过 3 段
  * 连续性优先成立

### D6. 截止时间惩罚与风险提示

* 内容：

  * 晚于 due_at 的任务标记 is_late
  * 无法排入或高风险任务单独输出 warnings
* 优先级：**P0**
* 验收：

  * 可输出 late 信息和 warning 列表

### D7. 三方案参数配置

* 内容：

  * conservative / balanced / aggressive 三套参数
* 优先级：**P0**
* 验收：

  * 生成结果存在明显差异
  * 每种方案都有 plan_type

### D8. 统一生成排期接口

* 接口：

  * `POST /schedules/generate`
* 优先级：**P0**
* 验收：

  * 一次返回 3 套方案
  * 可返回 sacrificable_tasks 建议

### D9. 方案选择接口

* 接口：

  * `POST /schedules/select`
* 优先级：**P0**
* 验收：

  * 用户可选择执行方案
  * 选中的方案能被今日执行页读取

### D10. 重新优化接口

* 接口：

  * `POST /schedules/reoptimize`
* 优先级：**P1**
* 验收：

  * 用户点击后能重新生成结果

---

## 模块 E：AI 任务输入

### E1. AI 服务抽象层

* 内容：

  * 定义统一 parser interface
  * 支持 mock provider
  * 预留真实 LLM provider
* 优先级：**P1**
* 验收：

  * 切换 provider 不影响业务层

### E2. 自然语言解析接口

* 接口：

  * `POST /ai/parse-task`
* 优先级：**P1**
* 验收：

  * 输入一句话可返回结构化任务字段

### E3. AI 结果确认写入流程

* 内容：

  * 前端拿到解析结果
  * 用户确认后再创建任务
* 优先级：**P1**
* 验收：

  * 不会未经确认直接入库

### E4. AI 参与排期参数建议

* 内容：

  * AI 可建议认知负荷/是否可拆分/大致 urgency
  * 最终仍由调度引擎执行
* 优先级：**P2**
* 验收：

  * 参数建议可被使用但不破坏主逻辑

---

## 模块 F：前端页面——任务列表页

### F1. 任务列表展示

* 内容：

  * 展示任务标题、时长、项目、截止时间、状态
* 优先级：**P0**
* 验收：

  * 列表可正确展示数据

### F2. 任务创建表单

* 内容：

  * 标题、时长、认知负荷、项目、截止时间、依赖、是否可拆分
* 优先级：**P0**
* 验收：

  * 能创建任务并写入数据库

### F3. 任务编辑 / 删除

* 优先级：**P0**
* 验收：

  * 可编辑和删除已有任务

### F4. AI 输入组件

* 内容：

  * 文本输入
  * 解析按钮
  * 结构化确认弹窗
* 优先级：**P1**
* 验收：

  * AI 解析后用户可确认创建

### F5. 任务筛选

* 内容：

  * 状态筛选
  * 项目筛选
* 优先级：**P2**
* 验收：

  * 可按基础条件筛选

---

## 模块 G：前端页面——日历页

### G1. 生成排期按钮与方案加载

* 优先级：**P0**
* 验收：

  * 点击后成功拉取 3 套方案

### G2. 方案切换组件

* 内容：

  * 稳妥型 / 平衡型 / 冲刺型 tabs
* 优先级：**P0**
* 验收：

  * 能切换查看不同方案

### G3. 日历展示组件

* 内容：

  * 基于 FullCalendar 的日视图
* 优先级：**P0**
* 验收：

  * 正确展示任务块

### G4. 方案选择按钮

* 优先级：**P0**
* 验收：

  * 用户可将某个方案设为 selected

### G5. 冲突检测

* 内容：

  * 拖拽后请求 `validate-move`
* 优先级：**P1**
* 验收：

  * 冲突时给出明确提示

### G6. 重新优化按钮

* 优先级：**P1**
* 验收：

  * 拖拽后可触发重新计算

### G7. 风险提示区

* 内容：

  * warnings
  * sacrificable_tasks
* 优先级：**P1**
* 验收：

  * 用户能看到高风险任务和建议牺牲任务

---

## 模块 H：前端页面——今日执行页

### H1. 今日任务流展示

* 内容：

  * 当前任务
  * 下一个任务
  * 今日完成进度
* 优先级：**P1**
* 验收：

  * 用户能清楚知道现在该做什么

### H2. 执行反馈表单

* 内容：

  * 完成 / 未完成
  * 实际开始结束时间
  * 实际用时
  * 主观状态
* 优先级：**P1**
* 验收：

  * 能提交反馈数据

### H3. 今日历史记录展示

* 优先级：**P2**
* 验收：

  * 能查看已提交的反馈

---

## 模块 I：精力模板与 blocked time 页面/组件

### I1. 默认模板 seed

* 内容：

  * early_bird
  * normal
  * night_owl
* 优先级：**P0**
* 验收：

  * 初始化后数据库里存在模板数据

### I2. 模板选择器

* 优先级：**P0**
* 验收：

  * 用户可切换模板

### I3. 曲线编辑器

* 内容：

  * 48 个点或折线编辑
* 优先级：**P1**
* 验收：

  * 可微调并保存

### I4. blocked time 编辑器

* 内容：

  * 添加上课 / 睡觉时段
* 优先级：**P0**
* 验收：

  * 能新增和删除 blocked time

---

## 模块 J：测试与稳定性

### J1. 后端单元测试

* 覆盖：

  * 环检测
  * slot 生成
  * 不可拆分任务放置
  * 可拆分任务放置
  * validate-move
* 优先级：**P1**
* 验收：

  * 核心逻辑有基础测试

### J2. 前端基础联调测试

* 覆盖：

  * 创建任务
  * 生成计划
  * 选择方案
  * 提交反馈
* 优先级：**P1**
* 验收：

  * 主闭环无阻塞

### J3. 演示数据与 Demo 场景

* 内容：

  * 预置大学生/考研党任务样例
* 优先级：**P1**
* 验收：

  * 可直接用于答辩演示

### J4. README 与部署说明

* 优先级：**P1**
* 验收：

  * 他人可按文档启动项目

---

# 四、第一版优先级总表

## P0：必须先做

| 模块   | 任务                                                                                                        |
| ---- | --------------------------------------------------------------------------------------------------------- |
| 基础设施 | 前后端初始化                                                                                                    |
| 数据库  | projects / tasks / task_dependencies / energy_templates / blocked_times / schedule_plans / schedule_items |
| 后端接口 | 项目 CRUD、任务 CRUD、精力模板接口、blocked time 接口、generate、select                                                    |
| 调度引擎 | 时间槽生成、依赖校验、优先级评分、不可拆分放置、三方案生成、风险输出                                                                        |
| 前端页面 | 任务列表页、日历页                                                                                                 |
| 前端能力 | 生成计划、切换方案、选择方案、日历展示                                                                                       |
| 精力能力 | 默认模板、模板选择、blocked time 编辑                                                                                 |
| 其他   | 系统内部待办池                                                                                                   |

## P1：建议第一版一起做

| 模块   | 任务                                                  |
| ---- | --------------------------------------------------- |
| 数据库  | execution_logs                                      |
| 后端接口 | execution 接口、reoptimize、validate-move、AI parse-task |
| 调度引擎 | 可拆分任务放置、重新优化                                        |
| 前端   | AI 输入组件、冲突提示、风险提示区、今日执行页、曲线编辑器                      |
| 测试   | 核心调度测试、联调测试、演示数据、README                             |

## P2：时间够再做

| 模块   | 任务                    |
| ---- | --------------------- |
| 调度引擎 | AI 参数建议更深入、任务筛选、执行历史页 |
| 前端   | 任务高级筛选、更多可视化          |
| 后端   | 更复杂 explain 接口        |

## P3：后续版本

| 模块  | 任务              |
| --- | --------------- |
| 产品化 | 登录、多用户、云同步      |
| 集成  | 日历同步、第三方导入      |
| 算法  | 遗传算法、历史学习、自适应调参 |
| 平台  | 桌面端             |

---

# 五、建议开发顺序表

这是最适合你当前情况的顺序。

## 第 0 阶段：开工准备

1. 建仓库
2. 确定目录结构
3. 写最小 README
4. 写数据库模型草稿

## 第 1 阶段：打通底座（P0）

1. 前后端初始化
2. 数据库迁移
3. 项目/任务 CRUD
4. 默认精力模板
5. blocked time CRUD

## 第 2 阶段：打通核心闭环（P0）

1. slot 生成
2. 依赖图处理
3. 基础评分函数
4. 生成三套方案
5. 日历展示
6. 方案选择

## 第 3 阶段：提升可用性（P1）

1. 拖拽冲突检测
2. 重新优化
3. 今日执行页
4. 执行反馈存储

## 第 4 阶段：做亮点（P1）

1. AI 自然语言输入
2. 曲线微调
3. 风险提示区
4. Demo 数据

## 第 5 阶段：打磨

1. 测试
2. UI 调整
3. README
4. 演示流程

---

# 六、第一版时间规划建议（10 天示例）

## Day 1

* 前后端初始化
* DB 连接
* 路由和 API client

## Day 2

* projects / tasks / dependencies 模型与接口

## Day 3

* 任务列表页
* 任务创建/编辑/删除

## Day 4

* energy templates / blocked times
* 默认模板 seed

## Day 5

* slot 生成
* blocked slot 处理
* graph 校验

## Day 6

* planner 主逻辑
* 三方案返回

## Day 7

* 日历页
* 方案切换
* 方案选择

## Day 8

* validate-move
* reoptimize
* 今日执行页

## Day 9

* AI parse-task
* 曲线编辑
* 风险提示

## Day 10

* 联调
* 测试
* demo 数据
* README

---

# 七、后续规划路线图

---

## V1.0（当前第一版）

### 目标

跑通完整闭环，适合演示与基础使用。

### 核心特性

* 待办池
* 项目优先级
* 任务依赖
* 精力模板
* blocked time
* 3 套今日排期方案
* 日历页
* 今日执行页
* AI 任务输入
* 冲突提示
* 手动重新优化

### 不做

* 自动学习
* 第三方接入
* 桌面端
* GA

---

## V1.1（第一版增强）

### 目标

增强可用性与解释性。

### 建议任务

* 任务筛选与搜索
* 风险解释文本
* 计划摘要卡片
* 今日完成率统计
* 历史执行记录页面
* 更好的 empty state / onboarding
* 数据导出（JSON / CSV）

### 优先级

* 风险解释：**P1**
* 历史记录：**P1**
* 数据导出：**P2**

---

## V2.0（智能增强版）

### 目标

从“规则排期”进入“轻智能排期”。

### 建议任务

* 历史行为学习
* AI 认知负荷估计优化
* AI 推荐拆分策略
* AI 风险建议
* AI 排期解释
* 周计划支持
* 更丰富的 blocked time 类型
* 局部重排

### 重点能力

* 根据执行日志调整任务估时
* 根据主观状态拟合精力偏移
* 根据拖拽行为学习用户偏好

### 优先级

* 周计划：**P1**
* 局部重排：**P1**
* 学习型估时：**P1**
* AI 排期解释：**P2**

---

## V2.5（算法升级版）

### 目标

增强算法亮点，适合论文/答辩/作品集升级。

### 建议任务

* 引入遗传算法
* 引入多目标优化
* 提供算法收敛图
* 增加不同调度策略对比
* 提供调度结果 explainability 视图

### 适用场景

* 毕设深挖
* 算法论文展示
* 作品集升级

### 优先级

* GA 核心：**P1**
* 收敛图：**P2**
* 策略对比：**P2**

---

## V3.0（产品化原型）

### 目标

从单人工具走向可产品化雏形。

### 建议任务

* 用户系统
* 云同步
* 跨设备
* Google Calendar / Outlook 同步
* Todoist / Notion / Trello 导入
* 桌面端封装（Tauri）
* 用户偏好配置中心
* 商业化试验功能（高级模板、深度分析）

### 优先级

* 用户系统：**P1**
* 云同步：**P1**
* 日历同步：**P1**
* 桌面端：**P2**

---

# 八、版本优先级路线总表

| 版本   | 目标     | 关键任务                       |
| ---- | ------ | -------------------------- |
| V1.0 | 跑通完整闭环 | 待办池、精力模板、三方案、日历、执行反馈、AI 输入 |
| V1.1 | 增强可用性  | 搜索筛选、历史记录、风险说明、导出          |
| V2.0 | 轻智能增强  | 周计划、局部重排、历史学习、AI 建议        |
| V2.5 | 算法升级   | GA、多目标优化、收敛图、策略对比          |
| V3.0 | 产品化    | 登录、云同步、第三方接入、桌面端           |

---

# 九、建议你当前只盯住的任务

如果你现在马上开工，只盯这 12 个就够：

1. 前端项目初始化
2. 后端项目初始化
3. 数据库模型与迁移
4. 任务 CRUD
5. 精力模板与 blocked time
6. slot 生成
7. 依赖图与环检测
8. 三方案 planner
9. 日历页展示
10. 方案选择
11. 今日执行页
12. AI 任务输入

这 12 个完成，第一版就成立了。

---

# 十、里程碑与验收

## 里程碑 M1：数据层完成

验收：

* 能创建项目和任务
* 能配置依赖、精力模板、blocked time

## 里程碑 M2：排期核心完成

验收：

* 能输入任务并返回 3 套排期方案

## 里程碑 M3：前端闭环完成

验收：

* 能在日历页查看方案并选择一个执行

## 里程碑 M4：执行反馈完成

验收：

* 今日执行页可反馈完成情况

## 里程碑 M5：演示版完成

验收：

* AI 任务输入可用
* 有 demo 数据
* 有 README 和演示流程

---

# 十一、一个更实用的建议

你这个项目最容易失控的地方有两个：

1. **过早做复杂算法**
2. **过早做太多集成功能**

所以建议你始终遵守这个原则：

> **先把产品闭环做出来，再给闭环增加“聪明程度”。**

也就是：

* 先做能用
* 再做好用
* 最后做很聪明

