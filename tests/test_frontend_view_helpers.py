from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_schedule_view_helper_script(script: str) -> dict:
    node_script = textwrap.dedent(
        f"""
        const fs = require("fs");
        const path = require("path");
        const ts = require(path.join(process.cwd(), "frontend", "node_modules", "typescript"));
        const file = path.join(process.cwd(), "frontend", "src", "lib", "scheduleView.ts");
        const source = fs.readFileSync(file, "utf8");
        const compiled = ts.transpileModule(source, {{
          compilerOptions: {{
            module: ts.ModuleKind.CommonJS,
            target: ts.ScriptTarget.ES2020,
          }},
        }}).outputText;
        const mod = {{ exports: {{}} }};
        const runner = new Function("exports", "require", "module", "__filename", "__dirname", compiled);
        runner(mod.exports, require, mod, file, path.dirname(file));
        const helpers = mod.exports;
        {script}
        """
    )
    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def run_export_view_helper_script(script: str) -> dict:
    node_script = textwrap.dedent(
        f"""
        const fs = require("fs");
        const path = require("path");
        const ts = require(path.join(process.cwd(), "frontend", "node_modules", "typescript"));
        const file = path.join(process.cwd(), "frontend", "src", "lib", "exportView.ts");
        const source = fs.readFileSync(file, "utf8");
        const compiled = ts.transpileModule(source, {{
          compilerOptions: {{
            module: ts.ModuleKind.CommonJS,
            target: ts.ScriptTarget.ES2020,
          }},
        }}).outputText;
        const mod = {{ exports: {{}} }};
        const runner = new Function("exports", "require", "module", "__filename", "__dirname", compiled);
        runner(mod.exports, require, mod, file, path.dirname(file));
        const helpers = mod.exports;
        {script}
        """
    )
    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def run_task_view_helper_script(script: str) -> dict:
    node_script = textwrap.dedent(
        f"""
        const fs = require("fs");
        const path = require("path");
        const ts = require(path.join(process.cwd(), "frontend", "node_modules", "typescript"));
        const file = path.join(process.cwd(), "frontend", "src", "lib", "taskView.ts");
        const source = fs.readFileSync(file, "utf8");
        const compiled = ts.transpileModule(source, {{
          compilerOptions: {{
            module: ts.ModuleKind.CommonJS,
            target: ts.ScriptTarget.ES2020,
          }},
        }}).outputText;
        const mod = {{ exports: {{}} }};
        const runner = new Function("exports", "require", "module", "__filename", "__dirname", compiled);
        runner(mod.exports, require, mod, file, path.dirname(file));
        const helpers = mod.exports;
        {script}
        """
    )
    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def run_review_view_helper_script(script: str) -> dict:
    node_script = textwrap.dedent(
        f"""
        const fs = require("fs");
        const path = require("path");
        const ts = require(path.join(process.cwd(), "frontend", "node_modules", "typescript"));
        const file = path.join(process.cwd(), "frontend", "src", "lib", "reviewView.ts");
        const source = fs.readFileSync(file, "utf8");
        const compiled = ts.transpileModule(source, {{
          compilerOptions: {{
            module: ts.ModuleKind.CommonJS,
            target: ts.ScriptTarget.ES2020,
          }},
        }}).outputText;
        const mod = {{ exports: {{}} }};
        const runner = new Function("exports", "require", "module", "__filename", "__dirname", compiled);
        runner(mod.exports, require, mod, file, path.dirname(file));
        const helpers = mod.exports;
        {script}
        """
    )
    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_schedule_items_are_sorted_and_labeled_for_display():
    result = run_schedule_view_helper_script(
        """
        const items = helpers.sortScheduleItems([
          { task_id: 2, start_datetime: "2026-04-26T10:30:00", end_datetime: "2026-04-26T11:00:00" },
          { task_id: 1, start_datetime: "2026-04-26T09:00:00", end_datetime: "2026-04-26T10:00:00" },
        ]);
        console.log(JSON.stringify({
          ids: items.map((item) => item.task_id),
          firstRange: helpers.formatTimeRange(items[0]),
          balancedLabel: helpers.getPlanLabel("balanced"),
        }));
        """
    )

    assert result == {
        "ids": [1, 2],
        "firstRange": "09:00-10:00",
        "balancedLabel": "Balanced",
    }


