export function formatMinutesValue(value: number | null): string {
  if (value === null) {
    return "-";
  }
  return `${value}`;
}

export function formatVarianceValue(value: number | null): string {
  if (value === null) {
    return "-";
  }
  return value > 0 ? `+${value}` : `${value}`;
}

export function formatCompletionRate(value: number): string {
  return `${Math.round(value * 100)}%`;
}

export function shiftDateByDays(date: string, days: number): string {
  const parts = date.split("-").map(Number);
  const year = parts[0] ?? 1970;
  const month = parts[1] ?? 1;
  const day = parts[2] ?? 1;
  const shifted = new Date(Date.UTC(year, month - 1, day));
  shifted.setUTCDate(shifted.getUTCDate() + days);
  return shifted.toISOString().slice(0, 10);
}

export function formatWeekRange(weekStart: string, weekEnd: string): string {
  return `${weekStart} - ${weekEnd}`;
}

export function formatDeltaValue(value: number | null, suffix = ""): string {
  if (value === null) {
    return "-";
  }
  return `${value > 0 ? "+" : ""}${value}${suffix}`;
}
