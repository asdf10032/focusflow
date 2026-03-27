我按**单人、1–2 周、Web 优先、MVP 先落地**来设计，目标是：

**先把“待办录入 → 生成 3 个今日排期方案 → 选择方案 → 执行反馈”完整跑通。**

---

# FocusFlow 技术方案与项目结构

## 1. 技术选型

### 前端

推荐直接定为：

* **React + TypeScript + Vite**
* **Tailwind CSS**
* **React Router**
* **Zustand**
* **FullCalendar**
* **ECharts**
* **dayjs**
* **React Hook Form + Zod**

这样选的原因很实际：

* React + TS 开发快，类型安全够用
* Zustand 比 Redux 轻，适合单人项目
* FullCalendar 直接承接日历展示和拖拽
* ECharts 画精力曲线简单
* React Hook Form 适合任务表单和 AI 填充确认

### 后端

推荐：

* **FastAPI**
* **SQLAlchemy 2.0**
* **Pydantic v2**
* **SQLite**（MVP）
* **Alembic**
* **NetworkX**
* **NumPy**
* **uvicorn**

这样做的好处是：

* FastAPI 出接口很快
* Pydantic 很适合任务对象校验
* SQLite 足够支撑 MVP
* NetworkX 正好处理依赖图和环检测

### AI 接入

第一版建议做成**可插拔 Provider**：

* 默认：Mock / Rule-based parser
* 可选：OpenAI / Gemini / Claude API

原因是你第一版核心不是 LLM 能力，而是排期闭环。
所以 AI 先做成一个服务接口，不要把全项目绑定死。

---

## 2. 总体架构

采用标准前后端分离：

```text
Frontend (React)
    |
    | HTTP / JSON
    v
Backend API (FastAPI)
    |
    | service layer
    v
Scheduling Engine
    |
    +--> Graph Validator
    +--> Heuristic Planner
    +--> Plan Variant Generator
    +--> Conflict Detector
    |
    v
SQLite Database
```

### 模块职责

#### 前端

负责：

* 任务录入与编辑
* 今日排期展示
* 方案选择
* 执行反馈
* 冲突提示

#### 后端 API

负责：

* 持久化任务与配置
* 调用调度引擎
* 返回 3 个方案
* 校验拖拽是否冲突
* 接 AI 解析服务

#### 调度引擎

负责：

* 预处理任务依赖
* 处理 blocked time
* 生成可行排期
* 产出稳妥/平衡/冲刺 3 种方案
* 输出风险信息

---

## 3. MVP 功能切分

这版只实现 5 个主模块：

### 模块 A：待办池

* 任务 CRUD
* 项目优先级
* 是否可拆分
* 截止时间
* 前置依赖

### 模块 B：精力模板

* 早鸟 / 普通 / 夜猫
* 用户微调
* 工作日 / 周末模板

### 模块 C：今日排期

* 读取任务 + 精力模板 + blocked time
* 生成 3 套方案
* 用户选择一个方案

### 模块 D：日历与冲突

* 日历展示任务块
* 手动拖拽
* 后端返回冲突提示
* 用户点击重新优化

### 模块 E：执行反馈

* 完成 / 未完成
* 实际开始结束时间
* 实际用时
* 主观状态

---

## 4. 数据库设计

MVP 用 SQLite，表尽量少但够用。

---

### 4.1 projects

```sql
id INTEGER PRIMARY KEY
name TEXT NOT NULL
priority INTEGER NOT NULL DEFAULT 5
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
```

### 4.2 tasks

```sql
id INTEGER PRIMARY KEY
title TEXT NOT NULL
description TEXT
estimated_minutes INTEGER NOT NULL
cognitive_load INTEGER NOT NULL
project_id INTEGER NOT NULL
due_at DATETIME
earliest_start_at DATETIME
fixed_start_at DATETIME
is_splittable BOOLEAN NOT NULL DEFAULT 0
max_split_count INTEGER NOT NULL DEFAULT 1
status TEXT NOT NULL DEFAULT 'pending'
source TEXT NOT NULL DEFAULT 'manual'  -- manual / ai
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
FOREIGN KEY(project_id) REFERENCES projects(id)
```

### 4.3 task_dependencies

