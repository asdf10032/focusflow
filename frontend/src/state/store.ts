import { create } from "zustand";
import type { GenerateScheduleResult, Task } from "../lib/api";
import {
  loadStoredLanguage,
  saveStoredLanguage,
  type Language,
} from "../lib/i18n";
import type { PlanType } from "../lib/scheduleView";

interface AppState {
  tasks: Task[];
  schedule: GenerateScheduleResult | null;
  activePlanType: PlanType;
  selectedPlanType: PlanType | null;
  language: Language;
  setTasks: (tasks: Task[]) => void;
  setSchedule: (schedule: GenerateScheduleResult | null) => void;
  setActivePlanType: (planType: PlanType) => void;
  setSelectedPlanType: (planType: PlanType | null) => void;
  setLanguage: (language: Language) => void;
}

export const useAppStore = create<AppState>((set) => ({
  tasks: [],
  schedule: null,
  activePlanType: "balanced",
  selectedPlanType: null,
  language: loadStoredLanguage(),
  setTasks: (tasks) => set(() => ({ tasks })),
  setSchedule: (schedule) => set(() => ({ schedule })),
  setActivePlanType: (planType) => set(() => ({ activePlanType: planType })),
  setSelectedPlanType: (planType) => set(() => ({ selectedPlanType: planType })),
  setLanguage: (language) => {
    saveStoredLanguage(language);
    set(() => ({ language }));
  },
}));
