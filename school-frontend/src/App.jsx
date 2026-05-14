import { useState, useEffect } from "react";
import botImage from "./assets/bot.png";

const API_URL =
  "https://multilingual-school-chatbot-nl-sql-rag.onrender.com";

function App() {
  const [user, setUser] = useState(null);
  const [students, setStudents] = useState([]);
  const [query, setQuery] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  // ---------------- INSIGHTS ----------------
  const insights = [
    "Consistency beats last-minute studying.",
    "Reading daily improves memory retention.",
    "Small progress every day leads to big achievements.",
    "Revision is the key to long-term learning.",
    "Focused study sessions improve productivity.",
    "Learning is more effective when practiced regularly.",
  ];

  const [randomInsight, setRandomInsight] = useState("");

  useEffect(() => {
    const random =
      insights[Math.floor(Math.random() * insights.length)];

    setRandomInsight(random);
  }, []);

  // ---------------- LOGIN ----------------
  const handleLogin = async () => {
    try {
      const res = await fetch(
        `${API_URL}/login?username=${username}&password=${password}`,
        {
          method: "POST",
        }
      );

      const data = await res.json();

      if (data.error) {
        alert("Invalid credentials");
        return;
      }

      setUser(data);

      const chatRes = await fetch(
        `${API_URL}/chat?user_id=${data.id}&role=${data.role}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: "hello",
          }),
        }
      );

      const chatData = await chatRes.json();

      setStudents(chatData.students || []);

      setMessages([
        {
          sender: "bot",
          text:
            "Welcome to EduAI Assistant.\n\nYou can ask about:\n• Marks\n• Assignments\n• Timetable",
        },
      ]);
    } catch (err) {
      alert("Backend not responding");
    }
  };

  // ---------------- SEND MESSAGE ----------------
  const sendMessage = async (customQuery = null) => {
    const finalQuery = customQuery || query;

    if (!finalQuery.trim()) return;

    const updatedMessages = [
      ...messages,
      {
        sender: "user",
        text: finalQuery,
      },
    ];

    setMessages(updatedMessages);

    setLoading(true);

    try {
      const res = await fetch(
        `${API_URL}/chat?user_id=${user.id}&role=${user.role}`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: finalQuery,
          }),
        }
      );

      const data = await res.json();

      if (data.students) {
        setStudents(data.students);
      }

      setMessages([
        ...updatedMessages,
        {
          sender: "bot",
          text: data.response,
        },
      ]);
    } catch (err) {
      setMessages([
        ...updatedMessages,
        {
          sender: "bot",
          text: "Server not responding.",
        },
      ]);
    }

    setQuery("");
    setLoading(false);
  };

  // ---------------- LOGIN SCREEN ----------------
  if (!user) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-[#081028] via-[#0f172a] to-[#111827] flex items-center justify-center px-6 relative overflow-hidden">

        {/* Glow Effects */}
        <div className="absolute w-[500px] h-[500px] bg-blue-500 opacity-20 blur-3xl rounded-full top-[-100px] left-[-100px]" />

        <div className="absolute w-[400px] h-[400px] bg-indigo-500 opacity-20 blur-3xl rounded-full bottom-[-100px] right-[-100px]" />

        {/* Login Card */}
        <div className="bg-[#111827]/90 backdrop-blur-xl border border-white/10 p-10 rounded-3xl w-full max-w-md shadow-2xl z-10">

          {/* Logo */}
          <div className="flex flex-col items-center mb-8">
            <img
              src={botImage}
              alt="bot"
              className="w-24 h-24 rounded-full shadow-2xl mb-5"
            />

            <h1 className="text-4xl font-bold text-white mb-2">
              EduAI Portal
            </h1>

            <p className="text-gray-400 text-center">
              Intelligent Academic Assistant
            </p>
          </div>

          {/* Inputs */}
          <div className="space-y-5">

            <input
              type="text"
              placeholder="Username"
              value={username}
              onChange={(e) =>
                setUsername(e.target.value)
              }
              className="w-full bg-[#1e293b] text-white p-4 rounded-xl outline-none border border-gray-700 focus:border-blue-500"
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              onChange={(e) =>
                setPassword(e.target.value)
              }
              className="w-full bg-[#1e293b] text-white p-4 rounded-xl outline-none border border-gray-700 focus:border-blue-500"
            />

            <button
              onClick={handleLogin}
              className="w-full bg-blue-600 hover:bg-blue-700 transition-all text-white py-4 rounded-xl font-semibold shadow-lg"
            >
              Login
            </button>
          </div>
        </div>
      </div>
    );
  }

  // ---------------- MAIN DASHBOARD ----------------
  return (
    <div className="min-h-screen bg-gradient-to-br from-[#081028] via-[#0f172a] to-[#172554] text-white flex">

      {/* SIDEBAR */}
      <div className="w-[340px] min-w-[340px] bg-[#0f172a]/90 border-r border-white/10 p-6 flex flex-col justify-between">

        <div>

          {/* Header */}
          <div className="mb-10">
            <h1 className="text-5xl font-bold tracking-tight text-white leading-tight">
              EduAI Dashboard
            </h1>

            <p className="text-lg text-slate-400 mt-3">
              Intelligent Student Workspace
            </p>
          </div>

          {/* STUDENT CARDS */}
          <div className="space-y-5">

            {students.map((student) => (
              <div
                key={student.id}
                className="bg-[#1e293b] p-6 rounded-3xl border border-white/10 shadow-xl"
              >
                <div className="flex items-center gap-5">

                  {/* Student Icon */}
                  <div className="w-20 h-20 rounded-full bg-blue-600 flex items-center justify-center text-3xl font-bold shadow-md">
                    {student.name[0]}
                  </div>

                  {/* Student Info */}
                  <div>
                    <h2 className="text-3xl font-semibold">
                      {student.name}
                    </h2>

                    <p className="text-gray-400 text-2xl mt-1">
                      Class {student.class}
                    </p>
                  </div>
                </div>
              </div>
            ))}

          </div>

          {/* INSIGHTS + SUGGESTIONS */}
          <div className="mt-8 space-y-5">

            {/* Quote Card */}
            <div className="bg-[#1e293b] border border-white/10 rounded-3xl p-8 shadow-xl">

              <p className="text-2xl italic text-slate-300 leading-relaxed">
                “{randomInsight}”
              </p>

              <div className="mt-5 text-lg text-slate-500">
                Daily Learning Insight
              </div>
            </div>

            {/* QUICK COMMANDS */}
            <div className="bg-gradient-to-br from-blue-600 to-indigo-700 rounded-3xl p-8 shadow-2xl overflow-hidden">

              <h3 className="font-bold text-white text-4xl mb-8">
                Quick Suggestions
              </h3>

              <div className="flex flex-wrap gap-4">

                {[
                  "Show my marks",
                  "Show unit test marks",
                  "Show midterm marks",
                  "Show final result",
                  "Show my rank",
                  "My improvement area",
                  "Performance analysis",
                  "Show assignments",
                  "Pending homework",
                  "Show timetable",
                  "When is my Maths class?"
                ].map((item, index) => (

                  <button
                    key={index}
                    onClick={() => sendMessage(item)}
                    className="text-lg bg-white/15 hover:bg-white/25 transition-all px-6 py-4 rounded-full text-white border border-white/10 whitespace-nowrap"
                  >
                    {item}
                  </button>

                ))}

              </div>
            </div>

          </div>
        </div>

        {/* LOGOUT */}
        <button
          onClick={() => {
            setUser(null);
            setStudents([]);
            setMessages([]);
          }}
          className="mt-10 bg-red-500 hover:bg-red-600 transition-all py-5 rounded-2xl font-semibold shadow-lg text-2xl"
        >
          Logout
        </button>
      </div>

      {/* MAIN CHAT AREA */}
      <div className="flex-1 flex flex-col">

        {/* TOP BAR */}
        <div className="p-8 border-b border-white/10 bg-[#0f172a]/70 backdrop-blur-lg">

          <div className="flex items-center gap-5">

            <img
              src={botImage}
              alt="bot"
              className="w-20 h-20 rounded-full shadow-lg"
            />

            <div>
              <h1 className="text-5xl font-bold">
                EduAI Assistant
              </h1>

              <p className="text-gray-400 text-2xl mt-2">
                Smart Academic Support System
              </p>
            </div>

          </div>
        </div>

        {/* CHAT AREA */}
        <div className="flex-1 overflow-y-auto p-8 space-y-8">

          {/* CHAT MESSAGES */}
          {messages.map((msg, index) => (
            <div
              key={index}
              className={`flex ${
                msg.sender === "user"
                  ? "justify-end"
                  : "justify-start"
              }`}
            >

              {msg.sender === "bot" ? (
                <div className="flex gap-4 items-start max-w-[75%]">

                  <img
                    src={botImage}
                    alt="bot"
                    className="w-14 h-14 rounded-full shadow-md"
                  />

                  <div className="bg-[#1e293b] p-6 rounded-3xl whitespace-pre-line border border-white/10 shadow-lg text-2xl leading-relaxed">
                    {msg.text}
                  </div>
                </div>
              ) : (
                <div className="bg-blue-600 p-6 rounded-3xl max-w-[75%] shadow-lg whitespace-pre-line text-2xl leading-relaxed">
                  {msg.text}
                </div>
              )}

            </div>
          ))}

          {loading && (
            <div className="text-gray-400 text-xl">
              Thinking...
            </div>
          )}
        </div>

        {/* INPUT BAR */}
        <div className="p-6 border-t border-white/10 bg-[#0f172a]/80 backdrop-blur-lg flex gap-4">

          <input
            type="text"
            placeholder="Ask about marks, timetable or assignments..."
            value={query}
            onChange={(e) =>
              setQuery(e.target.value)
            }
            onKeyDown={(e) =>
              e.key === "Enter" && sendMessage()
            }
            className="flex-1 bg-[#1e293b] text-white p-5 rounded-3xl outline-none border border-white/10 focus:border-blue-500 text-xl"
          />

          <button
            onClick={() => sendMessage()}
            className="bg-blue-600 hover:bg-blue-700 px-10 rounded-3xl font-semibold transition-all shadow-lg text-xl"
          >
            Send
          </button>

        </div>
      </div>
    </div>
  );
}

export default App;