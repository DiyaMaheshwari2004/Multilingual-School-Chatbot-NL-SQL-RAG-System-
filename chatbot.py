import sqlite3


def connect_db():
    return sqlite3.connect("school.db")


def chatbot(query, role, students):

    conn = connect_db()
    cursor = conn.cursor()

    query = query.lower()

    response = ""

    # ---------------- KEYWORDS ----------------

    performance_keywords = [
        "mark",
        "marks",
        "score",
        "scores",
        "result",
        "results",
        "performance",
        "perform",
        "academically",
        "report card",
        "report",
        "grade",
        "grades",
        "rank",
        "secured",
        "analysis",
        "standing",
        "exam result",
        "exam performance"
    ]

    assignment_keywords = [
        "assignment",
        "homework",
        "project",
        "pending work",
        "pending"
    ]

    timetable_keywords = [
        "timetable",
        "schedule",
        "class",
        "period"
    ]

    subject_keywords = [
        "maths",
        "english",
        "science",
        "evs"
    ]

    # ---------------- SUBJECT DETECTION ----------------

    selected_subject = None

    for sub in subject_keywords:
        if sub in query:
            selected_subject = sub.capitalize()

    # ---------------- PERFORMANCE ----------------

    if any(word in query for word in performance_keywords):

        response = "📊 Academic Performance:\n"

        exam_filter = None

        if "unit" in query:
            exam_filter = "Unit Test"

        elif "mid" in query:
            exam_filter = "Midterm"

        elif "final" in query:
            exam_filter = "Final"

        elif "previous" in query or "last" in query:
            exam_filter = "PREVIOUS"

        for s in students:

            cursor.execute(
                """
                SELECT subject, marks, exam
                FROM marks
                WHERE student_id=?
                """,
                (s["id"],)
            )

            marks = cursor.fetchall()

            filtered_marks = []

            for m in marks:

                subject = m[0]
                score = m[1]
                exam = m[2]

                # Subject filter
                if selected_subject:
                    if subject.lower() != selected_subject.lower():
                        continue

                # Exam filter
                if exam_filter == "Unit Test":
                    if exam != "Unit Test":
                        continue

                elif exam_filter == "Midterm":
                    if exam != "Midterm":
                        continue

                elif exam_filter == "Final":
                    if exam != "Final":
                        continue

                elif exam_filter == "PREVIOUS":
                    if exam == "Final":
                        continue

                filtered_marks.append(m)

            if filtered_marks:

                response += f"\n{s['name']}:\n"

                total = 0

                highest = ("", 0)
                lowest = ("", 101)

                for m in filtered_marks:

                    response += (
                        f"• {m[2]} | {m[0]}: "
                        f"{m[1]} marks\n"
                    )

                    total += m[1]

                    if m[1] > highest[1]:
                        highest = (m[0], m[1])

                    if m[1] < lowest[1]:
                        lowest = (m[0], m[1])

                average = total / len(filtered_marks)

                response += (
                    f"\n⭐ Average Score: "
                    f"{average:.1f}%\n"
                )

                # Performance text
                if average >= 90:
                    response += (
                        "🏆 Outstanding academic performance.\n"
                    )

                elif average >= 75:
                    response += (
                        "📈 Good and consistent performance.\n"
                    )

                else:
                    response += (
                        "📘 Improvement is needed.\n"
                    )

                response += (
                    f"🏆 Strongest Subject: "
                    f"{highest[0]} "
                    f"({highest[1]} marks)\n"
                )

                response += (
                    f"📘 Focus Area: "
                    f"{lowest[0]} "
                    f"({lowest[1]} marks)\n"
                )

                # ---------------- RANK ANALYSIS ----------------

                if average >= 92:
                    rank = "Top 3"

                elif average >= 85:
                    rank = "Top 5"

                elif average >= 75:
                    rank = "Top 10"

                else:
                    rank = "Top 20"

                response += (
                    f"🏅 Estimated Class Rank: "
                    f"{rank}\n"
                )

                # Extra analysis
                if average >= 90:
                    response += (
                        "🚀 Exceptional academic growth.\n"
                    )

                elif average >= 80:
                    response += (
                        "📚 Strong consistency across exams.\n"
                    )

                else:
                    response += (
                        "📘 More practice can improve results.\n"
                    )

            else:
                response += (
                    f"\n{s['name']}: "
                    f"No matching records found\n"
                )

    # ---------------- ASSIGNMENTS ----------------

    elif any(word in query for word in assignment_keywords):

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

            data = cursor.fetchall()

            response += f"\n{s['name']}:\n"

            for d in data:

                response += (
                    f"• {d[0]}: {d[1]} "
                    f"(Due: {d[2]})\n"
                )

    # ---------------- TIMETABLE ----------------

    elif any(word in query for word in timetable_keywords):

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

            data = cursor.fetchall()

            response += f"\n{s['name']}:\n"

            for d in data:

                if selected_subject:

                    if d[0].lower() == selected_subject.lower():

                        response += (
                            f"• {d[0]} class is on "
                            f"{d[2]} at {d[1]}\n"
                        )

                else:

                    response += (
                        f"• {d[2]} | "
                        f"{d[0]} at {d[1]}\n"
                    )

    # ---------------- IMPROVEMENT AREA ----------------

    elif "improvement" in query:

        response = "📘 Improvement Analysis:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, AVG(marks)
                FROM marks
                WHERE student_id=?
                GROUP BY subject
                ORDER BY AVG(marks) ASC
                LIMIT 1
                """,
                (s["id"],)
            )

            data = cursor.fetchone()

            if data:

                response += (
                    f"\n{s['name']}:\n"
                    f"Focus more on {data[0]}.\n"
                    f"Current Average: {data[1]:.1f}%\n"
                )

    # ---------------- DEFAULT ----------------

    else:

        response = (
            "I can help you with:\n"
            "• Marks & Performance\n"
            "• Assignments & Homework\n"
            "• Timetable & Schedule\n\n"
            "Try asking:\n"
            "- Show my marks\n"
            "- Show unit test marks\n"
            "- Show final exam result\n"
            "- What is my improvement area?\n"
            "- What rank did I secure?\n"
            "- Show assignments\n"
            "- When is my Maths class?"
        )

    conn.close()

    return response
