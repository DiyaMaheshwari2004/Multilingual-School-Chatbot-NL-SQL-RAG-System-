import { motion } from "framer-motion";
import {
  Bell,
  BookOpen,
  CalendarDays,
  LayoutDashboard,
  LogOut,
  MessageSquare,
  Search,
  SendHorizonal,
  Sparkles,
  UserCircle2,
} from "lucide-react";

export default function App() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-950 via-slate-900 to-slate-950 text-white overflow-hidden">
      
      {/* Background Glow */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-blue-500/20 blur-3xl rounded-full" />
      <div className="absolute bottom-0 right-0 w-96 h-96 bg-cyan-500/10 blur-3xl rounded-full" />

      <div className="relative z-10 flex min-h-screen">

        {/* Sidebar */}
        <aside className="w-80 border-r border-white/10 backdrop-blur-xl bg-white/5 p-6 flex flex-col justify-between">

          <div>
            <div className="flex items-center gap-3 mb-10">
              <div className="bg-blue-500 p-3 rounded-2xl shadow-lg shadow-blue-500/30">
                <Sparkles className="w-6 h-6" />
              </div>

              <div>
                <h1 className="text-2xl font-bold">EduAI Portal</h1>
                <p className="text-slate-400 text-sm">
                  Smart School Assistant
                </p>
              </div>
            </div>

            <nav className="space-y-3">
              {[
                {
                  icon: LayoutDashboard,
                  label: "Dashboard",
                  active: true,
                },
                {
                  icon: MessageSquare,
                  label: "AI Assistant",
                },
                {
                  icon: CalendarDays,
                  label: "Timetable",
                },
                {
                  icon: BookOpen,
                  label: "Assignments",
                },
                {
                  icon: Bell,
                  label: "Notifications",
                },
              ].map((item, i) => (
                <motion.button
                  whileHover={{ x: 4 }}
                  key={i}
                  className={`w-full flex items-center gap-4 px-5 py-4 rounded-2xl transition-all ${
                    item.active
                      ? "bg-blue-600 shadow-xl shadow-blue-600/20"
                      : "hover:bg-white/10"
                  }`}
                >
                  <item.icon className="w-5 h-5" />
                  <span className="font-medium">{item.label}</span>
                </motion.button>
              ))}
            </nav>
          </div>

          {/* Profile */}
          <motion.div
            whileHover={{ scale: 1.02 }}
            className="bg-white/10 border border-white/10 rounded-3xl p-5 backdrop-blur-xl"
          >
            <div className="flex items-center gap-4">

              <div className="bg-gradient-to-r from-cyan-500 to-blue-600 p-3 rounded-2xl">
                <UserCircle2 className="w-8 h-8" />
              </div>

              <div>
                <h2 className="font-semibold text-lg">Riya Sharma</h2>
                <p className="text-slate-400 text-sm">
                  Class 3 • Student
                </p>
              </div>

            </div>
          </motion.div>

        </aside>

        {/* Main */}
        <main className="flex-1 p-8 overflow-y-auto">

          {/* Topbar */}
          <div className="flex items-center justify-between mb-10">

            <div>
              <h1 className="text-4xl font-bold tracking-tight">
                Welcome back 👋
              </h1>

              <p className="text-slate-400 mt-2 text-lg">
                Track academics with AI-powered insights.
              </p>
            </div>

            <div className="flex items-center gap-4">

              <button className="bg-white/10 hover:bg-white/20 transition p-3 rounded-2xl border border-white/10">
                <Search className="w-5 h-5" />
              </button>

              <button className="bg-red-500 hover:bg-red-600 transition px-5 py-3 rounded-2xl flex items-center gap-2 shadow-lg shadow-red-500/20">
                <LogOut className="w-4 h-4" />
                Logout
              </button>

            </div>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-10">

            {[
              {
                title: "Average Marks",
                value: "89%",
                color: "from-blue-500 to-cyan-400",
              },
              {
                title: "Assignments Due",
                value: "03",
                color: "from-orange-500 to-yellow-400",
              },
              {
                title: "Classes Today",
                value: "05",
                color: "from-emerald-500 to-green-400",
              },
            ].map((card, i) => (
              <motion.div
                whileHover={{ y: -5 }}
                key={i}
                className="relative overflow-hidden rounded-3xl border border-white/10 bg-white/5 backdrop-blur-xl p-6"
              >
                <div
                  className={`absolute inset-0 bg-gradient-to-r ${card.color} opacity-10`}
                />

                <p className="text-slate-400 text-sm mb-3 relative z-10">
                  {card.title}
                </p>

                <h2 className="text-5xl font-bold relative z-10">
                  {card.value}
                </h2>
              </motion.div>
            ))}

          </div>

          {/* Main Grid */}
          <div className="grid grid-cols-1 xl:grid-cols-3 gap-8">

            {/* Chat */}
            <div className="xl:col-span-2 rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl overflow-hidden flex flex-col h-[720px]">

              {/* Chat Header */}
              <div className="px-8 py-6 border-b border-white/10 flex items-center justify-between bg-white/5 backdrop-blur-xl">

                <div>
                  <h2 className="text-2xl font-semibold flex items-center gap-2">
                    <Sparkles className="w-6 h-6 text-cyan-400" />
                    AI School Assistant
                  </h2>

                  <p className="text-slate-400 mt-1">
                    Ask anything about academics instantly.
                  </p>
                </div>

                <div className="bg-emerald-500/20 text-emerald-400 px-4 py-2 rounded-full text-sm border border-emerald-500/20">
                  ● Online
                </div>

              </div>

              {/* Messages */}
              <div className="flex-1 p-8 overflow-y-auto space-y-6 bg-gradient-to-b from-slate-900/20 to-slate-950/40">

                {/* Bot */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start"
                >
                  <div className="max-w-xl rounded-3xl rounded-tl-md bg-white/10 border border-white/10 px-6 py-5 backdrop-blur-xl">

                    <p className="text-slate-200 leading-relaxed">
                      Hello Riya 👋 I can help you with marks,
                      assignments, timetable, and attendance.
                    </p>

                  </div>
                </motion.div>

                {/* User */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-end"
                >
                  <div className="max-w-xl rounded-3xl rounded-tr-md bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-5 shadow-xl shadow-blue-500/20">
                    <p>Show my assignments for this week</p>
                  </div>
                </motion.div>

                {/* Response */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex justify-start"
                >
                  <div className="max-w-xl rounded-3xl rounded-tl-md bg-white/10 border border-white/10 px-6 py-5 backdrop-blur-xl">

                    <p className="font-semibold text-cyan-300 mb-3">
                      📝 Upcoming Assignments
                    </p>

                    <div className="space-y-3 text-slate-200">

                      <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                        <p className="font-medium">English Essay</p>

                        <p className="text-sm text-slate-400 mt-1">
                          Due: 2 May 2026
                        </p>
                      </div>

                      <div className="bg-white/5 border border-white/10 rounded-2xl p-4">
                        <p className="font-medium">Math Worksheet</p>

                        <p className="text-sm text-slate-400 mt-1">
                          Due: 4 May 2026
                        </p>
                      </div>

                    </div>

                  </div>
                </motion.div>

              </div>

              {/* Input */}
              <div className="p-6 border-t border-white/10 bg-white/5 backdrop-blur-xl flex items-center gap-4">

                <input
                  type="text"
                  placeholder="Ask your assistant anything..."
                  className="flex-1 bg-white/10 border border-white/10 rounded-2xl px-6 py-4 outline-none placeholder:text-slate-400 focus:ring-2 focus:ring-cyan-500"
                />

                <motion.button
                  whileTap={{ scale: 0.95 }}
                  whileHover={{ scale: 1.03 }}
                  className="bg-gradient-to-r from-blue-600 to-cyan-500 px-6 py-4 rounded-2xl shadow-xl shadow-cyan-500/20"
                >
                  <SendHorizonal className="w-5 h-5" />
                </motion.button>

              </div>

            </div>

            {/* Right Panel */}
            <div className="space-y-8">

              {/* Classes */}
              <div className="rounded-[32px] border border-white/10 bg-white/5 backdrop-blur-xl p-6">

                <h3 className="text-xl font-semibold mb-6">
                  📅 Today's Classes
                </h3>

                <div className="space-y-4">

                  {[
                    ["Mathematics", "10:00 AM"],
                    ["English", "11:30 AM"],
                    ["Science", "1:00 PM"],
                  ].map((item, i) => (
                    <div
                      key={i}
                      className="bg-white/5 border border-white/10 rounded-2xl p-4"
                    >
                      <p className="font-medium">{item[0]}</p>

                      <p className="text-sm text-slate-400 mt-1">
                        {item[1]}
                      </p>
                    </div>
                  ))}

                </div>
              </div>

              {/* Performance */}
              <div className="rounded-[32px] border border-white/10 bg-gradient-to-br from-blue-600 to-cyan-500 p-6 shadow-2xl shadow-blue-500/20">

                <p className="text-sm uppercase tracking-wider opacity-80">
                  Academic Performance
                </p>

                <h2 className="text-6xl font-bold mt-4">A+</h2>

                <p className="mt-4 text-white/80 leading-relaxed">
                  Excellent consistency in assignments and subject
                  performance this semester.
                </p>

              </div>

            </div>

          </div>

        </main>
      </div>
    </div>
  );
}