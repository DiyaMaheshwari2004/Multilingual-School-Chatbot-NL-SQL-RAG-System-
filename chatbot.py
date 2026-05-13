import sqlite3


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
        "marks",
        "score",
        "scores",
        "result",
        "results",
        "performance",
        "report card",
        "grades",
        "academically",
        "perform",
        "exam"
    ]

    # PREVIOUS EXAMS
    previous_keywords = [
        "previous",
        "past",
        "old",
        "last exam",
        "previous exam"
    ]

    # ASSIGNMENTS
    assignment_keywords = [
        "assignment",
        "homework",
        "pending",
        "project",
        "task",
        "work"
    ]

    # TIMETABLE
    timetable_keywords = [
        "timetable",
        "schedule",
        "class timing",
        "routine",
        "period",
        "timing",
        "class"
    ]

    if any(word in query for word in previous_keywords):
        return "previous"

    elif any(word in query for word in marks_keywords):
        return "marks"

    elif any(word in query for word in assignment_keywords):
        return "assignment"

    elif any(word in query for word in timetable_keywords):
        return "timetable"

    return "unknown"


# ---------------- SUBJECT DETECTION ----------------
def detect_subject(query):

    query = query.lower()

    subjects = [
        "maths",
        "science",
        "english",
        "evs"
    ]

    for subject in subjects:
        if subject in query:
            return subject.title()

    return None


# ---------------- EXAM DETECTION ----------------
def detect_exam(query):

    query = query.lower()

    if "unit test" in query:
        return "Unit Test"

    elif "midterm" in query:
        return "Midterm"

    elif "final" in query:
        return "Final"

    return None


# ---------------- CHATBOT ----------------
def chatbot(query, role, students):

    conn = connect_db()
    cursor = conn.cursor()

    intent = detect_intent(query)

    subject_filter = detect_subject(query)
    exam_filter = detect_exam(query)

    response = ""

    # ==================================================
    # MARKS / PERFORMANCE
    # ==================================================
    if intent == "marks":

        response = "📊 Academic Performance:\n"

        for s in students:

            sql = """
            SELECT subject, marks, exam
            FROM marks
            WHERE student_id=?
            """

            params = [s["id"]]

            # SUBJECT FILTER
            if subject_filter:
                sql += " AND subject=?"
                params.append(subject_filter)

            # EXAM FILTER
            if exam_filter:
                sql += " AND exam=?"
                params.append(exam_filter)

            sql += """
            ORDER BY
            CASE exam
                WHEN 'Unit Test' THEN 1
                WHEN 'Midterm' THEN 2
                WHEN 'Final' THEN 3
            END
            """

            cursor.execute(sql, tuple(params))

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                total = 0

                marks_list = []

                for m in marks:

                    marks_list.append(
                        f"• {m[2]} | {m[0]}: {m[1]} marks"
                    )

                    total += m[1]

                marks_list = remove_duplicates(marks_list)

                response += "\n".join(marks_list)

                avg = round(total / len(marks), 1)

                highest = max(marks, key=lambda x: x[1])
                lowest = min(marks, key=lambda x: x[1])

                response += f"\n\n⭐ Average Score: {avg}%\n"

                if avg >= 90:
                    response += "Excellent academic performance.\n"

                elif avg >= 75:
                    response += "Good and consistent performance.\n"

                else:
                    response += "Needs improvement in some subjects.\n"

                response += (
                    f"🏆 Strongest Subject: "
                    f"{highest[0]} ({highest[1]} marks)\n"
                )

                response += (
                    f"📘 Focus Area: "
                    f"{lowest[0]} ({lowest[1]} marks)\n"
                )

            else:
                response += f"\n{s['name']}: No marks found\n"

    # ==================================================
    # PREVIOUS EXAMS
    # ==================================================
    elif intent == "previous":

        response = "📚 Previous Exam Results:\n"

        for s in students:

            sql = """
            SELECT subject, marks, exam
            FROM marks
            WHERE student_id=?
            AND exam != 'Final'
            """

            params = [s["id"]]

            if subject_filter:
                sql += " AND subject=?"
                params.append(subject_filter)

            if exam_filter:
                sql += " AND exam=?"
                params.append(exam_filter)

            sql += """
            ORDER BY
            CASE exam
                WHEN 'Unit Test' THEN 1
                WHEN 'Midterm' THEN 2
            END
            """

            cursor.execute(sql, tuple(params))

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                total = 0

                for m in marks:

                    response += (
                        f"• {m[2]} | "
                        f"{m[0]}: {m[1]} marks\n"
                    )

                    total += m[1]

                avg = round(total / len(marks), 1)

                response += (
                    f"\n📈 Previous Exam Average: "
                    f"{avg}%\n"
                )

            else:
                response += (
                    f"\n{s['name']}: "
                    f"No previous exam records found\n"
                )

    # ==================================================
    # ASSIGNMENTS
    # ==================================================
    elif intent == "assignment":

        response = "📝 Pending Assignments:\n"

        total_assignments = 0

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

                assign_list = []

                for a in assignments:

                    assign_list.append(
                        f"• {a[0]}: "
                        f"{a[1]} "
                        f"(Due: {a[2]})"
                    )

                assign_list = remove_duplicates(assign_list)

                total_assignments += len(assign_list)

                response += "\n".join(assign_list)

                response += "\n"

            else:
                response += (
                    f"\n{s['name']}: "
                    f"No assignments found\n"
                )

        response += (
            f"\n📌 Total Assignments: "
            f"{total_assignments}"
        )

    # ==================================================
    # TIMETABLE
    # ==================================================
    elif intent == "timetable":

        response = "📅 Class Schedule:\n"

        for s in students:

            sql = """
            SELECT subject, time, day
            FROM timetable
            WHERE class=?
            """

            params = [s["class"]]

            if subject_filter:
                sql += " AND subject=?"
                params.append(subject_filter)

            cursor.execute(sql, tuple(params))

            timetable = cursor.fetchall()

            if timetable:

                response += f"\n{s['name']}:\n"

                time_list = []

                for t in timetable:

                    time_list.append(
                        f"• {t[0]} at {t[1]} on {t[2]}"
                    )

                time_list = remove_duplicates(time_list)

                response += "\n".join(time_list)

                response += "\n"

            else:
                response += (
                    f"\n{s['name']}: "
                    f"No timetable found\n"
                )

    # ==================================================
    # DEFAULT
    # ==================================================
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
