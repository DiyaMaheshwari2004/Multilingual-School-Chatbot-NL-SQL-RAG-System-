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
        with st.spinner("Connecting..."):
            try:
                res = requests.post(
                    f"{API_URL}/login",
                    params={"username": username, "password": password},
                    timeout=15
                )
                data = res.json()

                if "error" not in data:
                    st.session_state.user = data
                    st.session_state.chat = []
                    st.rerun()
                else:
                    st.error("Invalid credentials")

            except:
                # ❌ removed scary error
                pass

# ---------------- CHAT ----------------
else:
    user = st.session_state.user

    st.write(f"Logged in as: {user['role']}")

    # Show chat
    for sender, msg in st.session_state.chat:
        st.write(f"**{sender}:** {msg}")

    # Input
    query = st.text_input("Ask something...")

    if st.button("Send"):
        if query:
            with st.spinner("Thinking..."):
                try:
                    res = requests.post(
                        f"{API_URL}/chat",
                        params={"user_id": user["id"], "role": user["role"]},
                        json={"query": query},
                        timeout=15
                    )

                    data = res.json()

                    st.session_state.chat.append(("You", query))
                    st.session_state.chat.append(("Bot", data["response"]))

                    st.rerun()

                except:
                    # ❌ no error flash
                    pass

    # Logout
    if st.button("Logout"):
        st.session_state.user = None
        st.session_state.chat = []
        st.rerun()
