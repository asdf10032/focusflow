import type { PlanType } from "./scheduleView";
import type { ExecutionHistoryStatus, TaskStatus } from "./api";

export const LANGUAGES = ["zh-CN", "en"] as const;
export type Language = (typeof LANGUAGES)[number];

export const DEFAULT_LANGUAGE: Language = "zh-CN";
export const LANGUAGE_STORAGE_KEY = "focusflow.language";

export type TranslationKey =
  | "app.name"
  | "nav.tasks"
  | "nav.calendar"
  | "nav.today"
  | "nav.review"
  | "language.zh"
  | "language.en"
  | "language.label"
  | "common.loading"
  | "common.notAvailable"
  | "common.error"
  | "common.success"
  | "common.minutes"
  | "common.score"
  | "tasks.eyebrow"
  | "tasks.title"
  | "tasks.form.title"
  | "tasks.form.titlePlaceholder"
  | "tasks.form.minutes"
  | "tasks.form.load"
  | "tasks.form.due"
  | "tasks.form.status"
  | "tasks.form.splits"
  | "tasks.form.allowSplit"
  | "tasks.action.create"
  | "tasks.action.save"
  | "tasks.action.cancel"
  | "tasks.action.refresh"
  | "tasks.action.edit"
  | "tasks.action.delete"
  | "tasks.parser.title"
  | "tasks.parser.inputLabel"
  | "tasks.parser.placeholder"
  | "tasks.parser.action"
  | "tasks.parser.applied"
  | "tasks.parser.failed"
  | "tasks.filters.title"
  | "tasks.filters.status"
  | "tasks.filters.project"
  | "tasks.filters.allStatuses"
  | "tasks.filters.allProjects"
  | "tasks.filters.noProject"
  | "tasks.queue.eyebrow"
  | "tasks.queue.title"
  | "tasks.empty"
  | "tasks.noDueDate"
  | "tasks.message.titleRequired"
  | "tasks.message.loadFailed"
  | "tasks.message.created"
  | "tasks.message.updated"
  | "tasks.message.saveFailed"
  | "tasks.message.deleteFailed"
  | "tasks.meta.minutesSuffix"
  | "tasks.meta.load"
  | "calendar.eyebrow"
  | "calendar.title"
  | "calendar.date"
  | "calendar.action.generate"
  | "calendar.action.select"
  | "calendar.action.reoptimize"
  | "calendar.message.generatedPrefix"
  | "calendar.message.generatedSuffix"
  | "calendar.message.generateFailed"
  | "calendar.message.selected"
  | "calendar.message.selectionFailed"
  | "calendar.message.reoptimized"
  | "calendar.message.reoptimizeFailed"
  | "calendar.message.validateFailed"
  | "calendar.metric.items"
  | "calendar.metric.score"
  | "calendar.metric.risk"
  | "calendar.badge.selected"
  | "calendar.unplaced"
  | "calendar.unplacedReasons"
  | "calendar.explanation.title"
  | "calendar.explanation.risk"
  | "calendar.taskPrefix"
  | "calendar.segment"
  | "calendar.emptyPlanItems"
  | "calendar.emptyTitle"
  | "calendar.emptyDescription"
  | "calendar.validate.title"
  | "calendar.validate.task"
  | "calendar.validate.start"
  | "calendar.validate.end"
  | "calendar.validate.action"
  | "calendar.validate.valid"
  | "calendar.validate.invalid"
  | "calendar.validate.noItems"
  | "calendar.validate.conflicts"
  | "today.eyebrow"
  | "today.title"
  | "today.date"
  | "today.action.refresh"
  | "today.action.saveFeedback"
  | "today.emptyTitle"
  | "today.emptyDescription"
  | "today.status"
  | "today.message.loadFailed"
  | "today.message.feedbackSaved"
  | "today.message.feedbackFailed"
  | "today.metrics.title"
  | "today.metrics.planned"
  | "today.metrics.completed"
  | "today.metrics.skippedIncomplete"
  | "today.metrics.completionRate"
  | "review.eyebrow"
  | "review.title"
  | "review.date"
  | "review.action.refresh"
  | "review.emptyTitle"
  | "review.emptyDescription"
  | "review.message.loadFailed"
  | "review.summary.title"
  | "review.summary.planned"
  | "review.summary.completed"
  | "review.summary.skippedIncomplete"
  | "review.summary.completionRate"
  | "review.summary.plannedMinutes"
  | "review.summary.actualMinutes"
  | "review.summary.variance"
  | "review.table.task"
  | "review.table.outcome"
  | "review.table.estimate"
  | "review.table.actual"
  | "review.table.variance"
  | "review.table.note"
  | "status.todo"
  | "status.in_progress"
  | "status.done"
  | "status.canceled"
  | "status.skipped"
  | "status.incomplete"
  | "plan.conservative"
  | "plan.balanced"
  | "plan.aggressive"
  | "risk.low"
  | "risk.medium"
  | "risk.high";

