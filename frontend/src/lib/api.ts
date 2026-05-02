import { buildExportQuery, type ExportDateRange, type ExportPayload } from "./exportView";
import type { PlanType, ScheduleItem } from "./scheduleView";

export type TaskStatus = "todo" | "in_progress" | "done" | "canceled";
export type FeedbackStatus = TaskStatus | "skipped" | "incomplete";
export type ExecutionHistoryStatus = "done" | "skipped" | "incomplete" | "canceled";

export type Task = {
  id: number;
  title: string;
  notes: string | null;
  estimated_minutes: number;
  cognitive_load: number;
  due_at: string | null;
  earliest_start_at: string | null;
  fixed_start_at: string | null;
  is_splittable: boolean;
  max_split_count: number;
  status: TaskStatus;
  project_id: number | null;
};

export type Project = {
  id: number;
  name: string;
  priority: number;
};

export type TaskPayload = {
  title: string;
  notes?: string | null;
  estimated_minutes: number;
  cognitive_load: number;
  due_at?: string | null;
  is_splittable?: boolean;
  max_split_count?: number;
  status?: TaskStatus;
  project_id?: number | null;
};

export type SchedulePlan = {
  date: string;
  plan_type: PlanType;
  score: number | null;
  risk_level: string | null;
  summary: string;
  risk_explanation: string;
  items: ScheduleItem[];
};

export type UnplacedReason = {
  task_id: number;
  reason: string;
  message: string;
};

export type GenerateScheduleResult = {
  plans: SchedulePlan[];
  unplaced: number[];
  unplaced_reasons: UnplacedReason[];
  warnings: string[];
};

export type ScheduleConflict = {
  type: string;
  message: string;
  task_id?: number;
  start_datetime?: string;
  end_datetime?: string;
  start_minute_of_day?: number;
  end_minute_of_day?: number;
};

export type ValidateMoveResult = {
  valid: boolean;
  conflicts: ScheduleConflict[];
  proposed_item: ScheduleItem;
};

export type TaskDraft = TaskPayload;

export type DurationSuggestionConfidence = "high" | "medium" | "low";
export type DurationSuggestionSource = "history" | "fallback";

export type DurationSuggestionRequest = {
  title: string;
  project_id?: number | null;
  cognitive_load?: number | null;
  estimated_minutes?: number | null;
};

export type DurationSuggestion = {
  suggested_minutes: number;
  confidence: DurationSuggestionConfidence;
  sample_count: number;
  source: DurationSuggestionSource;
  reason_code: string;
  reason: string;
};

export type { ExportDateRange, ExportPayload };

export type TodayExecutionItem = ScheduleItem & {
  task: Task;
};

export type TodayExecution = {
  date: string;
  selected_plan: {
    id: number;
    date: string;
    plan_type: PlanType;
    score: number | null;
    risk_level: string | null;
    selected: boolean;
  } | null;
  items: TodayExecutionItem[];
};

export type ExecutionProgress = {
  date: string;
  selected_plan: TodayExecution["selected_plan"];
  planned_count: number;
  completed_count: number;
  skipped_incomplete_count: number;
  completion_rate: number;
};

export type ExecutionReviewSummary = ExecutionProgress & {
  planned_minutes: number;
  actual_minutes: number;
  estimate_variance_minutes: number | null;
};

export type ExecutionReviewItem = {
  id: number;
  task_id: number;
  task_title_snapshot: string;
  estimated_minutes_snapshot: number;
  date: string;
  status: ExecutionHistoryStatus;
  actual_minutes: number | null;
  note: string | null;
  created_at: string;
  estimate_variance_minutes: number | null;
};

export type ExecutionReview = {
  date: string;
  selected_plan: TodayExecution["selected_plan"];
  summary: ExecutionReviewSummary;
  items: ExecutionReviewItem[];
};

export type WeeklyReviewSummary = {
  logged_count: number;
  completed_count: number;
  skipped_incomplete_count: number;
  completion_rate: number;
  planned_minutes: number;
  actual_minutes: number;
  estimate_variance_minutes: number | null;
};

export type WeeklyReviewDay = {
  date: string;
  summary: WeeklyReviewSummary;
  items: ExecutionReviewItem[];
};

export type WeeklyReviewComparisonDeltas = {
  completion_rate: number | null;
  actual_minutes: number | null;
  estimate_variance_minutes: number | null;
};

export type WeeklyReviewComparison = {
  available: boolean;
  previous_week_start: string;
  previous_week_end: string;
  previous_summary: WeeklyReviewSummary | null;
  deltas: WeeklyReviewComparisonDeltas | null;
  message_code: string | null;
};

export type WeeklyReview = {
  week_start: string;
  week_end: string;
  summary: WeeklyReviewSummary;
  days: WeeklyReviewDay[];
  comparison: WeeklyReviewComparison;
};

type ApiEnvelope<T> = {
  status: "success" | "error";
  data: T | null;
  error: { code: string; message: string; details?: unknown } | null;
  meta: unknown;
};

export class ApiError extends Error {
  code: string;
  details?: unknown;

  constructor(code: string, message: string, details?: unknown) {
    super(message);
    this.name = "ApiError";
    this.code = code;
    this.details = details;
  }
}

