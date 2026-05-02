import type { Task, TaskStatus } from "./api";

export type TaskFilterState = {
  search: string;
  status: TaskStatus | "all";
  project: string;
};

export function normalizeTaskSearch(value: string): string {
  return value.trim().toLowerCase();
}

function matchesSearch(task: Pick<Task, "title" | "notes">, search: string): boolean {
  const query = normalizeTaskSearch(search);
  if (!query) {
    return true;
  }
  return (
    task.title.toLowerCase().includes(query) ||
    (task.notes ?? "").toLowerCase().includes(query)
  );
}

function matchesProject(task: Pick<Task, "project_id">, project: string): boolean {
  return (
    project === "all" ||
    (project === "none" && task.project_id === null) ||
    String(task.project_id) === project
  );
}

export function filterTasks<T extends Pick<Task, "title" | "notes" | "status" | "project_id">>(
  tasks: T[],
  filters: TaskFilterState,
): T[] {
  return tasks.filter(
    (task) =>
      matchesSearch(task, filters.search) &&
      (filters.status === "all" || task.status === filters.status) &&
      matchesProject(task, filters.project),
  );
}