export const translations: Record<Language, Record<TranslationKey, string>> = {
  "zh-CN": {
    "app.name": "FocusFlow",
    "nav.tasks": "任务",
    "nav.calendar": "日历",
    "nav.today": "今日",
    "nav.review": "复盘",
    "language.zh": "中文",
    "language.en": "English",
    "language.label": "语言",
    "common.loading": "加载中",
    "common.notAvailable": "不可用",
    "common.error": "错误",
    "common.success": "成功",
    "common.minutes": "分钟",
    "common.score": "分数",
    "tasks.eyebrow": "任务收集",
    "tasks.title": "先塑造任务，再安排今天。",
    "tasks.form.title": "标题",
    "tasks.form.titlePlaceholder": "撰写产品简报",
    "tasks.form.minutes": "分钟",
    "tasks.form.load": "负荷",
    "tasks.form.due": "截止时间",
    "tasks.form.status": "状态",
    "tasks.form.splits": "拆分",
    "tasks.form.allowSplit": "允许拆分排期",
    "tasks.action.create": "创建任务",
    "tasks.action.save": "保存任务",
    "tasks.action.cancel": "取消",
    "tasks.action.refresh": "刷新",
    "tasks.action.edit": "编辑",
    "tasks.action.delete": "删除",
    "tasks.parser.title": "快速解析",
    "tasks.parser.inputLabel": "任务描述",
    "tasks.parser.placeholder": "例如：写发布说明 90分钟 high",
    "tasks.parser.action": "解析为任务草稿",
    "tasks.parser.applied": "已填入任务草稿",
    "tasks.parser.failed": "解析任务失败",
    "tasks.filters.title": "筛选",
    "tasks.filters.status": "状态",
    "tasks.filters.project": "项目",
    "tasks.filters.allStatuses": "全部状态",
    "tasks.filters.allProjects": "全部项目",
    "tasks.filters.noProject": "无项目",
    "tasks.queue.eyebrow": "队列",
    "tasks.queue.title": "任务",
    "tasks.empty": "还没有任务。",
    "tasks.noDueDate": "无截止时间",
    "tasks.message.titleRequired": "请输入任务标题",
    "tasks.message.loadFailed": "加载任务失败",
    "tasks.message.created": "任务已创建",
    "tasks.message.updated": "任务已更新",
    "tasks.message.saveFailed": "保存任务失败",
    "tasks.message.deleteFailed": "删除任务失败",
    "tasks.meta.minutesSuffix": "分钟",
    "tasks.meta.load": "负荷",
    "calendar.eyebrow": "每日计划",
    "calendar.title": "选择一个真正能执行的今天。",
    "calendar.date": "日期",
    "calendar.action.generate": "生成方案",
    "calendar.action.select": "选择方案",
    "calendar.action.reoptimize": "重新优化",
    "calendar.message.generatedPrefix": "已生成",
    "calendar.message.generatedSuffix": "个方案",
    "calendar.message.generateFailed": "生成排期失败",
    "calendar.message.selected": "已选择",
    "calendar.message.selectionFailed": "选择方案失败",
    "calendar.message.reoptimized": "已重新优化",
    "calendar.message.reoptimizeFailed": "重新优化失败",
    "calendar.message.validateFailed": "校验移动失败",
    "calendar.metric.items": "项",
    "calendar.metric.score": "分数",
    "calendar.metric.risk": "风险",
    "calendar.badge.selected": "已选",
    "calendar.unplaced": "未排入任务",
    "calendar.unplacedReasons": "未排入原因",
    "calendar.explanation.title": "方案说明",
    "calendar.explanation.risk": "风险说明",
    "calendar.taskPrefix": "任务",
    "calendar.segment": "片段",
    "calendar.emptyPlanItems": "这个方案没有排入任务。",
    "calendar.emptyTitle": "还没有生成方案",
    "calendar.emptyDescription": "先添加几个任务，然后为所选日期生成方案。",
    "calendar.validate.title": "移动校验",
    "calendar.validate.task": "任务",
    "calendar.validate.start": "开始",
    "calendar.validate.end": "结束",
    "calendar.validate.action": "校验移动",
    "calendar.validate.valid": "可以移动",
    "calendar.validate.invalid": "存在冲突",
    "calendar.validate.noItems": "先生成一个含任务的方案。",
    "calendar.validate.conflicts": "冲突",
    "today.eyebrow": "今日执行",
    "today.title": "执行已选择的计划",
    "today.date": "日期",
    "today.action.refresh": "刷新今日",
    "today.action.saveFeedback": "提交反馈",
    "today.emptyTitle": "还没有选择今日方案",
    "today.emptyDescription": "先到日历中生成并选择一个方案。",
    "today.status": "状态",
    "today.message.loadFailed": "加载今日任务失败",
    "today.message.feedbackSaved": "反馈已提交",
    "today.message.feedbackFailed": "提交反馈失败",
    "today.metrics.title": "今日进度",
    "today.metrics.planned": "计划",
    "today.metrics.completed": "完成",
    "today.metrics.skippedIncomplete": "未完成",
    "today.metrics.completionRate": "完成率",
    "review.eyebrow": "每日复盘",
    "review.title": "查看一天的执行结果",
    "review.date": "日期",
    "review.action.refresh": "刷新复盘",
    "review.emptyTitle": "这一天还没有执行记录",
    "review.emptyDescription": "先在今日页提交反馈，或选择已有历史的日期。",
    "review.message.loadFailed": "加载复盘失败",
    "review.summary.title": "复盘摘要",
    "review.summary.planned": "计划任务",
    "review.summary.completed": "完成",
    "review.summary.skippedIncomplete": "未完成",
    "review.summary.completionRate": "完成率",
    "review.summary.plannedMinutes": "估算分钟",
    "review.summary.actualMinutes": "实际分钟",
    "review.summary.variance": "估算偏差",
    "review.table.task": "任务",
    "review.table.outcome": "结果",
    "review.table.estimate": "估算",
    "review.table.actual": "实际",
    "review.table.variance": "偏差",
    "review.table.note": "备注",
    "status.todo": "待办",
    "status.in_progress": "进行中",
    "status.done": "完成",
    "status.canceled": "取消",
    "status.skipped": "跳过",
    "status.incomplete": "未完成",
    "plan.conservative": "保守",
    "plan.balanced": "平衡",
    "plan.aggressive": "激进",
    "risk.low": "低",
    "risk.medium": "中",
    "risk.high": "高",
  },
  en: {
    "app.name": "FocusFlow",
    "nav.tasks": "Tasks",
    "nav.calendar": "Calendar",
    "nav.today": "Today",
    "nav.review": "Review",
    "language.zh": "中文",
    "language.en": "English",
    "language.label": "Language",
    "common.loading": "Loading",
    "common.notAvailable": "Not available",
    "common.error": "Error",
    "common.success": "Success",
    "common.minutes": "minutes",
    "common.score": "score",
    "tasks.eyebrow": "Task Intake",
    "tasks.title": "Shape the day before it starts.",
    "tasks.form.title": "Title",
    "tasks.form.titlePlaceholder": "Write product brief",
    "tasks.form.minutes": "Minutes",
    "tasks.form.load": "Load",
    "tasks.form.due": "Due",
    "tasks.form.status": "Status",
    "tasks.form.splits": "Splits",
    "tasks.form.allowSplit": "Allow split scheduling",
    "tasks.action.create": "Create Task",
    "tasks.action.save": "Save Task",
    "tasks.action.cancel": "Cancel",
    "tasks.action.refresh": "Refresh",
    "tasks.action.edit": "Edit",
    "tasks.action.delete": "Delete",
    "tasks.parser.title": "Quick Parse",
    "tasks.parser.inputLabel": "Task description",
    "tasks.parser.placeholder": "Example: Write launch notes 90min high",
    "tasks.parser.action": "Parse Draft",
    "tasks.parser.applied": "Draft applied to the form",
    "tasks.parser.failed": "Task parse failed",
    "tasks.filters.title": "Filters",
    "tasks.filters.status": "Status",
    "tasks.filters.project": "Project",
    "tasks.filters.allStatuses": "All statuses",
    "tasks.filters.allProjects": "All projects",
    "tasks.filters.noProject": "No project",
    "tasks.queue.eyebrow": "Queue",
    "tasks.queue.title": "Tasks",
    "tasks.empty": "No tasks yet.",
    "tasks.noDueDate": "No due date",
    "tasks.message.titleRequired": "Title is required",
    "tasks.message.loadFailed": "Failed to load tasks",
    "tasks.message.created": "Task created",
    "tasks.message.updated": "Task updated",
    "tasks.message.saveFailed": "Task save failed",
    "tasks.message.deleteFailed": "Delete failed",
    "tasks.meta.minutesSuffix": "min",
    "tasks.meta.load": "load",
    "calendar.eyebrow": "Daily Plan",
    "calendar.title": "Pick the version of today you can actually live.",
    "calendar.date": "Date",
    "calendar.action.generate": "Generate Plans",
    "calendar.action.select": "Select Plan",
    "calendar.action.reoptimize": "Reoptimize",
    "calendar.message.generatedPrefix": "Generated",
    "calendar.message.generatedSuffix": "plans",
    "calendar.message.generateFailed": "Schedule generation failed",
    "calendar.message.selected": "selected",
    "calendar.message.selectionFailed": "Plan selection failed",
    "calendar.message.reoptimized": "Reoptimized",
    "calendar.message.reoptimizeFailed": "Reoptimization failed",
    "calendar.message.validateFailed": "Move validation failed",
    "calendar.metric.items": "items",
    "calendar.metric.score": "score",
    "calendar.metric.risk": "risk",
    "calendar.badge.selected": "selected",
    "calendar.unplaced": "Unplaced tasks",
    "calendar.unplacedReasons": "Unplaced reasons",
    "calendar.explanation.title": "Plan explanation",
    "calendar.explanation.risk": "Risk explanation",
    "calendar.taskPrefix": "Task",
    "calendar.segment": "segment",
    "calendar.emptyPlanItems": "This plan has no scheduled items.",
    "calendar.emptyTitle": "No generated plan yet",
    "calendar.emptyDescription": "Add a few tasks, then generate plans for the selected date.",
    "calendar.validate.title": "Move Validation",
    "calendar.validate.task": "Task",
    "calendar.validate.start": "Start",
    "calendar.validate.end": "End",
    "calendar.validate.action": "Validate Move",
    "calendar.validate.valid": "Move is clear",
    "calendar.validate.invalid": "Conflicts found",
    "calendar.validate.noItems": "Generate a plan with tasks first.",
    "calendar.validate.conflicts": "Conflicts",
    "today.eyebrow": "Today Execution",
    "today.title": "Work the selected plan",
    "today.date": "Date",
    "today.action.refresh": "Refresh Today",
    "today.action.saveFeedback": "Submit Feedback",
    "today.emptyTitle": "No selected plan for today",
    "today.emptyDescription": "Generate and select a plan from the calendar first.",
    "today.status": "Status",
    "today.message.loadFailed": "Failed to load today",
    "today.message.feedbackSaved": "Feedback saved",
    "today.message.feedbackFailed": "Feedback failed",
    "today.metrics.title": "Today Progress",
    "today.metrics.planned": "Planned",
    "today.metrics.completed": "Completed",
    "today.metrics.skippedIncomplete": "Skipped/incomplete",
    "today.metrics.completionRate": "Completion",
    "review.eyebrow": "Daily Review",
    "review.title": "Review a day of execution",
    "review.date": "Date",
    "review.action.refresh": "Refresh Review",
    "review.emptyTitle": "No execution records for this day",
    "review.emptyDescription": "Submit feedback on Today, or choose a date with history.",
    "review.message.loadFailed": "Failed to load review",
    "review.summary.title": "Review Summary",
    "review.summary.planned": "Planned tasks",
    "review.summary.completed": "Completed",
    "review.summary.skippedIncomplete": "Skipped/incomplete",
    "review.summary.completionRate": "Completion rate",
    "review.summary.plannedMinutes": "Estimated minutes",
    "review.summary.actualMinutes": "Actual minutes",
    "review.summary.variance": "Estimate variance",
    "review.table.task": "Task",
    "review.table.outcome": "Outcome",
    "review.table.estimate": "Estimate",
    "review.table.actual": "Actual",
    "review.table.variance": "Variance",
    "review.table.note": "Note",
    "status.todo": "Todo",
    "status.in_progress": "In progress",
    "status.done": "Done",
    "status.canceled": "Canceled",
    "status.skipped": "Skipped",
    "status.incomplete": "Incomplete",
    "plan.conservative": "Conservative",
    "plan.balanced": "Balanced",
    "plan.aggressive": "Aggressive",
    "risk.low": "low",
    "risk.medium": "medium",
    "risk.high": "high",
  },
};

export function parseLanguage(value: unknown): Language {
  return LANGUAGES.includes(value as Language) ? (value as Language) : DEFAULT_LANGUAGE;
}

export function loadStoredLanguage(storage: Storage | undefined = globalThis.localStorage): Language {
  try {
    return parseLanguage(storage?.getItem(LANGUAGE_STORAGE_KEY));
  } catch {
    return DEFAULT_LANGUAGE;
  }
}

export function saveStoredLanguage(
  language: Language,
  storage: Storage | undefined = globalThis.localStorage,
): void {
  try {
    storage?.setItem(LANGUAGE_STORAGE_KEY, language);
  } catch {
    // Persistence is a convenience; the UI state remains authoritative.
  }
}

export function t(language: Language, key: TranslationKey): string {
  return translations[language][key];
}

export function getStatusLabel(language: Language, status: TaskStatus | ExecutionHistoryStatus): string {
  return t(language, `status.${status}`);
}

export function getPlanTypeLabel(language: Language, planType: PlanType): string {
  return t(language, `plan.${planType}`);
}
