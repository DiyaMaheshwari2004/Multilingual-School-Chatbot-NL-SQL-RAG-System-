import sqlite3


def connect_db():
    return sqlite3.connect("school.db")


def remove_duplicates(data):
    return list(dict.fromkeys(data))


# ---------------- INTENT DETECTION ----------------
def detect_intent(query):
    query = query.lower()

    marks_keywords = [
        "mark", "score", "performance", "result",
        "exam", "subject", "grade", "rank"
    ]

    assignment_keywords = [
        "assignment", "homework", "task",
        "pending", "due", "project"
    ]

    timetable_keywords = [
        "timetable", "schedule", "class timing",
        "period", "time", "routine"
    ]

    if any(word in query for word in marks_keywords):
        return "marks"

    elif any(word in query for word in assignment_keywords):
        return "assignments"

    elif any(word in query for word in timetable_keywords):
        return "timetable"

    return "unknown"


# ---------------- CHATBOT ----------------
def chatbot(query, role, students):

    conn = connect_db()
    cursor = conn.cursor()

    intent = detect_intent(query)

    response = ""

    # ---------------- MARKS ----------------
    if intent == "marks":

        response = "📊 Academic Performance:\n"

        for s in students:

            cursor.execute(
                """
                SELECT DISTINCT subject, marks, exam
                FROM marks
                WHERE student_id=?
                ORDER BY exam
                """,
                (s["id"],)
            )

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                marks_list = [
                    f"• {m[2]} | {m[0]}: {m[1]} marks"
                    for m in marks
                ]

                marks_list = remove_duplicates(marks_list)

                response += "\n".join(marks_list) + "\n"

            else:
                response += f"\n{s['name']}: No marks found\n"

    # ---------------- ASSIGNMENTS ----------------
    elif intent == "assignments":

        response = "📝 Assignments:\n"

        for s in students:

            cursor.execute(
                """
                SELECT DISTINCT subject, assignment, due_date
                FROM assignments
                WHERE class=?
                """,
                (s["class"],)
            )

            assignments = cursor.fetchall()

            if assignments:

                response += f"\n{s['name']}:\n"

                assign_list = [
                    f"• {a[0]}: {a[1]} (Due: {a[2]})"
                    for a in assignments
                ]

                assign_list = remove_duplicates(assign_list)

                response += "\n".join(assign_list) + "\n"

            else:
                response += f"\n{s['name']}: No assignments found\n"

    # ---------------- TIMETABLE ----------------
    elif intent == "timetable":

        response = "📅 Class Timetable:\n"

        for s in students:

            cursor.execute(
                """
                SELECT DISTINCT subject, time, day
                FROM timetable
                WHERE class=?
                """,
                (s["class"],)
            )

            timetable = cursor.fetchall()

            if timetable:

                response += f"\n{s['name']}:\n"

                time_list = [
                    f"• {t[0]} at {t[1]} on {t[2]}"
                    for t in timetable
                ]

                time_list = remove_duplicates(time_list)

                response += "\n".join(time_list) + "\n"

            else:
                response += f"\n{s['name']}: No timetable found\n"

    # ---------------- DEFAULT ----------------
    else:

        response = (
            "I can help you with:\n"
            "• Marks & Exam Performance\n"
            "• Assignments & Homework\n"
            "• Timetable & Schedule\n\n"
            "Try asking:\n"
            "- Show my exam performance\n"
            "- What homework is pending?\n"
            "- Show class schedule\n"
            "- Show my previous exam marks"
        )

    conn.close()

    return response
