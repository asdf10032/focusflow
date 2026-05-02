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
  | "exports.title"
  | "exports.tasksJson"
  | "exports.historyJson"
  | "exports.reviewCsv"
  | "exports.success"
  | "exports.failed"
  | "exports.empty"
  | "exports.emptyNoDownload"
  | "tasks.eyebrow"
  | "tasks.title"
  | "tasks.form.title"
  | "tasks.form.titlePlaceholder"
  | "tasks.form.notes"
  | "tasks.form.notesPlaceholder"
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
  | "tasks.suggestion.title"
  | "tasks.suggestion.action"
  | "tasks.suggestion.accept"
  | "tasks.suggestion.empty"
  | "tasks.suggestion.suggestedMinutes"
  | "tasks.suggestion.confidence"
  | "tasks.suggestion.confidence.high"
  | "tasks.suggestion.confidence.medium"
  | "tasks.suggestion.confidence.low"
  | "tasks.suggestion.samples"
  | "tasks.suggestion.source"
  | "tasks.suggestion.source.history"
  | "tasks.suggestion.source.fallback"
  | "tasks.suggestion.failed"
  | "tasks.suggestion.accepted"
  | "tasks.suggestion.needsTitle"
  | "tasks.suggestion.reason.history_project_load_match"
  | "tasks.suggestion.reason.history_project_match"
  | "tasks.suggestion.reason.history_load_match"
  | "tasks.suggestion.reason.history_title_match"
  | "tasks.suggestion.reason.fallback_current_estimate"
  | "tasks.suggestion.reason.fallback_low_load"
  | "tasks.suggestion.reason.fallback_medium_load"
  | "tasks.suggestion.reason.fallback_high_load"
  | "tasks.filters.title"
  | "tasks.filters.search"
  | "tasks.filters.searchPlaceholder"
  | "tasks.filters.status"
  | "tasks.filters.project"
  | "tasks.filters.allStatuses"
  | "tasks.filters.allProjects"
  | "tasks.filters.noProject"
  | "tasks.queue.eyebrow"
  | "tasks.queue.title"
  | "tasks.empty"
  | "tasks.emptyFiltered"
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
  | "calendar.action.partialReplan"
  | "calendar.message.generatedPrefix"
  | "calendar.message.generatedSuffix"
  | "calendar.message.generateFailed"
  | "calendar.message.selected"
  | "calendar.message.selectionFailed"
  | "calendar.message.reoptimized"
  | "calendar.message.reoptimizeFailed"
  | "calendar.message.partialReplanned"
  | "calendar.message.partialReplanFailed"
  | "calendar.message.partialReplanMissingSelected"
  | "calendar.message.partialReplanNoRemaining"
  | "calendar.message.partialReplanNoSchedulableTime"
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
  | "today.emptyPlanItems"
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
  | "review.view.daily"
  | "review.view.weekly"
  | "review.action.refresh"
  | "review.action.previousWeek"
  | "review.action.nextWeek"
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
  | "review.week.range"
  | "review.week.summaryTitle"
  | "review.week.logged"
  | "review.week.comparisonTitle"
  | "review.week.comparisonUnavailable"
  | "review.week.breakdownTitle"
  | "review.week.emptyTitle"
  | "review.week.emptyDescription"
  | "review.week.emptyDay"
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
    "exports.title": "导出",
    "exports.tasksJson": "导出任务 JSON",
    "exports.historyJson": "导出历史 JSON",
    "exports.reviewCsv": "导出复盘 CSV",
    "exports.success": "导出文件已准备",
    "exports.failed": "导出失败",
    "exports.empty": "暂无可导出的本地数据。",
    "exports.emptyNoDownload": "暂无可导出的本地数据。",
    "tasks.eyebrow": "任务收集",
    "tasks.title": "先塑造任务，再安排今天。",
    "tasks.form.title": "标题",
    "tasks.form.titlePlaceholder": "撰写产品简报",
    "tasks.form.notes": "备注",
    "tasks.form.notesPlaceholder": "补充背景、链接或验收要点",
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
    "tasks.suggestion.title": "时长建议",
    "tasks.suggestion.action": "建议时长",
    "tasks.suggestion.accept": "使用建议",
    "tasks.suggestion.empty": "输入标题后获取基于历史或负荷的建议。",
    "tasks.suggestion.suggestedMinutes": "建议时长",
    "tasks.suggestion.confidence": "置信度",
    "tasks.suggestion.confidence.high": "高",
    "tasks.suggestion.confidence.medium": "中",
    "tasks.suggestion.confidence.low": "低",
    "tasks.suggestion.samples": "样本",
    "tasks.suggestion.source": "来源",
    "tasks.suggestion.source.history": "历史",
    "tasks.suggestion.source.fallback": "兜底",
    "tasks.suggestion.failed": "获取时长建议失败",
    "tasks.suggestion.accepted": "已使用时长建议",
    "tasks.suggestion.needsTitle": "先输入任务标题再获取建议",
    "tasks.suggestion.reason.history_project_load_match": "相似已完成任务，且项目和负荷匹配",
    "tasks.suggestion.reason.history_project_match": "相似已完成任务，且项目匹配",
    "tasks.suggestion.reason.history_load_match": "相似已完成任务，且负荷匹配",
    "tasks.suggestion.reason.history_title_match": "基于相似已完成任务",
    "tasks.suggestion.reason.fallback_current_estimate": "使用当前填写的估算",
    "tasks.suggestion.reason.fallback_low_load": "基于低负荷默认值",
    "tasks.suggestion.reason.fallback_medium_load": "基于中等负荷默认值",
    "tasks.suggestion.reason.fallback_high_load": "基于高负荷默认值",
    "tasks.filters.title": "筛选",
    "tasks.filters.search": "搜索",
    "tasks.filters.searchPlaceholder": "搜索标题或备注",
    "tasks.filters.status": "状态",
    "tasks.filters.project": "项目",
    "tasks.filters.allStatuses": "全部状态",
    "tasks.filters.allProjects": "全部项目",
    "tasks.filters.noProject": "无项目",
    "tasks.queue.eyebrow": "队列",
    "tasks.queue.title": "任务",
    "tasks.empty": "还没有任务。",
    "tasks.emptyFiltered": "没有匹配当前搜索和筛选条件的任务。",
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
    "calendar.action.partialReplan": "重排剩余工作",
    "calendar.message.generatedPrefix": "已生成",
    "calendar.message.generatedSuffix": "个方案",
    "calendar.message.generateFailed": "生成排期失败",
    "calendar.message.selected": "已选择",
    "calendar.message.selectionFailed": "选择方案失败",
    "calendar.message.reoptimized": "已重新优化",
    "calendar.message.reoptimizeFailed": "重新优化失败",
    "calendar.message.partialReplanned": "已重排剩余工作，请重新选择方案",
    "calendar.message.partialReplanFailed": "重排剩余工作失败",
    "calendar.message.partialReplanMissingSelected": "请先选择一个当天方案，再重排剩余工作。",
    "calendar.message.partialReplanNoRemaining": "当天没有剩余工作需要重排。",
    "calendar.message.partialReplanNoSchedulableTime": "当天没有可用于剩余工作的可排时间。",
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
    "today.emptyPlanItems": "已选择方案，但当前没有可执行的任务项。",
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
    "review.view.daily": "每日",
    "review.view.weekly": "每周",
    "review.action.refresh": "刷新复盘",
    "review.action.previousWeek": "上一周",
    "review.action.nextWeek": "下一周",
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
    "review.week.range": "周范围",
    "review.week.summaryTitle": "周复盘摘要",
    "review.week.logged": "记录",
    "review.week.comparisonTitle": "与上一周对比",
    "review.week.comparisonUnavailable": "还没有上一周数据。",
    "review.week.breakdownTitle": "每日拆分",
    "review.week.emptyTitle": "这一周还没有执行记录",
    "review.week.emptyDescription": "在今日页提交反馈后，这里会显示周复盘。",
    "review.week.emptyDay": "这一天没有记录。",
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
    "exports.title": "Export",
    "exports.tasksJson": "Export tasks JSON",
    "exports.historyJson": "Export history JSON",
    "exports.reviewCsv": "Export review CSV",
    "exports.success": "Export file is ready",
    "exports.failed": "Export failed",
    "exports.empty": "No local data to export yet.",
    "exports.emptyNoDownload": "No local data to export yet.",
    "tasks.eyebrow": "Task Intake",
    "tasks.title": "Shape the day before it starts.",
    "tasks.form.title": "Title",
    "tasks.form.titlePlaceholder": "Write product brief",
    "tasks.form.notes": "Notes",
    "tasks.form.notesPlaceholder": "Add context, links, or acceptance notes",
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
    "tasks.suggestion.title": "Duration suggestion",
    "tasks.suggestion.action": "Suggest duration",
    "tasks.suggestion.accept": "Use suggestion",
    "tasks.suggestion.empty": "Enter a title to get a suggestion from history or load.",
    "tasks.suggestion.suggestedMinutes": "Suggested minutes",
    "tasks.suggestion.confidence": "Confidence",
    "tasks.suggestion.confidence.high": "high",
    "tasks.suggestion.confidence.medium": "medium",
    "tasks.suggestion.confidence.low": "low",
    "tasks.suggestion.samples": "samples",
    "tasks.suggestion.source": "source",
    "tasks.suggestion.source.history": "history",
    "tasks.suggestion.source.fallback": "fallback",
    "tasks.suggestion.failed": "Duration suggestion failed",
    "tasks.suggestion.accepted": "Duration suggestion applied",
    "tasks.suggestion.needsTitle": "Enter a task title before requesting a suggestion",
    "tasks.suggestion.reason.history_project_load_match": "Similar completed tasks with matching project and load",
    "tasks.suggestion.reason.history_project_match": "Similar completed tasks with matching project",
    "tasks.suggestion.reason.history_load_match": "Similar completed tasks with matching load",
    "tasks.suggestion.reason.history_title_match": "Similar completed tasks",
    "tasks.suggestion.reason.fallback_current_estimate": "Using the current estimate",
    "tasks.suggestion.reason.fallback_low_load": "Using the low-load default",
    "tasks.suggestion.reason.fallback_medium_load": "Using the medium-load default",
    "tasks.suggestion.reason.fallback_high_load": "Using the high-load default",
    "tasks.filters.title": "Filters",
    "tasks.filters.search": "Search",
    "tasks.filters.searchPlaceholder": "Search titles or notes",
    "tasks.filters.status": "Status",
    "tasks.filters.project": "Project",
    "tasks.filters.allStatuses": "All statuses",
    "tasks.filters.allProjects": "All projects",
    "tasks.filters.noProject": "No project",
    "tasks.queue.eyebrow": "Queue",
    "tasks.queue.title": "Tasks",
    "tasks.empty": "No tasks yet.",
    "tasks.emptyFiltered": "No tasks match the current search and filters.",
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
    "calendar.action.partialReplan": "Partial Replan",
    "calendar.message.generatedPrefix": "Generated",
    "calendar.message.generatedSuffix": "plans",
    "calendar.message.generateFailed": "Schedule generation failed",
    "calendar.message.selected": "selected",
    "calendar.message.selectionFailed": "Plan selection failed",
    "calendar.message.reoptimized": "Reoptimized",
    "calendar.message.reoptimizeFailed": "Reoptimization failed",
    "calendar.message.partialReplanned": "Remaining work replanned. Select a new plan to continue.",
    "calendar.message.partialReplanFailed": "Partial replan failed",
    "calendar.message.partialReplanMissingSelected": "Select a plan for this date before replanning remaining work.",
    "calendar.message.partialReplanNoRemaining": "There is no remaining work to replan for this date.",
    "calendar.message.partialReplanNoSchedulableTime": "There is no schedulable time left for the remaining work.",
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
    "today.emptyPlanItems": "A plan is selected, but it has no work items left.",
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
    "review.view.daily": "Daily",
    "review.view.weekly": "Weekly",
    "review.action.refresh": "Refresh Review",
    "review.action.previousWeek": "Previous week",
    "review.action.nextWeek": "Next week",
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
    "review.week.range": "Week range",
    "review.week.summaryTitle": "Weekly summary",
    "review.week.logged": "Logged",
    "review.week.comparisonTitle": "Compared with previous week",
    "review.week.comparisonUnavailable": "No previous-week data yet.",
    "review.week.breakdownTitle": "Daily breakdown",
    "review.week.emptyTitle": "No execution records for this week",
    "review.week.emptyDescription": "Submit feedback on Today to see weekly review data here.",
    "review.week.emptyDay": "No records for this day.",
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

export function getSuggestionReasonLabel(
  language: Language,
  reasonCode: string,
  fallback: string,
): string {
  const key = `tasks.suggestion.reason.${reasonCode}` as TranslationKey;
  return Object.prototype.hasOwnProperty.call(translations[language], key)
    ? translations[language][key]
    : fallback;
}
