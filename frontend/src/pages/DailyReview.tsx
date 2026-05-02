import { useEffect, useState } from "react";
import {
  exportDailyReview,
  exportExecutionHistory,
  getExecutionReview,
  getWeeklyExecutionReview,
  type ExecutionReview,
  type ExecutionReviewItem,
  type WeeklyReview,
  type WeeklyReviewDay,
} from "../lib/api";
import { triggerExportDownload } from "../lib/exportView";
import {
  formatCompletionRate,
  formatDeltaValue,
  formatMinutesValue,
  formatVarianceValue,
  formatWeekRange,
  shiftDateByDays,
} from "../lib/reviewView";
import { getPlanTypeLabel, getStatusLabel, t } from "../lib/i18n";
import { useAppStore } from "../state/store";

type ReviewMode = "daily" | "weekly";

function todayInputValue(): string {
  const date = new Date();
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return date.toISOString().slice(0, 10);
}

export default function DailyReview() {
  const { language } = useAppStore();
  const [date, setDate] = useState(todayInputValue());
  const [viewMode, setViewMode] = useState<ReviewMode>("daily");
  const [review, setReview] = useState<ExecutionReview | null>(null);
  const [weeklyReview, setWeeklyReview] = useState<WeeklyReview | null>(null);
  const [loading, setLoading] = useState(false);
  const [exportLoading, setExportLoading] = useState<"history" | "review" | null>(null);
  const [message, setMessage] = useState<string | null>(null);

  async function refreshActive(targetDate = date, targetMode = viewMode) {
    setLoading(true);
    setMessage(null);
    try {
      if (targetMode === "weekly") {
        setWeeklyReview(await getWeeklyExecutionReview(targetDate));
      } else {
        setReview(await getExecutionReview(targetDate));
      }
    } catch (error) {
      if (targetMode === "weekly") {
        setWeeklyReview(null);
      } else {
        setReview(null);
      }
      setMessage(error instanceof Error ? error.message : t(language, "review.message.loadFailed"));
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    void refreshActive(date, "daily");
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  async function handleViewModeChange(nextMode: ReviewMode) {
    setViewMode(nextMode);
    await refreshActive(date, nextMode);
  }

  async function handleWeekShift(days: number) {
    const nextDate = shiftDateByDays(date, days);
    setDate(nextDate);
    await refreshActive(nextDate, "weekly");
  }

  async function handleExportHistory() {
    setExportLoading("history");
    setMessage(null);
    try {
      const payload = await exportExecutionHistory({ date });
      if (payload.record_count === 0) {
        setMessage(t(language, "exports.emptyNoDownload"));
        return;
      }
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
      if (payload.record_count === 0) {
        setMessage(t(language, "exports.emptyNoDownload"));
        return;
      }
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
          <div className="inline-flex rounded border border-slate-300 bg-white p-1">
            {(["daily", "weekly"] as const).map((mode) => (
              <button
                key={mode}
                type="button"
                onClick={() => void handleViewModeChange(mode)}
                className={`px-3 py-2 text-sm font-black ${
                  viewMode === mode ? "bg-slate-950 text-white" : "text-slate-700"
                }`}
              >
                {t(language, mode === "daily" ? "review.view.daily" : "review.view.weekly")}
              </button>
            ))}
          </div>
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
          {viewMode === "weekly" && (
            <>
              <button
                type="button"
                onClick={() => void handleWeekShift(-7)}
                disabled={loading}
                className="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-black text-slate-700 disabled:opacity-50"
              >
                {t(language, "review.action.previousWeek")}
              </button>
              <button
                type="button"
                onClick={() => void handleWeekShift(7)}
                disabled={loading}
                className="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-black text-slate-700 disabled:opacity-50"
              >
                {t(language, "review.action.nextWeek")}
              </button>
            </>
          )}
          {viewMode === "daily" && (
            <>
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
            </>
          )}
          <button
            type="button"
            onClick={() => void refreshActive(date, viewMode)}
            disabled={loading}
            className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
          >
            {loading ? t(language, "common.loading") : t(language, "review.action.refresh")}
          </button>
        </div>
      </section>

      {message && <p className="text-sm font-semibold text-amber-800">{message}</p>}

      {viewMode === "daily" ? (
        <DailyReviewPanel review={review} />
      ) : (
        <WeeklyReviewPanel review={weeklyReview} />
      )}
    </div>
  );
}

function DailyReviewPanel({ review }: { review: ExecutionReview | null }) {
  const { language } = useAppStore();
  const summary = review?.summary;

  return (
    <>
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
              value={formatCompletionRate(summary.completion_rate)}
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
              value={formatVarianceValue(summary.estimate_variance_minutes)}
            />
          </div>
        </section>
      )}

      {review && review.items.length > 0 ? (
        <ol className="space-y-3">
          {review.items.map((item) => (
            <DailyReviewItem key={item.id} item={item} />
          ))}
        </ol>
      ) : (
        <EmptyState
          title={t(language, "review.emptyTitle")}
          description={t(language, "review.emptyDescription")}
        />
      )}
    </>
  );
}

function WeeklyReviewPanel({ review }: { review: WeeklyReview | null }) {
  const { language } = useAppStore();

  if (!review) {
    return (
      <EmptyState
        title={t(language, "review.week.emptyTitle")}
        description={t(language, "review.week.emptyDescription")}
      />
    );
  }

  const summary = review.summary;
  const comparison = review.comparison;
  const hasLogs = summary.logged_count > 0;

  return (
    <div className="space-y-6">
      <section className="space-y-3">
        <div className="flex flex-wrap items-center gap-2 text-sm font-black text-slate-600">
          <span className="rounded bg-white px-3 py-2">
            {t(language, "review.week.range")}: {formatWeekRange(review.week_start, review.week_end)}
          </span>
          <span className="rounded bg-white px-3 py-2">
            {t(language, "review.week.summaryTitle")}
          </span>
        </div>
        <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-3">
          <Metric
            label={t(language, "review.summary.completionRate")}
            value={formatCompletionRate(summary.completion_rate)}
          />
          <Metric
            label={t(language, "review.summary.actualMinutes")}
            value={summary.actual_minutes}
          />
          <Metric
            label={t(language, "review.summary.variance")}
            value={formatVarianceValue(summary.estimate_variance_minutes)}
          />
          <Metric label={t(language, "review.week.logged")} value={summary.logged_count} />
          <Metric label={t(language, "review.summary.completed")} value={summary.completed_count} />
          <Metric
            label={t(language, "review.summary.skippedIncomplete")}
            value={summary.skipped_incomplete_count}
          />
        </div>
      </section>

      <section className="space-y-3">
        <h2 className="text-xl font-black text-slate-950">
          {t(language, "review.week.comparisonTitle")}
        </h2>
        {comparison.available && comparison.deltas ? (
          <div className="grid gap-3 sm:grid-cols-3">
            <Metric
              label={t(language, "review.summary.completionRate")}
              value={formatDeltaValue(Math.round((comparison.deltas.completion_rate ?? 0) * 100), " pp")}
            />
            <Metric
              label={t(language, "review.summary.actualMinutes")}
              value={formatDeltaValue(comparison.deltas.actual_minutes, " min")}
            />
            <Metric
              label={t(language, "review.summary.variance")}
              value={formatDeltaValue(comparison.deltas.estimate_variance_minutes, " min")}
            />
          </div>
        ) : (
          <p className="text-sm font-semibold text-slate-500">
            {t(language, "review.week.comparisonUnavailable")}
          </p>
        )}
      </section>

      {hasLogs ? (
        <section className="space-y-3">
          <h2 className="text-xl font-black text-slate-950">
            {t(language, "review.week.breakdownTitle")}
          </h2>
          <ol className="space-y-3">
            {review.days.map((day) => (
              <WeeklyDay key={day.date} day={day} />
            ))}
          </ol>
        </section>
      ) : (
        <EmptyState
          title={t(language, "review.week.emptyTitle")}
          description={t(language, "review.week.emptyDescription")}
        />
      )}
    </div>
  );
}

function WeeklyDay({ day }: { day: WeeklyReviewDay }) {
  const { language } = useAppStore();

  return (
    <li className="rounded border border-slate-300 bg-white p-4 shadow-sm">
      <div className="grid gap-3 lg:grid-cols-[1fr_repeat(4,110px)]">
        <div>
          <p className="text-xs font-black uppercase text-slate-500">{day.date}</p>
          <h3 className="mt-1 text-lg font-black text-slate-950">
            {day.summary.logged_count} {t(language, "review.week.logged")}
          </h3>
        </div>
        <ReviewCell
          label={t(language, "review.summary.completionRate")}
          value={formatCompletionRate(day.summary.completion_rate)}
        />
        <ReviewCell
          label={t(language, "review.summary.actualMinutes")}
          value={formatMinutesValue(day.summary.actual_minutes)}
        />
        <ReviewCell
          label={t(language, "review.summary.variance")}
          value={formatVarianceValue(day.summary.estimate_variance_minutes)}
        />
        <ReviewCell
          label={t(language, "review.summary.completed")}
          value={`${day.summary.completed_count}`}
        />
      </div>
      {day.items.length > 0 ? (
        <ol className="mt-4 divide-y divide-slate-200 border-t border-slate-200">
          {day.items.map((item) => (
            <li key={item.id} className="grid gap-3 py-3 lg:grid-cols-[1fr_repeat(4,110px)]">
              <div>
                <p className="text-sm font-black text-slate-950">{item.task_title_snapshot}</p>
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
                value={formatMinutesValue(item.estimated_minutes_snapshot)}
              />
              <ReviewCell
                label={t(language, "review.table.actual")}
                value={formatMinutesValue(item.actual_minutes)}
              />
              <ReviewCell
                label={t(language, "review.table.variance")}
                value={formatVarianceValue(item.estimate_variance_minutes)}
              />
            </li>
          ))}
        </ol>
      ) : (
        <p className="mt-4 border-t border-slate-200 pt-3 text-sm font-semibold text-slate-500">
          {t(language, "review.week.emptyDay")}
        </p>
      )}
    </li>
  );
}

function DailyReviewItem({ item }: { item: ExecutionReviewItem }) {
  const { language } = useAppStore();

  return (
    <li className="grid gap-3 rounded border border-slate-300 bg-white p-4 shadow-sm lg:grid-cols-[1fr_120px_120px_120px_120px]">
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
        value={formatMinutesValue(item.estimated_minutes_snapshot)}
      />
      <ReviewCell
        label={t(language, "review.table.actual")}
        value={formatMinutesValue(item.actual_minutes)}
      />
      <ReviewCell
        label={t(language, "review.table.variance")}
        value={formatVarianceValue(item.estimate_variance_minutes)}
      />
    </li>
  );
}

function EmptyState({ title, description }: { title: string; description: string }) {
  return (
    <div className="rounded border border-dashed border-slate-300 bg-white p-10 text-center">
      <h2 className="text-xl font-black text-slate-950">{title}</h2>
      <p className="mt-2 text-sm font-semibold text-slate-500">{description}</p>
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