```sql
id INTEGER PRIMARY KEY
task_id INTEGER NOT NULL
depends_on_task_id INTEGER NOT NULL
FOREIGN KEY(task_id) REFERENCES tasks(id)
FOREIGN KEY(depends_on_task_id) REFERENCES tasks(id)
```

### 4.4 task_tags

可选，MVP 不一定先做。

### 4.5 energy_templates

```sql
id INTEGER PRIMARY KEY
name TEXT NOT NULL           -- early_bird / normal / night_owl
day_type TEXT NOT NULL       -- weekday / weekend
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
```

### 4.6 energy_template_slots

30 分钟一格。

```sql
id INTEGER PRIMARY KEY
template_id INTEGER NOT NULL
slot_index INTEGER NOT NULL   -- 0 ~ 47
energy_value INTEGER NOT NULL -- 1 ~ 10
FOREIGN KEY(template_id) REFERENCES energy_templates(id)
```

### 4.7 blocked_times

```sql
id INTEGER PRIMARY KEY
title TEXT NOT NULL           -- sleep / class
date TEXT NOT NULL            -- YYYY-MM-DD
start_minute INTEGER NOT NULL -- 0 ~ 1439
end_minute INTEGER NOT NULL
type TEXT NOT NULL            -- sleep / class / custom
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
```

### 4.8 schedule_plans

```sql
id INTEGER PRIMARY KEY
date TEXT NOT NULL
plan_type TEXT NOT NULL       -- conservative / balanced / aggressive
score REAL NOT NULL
risk_level TEXT NOT NULL      -- low / medium / high
status TEXT NOT NULL DEFAULT 'generated' -- generated / selected
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
```

### 4.9 schedule_items

```sql
id INTEGER PRIMARY KEY
plan_id INTEGER NOT NULL
task_id INTEGER NOT NULL
segment_index INTEGER NOT NULL DEFAULT 1
start_at DATETIME NOT NULL
end_at DATETIME NOT NULL
is_late BOOLEAN NOT NULL DEFAULT 0
is_conflicted BOOLEAN NOT NULL DEFAULT 0
FOREIGN KEY(plan_id) REFERENCES schedule_plans(id)
FOREIGN KEY(task_id) REFERENCES tasks(id)
```

### 4.10 execution_logs

```sql
id INTEGER PRIMARY KEY
task_id INTEGER NOT NULL
date TEXT NOT NULL
actual_start_at DATETIME
actual_end_at DATETIME
actual_minutes INTEGER
status TEXT NOT NULL          -- completed / skipped / interrupted
subjective_state TEXT         -- tired / focused / distracted
created_at DATETIME NOT NULL
updated_at DATETIME NOT NULL
FOREIGN KEY(task_id) REFERENCES tasks(id)
```

---

## 5. 后端目录结构

推荐这样落：

```text
backend/
├── app/
│   ├── api/
│   │   ├── routes/
│   │   │   ├── tasks.py
│   │   │   ├── projects.py
│   │   │   ├── energy.py
│   │   │   ├── blocked_times.py
│   │   │   ├── schedules.py
│   │   │   ├── execution.py
│   │   │   └── ai.py
│   │   └── deps.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── logging.py
│   │
│   ├── models/
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── task_dependency.py
│   │   ├── energy_template.py
│   │   ├── blocked_time.py
│   │   ├── schedule_plan.py
│   │   ├── schedule_item.py
│   │   └── execution_log.py
│   │
│   ├── schemas/
│   │   ├── project.py
│   │   ├── task.py
│   │   ├── energy.py
│   │   ├── blocked_time.py
│   │   ├── schedule.py
│   │   ├── execution.py
│   │   └── ai.py
│   │
│   ├── services/
│   │   ├── task_service.py
│   │   ├── energy_service.py
│   │   ├── blocked_time_service.py
│   │   ├── schedule_service.py
│   │   ├── conflict_service.py
│   │   └── ai_service.py
│   │
│   ├── scheduler/
│   │   ├── domain.py
│   │   ├── graph_utils.py
│   │   ├── slot_utils.py
│   │   ├── scoring.py
│   │   ├── planner.py
│   │   ├── variants.py
│   │   ├── validator.py
│   │   └── explain.py
│   │
│   ├── seed/
│   │   └── energy_templates.py
│   │
│   └── main.py
│
├── alembic/
├── tests/
│   ├── test_tasks.py
│   ├── test_graph_utils.py
│   ├── test_planner.py
│   ├── test_conflicts.py
│   └── test_ai_parser.py
│
├── requirements.txt
└── README.md
```

