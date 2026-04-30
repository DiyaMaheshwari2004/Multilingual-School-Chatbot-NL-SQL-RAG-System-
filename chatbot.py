import sqlite3


def connect_db():
    return sqlite3.connect("school.db")


#  Remove duplicates safely
def remove_duplicates(data):
    return list(dict.fromkeys(data))


def chatbot(query, role, students):
    conn = connect_db()
    cursor = conn.cursor()

    query = query.lower()
    response = ""

    # ---------------- MARKS ----------------
    if "mark" in query:

        response = "📊 Marks:\n"

        for s in students:
            cursor.execute(
                "SELECT DISTINCT subject, marks FROM marks WHERE student_id=?",
                (s["id"],)
            )
            marks = cursor.fetchall()

            if marks:
                response += f"\n{s['name']}:\n"

                marks_list = [
                    f"• {m[0]}: {m[1]} marks" for m in marks
                ]

                marks_list = remove_duplicates(marks_list)

                response += "\n".join(marks_list) + "\n"
            else:
                response += f"\n{s['name']}: No marks found\n"

    # ---------------- ASSIGNMENTS ----------------
    elif "assignment" in query:

        response = "📝 Assignments:\n"

        for s in students:
            cursor.execute(
                "SELECT DISTINCT subject, assignment, due_date FROM assignments WHERE class=?",
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
    elif "time" in query or "schedule" in query:

        response = "📅 Timetable:\n"

        for s in students:
            cursor.execute(
                "SELECT DISTINCT subject, time, day FROM timetable WHERE class=?",
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
            "• Marks\n"
            "• Assignments\n"
            "• Timetable\n\n"
            "Try asking:\n"
            "- Show my marks\n"
            "- Show assignments\n"
            "- Show timetable"
        )

    conn.close()
    return response
