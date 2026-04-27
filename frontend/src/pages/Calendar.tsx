import { useEffect, useMemo, useState } from "react";
import {
  generateSchedule,
  listTasks,
  reoptimizeSchedule,
  selectSchedulePlan,
  validateScheduleMove,
  type SchedulePlan,
  type ValidateMoveResult,
} from "../lib/api";
import { getPlanTypeLabel, t, type TranslationKey } from "../lib/i18n";
import {
  formatTimeRange,
  PLAN_TYPES,
  sortScheduleItems,
  type PlanType,
} from "../lib/scheduleView";
import { useAppStore } from "../state/store";

function todayInputValue(): string {
  const date = new Date();
  date.setMinutes(date.getMinutes() - date.getTimezoneOffset());
  return date.toISOString().slice(0, 10);
}

function riskClass(plan: SchedulePlan | undefined): string {
  if (plan?.risk_level === "high") {
    return "bg-red-100 text-red-800";
  }
  if (plan?.risk_level === "medium") {
    return "bg-amber-100 text-amber-800";
  }
  return "bg-emerald-100 text-emerald-800";
}

function riskKey(plan: SchedulePlan | undefined): TranslationKey {
  if (plan?.risk_level === "high") {
    return "risk.high";
  }
  if (plan?.risk_level === "medium") {
    return "risk.medium";
  }
  return "risk.low";
}