---

## 6. 前端目录结构

```text
frontend/
├── src/
│   ├── app/
│   │   ├── router.tsx
│   │   ├── store/
│   │   │   ├── taskStore.ts
│   │   │   ├── scheduleStore.ts
│   │   │   └── uiStore.ts
│   │   └── providers.tsx
│   │
│   ├── api/
│   │   ├── client.ts
│   │   ├── tasks.ts
│   │   ├── projects.ts
│   │   ├── energy.ts
│   │   ├── blockedTimes.ts
│   │   ├── schedules.ts
│   │   ├── execution.ts
│   │   └── ai.ts
│   │
│   ├── components/
│   │   ├── tasks/
│   │   │   ├── TaskForm.tsx
│   │   │   ├── TaskList.tsx
│   │   │   ├── TaskFilters.tsx
│   │   │   └── AITaskInput.tsx
│   │   │
│   │   ├── calendar/
│   │   │   ├── ScheduleCalendar.tsx
│   │   │   ├── PlanSwitcher.tsx
│   │   │   ├── ConflictDialog.tsx
│   │   │   └── ReoptimizeButton.tsx
│   │   │
│   │   ├── execution/
│   │   │   ├── TodayExecutionPanel.tsx
│   │   │   ├── TaskStatusCard.tsx
│   │   │   └── FeedbackForm.tsx
│   │   │
│   │   ├── energy/
│   │   │   ├── EnergyTemplateSelector.tsx
│   │   │   ├── EnergyCurveEditor.tsx
│   │   │   └── BlockedTimeEditor.tsx
│   │   │
│   │   └── common/
│   │       ├── PageHeader.tsx
│   │       ├── EmptyState.tsx
│   │       └── LoadingOverlay.tsx
│   │
│   ├── pages/
│   │   ├── TasksPage.tsx
│   │   ├── CalendarPage.tsx
│   │   ├── TodayPage.tsx
│   │   └── SettingsPage.tsx
│   │
│   ├── hooks/
│   │   ├── useTasks.ts
│   │   ├── useSchedules.ts
│   │   └── useEnergy.ts
│   │
│   ├── types/
│   │   ├── task.ts
│   │   ├── schedule.ts
│   │   ├── energy.ts
│   │   └── execution.ts
│   │
│   ├── utils/
│   │   ├── time.ts
│   │   ├── planLabel.ts
│   │   └── conflictMessage.ts
│   │
│   ├── styles/
│   │   └── calendar.css
│   │
│   ├── main.tsx
│   └── index.css
│
├── package.json
├── tsconfig.json
└── vite.config.ts
```

---

## 7. 核心接口设计

---

### 7.1 项目与任务

#### `GET /api/projects`

获取项目列表

#### `POST /api/projects`

创建项目

请求：

```json
{
  "name": "考研数学",
  "priority": 9
}
```

#### `GET /api/tasks`

支持过滤：

* status
* due_today
* project_id

#### `POST /api/tasks`

```json
{
  "title": "刷高数真题",
  "estimated_minutes": 120,
  "cognitive_load": 8,
  "project_id": 1,
  "due_at": "2026-03-27T21:00:00",
  "earliest_start_at": "2026-03-27T09:00:00",
  "fixed_start_at": null,
  "is_splittable": true,
  "max_split_count": 3,
  "dependency_ids": [2, 3]
}
```

#### `PUT /api/tasks/{id}`

更新任务

#### `DELETE /api/tasks/{id}`

删除任务

---

### 7.2 AI 输入

#### `POST /api/ai/parse-task`

```json
{
  "text": "今晚做两小时高数真题，比较费脑子，最好 9 点前完成"
}
```

返回：

```json
{
  "title": "高数真题",
  "estimated_minutes": 120,
  "cognitive_load": 8,
  "due_at": "2026-03-27T21:00:00",
  "is_splittable": false,
  "confidence": 0.82
}
```

前端拿到这个结果后，弹出确认表单，不直接入库。

---

### 7.3 精力模板

