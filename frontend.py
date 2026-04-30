import streamlit as st
import requests 
API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

st.set_page_config(page_title="School Assistant")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "chat" not in st.session_state:
    st.session_state.chat = []

# LOGIN
if not st.session_state.logged_in:
    st.title("🎓 School Portal Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
      res = requests.post(
        f"{API_URL}/login",
        params={"username": username, "password": password}
    )   
      data = res.json()

      if "error" not in data:
            st.session_state.logged_in = True
            st.session_state.user = data
            st.rerun()
      else:
            st.error("Invalid credentials")

    st.stop()

# USER
API_URL = "https://multilingual-school-chatbot-nl-sql-rag.onrender.com"

user = st.session_state.user

res = requests.post(
    f"{API_URL}/chat",
    params={"user_id": user["id"], "role": user["role"]},
    json={"query": "hello"}
)

data = res.json()

# HEADER
st.markdown("## 👋 Welcome")

if user["role"] == "student":
    st.write(f"Student: {data['students'][0]['name']} (Class {data['students'][0]['class']})")
else:
    st.write("Parent Dashboard")
    for s in data["students"]:
        st.write(f"👧 {s['name']} (Class {s['class']})")

if st.button("Logout"):
    st.session_state.clear()
    st.rerun()

st.divider()

# CHAT
for sender, msg in st.session_state.chat:
    st.write(f"**{sender}:** {msg}")

query = st.text_input("Ask something...")

if st.button("Send"):
    res = requests.post(
        f"{API_URL}/chat",
        params={"user_id": user["id"], "role": user["role"]},
        json={"query": query}
    )

    result = res.json()

    st.session_state.chat.append(("You", query))
    st.session_state.chat.append(("Bot", result["response"]))

    st.rerun()
