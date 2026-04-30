import sqlite3
from rag import retrieve_context


def connect_db():
    return sqlite3.connect("school.db")


# 🔥 MULTILINGUAL NORMALIZATION
def normalize_query(query):
    q = query.lower()

    # Hindi + Hinglish mapping
    if any(word in q for word in ["mark", "marks", "number", "result", "marks batao", "marks dikhao"]):
        return "marks"

    if any(word in q for word in ["assignment", "homework", "kaam", "kaam kya hai"]):
        return "assignment"

    if any(word in q for word in ["timetable", "time", "schedule", "samay"]):
        return "timetable"

    return "general"


# 🔥 LANGUAGE DETECTION (basic)
def detect_language(query):
    if any(word in query for word in ["kya", "hai", "ka", "mera", "dikhao"]):
        return "hindi"
    return "english"


def chatbot(query, role, students):
    intent = normalize_query(query)
    lang = detect_language(query)

    conn = connect_db()
    cursor = conn.cursor()

    # ---------------- MARKS ----------------
    if intent == "marks":
        response = "📊 Marks:\n" if lang == "english" else "📊 अंक:\n"

        for s in students:
            cursor.execute("SELECT subject, marks FROM marks WHERE student_id=?", (s["id"],))
            data = cursor.fetchall()

            response += f"\n{s['name']}:\n"
            for sub, mark in data:
                if lang == "english":
                    response += f" • {sub}: {mark} marks\n"
                else:
                    response += f" • {sub}: {mark} अंक\n"

        conn.close()
        return response

    # ---------------- ASSIGNMENT ----------------
    elif intent == "assignment":
        cls = students[0]["class"]
        cursor.execute("SELECT subject, assignment, due_date FROM assignments WHERE class=?", (cls,))
        data = cursor.fetchall()

        conn.close()

        if lang == "english":
            response = "📝 Assignments:\n"
            for sub, ass, due in data:
                response += f" • {sub}: {ass} (Due: {due})\n"
        else:
            response = "📝 कार्य:\n"
            for sub, ass, due in data:
                response += f" • {sub}: {ass} (अंतिम तिथि: {due})\n"

        return response

    # ---------------- TIMETABLE ----------------
    elif intent == "timetable":
        cls = students[0]["class"]
        cursor.execute("SELECT subject, time, day FROM timetable WHERE class=?", (cls,))
        data = cursor.fetchall()

        conn.close()

        if lang == "english":
            response = "📅 Timetable:\n"
            for sub, time, day in data:
                response += f" • {day}: {sub} at {time}\n"
        else:
            response = "📅 समय सारणी:\n"
            for sub, time, day in data:
                response += f" • {day}: {sub} {time} बजे\n"

        return response

    # ---------------- RAG ----------------
    else:
        conn.close()
        context = retrieve_context(query)

        if lang == "english":
            return f"📚 Info: {context}"
        else:
            return f"📚 जानकारी: {context}"