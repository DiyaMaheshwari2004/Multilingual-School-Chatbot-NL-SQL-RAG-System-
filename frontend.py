import streamlit as st
import requests

API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

st.set_page_config(
    page_title="EduAI Assistant",
    page_icon="🎓",
    layout="centered"
)

st.title("EduAI Assistant")

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
    "What is my improvement area?",
    "Show assignments",
    "Show timetable",
    "When is my Maths class?"
]

# ---------------- LOGIN ----------------
if not st.session_state.user:

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

                    # Welcome message
                    st.session_state.chat.append((
                        "Bot",
                        "Welcome to EduAI Assistant.\n\nYou can ask about:\n• Marks\n• Assignments\n• Timetable"
                    ))

                    st.rerun()

                else:
                    st.error("Invalid credentials")

            except:
                pass

# ---------------- CHAT ----------------
else:

    user = st.session_state.user

    st.success(f"Logged in as: {user['role']}")

    # ---------------- SUGGESTIONS ----------------
    st.markdown("### Quick Suggestions")

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
                    pass

    st.divider()

    # ---------------- CHAT HISTORY ----------------
    for sender, msg in st.session_state.chat:

        if sender == "You":
            st.markdown(f"**🧑 You:** {msg}")

        else:
            st.markdown(f"**🤖 Bot:** {msg}")

    # ---------------- INPUT ----------------
    query = st.text_input("Ask something...")

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
                    pass

    # ---------------- LOGOUT ----------------
    st.divider()

    if st.button("Logout"):

        st.session_state.user = None
        st.session_state.chat = []

        st.rerun()
