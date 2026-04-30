from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from chatbot import chatbot

app = FastAPI()

class Query(BaseModel):
    query: str


def connect_db():
    return sqlite3.connect("school.db")


@app.post("/login")
def login(username: str, password: str):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT role, ref_id FROM users WHERE username=? AND password=?",
        (username, password)
    )

    user = cursor.fetchone()
    conn.close()

    if user:
        return {"role": user[0], "id": user[1]}
    return {"error": "Invalid credentials"}


@app.post("/chat")
def chat(q: Query, user_id: int, role: str):

    conn = connect_db()
    cursor = conn.cursor()

    students = []

    if role == "student":
        cursor.execute("SELECT id, name, class FROM students WHERE id=?", (user_id,))
        s = cursor.fetchone()
        students.append({"id": s[0], "name": s[1], "class": s[2]})

    elif role == "parent":
        cursor.execute("SELECT id, name, class FROM students WHERE parent_id=?", (user_id,))
        data = cursor.fetchall()

        for s in data:
            students.append({"id": s[0], "name": s[1], "class": s[2]})

    conn.close()

    response = chatbot(q.query, role, students)

    return {
        "students": students,
        "response": response
    }