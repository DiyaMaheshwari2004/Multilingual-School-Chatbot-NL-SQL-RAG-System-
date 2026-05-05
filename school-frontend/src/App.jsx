import { useState } from "react";

const API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [user, setUser] = useState(null);

  const [students, setStudents] = useState([]);

  const [messages, setMessages] = useState([
    {
      sender: "Bot",
      text: "Hello 👋 Ask me about marks, assignments or timetable.",
    },
  ]);

  const [query, setQuery] = useState("");

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

      // Parent Dashboard Auto Load
      if (data.role === "parent") {
        const chatRes = await fetch(
          `${API_URL}/chat?user_id=${data.id}&role=parent`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              query: "show my marks",
            }),
          }
        );

        const chatData = await chatRes.json();

        setStudents(chatData.students || []);

        setMessages([
          {
            sender: "Bot",
            text: chatData.response,
          },
        ]);
      }

      // Student Dashboard
      else {
        const chatRes = await fetch(
          `${API_URL}/chat?user_id=${data.id}&role=student`,
          {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            body: JSON.stringify({
              query: "show my marks",
            }),
          }
        );

        const chatData = await chatRes.json();

        setStudents(chatData.students || []);

        setMessages([
          {
            sender: "Bot",
            text: chatData.response,
          },
        ]);
      }
    } catch (err) {
      console.error(err);
      alert("Backend not responding");
    }
  };

  // ---------------- CHAT ----------------
  const sendMessage = async () => {
    if (!query) return;

    const userMessage = {
      sender: "You",
      text: query,
    };

    setMessages((prev) => [...prev, userMessage]);

    try {
      const res = await fetch(
        `${API_URL}/chat?user_id=${user.id}&role=${user.role}`,
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

      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: data.response,
        },
      ]);

      if (data.students) {
        setStudents(data.students);
      }
    } catch (err) {
      console.error(err);

      setMessages((prev) => [
        ...prev,
        {
          sender: "Bot",
          text: "⚠️ Backend server not responding",
        },
      ]);
    }

    setQuery("");
  };

  // ---------------- LOGOUT ----------------
  const logout = () => {
    setUser(null);
    setStudents([]);
    setMessages([
      {
        sender: "Bot",
        text: "Hello 👋 Ask me about marks, assignments or timetable.",
      },
    ]);
  };

  // ---------------- LOGIN PAGE ----------------
  if (!user) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background: "linear-gradient(to right, #0f172a, #1e3a8a)",
          color: "white",
          fontFamily: "Arial",
        }}
      >
        <div
          style={{
            width: "380px",
            padding: "40px",
            borderRadius: "20px",
            background: "rgba(255,255,255,0.08)",
            backdropFilter: "blur(10px)",
            boxShadow: "0 0 30px rgba(0,0,0,0.3)",
          }}
        >
          <h1
            style={{
              textAlign: "center",
              marginBottom: "10px",
            }}
          >
            🎓 EduAI Portal
          </h1>

          <p
            style={{
              textAlign: "center",
              opacity: 0.8,
              marginBottom: "30px",
            }}
          >
            AI Powered School Assistant
          </p>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "15px",
              borderRadius: "10px",
              border: "none",
              outline: "none",
              fontSize: "16px",
              background: "rgba(255,255,255,0.15)",
              color: "white",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "14px",
              marginBottom: "20px",
              borderRadius: "10px",
              border: "none",
              outline: "none",
              fontSize: "16px",
              background: "rgba(255,255,255,0.15)",
              color: "white",
            }}
          />

          <button
            onClick={handleLogin}
            style={{
              width: "100%",
              padding: "14px",
              borderRadius: "10px",
              border: "none",
              background: "#2563eb",
              color: "white",
              fontSize: "16px",
              cursor: "pointer",
              fontWeight: "bold",
            }}
          >
            Login
          </button>

          <div
            style={{
              marginTop: "25px",
              fontSize: "14px",
              opacity: 0.8,
            }}
          >
            <p>Demo Credentials:</p>
            <p>Parent → rajesh / 123</p>
            <p>Student → rahul / 123</p>
          </div>
        </div>
      </div>
    );
  }

  // ---------------- MAIN DASHBOARD ----------------
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        background: "linear-gradient(to right, #020617, #1e3a8a)",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      {/* SIDEBAR */}
      <div
        style={{
          width: "320px",
          background: "rgba(255,255,255,0.06)",
          padding: "25px",
          borderRight: "1px solid rgba(255,255,255,0.1)",
        }}
      >
        <h2 style={{ marginBottom: "30px" }}>
          📊 EduAI Dashboard
        </h2>

        {students.map((student, index) => (
          <div
            key={index}
            style={{
              background: "rgba(255,255,255,0.1)",
              padding: "20px",
              borderRadius: "18px",
              marginBottom: "20px",
            }}
          >
            <h3>{student.name}</h3>

            <p
              style={{
                opacity: 0.8,
              }}
            >
              Class: {student.class}
            </p>
          </div>
        ))}

        <button
          onClick={logout}
          style={{
            width: "100%",
            marginTop: "20px",
            padding: "14px",
            border: "none",
            borderRadius: "12px",
            background: "#ef4444",
            color: "white",
            fontSize: "16px",
            fontWeight: "bold",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>

      {/* CHAT AREA */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* TOP BAR */}
        <div
          style={{
            padding: "20px",
            borderBottom: "1px solid rgba(255,255,255,0.1)",
            background: "rgba(255,255,255,0.03)",
          }}
        >
          <h2>🤖 AI School Chatbot</h2>

          <p
            style={{
              opacity: 0.8,
            }}
          >
            Logged in as: {user.role}
          </p>
        </div>

        {/* CHAT MESSAGES */}
        <div
          style={{
            flex: 1,
            overflowY: "auto",
            padding: "30px",
          }}
        >
          {messages.map((msg, index) => (
            <div
              key={index}
              style={{
                display: "flex",
                justifyContent:
                  msg.sender === "You"
                    ? "flex-end"
                    : "flex-start",
                marginBottom: "20px",
              }}
            >
              <div
                style={{
                  background:
                    msg.sender === "You"
                      ? "#2563eb"
                      : "rgba(255,255,255,0.1)",
                  padding: "18px",
                  borderRadius: "18px",
                  maxWidth: "70%",
                  whiteSpace: "pre-line",
                  lineHeight: "1.6",
                }}
              >
                <strong>{msg.sender}:</strong>

                <div style={{ marginTop: "8px" }}>
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
            gap: "10px",
            borderTop: "1px solid rgba(255,255,255,0.1)",
            background: "rgba(255,255,255,0.03)",
          }}
        >
          <input
            type="text"
            placeholder="Ask about marks, timetable, assignments..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              flex: 1,
              padding: "15px",
              borderRadius: "12px",
              border: "none",
              outline: "none",
              fontSize: "16px",
              background: "rgba(255,255,255,0.1)",
              color: "white",
            }}
          />

          <button
            onClick={sendMessage}
            style={{
              padding: "15px 30px",
              borderRadius: "12px",
              border: "none",
              background: "#2563eb",
              color: "white",
              fontSize: "16px",
              fontWeight: "bold",
              cursor: "pointer",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}