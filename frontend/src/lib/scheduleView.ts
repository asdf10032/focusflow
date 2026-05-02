export const PLAN_TYPES = ["conservative", "balanced", "aggressive"] as const;

export type PlanType = (typeof PLAN_TYPES)[number];

export type ScheduleItem = {
  task_id: number;
  start_datetime: string;
  end_datetime: string;
  segment_index?: number | null;
  warning?: string | null;
};

const PLAN_LABELS: Record<PlanType, string> = {
  conservative: "Conservative",
  balanced: "Balanced",
  aggressive: "Aggressive",
};

export function getPlanLabel(planType: string): string {
  return PLAN_LABELS[planType as PlanType] ?? planType;
}

export function sortScheduleItems(items: ScheduleItem[]): ScheduleItem[] {
  return [...items].sort((left, right) =>
    left.start_datetime.localeCompare(right.start_datetime),
  );
}

function formatClock(value: string): string {
  const parsed = new Date(value);
  if (!Number.isNaN(parsed.getTime())) {
    const hours = String(parsed.getHours()).padStart(2, "0");
    const minutes = String(parsed.getMinutes()).padStart(2, "0");
    return `${hours}:${minutes}`;
  }

  return value.slice(11, 16);
}

export function formatTimeRange(item: ScheduleItem): string {
  return `${formatClock(item.start_datetime)}-${formatClock(item.end_datetime)}`;
}