#### `GET /api/energy/templates?day_type=weekday`

获取模板及 slot 数据

#### `PUT /api/energy/templates/{id}`

保存微调后的模板

请求：

```json
{
  "slots": [
    { "slot_index": 0, "energy_value": 2 },
    { "slot_index": 1, "energy_value": 2 },
    { "slot_index": 20, "energy_value": 8 }
  ]
}
```

---

### 7.4 blocked time

#### `GET /api/blocked-times?date=2026-03-27`

#### `POST /api/blocked-times`

```json
{
  "title": "线代课",
  "date": "2026-03-27",
  "start_minute": 480,
  "end_minute": 600,
  "type": "class"
}
```

---

### 7.5 生成排期

#### `POST /api/schedules/generate`

请求：

```json
{
  "date": "2026-03-27",
  "day_type": "weekday",
  "task_ids": [1, 2, 3, 4]
}
```

返回：

```json
{
  "plans": [
    {
      "plan_type": "conservative",
      "score": 81.2,
      "risk_level": "low",
      "warnings": [],
      "items": [
        {
          "task_id": 1,
          "title": "刷高数真题",
          "segment_index": 1,
          "start_at": "2026-03-27T09:00:00",
          "end_at": "2026-03-27T10:30:00",
          "is_late": false
        }
      ]
    },
    {
      "plan_type": "balanced",
      "score": 86.4,
      "risk_level": "medium",
      "warnings": [],
      "items": []
    },
    {
      "plan_type": "aggressive",
      "score": 90.8,
      "risk_level": "high",
      "warnings": ["可能导致晚间疲劳累积"],
      "items": []
    }
  ],
  "sacrificable_tasks": [
    { "task_id": 6, "reason": "优先级较低且无明确截止时间" }
  ]
}
```

---

### 7.6 选择方案

#### `POST /api/schedules/select`

```json
{
  "date": "2026-03-27",
  "plan_type": "balanced"
}
```

作用：

* 将该方案状态标为 selected
* 今日执行页从这里读取

---

### 7.7 拖拽冲突校验

#### `POST /api/schedules/validate-move`

```json
{
  "plan_id": 12,
  "item_id": 88,
  "new_start_at": "2026-03-27T13:30:00",
  "new_end_at": "2026-03-27T14:30:00"
}
```

返回：

```json
{
  "valid": false,
  "conflicts": [
    {
      "type": "blocked_time",
      "message": "该时间段与上课时间冲突"
    },
    {
      "type": "dependency",
      "message": "该任务必须在“整理错题”之后执行"
    }
  ]
}
```

---

### 7.8 重新优化

#### `POST /api/schedules/reoptimize`

请求：

```json
{
  "date": "2026-03-27",
  "plan_type": "balanced"
}
```

它本质上可以直接复用 generate，只是前端语义 अलग，不需要另写复杂逻辑。

---

### 7.9 执行反馈

#### `POST /api/execution/logs`

```json
{
  "task_id": 1,
  "date": "2026-03-27",
  "actual_start_at": "2026-03-27T09:10:00",
  "actual_end_at": "2026-03-27T10:55:00",
  "actual_minutes": 105,
  "status": "completed",
  "subjective_state": "focused"
}
```

#### `GET /api/execution/today?date=2026-03-27`

获取今日执行页数据

---

## 8. 调度引擎实现方案

这里不建议你第一版做 GA。
第一版直接用**启发式规则 + 参数化变体**就够了，而且更稳。

---

### 8.1 核心思想

先把一天切成 48 个 30 分钟槽位。

然后把问题转成：

* 哪些槽位不能用
* 哪些任务可以排
* 哪些任务依赖未满足
* 哪些任务需要高精力时段
* 哪些任务可拆分

最后生成一个合法且尽量高分的时间表。

---

### 8.2 调度流程

#### Step 1：读取输入

* 今日候选任务
* blocked time
* energy slots
* 当前 day type

#### Step 2：过滤任务

排除：

* 已完成任务
* fixed_start_at 不属于当天的任务
* 明显不该进入今日计划的任务

#### Step 3：依赖校验

* 用 NetworkX 建图
* 环检测
* 找到可执行任务集合

#### Step 4：构造时间槽

建立数组：

```python
slots = [Slot(index=0..47)]
```

