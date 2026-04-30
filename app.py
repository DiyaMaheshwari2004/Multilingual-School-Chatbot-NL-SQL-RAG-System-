from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import database  # runs DB setup on startup
from chatbot import chatbot

app = FastAPI()


# Request model
class Query(BaseModel):
    query: str


# DB connection
def connect_db():
    return sqlite3.connect("school.db")


# ---------------- LOGIN ----------------
@app.post("/login")
def login(username: str, password: str):
    conn = connect_db()
    cursor = conn.cursor()

    # ✅ Case-insensitive username
    cursor.execute(
        "SELECT role, ref_id FROM users WHERE LOWER(username)=LOWER(?) AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {
            "role": user[0],
            "id": user[1]
        }

    return {"error": "Invalid credentials"}


# ---------------- CHAT ----------------
@app.post("/chat")
def chat(q: Query, user_id: int, role: str):

    conn = connect_db()
    cursor = conn.cursor()

    students = []

    # 👤 STUDENT ROLE
    if role == "student":
        cursor.execute(
            "SELECT id, name, class FROM students WHERE id=?",
            (user_id,)
        )
        s = cursor.fetchone()

        if not s:
            return {"response": "Student not found"}

        students.append({
            "id": s[0],
            "name": s[1],
            "class": s[2]
        })

    # 👨‍👩‍👧 PARENT ROLE
    elif role == "parent":
        cursor.execute(
            "SELECT id, name, class FROM students WHERE parent_id=?",
            (user_id,)
        )
        data = cursor.fetchall()

        if not data:
            return {"response": "No children found"}

        for s in data:
            students.append({
                "id": s[0],
                "name": s[1],
                "class": s[2]
            })

    conn.close()

    # 🤖 Chatbot response
    response = chatbot(q.query, role, students)

    return {
        "students": students,
        "response": response
    }
