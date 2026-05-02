## FocusFlow v1.3 本地演示

FocusFlow 是一个本地优先的智能精力排期 MVP：录入任务，生成三套日程方案，选择今日计划，提交执行反馈，并从执行历史中获得可解释的时长建议。v1.3 增加了本地导出、剩余工作重排、任务备注搜索和更清楚的空状态。下面命令默认从仓库根目录运行。

### 后端启动

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install fastapi uvicorn sqlalchemy alembic pydantic pydantic-settings pytest
alembic upgrade head
python -m backend.app.services.seeds.demo_data --date 2026-05-01
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

`demo_data` 是可重复、非破坏性的演示种子：它会补齐默认精力模板，upsert 演示项目和任务，创建 blocked time，生成三套排期，选择 balanced 方案，并写入带备注、项目和认知负荷快照的执行历史。省略 `--date` 时默认使用今天。

### 前端启动

```powershell
cd frontend
npm install
npm.cmd run dev
npm.cmd run build
```

开发服务默认访问 `http://127.0.0.1:5173/`。

### v1.3 演示路径

1. Tasks：搜索 `advisor` 或任务备注里的关键词，确认标题和 notes 都能命中，并可与项目/状态筛选组合。
2. Tasks：使用本地导出按钮导出任务 JSON；没有数据时会显示空状态提示而不是下载空文件。
3. Calendar：查看三套计划，选择 balanced 方案；对同一天运行 Partial Replan，只保留未反馈的剩余工作。
4. Calendar：重新选择新生成的方案。
5. Today：查看选中方案中的剩余工作，提交状态、实际分钟数和备注。
6. Daily Review：切到同一天，查看执行历史、完成率、实际用时和估算偏差，并导出历史或复盘数据。

### 验证

```powershell
python -m pytest tests/test_phase15_task_search.py tests/test_demo_flow.py -q -p no:cacheprovider
python -m pytest tests/test_phase1_api.py tests/test_phase4_api.py tests/test_phase6_execution_history.py tests/test_phase7_execution_review.py tests/test_phase8_explanations.py tests/test_phase13_exports.py tests/test_phase14_partial_replan.py tests/test_phase15_task_search.py tests/test_demo_flow.py tests/test_frontend_i18n.py tests/test_frontend_view_helpers.py tests/test_scheduler_engine.py -q -p no:cacheprovider
python -m compileall backend alembic
cd frontend
npm.cmd run build
```

---

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