每个 slot 包含：

* start_time
* end_time
* energy_value
* is_blocked
* occupied_by_task

#### Step 5：任务排序

候选任务按综合优先级排序，建议先算一个 priority score：

[
priority = w_1 * deadline_urgency + w_2 * project_priority + w_3 * cognitive_load - w_4 * split_penalty
]

#### Step 6：尝试放置任务

对每个任务：

* 找满足依赖的可用槽区间
* 计算该区间的匹配分
* 选择最高分区间
* 若可拆分，则在不超过 3 段内尝试组合

#### Step 7：输出 warnings

如果任务排不下：

* 标记原因
* 进入 sacrificable_tasks

#### Step 8：生成 3 个方案

不是跑 3 套算法，而是同一个 planner 用不同权重。

---

### 8.3 评分函数建议

第一版用这个就够了：

[
score = match_score + urgency_score + continuity_score - lateness_penalty - fragmentation_penalty
]

#### 1. `match_score`

精力和认知负荷越接近越高：

[
match = 10 - |energy - cognitive|
]

#### 2. `urgency_score`

deadline 越近越高

#### 3. `continuity_score`

连续安排加分

#### 4. `lateness_penalty`

超截止时间强惩罚

#### 5. `fragmentation_penalty`

被拆太碎扣分

---

### 8.4 三方案参数映射

#### 稳妥型

```python
{
  "buffer_weight": 1.0,
  "lateness_penalty": 1.2,
  "fragmentation_penalty": 1.0,
  "continuity_bonus": 0.8,
  "aggressive_fill": 0.4
}
```

#### 平衡型

```python
{
  "buffer_weight": 0.7,
  "lateness_penalty": 1.0,
  "fragmentation_penalty": 0.8,
  "continuity_bonus": 1.0,
  "aggressive_fill": 0.7
}
```

#### 冲刺型

```python
{
  "buffer_weight": 0.3,
  "lateness_penalty": 0.8,
  "fragmentation_penalty": 0.6,
  "continuity_bonus": 1.1,
  "aggressive_fill": 1.0
}
```

这样做的好处是：

* 逻辑一致
* 好调参
* 容易解释
* 实现快

---

## 9. 调度引擎代码骨架

### `scheduler/domain.py`

定义：

* TaskNode
* TimeSlot
* PlanVariant
* PlannedItem
* Conflict

### `scheduler/graph_utils.py`

实现：

* build_dependency_graph(tasks)
* detect_cycles(graph)
* topo_sort(graph)
* get_ready_tasks(tasks, completed_tasks)

### `scheduler/slot_utils.py`

实现：

* generate_day_slots(date, energy_profile, blocked_times)
* find_contiguous_ranges(slots, duration_slots)
* reserve_slots(slots, range, task_id)

### `scheduler/scoring.py`

实现：

* compute_task_priority(task, now)
* compute_slot_match(task, slot_range)
* compute_plan_score(items)

### `scheduler/planner.py`

实现主入口：

* generate_plan(tasks, slots, config)
* place_task(task, slots, config)
* split_and_place_task(task, slots, config)

### `scheduler/variants.py`

实现：

* get_variant_config(plan_type)
* generate_all_variants(tasks, slots)

### `scheduler/validator.py`

实现：

* validate_move(item, new_time, plan, blocked_times)
* check_dependency_conflict(...)
* check_overlap_conflict(...)
* check_deadline_conflict(...)

---

## 10. 前端页面实现建议

---

### 10.1 任务列表页 `TasksPage`

布局建议：

左边：

* 待办列表
* 搜索 / 状态筛选 / 项目筛选

右边：

* 任务表单
* AI 任务输入框
* 快速创建按钮

交互重点：

* 新建后立即加入待办池
* dependency 字段用多选下拉
* due time 支持日期和具体时间

---

### 10.2 日历页 `CalendarPage`

布局建议：

上方：

* 日期选择
* 生成排期按钮
* 方案切换 Tabs
* 重新优化按钮

中间：

* FullCalendar 日视图

右侧：

* 当前方案摘要
* 风险提示
* 可牺牲任务建议

交互重点：

* 先生成 3 套方案，再切换查看
* 选择方案后可固定执行
* 拖拽只做 validate-move

---

### 10.3 今日执行页 `TodayPage`

