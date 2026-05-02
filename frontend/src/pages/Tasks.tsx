import { FormEvent, useEffect, useMemo, useState } from "react";
import {
  createTask,
  deleteTask,
  exportTasks,
  listProjects,
  listTasks,
  parseTaskDraft,
  suggestTaskDuration,
  type DurationSuggestion,
  type DurationSuggestionConfidence,
  type DurationSuggestionRequest,
  type DurationSuggestionSource,
  type Project,
  type Task,
  type TaskPayload,
  type TaskStatus,
  updateTask,
} from "../lib/api";
import { triggerExportDownload } from "../lib/exportView";
import { getStatusLabel, getSuggestionReasonLabel, t, type TranslationKey } from "../lib/i18n";
import { filterTasks } from "../lib/taskView";
import { useAppStore } from "../state/store";

const STATUS_OPTIONS: TaskStatus[] = ["todo", "in_progress", "done", "canceled"];

type TaskForm = {
  title: string;
  notes: string;
  estimated_minutes: string;
  cognitive_load: string;
  due_at: string;
  is_splittable: boolean;
  max_split_count: string;
  status: TaskStatus;
};

const EMPTY_FORM: TaskForm = {
  title: "",
  notes: "",
  estimated_minutes: "60",
  cognitive_load: "5",
  due_at: "",
  is_splittable: false,
  max_split_count: "1",
  status: "todo",
};

function taskToForm(task: Task): TaskForm {
  return {
    title: task.title,
    notes: task.notes ?? "",
    estimated_minutes: String(task.estimated_minutes),
    cognitive_load: String(task.cognitive_load),
    due_at: task.due_at ? task.due_at.slice(0, 16) : "",
    is_splittable: task.is_splittable,
    max_split_count: String(task.max_split_count),
    status: task.status,
  };
}

function formToPayload(form: TaskForm): TaskPayload {
  return {
    title: form.title.trim(),
    notes: form.notes.trim() ? form.notes.trim() : null,
    estimated_minutes: Number(form.estimated_minutes),
    cognitive_load: Number(form.cognitive_load),
    due_at: form.due_at ? form.due_at : null,
    is_splittable: form.is_splittable,
    max_split_count: Number(form.max_split_count),
    status: form.status,
  };
}

function optionalInt(value: string, min: number, max: number): number | null {
  const parsed = Number(value);
  return Number.isInteger(parsed) && parsed >= min && parsed <= max ? parsed : null;
}

function suggestionPayloadFromForm(form: TaskForm): DurationSuggestionRequest | null {
  const title = form.title.trim();
  if (!title) {
    return null;
  }

  const cognitiveLoad = optionalInt(form.cognitive_load, 1, 10);
  const estimatedMinutes = optionalInt(form.estimated_minutes, 1, 480);
  return {
    title,
    ...(cognitiveLoad === null ? {} : { cognitive_load: cognitiveLoad }),
    ...(estimatedMinutes === null ? {} : { estimated_minutes: estimatedMinutes }),
  };
}

function confidenceKey(confidence: DurationSuggestionConfidence): TranslationKey {
  return `tasks.suggestion.confidence.${confidence}`;
}

function sourceKey(source: DurationSuggestionSource): TranslationKey {
  return `tasks.suggestion.source.${source}`;
}

function formatDue(value: string | null, noDueLabel: string): string {
  if (!value) {
    return noDueLabel;
  }
  return value.slice(0, 16).replace("T", " ");
}

