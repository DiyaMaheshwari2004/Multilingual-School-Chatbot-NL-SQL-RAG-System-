from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import database
from chatbot import chatbot

app = FastAPI()

# ---------------- CORS ----------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------- REQUEST MODEL ----------------
class Query(BaseModel):
    query: str


# ---------------- DB CONNECTION ----------------
def connect_db():
    return sqlite3.connect("school.db")


# ---------------- LOGIN ----------------
@app.post("/login")
def login(username: str, password: str):

    conn = connect_db()
    cursor = conn.cursor()

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

    # ---------------- STUDENT ----------------
    if role == "student":

        cursor.execute(
            "SELECT id, name, class FROM students WHERE id=?",
            (user_id,)
        )

        s = cursor.fetchone()

        if not s:
            conn.close()
            return {"response": "Student not found"}

        students.append({
            "id": s[0],
            "name": s[1],
            "class": s[2]
        })

    # ---------------- PARENT ----------------
    elif role == "parent":

        cursor.execute(
            "SELECT id, name, class FROM students WHERE parent_id=?",
            (user_id,)
        )

        data = cursor.fetchall()

        if not data:
            conn.close()
            return {"response": "No children found"}

        for s in data:
            students.append({
                "id": s[0],
                "name": s[1],
                "class": s[2]
            })

    conn.close()

    # ---------------- CHATBOT RESPONSE ----------------
    response = chatbot(q.query, role, students)

    return {
        "students": students,
        "response": response
    }