布局建议：

上半区：

* 当前任务
* 下一个任务
* 今日完成进度

下半区：

* 执行反馈表单
* 已完成记录

交互重点：

* 把“现在该做什么”做得很清楚
* 避免信息过多

---

## 11. 开发顺序

这是最适合你现在的切法。

---

### 第 1 天：项目初始化

前端：

* Vite + React + TS
* Tailwind
* Router
* Zustand
* API client

后端：

* FastAPI
* SQLAlchemy
* Alembic
* SQLite
* 基础目录搭建

---

### 第 2 天：数据库与基础接口

完成：

* projects
* tasks
* task_dependencies
* blocked_times
* energy_templates

先把 CRUD 跑通。

---

### 第 3 天：任务页

完成：

* 任务列表
* 新建/编辑/删除
* 项目优先级
* 依赖设置

---

### 第 4 天：精力模板与 blocked time

完成：

* 早鸟/普通/夜猫模板 seed
* 曲线编辑
* 上课/睡觉时间配置

---

### 第 5 天：调度引擎 MVP

完成：

* slot 生成
* 依赖校验
* 启发式排期
* 3 套参数方案输出

这是最核心的一天。

---

### 第 6 天：日历页

完成：

* FullCalendar 展示
* 方案切换
* 选择方案
* 拖拽校验

---

### 第 7 天：今日执行页

完成：

* 当前任务显示
* 完成/未完成
* 实际用时
* 主观状态

---

### 第 8 天：AI 输入

完成：

* AI 输入框
* parse-task 接口
* 确认后入库

---

### 第 9 天：测试与修复

重点测：

* 依赖环
* blocked time 冲突
* 无 deadline 任务
* 可拆分任务
* 拖拽冲突提示

---

### 第 10 天：打磨

* UI
* 默认数据
* README
* 演示用例
* 截图与答辩材料

---

## 12. 你现在最该先写的文件

如果你要马上开工，优先级是：

### 后端先写

1. `app/main.py`
2. `app/core/database.py`
3. `app/models/task.py`
4. `app/models/project.py`
5. `app/models/task_dependency.py`
6. `app/api/routes/tasks.py`
7. `app/scheduler/domain.py`
8. `app/scheduler/graph_utils.py`
9. `app/scheduler/slot_utils.py`
10. `app/scheduler/planner.py`

### 前端先写

1. `src/api/client.ts`
2. `src/pages/TasksPage.tsx`
3. `src/components/tasks/TaskForm.tsx`
4. `src/components/tasks/TaskList.tsx`
5. `src/pages/CalendarPage.tsx`
6. `src/components/calendar/ScheduleCalendar.tsx`
7. `src/pages/TodayPage.tsx`

---

## 13. 环境变量建议

### 后端 `.env`

```env
APP_NAME=FocusFlow
APP_ENV=dev
DATABASE_URL=sqlite:///./focusflow.db
AI_PROVIDER=mock
OPENAI_API_KEY=
GEMINI_API_KEY=
```

### 前端 `.env`

```env
VITE_API_BASE_URL=http://127.0.0.1:8000/api
```

---

## 14. 最低测试清单

你至少要覆盖这些情况：

### 调度正确性

* 有依赖任务时，顺序必须正确
* blocked time 不能被占用
* 可拆分任务最多拆 3 段
* 不可拆分任务必须连续
* 无截止时间任务可排但优先级下降

### 冲突校验

* 拖拽到上课时间
* 拖拽到睡觉时间
* 拖拽导致依赖逆序
* 拖拽导致任务重叠
* 拖拽后超过截止时间

### AI 输入

* 能识别标题
* 能识别时长
* 能识别大致截止时间
* 置信度不足时提示用户手动修正

---

## 15. 最终建议

如果你要确保 1–2 周能跑出来，有三条一定要守住：

### 第一，不要先做 GA

GA 很容易吃掉你大量时间，但对 MVP 展示价值不如“完整可运行闭环”。

### 第二，不要先做太复杂的 AI

AI 先做“自然语言 → 结构化任务”就够亮点了。

### 第三，不要把页面做太多

你已经选了最重要的 3 页，这个决策是对的：

* 任务列表页
* 日历页
* 今日执行页

只要这三页通了，项目就成立了。

