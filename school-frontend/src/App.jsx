import { useState } from "react";

export default function App() {
  const [loggedIn, setLoggedIn] = useState(false);

  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [messages, setMessages] = useState([
    {
      sender: "Bot",
      text: "Hello 👋 Ask me about assignments, marks or timetable.",
    },
  ]);

  const [query, setQuery] = useState("");

  // DEMO DASHBOARD DATA
  const student = {
    name: username || "Student",
    class: "5A",
    attendance: "92%",
    marks: "88%",
    assignments: 3,
  };

  // LOGIN
  const handleLogin = () => {
    if (username.trim() !== "" && password.trim() !== "") {
      setLoggedIn(true);
    }
  };

  // CHAT API
  const sendMessage = async () => {
    if (query.trim() === "") return;

    const userMessage = {
      sender: username,
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    setQuery("");

    try {
      const res = await fetch(
        "https://multilingual-school-chatbot-nl-sql-rag.onrender.com/chat",
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            query: query,
          }),
        }
      );

      const data = await res.json();

      const botMessage = {
        sender: "Bot",
        text: data.response,
      };

      setMessages((prev) => [...prev, botMessage]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: "⚠️ Server not responding.",
        },
      ]);
    }
  };

  // LOGIN PAGE
  if (!loggedIn) {
    return (
      <div
        style={{
          height: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background:
            "linear-gradient(135deg, #0f172a, #111827, #1e3a8a)",
          fontFamily: "Arial",
        }}
      >
        <div
          style={{
            width: "380px",
            padding: "40px",
            borderRadius: "24px",
            background: "rgba(255,255,255,0.08)",
            backdropFilter: "blur(10px)",
            border: "1px solid rgba(255,255,255,0.1)",
            boxShadow: "0 0 30px rgba(0,0,0,0.3)",
          }}
        >
          <h1
            style={{
              color: "white",
              textAlign: "center",
              marginBottom: "10px",
              fontSize: "32px",
            }}
          >
            🎓 EduAI
          </h1>

          <p
            style={{
              color: "#cbd5e1",
              textAlign: "center",
              marginBottom: "30px",
            }}
          >
            Smart School Assistant
          </p>

          {/* USERNAME */}
          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "18px",
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(255,255,255,0.08)",
              color: "white",
              fontSize: "16px",
              outline: "none",
            }}
          />

          {/* PASSWORD */}
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "22px",
              borderRadius: "12px",
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(255,255,255,0.08)",
              color: "white",
              fontSize: "16px",
              outline: "none",
            }}
          />

          {/* LOGIN BUTTON */}
          <button
            onClick={handleLogin}
            style={{
              width: "100%",
              padding: "14px",
              border: "none",
              borderRadius: "12px",
              background:
                "linear-gradient(135deg, #2563eb, #3b82f6)",
              color: "white",
              fontSize: "16px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Login
          </button>
        </div>
      </div>
    );
  }

  // MAIN PAGE
  return (
    <div
      style={{
        height: "100vh",
        display: "flex",
        background:
          "linear-gradient(135deg, #0f172a, #111827, #1e3a8a)",
        fontFamily: "Arial",
      }}
    >
      {/* SIDEBAR */}
      <div
        style={{
          width: "280px",
          background: "rgba(255,255,255,0.06)",
          backdropFilter: "blur(12px)",
          borderRight: "1px solid rgba(255,255,255,0.1)",
          padding: "25px",
          color: "white",
        }}
      >
        <h2 style={{ marginBottom: "25px" }}>
          🎓 EduAI Dashboard
        </h2>

        {/* PROFILE CARD */}
        <div
          style={{
            background: "rgba(255,255,255,0.08)",
            padding: "20px",
            borderRadius: "18px",
            marginBottom: "25px",
          }}
        >
          <h3>{student.name}</h3>
          <p style={{ color: "#cbd5e1" }}>
            Class: {student.class}
          </p>
        </div>

        {/* DASHBOARD CARDS */}
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            gap: "15px",
          }}
        >
          <div
            style={{
              background: "#2563eb",
              padding: "18px",
              borderRadius: "16px",
            }}
          >
            <h4>📚 Attendance</h4>
            <h2>{student.attendance}</h2>
          </div>

          <div
            style={{
              background: "#16a34a",
              padding: "18px",
              borderRadius: "16px",
            }}
          >
            <h4>📝 Average Marks</h4>
            <h2>{student.marks}</h2>
          </div>

          <div
            style={{
              background: "#ea580c",
              padding: "18px",
              borderRadius: "16px",
            }}
          >
            <h4>📌 Assignments</h4>
            <h2>{student.assignments}</h2>
          </div>
        </div>

        {/* LOGOUT */}
        <button
          onClick={() => setLoggedIn(false)}
          style={{
            marginTop: "30px",
            width: "100%",
            padding: "12px",
            border: "none",
            borderRadius: "12px",
            background: "#ef4444",
            color: "white",
            cursor: "pointer",
            fontWeight: "bold",
          }}
        >
          Logout
        </button>
      </div>

      {/* MAIN CHAT */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* HEADER */}
        <div
          style={{
            padding: "20px 30px",
            color: "white",
            borderBottom: "1px solid rgba(255,255,255,0.1)",
            background: "rgba(255,255,255,0.05)",
            backdropFilter: "blur(10px)",
          }}
        >
          <h2>🤖 AI School Chatbot</h2>
        </div>

        {/* CHAT AREA */}
        <div
          style={{
            flex: 1,
            padding: "25px",
            overflowY: "auto",
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                justifyContent:
                  msg.sender === username
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "18px",
              }}
            >
              <div
                style={{
                  padding: "14px 18px",
                  borderRadius: "18px",
                  maxWidth: "70%",
                  background:
                    msg.sender === username
                      ? "linear-gradient(135deg, #2563eb, #3b82f6)"
                      : "rgba(255,255,255,0.08)",
                  color: "white",
                  backdropFilter: "blur(8px)",
                }}
              >
                <strong>{msg.sender}: </strong>

                <div style={{ marginTop: "6px" }}>
                  {msg.text}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* INPUT */}
        <div
          style={{
            padding: "20px",
            display: "flex",
            gap: "12px",
            background: "rgba(255,255,255,0.05)",
            borderTop: "1px solid rgba(255,255,255,0.1)",
          }}
        >
          <input
            type="text"
            placeholder="Ask something..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
            style={{
              flex: 1,
              padding: "14px",
              borderRadius: "14px",
              border: "1px solid rgba(255,255,255,0.1)",
              background: "rgba(255,255,255,0.08)",
              color: "white",
              fontSize: "16px",
              outline: "none",
            }}
          />

          <button
            onClick={sendMessage}
            style={{
              padding: "14px 24px",
              border: "none",
              borderRadius: "14px",
              background:
                "linear-gradient(135deg, #2563eb, #3b82f6)",
              color: "white",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}