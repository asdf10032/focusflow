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
