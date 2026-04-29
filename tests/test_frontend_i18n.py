from __future__ import annotations

import json
import subprocess
import textwrap
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def run_i18n_script(script: str) -> dict:
    node_script = textwrap.dedent(
        f"""
        const fs = require("fs");
        const path = require("path");
        const ts = require(path.join(process.cwd(), "frontend", "node_modules", "typescript"));
        const file = path.join(process.cwd(), "frontend", "src", "lib", "i18n.ts");
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
        const i18n = mod.exports;
        {script}
        """
    )
    result = subprocess.run(
        ["node", "-e", node_script],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        capture_output=True,
        check=True,
    )
    return json.loads(result.stdout)


def test_translation_keys_are_complete_for_both_languages():
    result = run_i18n_script(
        """
        const englishKeys = Object.keys(i18n.translations.en).sort();
        const chineseKeys = Object.keys(i18n.translations["zh-CN"]).sort();
        console.log(JSON.stringify({
          languages: i18n.LANGUAGES,
          defaultLanguage: i18n.DEFAULT_LANGUAGE,
          storageKey: i18n.LANGUAGE_STORAGE_KEY,
          sameKeys: JSON.stringify(englishKeys) === JSON.stringify(chineseKeys),
          keyCount: englishKeys.length,
        }));
        """
    )

    assert result["languages"] == ["zh-CN", "en"]
    assert result["defaultLanguage"] == "zh-CN"
    assert result["storageKey"] == "focusflow.language"
    assert result["sameKeys"] is True
    assert result["keyCount"] >= 90


def test_labels_and_language_parsing_are_stable():
    result = run_i18n_script(
        """
        console.log(JSON.stringify({
          zhTask: i18n.t("zh-CN", "nav.tasks"),
          enTask: i18n.t("en", "nav.tasks"),
          zhTodo: i18n.getStatusLabel("zh-CN", "todo"),
          enTodo: i18n.getStatusLabel("en", "todo"),
          zhBalanced: i18n.getPlanTypeLabel("zh-CN", "balanced"),
          enBalanced: i18n.getPlanTypeLabel("en", "balanced"),
          parseValid: i18n.parseLanguage("en"),
          parseInvalid: i18n.parseLanguage("fr"),
        }));
        """
    )

    assert result == {
        "zhTask": "任务",
        "enTask": "Tasks",
        "zhTodo": "待办",
        "enTodo": "Todo",
        "zhBalanced": "平衡",
        "enBalanced": "Balanced",
        "parseValid": "en",
        "parseInvalid": "zh-CN",
    }


def test_phase4_usability_labels_are_localized():
    result = run_i18n_script(
        """
        const phase4Keys = [
          "nav.today",
          "tasks.parser.title",
          "tasks.parser.action",
          "calendar.action.reoptimize",
          "calendar.validate.title",
          "today.title",
          "today.action.refresh",
          "today.message.feedbackSaved",
        ];
        console.log(JSON.stringify({
          zh: Object.fromEntries(phase4Keys.map((key) => [key, i18n.t("zh-CN", key)])),
          en: Object.fromEntries(phase4Keys.map((key) => [key, i18n.t("en", key)])),
        }));
        """
    )

    assert result["zh"]["nav.today"] == "今日"
    assert result["zh"]["tasks.parser.action"] == "解析为任务草稿"
    assert result["zh"]["calendar.action.reoptimize"] == "重新优化"
    assert result["zh"]["today.message.feedbackSaved"] == "反馈已提交"
    assert result["en"]["nav.today"] == "Today"
    assert result["en"]["tasks.parser.action"] == "Parse Draft"
    assert result["en"]["calendar.action.reoptimize"] == "Reoptimize"
    assert result["en"]["today.message.feedbackSaved"] == "Feedback saved"


def test_phase7_review_labels_are_localized():
    result = run_i18n_script(
        """
        const phase7Keys = [
          "nav.review",
          "today.metrics.title",
          "today.metrics.planned",
          "today.metrics.completed",
          "today.metrics.skippedIncomplete",
          "today.metrics.completionRate",
          "review.title",
          "review.summary.actualMinutes",
          "review.summary.variance",
          "review.emptyTitle",
        ];
        console.log(JSON.stringify({
          zh: Object.fromEntries(phase7Keys.map((key) => [key, i18n.t("zh-CN", key)])),
          en: Object.fromEntries(phase7Keys.map((key) => [key, i18n.t("en", key)])),
        }));
        """
    )

    assert result["en"]["nav.review"] == "Review"
    assert result["en"]["today.metrics.completionRate"] == "Completion"
    assert result["en"]["review.summary.variance"] == "Estimate variance"
    assert all(value and not value.startswith("missing:") for value in result["zh"].values())


def test_phase8_explanation_and_filter_labels_are_localized():
    result = run_i18n_script(
        """
        const phase8Keys = [
          "calendar.explanation.title",
          "calendar.explanation.risk",
          "calendar.unplacedReasons",
          "tasks.filters.title",
          "tasks.filters.status",
          "tasks.filters.project",
          "tasks.filters.allStatuses",
          "tasks.filters.allProjects",
          "tasks.filters.noProject",
        ];
        console.log(JSON.stringify({
          zh: Object.fromEntries(phase8Keys.map((key) => [key, i18n.t("zh-CN", key)])),
          en: Object.fromEntries(phase8Keys.map((key) => [key, i18n.t("en", key)])),
        }));
        """
    )

    assert result["en"]["calendar.explanation.title"] == "Plan explanation"
    assert result["en"]["tasks.filters.allStatuses"] == "All statuses"
    assert result["en"]["tasks.filters.noProject"] == "No project"
    assert all(value and not value.startswith("missing:") for value in result["zh"].values())
