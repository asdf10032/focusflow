import { Link, NavLink, Route, Routes } from "react-router-dom";
import { LANGUAGES, t, type Language } from "./lib/i18n";
import Calendar from "./pages/Calendar";
import DailyReview from "./pages/DailyReview";
import Tasks from "./pages/Tasks";
import Today from "./pages/Today";
import { useAppStore } from "./state/store";

export default function App() {
  const { language, setLanguage } = useAppStore();

  return (
    <div className="min-h-screen bg-[#f4f2eb] text-slate-950">
      <header className="sticky top-0 z-10 border-b border-slate-300 bg-[#f4f2eb]/90 backdrop-blur">
        <div className="mx-auto flex max-w-7xl items-center justify-between gap-3 px-4 py-3">
          <Link to="/" className="text-lg font-black tracking-wide text-slate-950">
            {t(language, "app.name")}
          </Link>
          <div className="flex items-center gap-2">
            <nav className="flex items-center gap-2 text-sm font-semibold">
              <NavLink
                to="/tasks"
                className={({ isActive }) =>
                  `rounded px-3 py-2 ${
                    isActive
                      ? "bg-slate-950 text-white"
                      : "text-slate-600 hover:bg-white hover:text-slate-950"
                  }`
                }
              >
                {t(language, "nav.tasks")}
              </NavLink>
              <NavLink
                to="/calendar"
                className={({ isActive }) =>
                  `rounded px-3 py-2 ${
                    isActive
                      ? "bg-slate-950 text-white"
                      : "text-slate-600 hover:bg-white hover:text-slate-950"
                  }`
                }
              >
                {t(language, "nav.calendar")}
              </NavLink>
              <NavLink
                to="/today"
                className={({ isActive }) =>
                  `rounded px-3 py-2 ${
                    isActive
                      ? "bg-slate-950 text-white"
                      : "text-slate-600 hover:bg-white hover:text-slate-950"
                  }`
                }
              >
                {t(language, "nav.today")}
              </NavLink>
              <NavLink
                to="/review"
                className={({ isActive }) =>
                  `rounded px-3 py-2 ${
                    isActive
                      ? "bg-slate-950 text-white"
                      : "text-slate-600 hover:bg-white hover:text-slate-950"
                  }`
                }
              >
                {t(language, "nav.review")}
              </NavLink>
            </nav>
            <label className="sr-only" htmlFor="language">
              {t(language, "language.label")}
            </label>
            <select
              id="language"
              value={language}
              onChange={(event) => setLanguage(event.target.value as Language)}
              className="rounded border border-slate-300 bg-white px-2 py-2 text-sm font-bold text-slate-700 outline-none focus:border-amber-600"
            >
              {LANGUAGES.map((item) => (
                <option key={item} value={item}>
                  {item === "zh-CN" ? t(language, "language.zh") : t(language, "language.en")}
                </option>
              ))}
            </select>
          </div>
        </div>
      </header>

      <main className="mx-auto max-w-7xl px-4 py-6">
        <Routes>
          <Route path="/" element={<Tasks />} />
          <Route path="/tasks" element={<Tasks />} />
          <Route path="/calendar" element={<Calendar />} />
          <Route path="/today" element={<Today />} />
          <Route path="/review" element={<DailyReview />} />
        </Routes>
      </main>
    </div>
  );
}
