import { useEffect, useState } from "react";
import {
  exportDailyReview,
  exportExecutionHistory,
  getExecutionReview,
  type ExecutionReview,
} from "../lib/api";
import { triggerExportDownload } from "../lib/exportView";
import { getPlanTypeLabel, getStatusLabel, t } from "../lib/i18n";
import { useAppStore } from "../state/store";

function todayInputValue(): string {
  const date = new Date();
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return date.toISOString().slice(0, 10);
}

function formatMinutes(value: number | null): string {
  if (value === null) {
    return "—";
  }
  return `${value}`;
}

function formatVariance(value: number | null): string {
  if (value === null) {
    return "—";
  }
  return value > 0 ? `+${value}` : `${value}`;
}

export default function DailyReview() {
  const { language } = useAppStore();
  const [date, setDate] = useState(todayInputValue());
  const [review, setReview] = useState<ExecutionReview | null>(null);
  const [loading, setLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState<"history" | "review" | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function refreshReview(targetDate = date) {
    setLoading(true);
    setMessage(null);
    try {
      setReview(await getExecutionReview(targetDate));
    } catch (error) {
      setReview(null);
      setMessage(error instanceof Error ? error.message : t(language, "review.message.loadFailed"));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshReview(date);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  const summary = review?.summary;

  async function handleExportHistory() {
    setExportLoading("history");
    setMessage(null);
    try {
      const payload = await exportExecutionHistory({ date });
      triggerExportDownload(payload);
      setMessage(t(language, "exports.success"));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "exports.failed"));
    } finally {
      setExportLoading(null);
    }
  }

  async function handleExportReview() {
    setExportLoading("review");
    setMessage(null);
    try {
      const payload = await exportDailyReview({ date });
      triggerExportDownload(payload);
      setMessage(t(language, "exports.success"));
    } catch (error) {
      setMessage(error instanceof Error ? error.message : t(language, "exports.failed"));
    } finally {
      setExportLoading(null);
    }
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-5 border-b border-slate-300 pb-6 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.2em] text-amber-700">
            {t(language, "review.eyebrow")}
          </p>
          <h1 className="mt-2 text-4xl font-black text-slate-950">
            {t(language, "review.title")}
          </h1>
        </div>
        <div className="flex flex-wrap items-end gap-3">
          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "review.date")}
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
            onClick={() => void handleExportHistory()}
            disabled={exportLoading !== null}
            className="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-black text-slate-700 disabled:opacity-50"
          >
            {exportLoading === "history" ? t(language, "common.loading") : t(language, "exports.historyJson")}
          </button>
          <button
            type="button"
            onClick={() => void handleExportReview()}
            disabled={exportLoading !== null}
            className="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-black text-slate-700 disabled:opacity-50"
          >
            {exportLoading === "review" ? t(language, "common.loading") : t(language, "exports.reviewCsv")}
          </button>
          <button
            type="button"
            onClick={() => void refreshReview(date)}
            disabled={loading}
            className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
          >
            {t(language, "review.action.refresh")}
          </button>
        </div>
      </section>

      {message && <p className="text-sm font-semibold text-amber-800">{message}</p>}

      {summary && (
        <section className="space-y-3">
          <div className="flex flex-wrap items-center gap-2 text-sm font-black text-slate-600">
            {review?.selected_plan && (
              <span className="rounded bg-white px-3 py-2">
                {getPlanTypeLabel(language, review.selected_plan.plan_type)}
              </span>
            )}
            <span className="rounded bg-white px-3 py-2">
              {t(language, "review.summary.title")}
            </span>
          </div>
          <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
            <Metric label={t(language, "review.summary.planned")} value={summary.planned_count} />
            <Metric label={t(language, "review.summary.completed")} value={summary.completed_count} />
            <Metric
              label={t(language, "review.summary.skippedIncomplete")}
              value={summary.skipped_incomplete_count}
            />
            <Metric
              label={t(language, "review.summary.completionRate")}
              value={`${Math.round(summary.completion_rate * 100)}%`}
            />
            <Metric
              label={t(language, "review.summary.plannedMinutes")}
              value={summary.planned_minutes}
            />
            <Metric
              label={t(language, "review.summary.actualMinutes")}
              value={summary.actual_minutes}
            />
            <Metric
              label={t(language, "review.summary.variance")}
              value={formatVariance(summary.estimate_variance_minutes)}
            />
          </div>
        </section>
      )}

      {review && review.items.length > 0 ? (
        <ol className="space-y-3">
          {review.items.map((item) => (
            <li
              key={item.id}
              className="grid gap-3 rounded border border-slate-300 bg-white p-4 shadow-sm lg:grid-cols-[1fr_120px_120px_120px_120px]"
            >
              <div>
                <p className="text-xs font-black uppercase text-slate-500">
                  {t(language, "review.table.task")}
                </p>
                <h2 className="mt-1 text-lg font-black text-slate-950">
                  {item.task_title_snapshot}
                </h2>
                {item.note && (
                  <p className="mt-1 text-sm font-semibold text-slate-500">
                    {t(language, "review.table.note")}: {item.note}
                  </p>
                )}
              </div>
              <ReviewCell
                label={t(language, "review.table.outcome")}
                value={getStatusLabel(language, item.status)}
              />
              <ReviewCell
                label={t(language, "review.table.estimate")}
                value={formatMinutes(item.estimated_minutes_snapshot)}
              />
              <ReviewCell
                label={t(language, "review.table.actual")}
                value={formatMinutes(item.actual_minutes)}
              />
              <ReviewCell
                label={t(language, "review.table.variance")}
                value={formatVariance(item.estimate_variance_minutes)}
              />
            </li>
          ))}
        </ol>
      ) : (
        <div className="rounded border border-dashed border-slate-300 bg-white p-10 text-center">
          <h2 className="text-xl font-black text-slate-950">{t(language, "review.emptyTitle")}</h2>
          <p className="mt-2 text-sm font-semibold text-slate-500">
            {t(language, "review.emptyDescription")}
          </p>
        </div>
      )}
    </div>
  );
}

function Metric({ label, value }: { label: string; value: number | string }) {
  return (
    <div className="rounded border border-slate-300 bg-white p-4">
      <p className="text-xs font-black uppercase text-slate-500">{label}</p>
      <p className="mt-2 text-2xl font-black text-slate-950">{value}</p>
    </div>
  );
}

function ReviewCell({ label, value }: { label: string; value: string }) {
  return (
    <div>
      <p className="text-xs font-black uppercase text-slate-500">{label}</p>
      <p className="mt-1 text-sm font-bold text-slate-950">{value}</p>
    </div>
  );
}