export default function Calendar() {
  const {
    tasks,
    setTasks,
    schedule,
    setSchedule,
    activePlanType,
    setActivePlanType,
    selectedPlanType,
    setSelectedPlanType,
    language,
  } = useAppStore();
  const [date, setDate] = useState(todayInputValue());
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);
  const [validateTaskId, setValidateTaskId] = useState("");
  const [validateStart, setValidateStart] = useState("");
  const [validateEnd, setValidateEnd] = useState("");
  const [validationResult, setValidationResult] = useState<ValidateMoveResult | null>(null);

  useEffect(() => {
    if (tasks.length === 0) {
      listTasks()
        .then(setTasks)
        .catch(() => setTasks([]));
    }
  }, [setTasks, tasks.length]);

  const activePlan = useMemo(
    () => schedule?.plans.find((plan) => plan.plan_type === activePlanType),
    [activePlanType, schedule],
  );

  const sortedItems = useMemo(
    () => sortScheduleItems(activePlan?.items ?? []),
    [activePlan],
  );

  useEffect(() => {
    const firstItem = sortedItems[0];
    if (!firstItem) {
      setValidateTaskId("");
      setValidateStart("");
      setValidateEnd("");
      setValidationResult(null);
      return;
    }
    setValidateTaskId(String(firstItem.task_id));
    setValidateStart(firstItem.start_datetime.slice(0, 16));
    setValidateEnd(firstItem.end_datetime.slice(0, 16));
    setValidationResult(null);
  }, [sortedItems]);

  const titleByTaskId = useMemo(
    () => new Map(tasks.map((task) => [task.id, task.title])),
    [tasks],
  );

  async function handleGenerate() {
    setLoading(true);
    setMessage(null);
    try {
      const result = await generateSchedule(date);
      const defaultPlanType = result.plans.some((plan) => plan.plan_type === "balanced")
        ? "balanced"
        : result.plans[0]?.plan_type ?? "balanced";
      setSchedule(result);
      setActivePlanType(defaultPlanType);
      setSelectedPlanType(null);
      setMessage(
        `${t(language, "calendar.message.generatedPrefix")} ${result.plans.length} ${t(
          language,
          "calendar.message.generatedSuffix",
        )}`,
      );
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : t(language, "calendar.message.generateFailed"),
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleSelect(planType: PlanType) {
    setLoading(true);
    setMessage(null);
    try {
      await selectSchedulePlan(date, planType);
      setSelectedPlanType(planType);
      setMessage(
        `${getPlanTypeLabel(language, planType)} ${t(language, "calendar.message.selected")}`,
      );
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : t(language, "calendar.message.selectionFailed"),
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleReoptimize() {
    setLoading(true);
    setMessage(null);
    setValidationResult(null);
    try {
      const result = await reoptimizeSchedule(date);
      const defaultPlanType = result.plans.some((plan) => plan.plan_type === "balanced")
        ? "balanced"
        : result.plans[0]?.plan_type ?? "balanced";
      setSchedule(result);
      setActivePlanType(defaultPlanType);
      setSelectedPlanType(null);
      setMessage(t(language, "calendar.message.reoptimized"));
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : t(language, "calendar.message.reoptimizeFailed"),
      );
    } finally {
      setLoading(false);
    }
  }

  async function handleValidateMove() {
    if (!activePlan || !validateTaskId || !validateStart || !validateEnd) {
      setMessage(t(language, "calendar.validate.noItems"));
      return;
    }
    setLoading(true);
    setMessage(null);
    try {
      const result = await validateScheduleMove({
        date,
        plan_type: activePlan.plan_type,
        task_id: Number(validateTaskId),
        start_datetime: validateStart,
        end_datetime: validateEnd,
      });
      setValidationResult(result);
    } catch (error) {
      setMessage(
        error instanceof Error ? error.message : t(language, "calendar.message.validateFailed"),
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-6">
      <section className="grid gap-5 border-b border-slate-300 pb-6 lg:grid-cols-[1fr_auto] lg:items-end">
        <div>
          <p className="text-xs font-black uppercase tracking-[0.2em] text-amber-700">
            {t(language, "calendar.eyebrow")}
          </p>
          <h1 className="mt-2 text-4xl font-black text-slate-950">
            {t(language, "calendar.title")}
          </h1>
        </div>
        <div className="flex flex-wrap items-end gap-3">
          <label className="block">
            <span className="text-sm font-bold text-slate-700">
              {t(language, "calendar.date")}
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
            onClick={() => void handleGenerate()}
            disabled={loading}
            className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
          >
            {t(language, "calendar.action.generate")}
          </button>
          <button
            type="button"
            onClick={() => void handleReoptimize()}
            disabled={loading}
            className="rounded border border-slate-300 bg-white px-4 py-2 text-sm font-black text-slate-800 disabled:opacity-50"
          >
            {t(language, "calendar.action.reoptimize")}
          </button>
        </div>
      </section>

      {message && <p className="text-sm font-semibold text-amber-800">{message}</p>}

      <section className="grid gap-4 lg:grid-cols-[280px_1fr]">
        <aside className="space-y-3">
          {PLAN_TYPES.map((planType) => {
            const plan = schedule?.plans.find((item) => item.plan_type === planType);
            const isActive = activePlanType === planType;
            const isSelected = selectedPlanType === planType;
            return (
              <button
                key={planType}
                type="button"
                onClick={() => setActivePlanType(planType)}
                disabled={!plan}
                className={`w-full rounded border p-4 text-left shadow-sm disabled:cursor-not-allowed disabled:opacity-40 ${
                  isActive
                    ? "border-slate-950 bg-white"
                    : "border-slate-300 bg-white/70 hover:bg-white"
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="font-black">{getPlanTypeLabel(language, planType)}</span>
                  {isSelected && (
                    <span className="rounded bg-slate-950 px-2 py-1 text-xs font-black text-white">
                      {t(language, "calendar.badge.selected")}
                    </span>
                  )}
                </div>
                <div className="mt-2 flex items-center gap-2 text-xs font-bold text-slate-600">
                  <span>
                    {plan?.items.length ?? 0} {t(language, "calendar.metric.items")}
                  </span>
                  <span>
                    {plan?.score ?? 0} {t(language, "calendar.metric.score")}
                  </span>
                </div>
              </button>
            );
          })}
        </aside>

        <div className="rounded border border-slate-300 bg-white p-5 shadow-sm">
          {activePlan ? (
            <div className="space-y-5">
              <div className="flex flex-wrap items-center justify-between gap-3">
                <div>
                  <h2 className="text-2xl font-black text-slate-950">
                    {getPlanTypeLabel(language, activePlan.plan_type)}
                  </h2>
                  <div className="mt-2 flex flex-wrap gap-2 text-xs font-black uppercase">
                    <span className="rounded bg-slate-100 px-2 py-1 text-slate-700">
                      {t(language, "calendar.metric.score")} {activePlan.score ?? 0}
                    </span>
                    <span className={`rounded px-2 py-1 ${riskClass(activePlan)}`}>
                      {t(language, "calendar.metric.risk")} {t(language, riskKey(activePlan))}
                    </span>
                  </div>
                </div>
                <button
                  type="button"
                  onClick={() => void handleSelect(activePlan.plan_type)}
                  disabled={loading}
                  className="rounded bg-amber-600 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
                >
                  {t(language, "calendar.action.select")}
                </button>
              </div>

              {schedule?.warnings.length ? (
                <div className="rounded border border-amber-200 bg-amber-50 p-3 text-sm font-semibold text-amber-900">
                  {schedule.warnings.join(" ")}
                </div>
              ) : null}

              {schedule?.unplaced.length ? (
                <div className="rounded border border-red-200 bg-red-50 p-3 text-sm font-semibold text-red-800">
                  {t(language, "calendar.unplaced")}: {schedule.unplaced.join(", ")}
                </div>
              ) : null}

              <div className="rounded border border-slate-200 bg-[#faf9f4] p-4">
                <h3 className="text-sm font-black uppercase text-slate-600">
                  {t(language, "calendar.validate.title")}
                </h3>
                {sortedItems.length ? (
                  <div className="mt-3 grid gap-3 lg:grid-cols-[1fr_1fr_1fr_auto] lg:items-end">
                    <label className="block">
                      <span className="text-sm font-bold text-slate-700">
                        {t(language, "calendar.validate.task")}
                      </span>
                      <select
                        value={validateTaskId}
                        onChange={(event) => setValidateTaskId(event.target.value)}
                        className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
                      >
                        {sortedItems.map((item) => (
                          <option
                            key={`${item.task_id}-${item.start_datetime}-${item.segment_index ?? 0}`}
                            value={item.task_id}
                          >
                            {titleByTaskId.get(item.task_id) ??
                              `${t(language, "calendar.taskPrefix")} #${item.task_id}`}
                          </option>
                        ))}
                      </select>
                    </label>
                    <label className="block">
                      <span className="text-sm font-bold text-slate-700">
                        {t(language, "calendar.validate.start")}
                      </span>
                      <input
                        type="datetime-local"
                        value={validateStart}
                        onChange={(event) => setValidateStart(event.target.value)}
                        className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
                      />
                    </label>
                    <label className="block">
                      <span className="text-sm font-bold text-slate-700">
                        {t(language, "calendar.validate.end")}
                      </span>
                      <input
                        type="datetime-local"
                        value={validateEnd}
                        onChange={(event) => setValidateEnd(event.target.value)}
                        className="mt-1 w-full rounded border border-slate-300 bg-white px-3 py-2 outline-none focus:border-amber-600"
                      />
                    </label>
                    <button
                      type="button"
                      onClick={() => void handleValidateMove()}
                      disabled={loading}
                      className="rounded bg-slate-950 px-4 py-2 text-sm font-black text-white disabled:opacity-50"
                    >
                      {t(language, "calendar.validate.action")}
                    </button>
                  </div>
                ) : (
                  <p className="mt-2 text-sm font-semibold text-slate-500">
                    {t(language, "calendar.validate.noItems")}
                  </p>
                )}
                {validationResult && (
                  <div
                    className={`mt-3 rounded border p-3 text-sm font-semibold ${
                      validationResult.valid
                        ? "border-emerald-200 bg-emerald-50 text-emerald-800"
                        : "border-red-200 bg-red-50 text-red-800"
                    }`}
                  >
                    {validationResult.valid
                      ? t(language, "calendar.validate.valid")
                      : t(language, "calendar.validate.invalid")}
                    {validationResult.conflicts.length > 0 && (
                      <ul className="mt-2 list-disc pl-5">
                        {validationResult.conflicts.map((conflict, index) => (
                          <li key={`${conflict.type}-${index}`}>
                            {t(language, "calendar.validate.conflicts")}: {conflict.message}
                          </li>
                        ))}
                      </ul>
                    )}
                  </div>
                )}
              </div>

              <ol className="space-y-3">
                {sortedItems.map((item) => (
                  <li
                    key={`${item.task_id}-${item.start_datetime}-${item.segment_index ?? 0}`}
                    className="grid gap-3 rounded border border-slate-200 bg-[#faf9f4] p-4 sm:grid-cols-[120px_1fr]"
                  >
                    <time className="font-black text-slate-950">{formatTimeRange(item)}</time>
                    <div>
                      <div className="font-black text-slate-950">
                        {titleByTaskId.get(item.task_id) ??
                          `${t(language, "calendar.taskPrefix")} #${item.task_id}`}
                      </div>
                      <div className="mt-1 text-sm font-semibold text-slate-500">
                        {t(language, "calendar.taskPrefix")} #{item.task_id}
                        {item.segment_index
                          ? ` · ${t(language, "calendar.segment")} ${item.segment_index}`
                          : ""}
                      </div>
                      {item.warning && (
                        <p className="mt-2 text-sm font-semibold text-amber-800">
                          {item.warning}
                        </p>
                      )}
                    </div>
                  </li>
                ))}
              </ol>

              {sortedItems.length === 0 && (
                <div className="rounded border border-dashed border-slate-300 p-8 text-center text-sm font-semibold text-slate-500">
                  {t(language, "calendar.emptyPlanItems")}
                </div>
              )}
            </div>
          ) : (
            <div className="rounded border border-dashed border-slate-300 p-10 text-center">
              <h2 className="text-xl font-black text-slate-950">
                {t(language, "calendar.emptyTitle")}
              </h2>
              <p className="mt-2 text-sm font-semibold text-slate-500">
                {t(language, "calendar.emptyDescription")}
              </p>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}
