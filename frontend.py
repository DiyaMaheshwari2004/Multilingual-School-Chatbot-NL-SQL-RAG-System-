import streamlit as st
import requests

API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

st.title("School Chatbot")

# ---------------- SESSION ----------------
if "user" not in st.session_state:
    st.session_state.user = None

if "chat" not in st.session_state:
    st.session_state.chat = []

# ---------------- LOGIN ----------------
if not st.session_state.user:
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

# ---------------- CHAT ----------------
else:
    user = st.session_state.user

    st.write(f"Logged in as: {user['role']}")

    # Show chat history
    for sender, msg in st.session_state.chat:
        st.write(f"**{sender}:** {msg}")

    # Input
    query = st.text_input("Ask something...")

    if st.button("Send"):
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
            st.error("Server not responding")

    # Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.chat = []
        st.rerun()