async function requestJson<T>(path: string, init?: RequestInit): Promise<T> {
  const response = await fetch(`/api/v1${path}`, {
    headers: {
      "Content-Type": "application/json",
      ...(init?.headers ?? {}),
    },
    ...init,
  });
  const payload = (await response.json()) as ApiEnvelope<T>;

  if (!response.ok || payload.status === "error") {
    throw new ApiError(
      payload.error?.code ?? "request_failed",
      payload.error?.message ?? `Request failed: ${response.status}`,
      payload.error?.details,
    );
  }

  if (payload.data === null) {
    throw new Error("Response did not include data");
  }

  return payload.data;
}

export function listTasks(params?: {
  q?: string;
  status?: TaskStatus | "all";
  project_id?: number | null;
}): Promise<Task[]> {
  const query = new URLSearchParams();
  if (params?.q?.trim()) {
    query.set("q", params.q.trim());
  }
  if (params?.status && params.status !== "all") {
    query.set("status", params.status);
  }
  if (typeof params?.project_id === "number") {
    query.set("project_id", String(params.project_id));
  }
  const suffix = query.toString() ? `?${query.toString()}` : "";
  return requestJson<Task[]>(`/tasks${suffix}`);
}

export function listProjects(): Promise<Project[]> {
  return requestJson<Project[]>("/projects");
}

export function createTask(payload: TaskPayload): Promise<Task> {
  return requestJson<Task>("/tasks", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function updateTask(taskId: number, payload: Partial<TaskPayload>): Promise<Task> {
  return requestJson<Task>(`/tasks/${taskId}`, {
    method: "PUT",
    body: JSON.stringify(payload),
  });
}

export function deleteTask(taskId: number): Promise<boolean> {
  return requestJson<boolean>(`/tasks/${taskId}`, {
    method: "DELETE",
  });
}

export function generateSchedule(date: string): Promise<GenerateScheduleResult> {
  return requestJson<GenerateScheduleResult>("/schedules/generate", {
    method: "POST",
    body: JSON.stringify({ date }),
  });
}

export function selectSchedulePlan(
  date: string,
  planType: PlanType,
): Promise<{ date: string; plan_type: PlanType; selected: boolean }> {
  return requestJson("/schedules/select", {
    method: "POST",
    body: JSON.stringify({ date, plan_type: planType }),
  });
}

export function validateScheduleMove(payload: {
  date: string;
  plan_type: PlanType;
  task_id: number;
  start_datetime: string;
  end_datetime: string;
  segment_index?: number | null;
}): Promise<ValidateMoveResult> {
  return requestJson<ValidateMoveResult>("/schedules/validate-move", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function reoptimizeSchedule(date: string): Promise<GenerateScheduleResult> {
  return requestJson<GenerateScheduleResult>("/schedules/reoptimize", {
    method: "POST",
    body: JSON.stringify({ date }),
  });
}

export function partialReplanSchedule(date: string): Promise<GenerateScheduleResult> {
  return requestJson<GenerateScheduleResult>("/schedules/partial-replan", {
    method: "POST",
    body: JSON.stringify({ date }),
  });
}

export function getTodayExecution(date: string): Promise<TodayExecution> {
  return requestJson<TodayExecution>(`/execution/today?date=${encodeURIComponent(date)}`);
}

export function getExecutionProgress(date: string): Promise<ExecutionProgress> {
  return requestJson<ExecutionProgress>(`/execution/progress?date=${encodeURIComponent(date)}`);
}

export function getExecutionReview(date: string): Promise<ExecutionReview> {
  return requestJson<ExecutionReview>(`/execution/review?date=${encodeURIComponent(date)}`);
}

export function getWeeklyExecutionReview(date: string): Promise<WeeklyReview> {
  return requestJson<WeeklyReview>(`/execution/weekly-review?date=${encodeURIComponent(date)}`);
}

export function submitExecutionFeedback(
  taskId: number,
  status: FeedbackStatus,
  options?: { date?: string; actual_minutes?: number | null; note?: string | null },
): Promise<Task> {
  return requestJson<Task>("/execution/feedback", {
    method: "POST",
    body: JSON.stringify({ task_id: taskId, status, ...(options ?? {}) }),
  });
}

export function parseTaskDraft(text: string): Promise<TaskDraft> {
  return requestJson<TaskDraft>("/ai/parse-task", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}

export function suggestTaskDuration(payload: DurationSuggestionRequest): Promise<DurationSuggestion> {
  return requestJson<DurationSuggestion>("/ai/suggest-duration", {
    method: "POST",
    body: JSON.stringify(payload),
  });
}

export function exportTasks(): Promise<ExportPayload> {
  return requestJson<ExportPayload>("/exports/tasks");
}

export function exportExecutionHistory(params: ExportDateRange): Promise<ExportPayload> {
  return requestJson<ExportPayload>(`/exports/execution-history${buildExportQuery(params)}`);
}

export function exportDailyReview(params: ExportDateRange): Promise<ExportPayload> {
  return requestJson<ExportPayload>(`/exports/daily-review${buildExportQuery(params)}`);
}
