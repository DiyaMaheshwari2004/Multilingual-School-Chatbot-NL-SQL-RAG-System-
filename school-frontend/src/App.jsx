import { useState, useEffect } from "react";

const API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com";

export default function App() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const [user, setUser] = useState(null);

  const [students, setStudents] = useState([]);

  const [messages, setMessages] = useState([
    {
      sender: "Assistant",
      text: "Welcome to EduAI Assistant. Ask about marks, assignments or timetable.",
    },
  ]);

  const [query, setQuery] = useState("");

  // ---------------- RANDOM FACTS ----------------
  const facts = [
    "Students who revise within 24 hours remember information longer.",
    "Reading 20 minutes daily improves vocabulary and focus.",
    "Short study sessions are often more effective than long sessions.",
    "Sleep plays a major role in memory retention and learning.",
    "Mathematics improves logical and analytical thinking skills.",
    "Consistency is more important than studying for long hours occasionally.",
  ];

  const [fact, setFact] = useState("");

  useEffect(() => {
    const randomFact =
      facts[Math.floor(Math.random() * facts.length)];

    setFact(randomFact);
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

      const roleType =
        data.role === "parent" ? "parent" : "student";

      const chatRes = await fetch(
        `${API_URL}/chat?user_id=${data.id}&role=${roleType}`,
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
          sender: "Assistant",
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
          sender: "Assistant",
          text: "Server is temporarily unavailable.",
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
        sender: "Assistant",
        text: "Welcome to EduAI Assistant.",
      },
    ]);
  };

  // ---------------- LOGIN SCREEN ----------------
  if (!user) {
    return (
      <div
        style={{
          minHeight: "100vh",
          display: "flex",
          justifyContent: "center",
          alignItems: "center",
          background:
            "linear-gradient(to right, #0f172a, #1e3a8a)",
          fontFamily: "Arial",
        }}
      >
        <div
          style={{
            width: "390px",
            background: "rgba(255,255,255,0.08)",
            padding: "45px",
            borderRadius: "24px",
            backdropFilter: "blur(12px)",
            boxShadow: "0 0 40px rgba(0,0,0,0.3)",
            color: "white",
          }}
        >
          <h1
            style={{
              textAlign: "center",
              marginBottom: "10px",
              fontSize: "34px",
            }}
          >
            EduAI Portal
          </h1>

          <p
            style={{
              textAlign: "center",
              opacity: 0.8,
              marginBottom: "35px",
            }}
          >
            Smart Academic Assistant
          </p>

          <input
            type="text"
            placeholder="Username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            style={{
              width: "100%",
              padding: "15px",
              borderRadius: "12px",
              border: "none",
              outline: "none",
              marginBottom: "18px",
              background: "rgba(255,255,255,0.12)",
              color: "white",
              fontSize: "16px",
            }}
          />

          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={{
              width: "100%",
              padding: "15px",
              borderRadius: "12px",
              border: "none",
              outline: "none",
              marginBottom: "22px",
              background: "rgba(255,255,255,0.12)",
              color: "white",
              fontSize: "16px",
            }}
          />

          <button
            onClick={handleLogin}
            style={{
              width: "100%",
              padding: "15px",
              border: "none",
              borderRadius: "12px",
              background: "#2563eb",
              color: "white",
              fontWeight: "bold",
              fontSize: "16px",
              cursor: "pointer",
            }}
          >
            Login
          </button>
        </div>
      </div>
    );
  }

  // ---------------- MAIN UI ----------------
  return (
    <div
      style={{
        minHeight: "100vh",
        display: "flex",
        background:
          "linear-gradient(to right, #020617, #1e3a8a)",
        color: "white",
        fontFamily: "Arial",
      }}
    >
      {/* SIDEBAR */}
      <div
        style={{
          width: "330px",
          padding: "25px",
          background: "rgba(255,255,255,0.06)",
          borderRight: "1px solid rgba(255,255,255,0.08)",
          display: "flex",
          flexDirection: "column",
          justifyContent: "space-between",
        }}
      >
        <div>
          <h2
            style={{
              marginBottom: "30px",
              fontSize: "28px",
            }}
          >
            Student Dashboard
          </h2>

          {students.map((student, index) => (
            <div
              key={index}
              style={{
                background: "rgba(255,255,255,0.1)",
                padding: "22px",
                borderRadius: "20px",
                marginBottom: "22px",
                boxShadow: "0 0 20px rgba(0,0,0,0.15)",
              }}
            >
              <div
                style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "15px",
                }}
              >
                <div
                  style={{
                    width: "60px",
                    height: "60px",
                    borderRadius: "50%",
                    background: "#2563eb",
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    fontSize: "24px",
                    fontWeight: "bold",
                  }}
                >
                  {student.name.charAt(0)}
                </div>

                <div>
                  <h3>{student.name}</h3>

                  <p
                    style={{
                      opacity: 0.8,
                    }}
                  >
                    Class {student.class}
                  </p>
                </div>
              </div>
            </div>
          ))}

          {/* FACT CARD */}
          <div
            style={{
              marginTop: "30px",
              background: "rgba(255,255,255,0.08)",
              padding: "20px",
              borderRadius: "18px",
              lineHeight: "1.7",
            }}
          >
            <h3
              style={{
                marginBottom: "12px",
              }}
            >
              Daily Learning Insight
            </h3>

            <p
              style={{
                opacity: 0.85,
              }}
            >
              {fact}
            </p>
          </div>
        </div>

        {/* LOGOUT */}
        <button
          onClick={logout}
          style={{
            width: "100%",
            marginTop: "30px",
            padding: "15px",
            borderRadius: "12px",
            border: "none",
            background: "#dc2626",
            color: "white",
            fontWeight: "bold",
            fontSize: "16px",
            cursor: "pointer",
          }}
        >
          Logout
        </button>
      </div>

      {/* CHAT SECTION */}
      <div
        style={{
          flex: 1,
          display: "flex",
          flexDirection: "column",
        }}
      >
        {/* TOP HEADER */}
        <div
          style={{
            padding: "22px",
            borderBottom:
              "1px solid rgba(255,255,255,0.08)",
            background: "rgba(255,255,255,0.03)",
          }}
        >
          <h2
            style={{
              fontSize: "30px",
              marginBottom: "8px",
            }}
          >
            EduAI Assistant
          </h2>

          <p
            style={{
              opacity: 0.8,
            }}
          >
            Academic support powered by AI
          </p>
        </div>

        {/* WELCOME SECTION */}
        <div
          style={{
            padding: "25px",
            background: "rgba(255,255,255,0.03)",
            borderBottom:
              "1px solid rgba(255,255,255,0.08)",
          }}
        >
          <div
            style={{
              background: "rgba(37,99,235,0.15)",
              border: "1px solid rgba(37,99,235,0.3)",
              padding: "20px",
              borderRadius: "18px",
            }}
          >
            <h3
              style={{
                marginBottom: "10px",
              }}
            >
              Quick Suggestions
            </h3>

            <div
              style={{
                display: "flex",
                gap: "12px",
                flexWrap: "wrap",
              }}
            >
              {[
                "Show my marks",
                "Show assignments",
                "Show timetable",
              ].map((item, index) => (
                <button
                  key={index}
                  onClick={() => setQuery(item)}
                  style={{
                    padding: "10px 16px",
                    borderRadius: "12px",
                    border: "none",
                    background: "#2563eb",
                    color: "white",
                    cursor: "pointer",
                  }}
                >
                  {item}
                </button>
              ))}
            </div>
          </div>
        </div>

        {/* CHAT */}
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
                <strong>{msg.sender}</strong>

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
            padding: "22px",
            display: "flex",
            gap: "12px",
            borderTop:
              "1px solid rgba(255,255,255,0.08)",
            background: "rgba(255,255,255,0.03)",
          }}
        >
          <input
            type="text"
            placeholder="Ask about academics..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            style={{
              flex: 1,
              padding: "16px",
              borderRadius: "12px",
              border: "none",
              outline: "none",
              background: "rgba(255,255,255,0.1)",
              color: "white",
              fontSize: "16px",
            }}
          />

          <button
            onClick={sendMessage}
            style={{
              padding: "16px 28px",
              borderRadius: "12px",
              border: "none",
              background: "#2563eb",
              color: "white",
              fontWeight: "bold",
              cursor: "pointer",
              fontSize: "16px",
            }}
          >
            Send
          </button>
        </div>
      </div>
    </div>
  );
}