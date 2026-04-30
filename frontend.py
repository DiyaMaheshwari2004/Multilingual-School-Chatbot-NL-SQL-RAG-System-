import streamlit as st
import requests

API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

st.set_page_config(page_title="School Assistant", layout="wide")

# ---------------- STYLES ----------------
st.markdown("""
<style>
.main {
    background-color: #f5f7fa;
}
.card {
    background-color: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.1);
    margin-bottom: 10px;
}
.title {
    font-size: 28px;
    font-weight: bold;
}
.subtitle {
    color: gray;
}
.chat-user {
    background-color: #d1e7ff;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
.chat-bot {
    background-color: #e2ffe2;
    padding: 10px;
    border-radius: 10px;
    margin: 5px 0;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- LOGIN ----------------
if not st.session_state.user:

    st.markdown("<div class='title'>🏫 School AI Assistant</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Login to continue</div>", unsafe_allow_html=True)

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        try:
            res = requests.post(
                f"{API_URL}/login",
                params={"username": username, "password": password}
            )
            data = res.json()

            if "error" not in data:
                st.session_state.user = data
                st.session_state.chat = []
                st.rerun()
            else:
                st.error("Invalid credentials")

        except:
            st.error("Server not reachable")

# ---------------- MAIN DASHBOARD ----------------
else:
    user = st.session_state.user

    col1, col2 = st.columns([3,1])

    with col1:
        st.markdown("<div class='title'>📊 School Dashboard</div>", unsafe_allow_html=True)

    with col2:
        if st.button("Logout"):
            st.session_state.user = None
            st.session_state.chat = []
            st.rerun()

    st.markdown("---")

    # -------- STUDENT INFO --------
    st.markdown("<div class='card'><b>👤 Logged in</b></div>", unsafe_allow_html=True)
    st.write(f"Role: {user['role'].capitalize()}")

    # -------- CHAT SECTION --------
    st.markdown("### 💬 Ask Your Assistant")

    chat_container = st.container()

    with chat_container:
        for sender, msg in st.session_state.chat:
            if sender == "You":
                st.markdown(f"<div class='chat-user'><b>You:</b> {msg}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bot'><b>Bot:</b><br>{msg}</div>", unsafe_allow_html=True)

    query = st.text_input("Type your question...")

    if st.button("Send"):
        if query.strip() == "":
            st.warning("Please enter a question")
        else:
            with st.spinner("Fetching data..."):
                try:
                    res = requests.post(
                        f"{API_URL}/chat",
                        params={"user_id": user["id"], "role": user["role"]},
                        json={"query": query}
                    )

                    result = res.json()

                    st.session_state.chat.append(("You", query))
                    st.session_state.chat.append(("Bot", result["response"]))

                    st.rerun()

                except:
                    st.error("Server not responding. Try again.")