def test_plan_type_metadata_has_stable_order():
    result = run_schedule_view_helper_script(
        """
        console.log(JSON.stringify({
          types: helpers.PLAN_TYPES,
          labels: helpers.PLAN_TYPES.map((type) => helpers.getPlanLabel(type)),
        }));
        """
    )

    assert result == {
        "types": ["conservative", "balanced", "aggressive"],
        "labels": ["Conservative", "Balanced", "Aggressive"],
    }


def test_export_query_builder_is_stable():
    result = run_export_view_helper_script(
        """
        console.log(JSON.stringify({
          empty: helpers.buildExportQuery(),
          singleDate: helpers.buildExportQuery({ date: "2026-05-01" }),
          range: helpers.buildExportQuery({
            start_date: "2026-05-01",
            end_date: "2026-05-03",
          }),
        }));
        """
    )

    assert result == {
        "empty": "",
        "singleDate": "?date=2026-05-01",
        "range": "?start_date=2026-05-01&end_date=2026-05-03",
    }


def test_task_search_matches_title_and_notes_with_filters():
    result = run_task_view_helper_script(
        """
        const tasks = [
          { id: 1, title: "Write launch brief", notes: "alpha notes", status: "todo", project_id: 1 },
          { id: 2, title: "Archive receipts", notes: "launch paperwork", status: "done", project_id: 1 },
          { id: 3, title: "Plan workshop", notes: "alpha notes", status: "todo", project_id: 2 },
        ];
        const byTitle = helpers.filterTasks(tasks, { search: "launch", status: "all", project: "all" });
        const byNotes = helpers.filterTasks(tasks, { search: "paper", status: "all", project: "all" });
        const combined = helpers.filterTasks(tasks, { search: "alpha", status: "todo", project: "1" });
        console.log(JSON.stringify({
          byTitle: byTitle.map((task) => task.id),
          byNotes: byNotes.map((task) => task.id),
          combined: combined.map((task) => task.id),
          normalized: helpers.normalizeTaskSearch("  Launch  "),
        }));
        """
    )

    assert result == {
        "byTitle": [1, 2],
        "byNotes": [2],
        "combined": [1],
        "normalized": "launch",
    }


def test_review_view_helpers_format_weekly_metrics_and_navigation():
    result = run_review_view_helper_script(
        """
        console.log(JSON.stringify({
          minutes: helpers.formatMinutesValue(45),
          noMinutes: helpers.formatMinutesValue(null),
          positiveVariance: helpers.formatVarianceValue(15),
          negativeVariance: helpers.formatVarianceValue(-5),
          noVariance: helpers.formatVarianceValue(null),
          rate: helpers.formatCompletionRate(0.625),
          previousWeek: helpers.shiftDateByDays("2026-05-06", -7),
          nextWeek: helpers.shiftDateByDays("2026-05-06", 7),
          range: helpers.formatWeekRange("2026-05-04", "2026-05-10"),
          positiveDelta: helpers.formatDeltaValue(12, " min"),
          negativeDelta: helpers.formatDeltaValue(-8, " min"),
          noDelta: helpers.formatDeltaValue(null, " min"),
        }));
        """
    )

    assert result == {
        "minutes": "45",
        "noMinutes": "-",
        "positiveVariance": "+15",
        "negativeVariance": "-5",
        "noVariance": "-",
        "rate": "63%",
        "previousWeek": "2026-04-29",
        "nextWeek": "2026-05-13",
        "range": "2026-05-04 - 2026-05-10",
        "positiveDelta": "+12 min",
        "negativeDelta": "-8 min",
        "noDelta": "-",
    }
