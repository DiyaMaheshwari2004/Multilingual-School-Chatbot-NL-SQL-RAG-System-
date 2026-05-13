import streamlit as st
import requests

API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="EduAI Assistant",
    page_icon="🎓",
    layout="centered"
)

# ---------------- CUSTOM UI ----------------
st.markdown("""
<style>

.main {
    background: linear-gradient(135deg, #0f172a, #111827);
    color: white;
}

.stTextInput > div > div > input {
    background-color: #1e293b;
    color: white;
    border-radius: 10px;
    border: 1px solid #334155;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    border: none;
    background: #2563eb;
    color: white;
    font-weight: 600;
    padding: 0.6rem;
    transition: 0.3s;
}

.stButton > button:hover {
    background: #1d4ed8;
}

.chat-user {
    background: #2563eb;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: white;
}

.chat-bot {
    background: #1e293b;
    padding: 14px;
    border-radius: 14px;
    margin-bottom: 12px;
    color: white;
    border: 1px solid #334155;
}

.quick-title {
    font-size: 18px;
    font-weight: 700;
    margin-top: 15px;
    margin-bottom: 10px;
}

.insight-box {
    background: linear-gradient(135deg, #1e3a8a, #312e81);
    padding: 18px;
    border-radius: 16px;
    margin-bottom: 20px;
    color: white;
    border: 1px solid rgba(255,255,255,0.1);
}

.small-text {
    color: #cbd5e1;
    font-size: 14px;
}

</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown(
    "<h1 style='text-align:center; color:white;'>EduAI Assistant</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p style='text-align:center; color:#94a3b8;'>Smart Academic Support System</p>",
    unsafe_allow_html=True
)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- QUICK SUGGESTIONS ----------------
suggestions = [
    "Show my marks",
    "Show unit test marks",
    "Show midterm marks",
    "Show final exam result",
    "What rank did I secure?",
    "What is my improvement area?",
    "Show assignments",
    "Show timetable",
    "When is my Maths class?",
    "How am I performing academically?"
]

# ---------------- LEARNING INSIGHTS ----------------
insights = [
    "Consistency is more effective than last-minute studying.",
    "Revision improves long-term memory retention.",
    "Strong fundamentals create better academic performance.",
    "Regular practice improves subject confidence.",
    "Balanced study routines reduce academic stress.",
    "Understanding concepts is better than memorization."
]

import random

random_insight = random.choice(insights)

# ---------------- LOGIN ----------------
if not st.session_state.user:

    st.markdown("""
    <div class='insight-box'>
        <h3>Welcome to EduAI Portal</h3>
        <p class='small-text'>
        Access academic performance, assignments,
        timetable and intelligent student insights instantly.
        </p>
    </div>
    """, unsafe_allow_html=True)

    st.subheader("Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        with st.spinner("Connecting..."):

            try:

                res = requests.post(
                    f"{API_URL}/login",
                    params={
                        "username": username,
                        "password": password
                    },
                    timeout=15
                )

                data = res.json()

                if "error" not in data:

                    st.session_state.user = data
                    st.session_state.chat = []

                    st.session_state.chat.append((
                        "Bot",
                        "Welcome to EduAI Assistant.\n\nYou can ask about:\n• Marks\n• Assignments\n• Timetable"
                    ))

                    st.rerun()

                else:
                    st.error("Invalid credentials")

            except:
                st.error("Server not responding")

# ---------------- CHAT AREA ----------------
else:

    user = st.session_state.user

    st.success(f"Logged in as: {user['role']}")

    # ---------------- INSIGHT BOX ----------------
    st.markdown(f"""
    <div class='insight-box'>
        <h3>Daily Learning Insight</h3>
        <p class='small-text'>
        “{random_insight}”
        </p>
    </div>
    """, unsafe_allow_html=True)

    # ---------------- QUICK SUGGESTIONS ----------------
    st.markdown(
        "<div class='quick-title'>Quick Suggestions</div>",
        unsafe_allow_html=True
    )

    cols = st.columns(2)

    for i, suggestion in enumerate(suggestions):

        if cols[i % 2].button(suggestion):

            with st.spinner("Thinking..."):

                try:

                    res = requests.post(
                        f"{API_URL}/chat",
                        params={
                            "user_id": user["id"],
                            "role": user["role"]
                        },
                        json={"query": suggestion},
                        timeout=15
                    )

                    data = res.json()

                    st.session_state.chat.append((
                        "You",
                        suggestion
                    ))

                    st.session_state.chat.append((
                        "Bot",
                        data["response"]
                    ))

                    st.rerun()

                except:
                    st.error("Unable to fetch response")

    st.divider()

    # ---------------- CHAT HISTORY ----------------
    for sender, msg in st.session_state.chat:

        if sender == "You":

            st.markdown(
                f"<div class='chat-user'><b>🧑 You:</b><br>{msg}</div>",
                unsafe_allow_html=True
            )

        else:

            formatted_msg = msg.replace("\n", "<br>")

            st.markdown(
                f"<div class='chat-bot'><b>🤖 EduAI:</b><br>{formatted_msg}</div>",
                unsafe_allow_html=True
            )

    # ---------------- INPUT ----------------
    query = st.text_input(
        "Ask about marks, assignments or timetable..."
    )

    if st.button("Send"):

        if query:

            with st.spinner("Thinking..."):

                try:

                    res = requests.post(
                        f"{API_URL}/chat",
                        params={
                            "user_id": user["id"],
                            "role": user["role"]
                        },
                        json={"query": query},
                        timeout=15
                    )

                    data = res.json()

                    st.session_state.chat.append((
                        "You",
                        query
                    ))

                    st.session_state.chat.append((
                        "Bot",
                        data["response"]
                    ))

                    st.rerun()

                except:
                    st.error("Unable to fetch response")

    # ---------------- LOGOUT ----------------
    st.divider()

    if st.button("Logout"):

        st.session_state.user = None
        st.session_state.chat = []

        st.rerun()
