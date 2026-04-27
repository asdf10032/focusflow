import { useEffect, useState } from "react";
import {
  getTodayExecution,
  submitExecutionFeedback,
  type TaskStatus,
  type TodayExecution,
} from "../lib/api";
import { getPlanTypeLabel, getStatusLabel, t } from "../lib/i18n";
import { formatTimeRange } from "../lib/scheduleView";
import { useAppStore } from "../state/store";

const STATUS_OPTIONS: TaskStatus[] = ["todo", "in_progress", "done", "canceled"];

function todayInputValue(): string {
  const date = new Date();
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return date.toISOString().slice(0, 10);
}

export default function Today() {
  const { language } = useAppStore();
  const [date, setDate] = useState(todayInputValue());
  const [execution, setExecution] = useState<TodayExecution | null>(null);
  const [feedbackByTaskId, setFeedbackByTaskId] = useState<Record<number, TaskStatus>>({});
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  async function refreshToday(targetDate = date) {
    setLoading(true);
    setMessage(null);
    try {
      const payload = await getTodayExecution(targetDate);
      setExecution(payload);
      setFeedbackByTaskId(
        Object.fromEntries(payload.items.map((item) => [item.task.id, item.task.status])),
      );
    } catch (error) {
      setExecution(null);
      setMessage(error instanceof Error ? error.message : t(language, "today.message.loadFailed"));
    } finally {
      setLoading(false);
    }
  }

  async function handleFeedback(taskId: number) {
    const status = feedbackByTaskId[taskId];
    if (!status) {
      return;
    }
    setLoading(true);
    setMessage(null);
    try {
      await submitExecutionFeedback(taskId, status);
      setMessage(t(language, "today.message.feedbackSaved"));
      await refreshToday(date);
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : t(language, "today.message.feedbackFailed"),
      );
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshToday(date);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="space-y-6">
      <section className="grid gap-5 border-b border-slate-300 pb-6 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.2em] text-amber-700">
            {t(language, "today.eyebrow")}
          </p>
          <h1 className="mt-2 text-4xl font-black text-slate-950">
            {t(language, "today.title")}
          </h1>
        </div>
        <div className="flex flex-wrap items-end gap-3">
          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "today.date")}
            </span>
            <input
              type="date"
              value={date}
              onChange={(event) => setDate(event.target.value)}
              className="mt-1 rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
            />
          </label>
          <button
            type="button"
            onClick={() => void refreshToday(date)}
            disabled={loading}
            className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
          >
            {t(language, "today.action.refresh")}
          </button>
        </div>
      </section>

      {message && <p className="text-sm font-semibold text-amber-800">{message}</p>}

      {execution?.selected_plan ? (
        <section className="space-y-4">
          <div className="flex flex-wrap items-center gap-2 text-sm font-black text-slate-600">
            <span className="rounded bg-white px-3 py-2">
              {getPlanTypeLabel(language, execution.selected_plan.plan_type)}
            </span>
            <span className="rounded bg-white px-3 py-2">
              {execution.items.length} {t(language, "calendar.metric.items")}
            </span>
          </div>

          <ol className="space-y-3">
            {execution.items.map((item) => (
              <li
                key={`${item.task_id}-${item.start_datetime}-${item.segment_index ?? 0}`}
                className="grid gap-4 rounded border border-slate-300 bg-white p-4 shadow-sm lg:grid-cols-[140px_1fr_auto]"
              >
                <time className="font-black text-slate-950">{formatTimeRange(item)}</time>
                <div>
                  <h2 className="text-lg font-black text-slate-950">{item.task.title}</h2>
                  <p className="mt-1 text-sm font-semibold text-slate-500">
                    {item.task.estimated_minutes} {t(language, "common.minutes")} -{" "}
                    {t(language, "tasks.meta.load")} {item.task.cognitive_load}
                  </p>
                </div>
                <div className="flex flex-wrap items-end gap-2">
                  <label className="block">
                    <span className="text-sm font-bold text-slate-700">
                      {t(language, "today.status")}
                    </span>
                    <select
                      value={feedbackByTaskId[item.task.id] ?? item.task.status}
                      onChange={(event) =>
                        setFeedbackByTaskId({
                          ...feedbackByTaskId,
                          [item.task.id]: event.target.value as TaskStatus,
                        })
                      }
                      className="mt-1 rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
                    >
                      {STATUS_OPTIONS.map((status) => (
                        <option key={status} value={status}>
                          {getStatusLabel(language, status)}
                        </option>
                      ))}
                    </select>
                  </label>
                  <button
                    type="button"
                    onClick={() => void handleFeedback(item.task.id)}
                    disabled={loading}
                    className="rounded bg-amber-600 px-3 py-2 text-sm font-black text-white disabled:opacity-50"
                  >
                    {t(language, "today.action.saveFeedback")}
                  </button>
                </div>
              </li>
            ))}
          </ol>
        </section>
      ) : (
        <div className="rounded border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-xl font-black text-slate-950">{t(language, "today.emptyTitle")}</h2>
          <p className="mt-2 text-sm font-semibold text-slate-500">
            {t(language, "today.emptyDescription")}
          </p>
        </div>
      )}
    </div>
  );
}