export default function Tasks() {
  const { tasks, setTasks, language } = useAppStore();
  const [form, setForm] = useState<TaskForm>(EMPTY_FORM);
  const [editingId, setEditingId] = useState<number | null>(null);
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [parserText, setParserText] = useState("");
  const [suggestion, setSuggestion] = useState<DurationSuggestion | null>(null);
  const [suggestionLoading, setSuggestionLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState(false);
  const [projects, setProjects] = useState<Project[]>([]);
  const [searchText, setSearchText] = useState("");
  const [statusFilter, setStatusFilter] = useState<TaskStatus | "all">("all");
  const [projectFilter, setProjectFilter] = useState("all");

  async function refreshTasks() {
    setLoading(true);
    setMessage(null);
    try {
      setTasks(await listTasks());
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "tasks.message.loadFailed"));
      setTasks([]);
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshTasks();
    listProjects()
      .then(setProjects)
      .catch(() => setProjects([]));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const counts = useMemo(
    () =>
      tasks.reduce<Record<TaskStatus, number>>(
        (acc, task) => {
          acc[task.status] += 1;
          return acc;
        },
        { todo: 0, in_progress: 0, done: 0, canceled: 0 },
      ),
    [tasks],
  );

  const filteredTasks = useMemo(
    () =>
      filterTasks(tasks, {
        search: searchText,
        status: statusFilter,
        project: projectFilter,
      }),
    [projectFilter, searchText, statusFilter, tasks],
  );

  function updateForm(changes: Partial<TaskForm>) {
    setForm((current) => ({ ...current, ...changes }));
    setSuggestion(null);
  }

  async function fetchSuggestionForForm(nextForm: TaskForm): Promise<DurationSuggestion> {
    const payload = suggestionPayloadFromForm(nextForm);
    if (payload === null) {
      throw new Error(t(language, "tasks.suggestion.needsTitle"));
    }

    setSuggestionLoading(true);
    try {
      const nextSuggestion = await suggestTaskDuration(payload);
      setSuggestion(nextSuggestion);
      return nextSuggestion;
    } finally {
      setSuggestionLoading(false);
    }
  }

  async function handleSuggestDuration() {
    setMessage(null);
    try {
      await fetchSuggestionForForm(form);
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "tasks.suggestion.failed"));
    }
  }

  function handleAcceptSuggestion() {
    if (suggestion === null) {
      return;
    }
    setForm((current) => ({
      ...current,
      estimated_minutes: String(suggestion.suggested_minutes),
    }));
    setMessage(t(language, "tasks.suggestion.accepted"));
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    const payload = formToPayload(form);
    if (!payload.title) {
      setMessage(t(language, "tasks.message.titleRequired"));
      return;
    }

    setLoading(true);
    setMessage(null);
    try {
      if (editingId === null) {
        await createTask(payload);
        setMessage(t(language, "tasks.message.created"));
      } else {
        await updateTask(editingId, payload);
        setMessage(t(language, "tasks.message.updated"));
      }
      setForm(EMPTY_FORM);
      setEditingId(null);
      setSuggestion(null);
      setTasks(await listTasks());
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "tasks.message.saveFailed"));
    } finally {
      setLoading(false);
    }
  }

  async function handleParseDraft() {
    const text = parserText.trim();
    if (!text) {
      setMessage(t(language, "tasks.message.titleRequired"));
      return;
    }

    setLoading(true);
    setMessage(null);
    setSuggestion(null);
    try {
      const draft = await parseTaskDraft(text);
      const nextForm = {
        title: draft.title,
        notes: "",
        estimated_minutes: String(draft.estimated_minutes),
        cognitive_load: String(draft.cognitive_load),
        due_at: draft.due_at ? draft.due_at.slice(0, 16) : "",
        is_splittable: draft.is_splittable ?? false,
        max_split_count: String(draft.max_split_count ?? 1),
        status: draft.status ?? "todo",
      };
      setForm(nextForm);
      try {
        await fetchSuggestionForForm(nextForm);
        setMessage(t(language, "tasks.parser.applied"));
      } catch {
        setMessage(`${t(language, "tasks.parser.applied")} ${t(language, "tasks.suggestion.failed")}`);
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "tasks.parser.failed"));
    } finally {
      setLoading(false);
    }
  }

  async function handleDelete(taskId: number) {
    setLoading(true);
    setMessage(null);
    try {
      await deleteTask(taskId);
      setTasks(await listTasks());
      if (editingId === taskId) {
        setEditingId(null);
        setForm(EMPTY_FORM);
        setSuggestion(null);
      }
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "tasks.message.deleteFailed"));
    } finally {
      setLoading(false);
    }
  }

  function beginEdit(task: Task) {
    setEditingId(task.id);
    setForm(taskToForm(task));
    setSuggestion(null);
    setMessage(null);
  }

  function cancelEdit() {
    setEditingId(null);
    setForm(EMPTY_FORM);
    setSuggestion(null);
    setMessage(null);
  }

  async function handleExportTasks() {
    setExportLoading(true);
    setMessage(null);
    try {
      const payload = await exportTasks();
      if (payload.record_count === 0) {
        setMessage(t(language, "exports.emptyNoDownload"));
        return;
      }
      triggerExportDownload(payload);
      setMessage(t(language, "exports.success"));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "exports.failed"));
    } finally {
      setExportLoading(false);
    }
  }

  return (
    <div className="grid gap-6 lg:grid-cols-[minmax(320px,420px)_1fr]">
      <section className="rounded border border-slate-300 bg-white p-5 shadow-sm">
        <div className="mb-5">
          <p className="text-xs font-black uppercase tracking-[0.2em] text-amber-700">
            {t(language, "tasks.eyebrow")}
          </p>
          <h1 className="mt-2 text-3xl font-black text-slate-950">
            {t(language, "tasks.title")}
          </h1>
        </div>

        <form className="space-y-4" onSubmit={handleSubmit}>
          <div className="rounded border border-amber-200 bg-amber-50 p-3">
            <h2 className="text-sm font-black text-slate-950">
              {t(language, "tasks.parser.title")}
            </h2>
            <label className="mt-3 block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.parser.inputLabel")}
              </span>
              <textarea
                value={parserText}
                onChange={(event) => setParserText(event.target.value)}
                rows={3}
                className="mt-1 w-full resize-none rounded border border-amber-200 bg-white px-3 py-2 outline-none focus:border-amber-600"
                placeholder={t(language, "tasks.parser.placeholder")}
              />
            </label>
            <button
              type="button"
              onClick={() => void handleParseDraft()}
              disabled={loading}
              className="mt-3 rounded bg-amber-600 px-3 py-2 text-sm font-black text-white disabled:opacity-50"
            >
              {t(language, "tasks.parser.action")}
            </button>
          </div>

          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "tasks.form.title")}
            </span>
            <input
              value={form.title}
              onChange={(event) => updateForm({ title: event.target.value })}
              className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
              placeholder={t(language, "tasks.form.titlePlaceholder")}
            />
          </label>

          <div className="grid grid-cols-2 gap-3">
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.form.minutes")}
              </span>
              <input
                type="number"
                min={1}
                max={480}
                value={form.estimated_minutes}
                onChange={(event) =>
                  updateForm({ estimated_minutes: event.target.value })
                }
                className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
              />
            </label>
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.form.load")}
              </span>
              <input
                type="number"
                min={1}
                max={10}
                value={form.cognitive_load}
                onChange={(event) => updateForm({ cognitive_load: event.target.value })}
                className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
              />
            </label>
          </div>

          <div className="rounded border border-slate-200 bg-slate-50 p-3">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
              <div>
                <h2 className="text-sm font-black text-slate-950">
                  {t(language, "tasks.suggestion.title")}
                </h2>
                {!suggestion && (
                  <p className="mt-1 text-sm text-slate-600">
                    {t(language, "tasks.suggestion.empty")}
                  </p>
                )}
              </div>
              <button
                type="button"
                onClick={() => void handleSuggestDuration()}
                disabled={loading || suggestionLoading}
                className="rounded border border-slate-300 bg-white px-3 py-2 text-sm font-bold text-slate-700 disabled:opacity-50"
              >
                {suggestionLoading
                  ? t(language, "common.loading")
                  : t(language, "tasks.suggestion.action")}
              </button>
            </div>
            {suggestion && (
              <div className="mt-3 space-y-3">
                <div className="grid gap-2 sm:grid-cols-2">
                  <div className="rounded border border-slate-200 bg-white p-2">
                    <div className="text-xs font-bold uppercase text-slate-500">
                      {t(language, "tasks.suggestion.suggestedMinutes")}
                    </div>
                    <div className="mt-1 text-lg font-black text-slate-950">
                      {suggestion.suggested_minutes} {t(language, "common.minutes")}
                    </div>
                  </div>
                  <div className="rounded border border-slate-200 bg-white p-2">
                    <div className="text-xs font-bold uppercase text-slate-500">
                      {t(language, "tasks.suggestion.confidence")}
                    </div>
                    <div className="mt-1 text-lg font-black text-slate-950">
                      {t(language, confidenceKey(suggestion.confidence))}
                    </div>
                  </div>
                </div>
                <p className="text-sm text-slate-700">
                  {t(language, "tasks.suggestion.source")}:{" "}
                  <span className="font-bold">{t(language, sourceKey(suggestion.source))}</span>
                  {" · "}
                  {t(language, "tasks.suggestion.samples")}:{" "}
                  <span className="font-bold">{suggestion.sample_count}</span>
                </p>
                <p className="text-sm text-slate-600">
                  {getSuggestionReasonLabel(language, suggestion.reason_code, suggestion.reason)}
                </p>
                <button
                  type="button"
                  onClick={handleAcceptSuggestion}
                  className="rounded bg-slate-950 px-3 py-2 text-sm font-black text-white"
                >
                  {t(language, "tasks.suggestion.accept")}
                </button>
              </div>
            )}
          </div>

          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "tasks.form.due")}
            </span>
            <input
              type="datetime-local"
              value={form.due_at}
              onChange={(event) => updateForm({ due_at: event.target.value })}
              className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
            />
          </label>

          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "tasks.form.notes")}
            </span>
            <textarea
              value={form.notes}
              onChange={(event) => updateForm({ notes: event.target.value })}
              rows={3}
              className="mt-1 w-full resize-none rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
              placeholder={t(language, "tasks.form.notesPlaceholder")}
            />
          </label>

          <div className="grid grid-cols-2 gap-3">
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.form.status")}
              </span>
              <select
                value={form.status}
                onChange={(event) =>
                  updateForm({ status: event.target.value as TaskStatus })
                }
                className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600"
              >
                {STATUS_OPTIONS.map((status) => (
                  <option key={status} value={status}>
                    {getStatusLabel(language, status)}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.form.splits")}
              </span>
              <input
                type="number"
                min={1}
                max={3}
                value={form.max_split_count}
                disabled={!form.is_splittable}
                onChange={(event) => updateForm({ max_split_count: event.target.value })}
                className="mt-1 w-full rounded border border-slate-300 px-3 py-2 outline-none focus:border-amber-600 disabled:bg-slate-100"
              />
            </label>
          </div>

          <label className="flex items-center gap-2 text-sm font-semibold text-slate-700">
            <input
              type="checkbox"
              checked={form.is_splittable}
              onChange={(event) =>
                updateForm({
                  is_splittable: event.target.checked,
                  max_split_count: event.target.checked ? form.max_split_count : "1",
                })
              }
            />
            {t(language, "tasks.form.allowSplit")}
          </label>

          <div className="flex gap-2">
            <button
              type="submit"
              disabled={loading}
              className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
            >
              {editingId === null
                ? t(language, "tasks.action.create")
                : t(language, "tasks.action.save")}
            </button>
            {editingId !== null && (
              <button
                type="button"
                onClick={cancelEdit}
                className="rounded border border-slate-300 px-4 py-2 text-sm font-bold text-slate-700"
              >
                {t(language, "tasks.action.cancel")}
              </button>
            )}
          </div>
        </form>

        {message && <p className="mt-4 text-sm font-semibold text-amber-800">{message}</p>}
      </section>

      <section className="space-y-4">
        <div className="flex flex-wrap items-center justify-between gap-3">
          <div>
            <p className="text-xs font-black uppercase tracking-[0.2em] text-slate-500">
              {t(language, "tasks.queue.eyebrow")}
            </p>
            <h2 className="text-2xl font-black text-slate-950">
              {t(language, "tasks.queue.title")}
            </h2>
          </div>
          <div className="flex flex-wrap gap-2">
            <button
              type="button"
              onClick={() => void handleExportTasks()}
              disabled={exportLoading}
              className="rounded border border-slate-300 bg-white px-3 py-2 text-sm font-bold text-slate-700 disabled:opacity-50"
            >
              {exportLoading ? t(language, "common.loading") : t(language, "exports.tasksJson")}
            </button>
            <button
              type="button"
              onClick={() => void refreshTasks()}
              disabled={loading}
              className="rounded border border-slate-300 bg-white px-3 py-2 text-sm font-bold text-slate-700 disabled:opacity-50"
            >
              {t(language, "tasks.action.refresh")}
            </button>
          </div>
        </div>

        <div className="grid gap-2 sm:grid-cols-4">
          {STATUS_OPTIONS.map((status) => (
            <div key={status} className="rounded border border-slate-300 bg-white p-3">
              <div className="text-xs font-bold uppercase text-slate-500">
                {getStatusLabel(language, status)}
              </div>
              <div className="mt-1 text-2xl font-black">{counts[status]}</div>
            </div>
          ))}
        </div>

        <div className="rounded border border-slate-300 bg-white p-4">
          <div className="text-sm font-black text-slate-950">
            {t(language, "tasks.filters.title")}
          </div>
          <div className="mt-3 grid gap-3 lg:grid-cols-3">
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.filters.search")}
              </span>
              <input
                value={searchText}
                onChange={(event) => setSearchText(event.target.value)}
                className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
                placeholder={t(language, "tasks.filters.searchPlaceholder")}
              />
            </label>
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.filters.status")}
              </span>
              <select
                value={statusFilter}
                onChange={(event) =>
                  setStatusFilter(event.target.value as TaskStatus | "all")
                }
                className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
              >
                <option value="all">{t(language, "tasks.filters.allStatuses")}</option>
                {STATUS_OPTIONS.map((status) => (
                  <option key={status} value={status}>
                    {getStatusLabel(language, status)}
                  </option>
                ))}
              </select>
            </label>
            <label className="block">
              <span className="text-sm font-bold text-slate-700">
                {t(language, "tasks.filters.project")}
              </span>
              <select
                value={projectFilter}
                onChange={(event) => setProjectFilter(event.target.value)}
                className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
              >
                <option value="all">{t(language, "tasks.filters.allProjects")}</option>
                <option value="none">{t(language, "tasks.filters.noProject")}</option>
                {projects.map((project) => (
                  <option key={project.id} value={project.id}>
                    {project.name}
                  </option>
                ))}
              </select>
            </label>
          </div>
        </div>

        <ul className="space-y-3">
          {filteredTasks.map((task) => (
            <li key={task.id} className="rounded border border-slate-300 bg-white p-4 shadow-sm">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                  <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-lg font-black text-slate-950">{task.title}</h3>
                    <span className="rounded bg-amber-100 px-2 py-1 text-xs font-black text-amber-800">
                      {getStatusLabel(language, task.status)}
                    </span>
                  </div>
                  <p className="mt-2 text-sm text-slate-600">
                    {task.estimated_minutes} {t(language, "tasks.meta.minutesSuffix")} ·{" "}
                    {t(language, "tasks.meta.load")} {task.cognitive_load} ·{" "}
                    {formatDue(task.due_at, t(language, "tasks.noDueDate"))}
                  </p>
                  {task.notes && (
                    <p className="mt-2 text-sm font-semibold text-slate-500">{task.notes}</p>
                  )}
                </div>
                <div className="flex gap-2">
                  <button
                    type="button"
                    onClick={() => beginEdit(task)}
                    className="rounded border border-slate-300 px-3 py-2 text-sm font-bold text-slate-700"
                  >
                    {t(language, "tasks.action.edit")}
                  </button>
                  <button
                    type="button"
                    onClick={() => void handleDelete(task.id)}
                    className="rounded border border-red-200 px-3 py-2 text-sm font-bold text-red-700"
                  >
                    {t(language, "tasks.action.delete")}
                  </button>
                </div>
              </div>
            </li>
          ))}
        </ul>

        {filteredTasks.length === 0 && (
          <div className="rounded border border-dashed border-slate-300 bg-white p-8 text-center text-sm font-semibold text-slate-500">
            {tasks.length > 0 ? t(language, "tasks.emptyFiltered") : t(language, "tasks.empty")}
          </div>
        )}
      </section>
    </div>
  );
}
