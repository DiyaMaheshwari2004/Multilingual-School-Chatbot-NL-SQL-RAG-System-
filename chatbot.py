import sqlite3


# ---------------- DATABASE ----------------
def connect_db():
    return sqlite3.connect("school.db")


# ---------------- REMOVE DUPLICATES ----------------
def remove_duplicates(data):
    return list(dict.fromkeys(data))


# ---------------- INTENT DETECTION ----------------
def detect_intent(query):

    query = query.lower()

    # MARKS / PERFORMANCE
    marks_keywords = [
        "mark",
        "marks",
        "score",
        "scores",
        "grade",
        "grades",
        "result",
        "results",
        "performance",
        "perform",
        "academic",
        "academically",
        "rank",
        "report card",
        "how am i doing",
        "how did i perform",
        "exam performance",
        "subject scores"
    ]

    # PREVIOUS EXAMS
    previous_exam_keywords = [
        "previous exam",
        "previous exams",
        "last exam",
        "past exam",
        "older exam",
        "previous result",
        "past performance",
        "previous marks"
    ]

    # ASSIGNMENTS
    assignment_keywords = [
        "assignment",
        "assignments",
        "homework",
        "task",
        "tasks",
        "pending",
        "due",
        "project",
        "projects",
        "pending work",
        "home work"
    ]

    # TIMETABLE
    timetable_keywords = [
        "timetable",
        "schedule",
        "routine",
        "class timing",
        "class timings",
        "timing",
        "time table",
        "period",
        "class schedule"
    ]

    # ---------- PREVIOUS EXAM ----------
    for word in previous_exam_keywords:
        if word in query:
            return "previous_exam"

    # ---------- MARKS ----------
    for word in marks_keywords:
        if word in query:
            return "marks"

    # ---------- ASSIGNMENTS ----------
    for word in assignment_keywords:
        if word in query:
            return "assignments"

    # ---------- TIMETABLE ----------
    for word in timetable_keywords:
        if word in query:
            return "timetable"

    return "unknown"


# ---------------- CHATBOT ----------------
def chatbot(query, role, students):

    conn = connect_db()
    cursor = conn.cursor()

    intent = detect_intent(query)

    response = ""

    # =========================================================
    # MARKS / PERFORMANCE
    # =========================================================
    if intent == "marks":

        response = "📊 Academic Performance:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, marks, exam
                FROM marks
                WHERE student_id=?
                ORDER BY exam DESC
                """,
                (s["id"],)
            )

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                marks_list = [
                    f"• {exam} | {subject}: {score} marks"
                    for subject, score, exam in marks
                ]

                marks_list = remove_duplicates(marks_list)

                response += "\n".join(marks_list)

                # ---------- AVERAGE ----------
                total = sum([m[1] for m in marks])
                avg = round(total / len(marks), 1)

                response += f"\n\n⭐ Average Score: {avg}%\n"

                # ---------- INSIGHT ----------
                if avg >= 90:
                    response += "Excellent academic performance.\n"

                elif avg >= 75:
                    response += "Good and consistent performance.\n"

                else:
                    response += "Needs improvement in some subjects.\n"

            else:
                response += f"\n{s['name']}: No marks found\n"

    # =========================================================
    # PREVIOUS EXAMS
    # =========================================================
    elif intent == "previous_exam":

        response = "📚 Previous Exam Results:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, marks, exam
                FROM marks
                WHERE student_id=?
                AND exam != 'Final'
                ORDER BY exam DESC
                """,
                (s["id"],)
            )

            exams = cursor.fetchall()

            if exams:

                response += f"\n{s['name']}:\n"

                exam_list = [
                    f"• {exam} | {subject}: {score} marks"
                    for subject, score, exam in exams
                ]

                exam_list = remove_duplicates(exam_list)

                response += "\n".join(exam_list)

                # ---------- PREVIOUS EXAM AVERAGE ----------
                total = sum([m[1] for m in exams])
                avg = round(total / len(exams), 1)

                response += f"\n\n📈 Previous Exam Average: {avg}%\n"

            else:
                response += f"\n{s['name']}: No previous exams found\n"

    # =========================================================
    # ASSIGNMENTS
    # =========================================================
    elif intent == "assignments":

        response = "📝 Pending Assignments:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, assignment, due_date
                FROM assignments
                WHERE class=?
                """,
                (s["class"],)
            )

            assignments = cursor.fetchall()

            if assignments:

                response += f"\n{s['name']}:\n"

                assign_list = [
                    f"• {subject}: {assignment} (Due: {due})"
                    for subject, assignment, due in assignments
                ]

                assign_list = remove_duplicates(assign_list)

                response += "\n".join(assign_list)

                response += f"\n\n📌 Total Assignments: {len(assign_list)}\n"

            else:
                response += f"\n{s['name']}: No assignments found\n"

    # =========================================================
    # TIMETABLE
    # =========================================================
    elif intent == "timetable":

        response = "📅 Class Schedule:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, time, day
                FROM timetable
                WHERE class=?
                """,
                (s["class"],)
            )

            timetable = cursor.fetchall()

            if timetable:

                response += f"\n{s['name']}:\n"

                time_list = [
                    f"• {day} | {subject} at {time}"
                    for subject, time, day in timetable
                ]

                time_list = remove_duplicates(time_list)

                response += "\n".join(time_list)

                response += "\n"

            else:
                response += f"\n{s['name']}: No timetable found\n"

    # =========================================================
    # DEFAULT
    # =========================================================
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
