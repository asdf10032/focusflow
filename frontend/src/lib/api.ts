import type { PlanType, ScheduleItem } from "./scheduleView";

export type TaskStatus = "todo" | "in_progress" | "done" | "canceled";

export type Task = {
  id: number;
  title: string;
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

export type TaskPayload = {
  title: string;
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
  items: ScheduleItem[];
};

export type GenerateScheduleResult = {
  plans: SchedulePlan[];
  unplaced: number[];
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

type ApiEnvelope<T> = {
  status: "success" | "error";
  data: T | null;
  error: { code: string; message: string; details?: unknown } | null;
  meta: unknown;
};

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
    throw new Error(payload.error?.message ?? `Request failed: ${response.status}`);
  }

  if (payload.data === null) {
    throw new Error("Response did not include data");
  }

  return payload.data;
}

export function listTasks(): Promise<Task[]> {
  return requestJson<Task[]>("/tasks");
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

export function getTodayExecution(date: string): Promise<TodayExecution> {
  return requestJson<TodayExecution>(`/execution/today?date=${encodeURIComponent(date)}`);
}

export function submitExecutionFeedback(taskId: number, status: TaskStatus): Promise<Task> {
  return requestJson<Task>("/execution/feedback", {
    method: "POST",
    body: JSON.stringify({ task_id: taskId, status }),
  });
}

export function parseTaskDraft(text: string): Promise<TaskDraft> {
  return requestJson<TaskDraft>("/ai/parse-task", {
    method: "POST",
    body: JSON.stringify({ text }),
  });
}
