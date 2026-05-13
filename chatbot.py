import sqlite3


def connect_db():
    return sqlite3.connect("school.db")


# ---------------- REMOVE DUPLICATES ----------------
def remove_duplicates(data):
    return list(dict.fromkeys(data))


# ---------------- CHATBOT ----------------
def chatbot(query, role, students):

    conn = connect_db()
    cursor = conn.cursor()

    query = query.lower().strip()

    response = ""

    # =====================================================
    # SUBJECT DETECTION
    # =====================================================

    subject_filter = None

    subjects = [
        "maths",
        "science",
        "english",
        "evs"
    ]

    for sub in subjects:
        if sub in query:
            subject_filter = sub.capitalize()

    # =====================================================
    # EXAM TYPE DETECTION
    # =====================================================

    exam_filter = None

    if "unit" in query:
        exam_filter = "Unit Test"

    elif "mid" in query:
        exam_filter = "Midterm"

    elif "final" in query:
        exam_filter = "Final"

    # =====================================================
    # INTENT KEYWORDS
    # =====================================================

    marks_keywords = [
        "marks",
        "score",
        "result",
        "performance",
        "report",
        "grades",
        "academically",
        "perform",
        "exam",
    ]

    previous_keywords = [
        "previous",
        "old",
        "past",
        "earlier",
        "last exam",
    ]

    assignment_keywords = [
        "assignment",
        "homework",
        "pending",
        "project",
        "task",
        "work",
    ]

    timetable_keywords = [
        "timetable",
        "schedule",
        "class",
        "routine",
        "period",
        "timing",
    ]

    improvement_keywords = [
        "improvement",
        "weak",
        "focus area",
        "weak subject",
        "improve",
    ]

    # =====================================================
    # SUBJECT CLASS QUERY
    # =====================================================

    if (
        "class" in query
        and subject_filter
    ):

        response = "📅 Subject Schedule:\n"

        for s in students:

            cursor.execute(
                """
                SELECT day, time
                FROM timetable
                WHERE class=? AND subject=?
                """,
                (s["class"], subject_filter)
            )

            result = cursor.fetchone()

            if result:

                response += (
                    f"\n{s['name']}:\n"
                    f"• {subject_filter} class is on "
                    f"{result[0]} at {result[1]}\n"
                )

            else:

                response += (
                    f"\n{s['name']}:\n"
                    f"No class found\n"
                )

    # =====================================================
    # IMPROVEMENT AREA
    # =====================================================

    elif any(word in query for word in improvement_keywords):

        response = "📘 Improvement Analysis:\n"

        for s in students:

            cursor.execute(
                """
                SELECT subject, AVG(marks)
                FROM marks
                WHERE student_id=?
                GROUP BY subject
                """,
                (s["id"],)
            )

            data = cursor.fetchall()

            if data:

                weakest = min(data, key=lambda x: x[1])

                strongest = max(data, key=lambda x: x[1])

                response += f"\n{s['name']}:\n"

                response += (
                    f"• Strongest Subject: "
                    f"{strongest[0]} "
                    f"({round(strongest[1],1)}%)\n"
                )

                response += (
                    f"• Improvement Area: "
                    f"{weakest[0]} "
                    f"({round(weakest[1],1)}%)\n"
                )

                if weakest[1] >= 80:
                    response += (
                        "• Overall performance is very good.\n"
                    )

                else:
                    response += (
                        f"• More revision needed in "
                        f"{weakest[0]}.\n"
                    )

    # =====================================================
    # PREVIOUS EXAM RESULTS
    # =====================================================

    elif any(word in query for word in previous_keywords):

        response = "📚 Previous Exam Results:\n"

        for s in students:

            if subject_filter:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    AND subject=?
                    AND exam!='Final'
                    ORDER BY
                    CASE exam
                        WHEN 'Unit Test' THEN 1
                        WHEN 'Midterm' THEN 2
                    END
                    """,
                    (s["id"], subject_filter)
                )

            else:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    AND exam!='Final'
                    ORDER BY
                    CASE exam
                        WHEN 'Unit Test' THEN 1
                        WHEN 'Midterm' THEN 2
                    END
                    """,
                    (s["id"],)
                )

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                total = 0

                for m in marks:

                    response += (
                        f"• {m[0]} | "
                        f"{m[1]}: "
                        f"{m[2]} marks\n"
                    )

                    total += m[2]

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

    # =====================================================
    # MARKS / PERFORMANCE
    # =====================================================

    elif any(word in query for word in marks_keywords):

        response = "📊 Academic Performance:\n"

        for s in students:

            # ---------------- BOTH SUBJECT + EXAM ----------------

            if subject_filter and exam_filter:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    AND subject=?
                    AND exam=?
                    """,
                    (
                        s["id"],
                        subject_filter,
                        exam_filter
                    )
                )

            # ---------------- ONLY SUBJECT ----------------

            elif subject_filter:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    AND subject=?
                    ORDER BY
                    CASE exam
                        WHEN 'Unit Test' THEN 1
                        WHEN 'Midterm' THEN 2
                        WHEN 'Final' THEN 3
                    END
                    """,
                    (
                        s["id"],
                        subject_filter
                    )
                )

            # ---------------- ONLY EXAM ----------------

            elif exam_filter:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    AND exam=?
                    """,
                    (
                        s["id"],
                        exam_filter
                    )
                )

            # ---------------- NORMAL ----------------

            else:

                cursor.execute(
                    """
                    SELECT exam, subject, marks
                    FROM marks
                    WHERE student_id=?
                    ORDER BY
                    CASE exam
                        WHEN 'Unit Test' THEN 1
                        WHEN 'Midterm' THEN 2
                        WHEN 'Final' THEN 3
                    END
                    """,
                    (s["id"],)
                )

            marks = cursor.fetchall()

            if marks:

                response += f"\n{s['name']}:\n"

                total = 0

                all_marks = []

                for m in marks:

                    response += (
                        f"• {m[0]} | "
                        f"{m[1]}: "
                        f"{m[2]} marks\n"
                    )

                    total += m[2]

                    all_marks.append((m[2], m[1]))

                avg = round(total / len(marks), 1)

                response += (
                    f"\n⭐ Average Score: "
                    f"{avg}%\n"
                )

                # PERFORMANCE MESSAGE

                if avg >= 90:

                    response += (
                        "Outstanding academic performance.\n"
                    )

                elif avg >= 75:

                    response += (
                        "Good and consistent performance.\n"
                    )

                else:

                    response += (
                        "Needs improvement in academics.\n"
                    )

                highest = max(all_marks)

                lowest = min(all_marks)

                response += (
                    f"🏆 Strongest Subject: "
                    f"{highest[1]} "
                    f"({highest[0]} marks)\n"
                )

                subjects_used = list(
                    set([m[1] for m in all_marks])
                )

                if len(subjects_used) > 1:

                    response += (
                        f"📘 Focus Area: "
                        f"{lowest[1]} "
                        f"({lowest[0]} marks)"
                    )

                else:

                    if avg >= 90:

                        response += (
                            "📈 Excellent consistency across exams."
                        )

                    elif avg >= 75:

                        response += (
                            "📈 Steady improvement observed."
                        )

                    else:

                        response += (
                            "📈 More revision can improve scores."
                        )

                response += "\n"

            else:

                response += (
                    f"\n{s['name']}: "
                    f"No records found\n"
                )

    # =====================================================
    # ASSIGNMENTS
    # =====================================================

    elif any(word in query for word in assignment_keywords):

        response = "📝 Pending Assignments:\n"

        for s in students:

            if subject_filter:

                cursor.execute(
                    """
                    SELECT subject, assignment, due_date
                    FROM assignments
                    WHERE class=? AND subject=?
                    """,
                    (
                        s["class"],
                        subject_filter
                    )
                )

            else:

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

                for a in assignments:

                    response += (
                        f"• {a[0]}: "
                        f"{a[1]} "
                        f"(Due: {a[2]})\n"
                    )

                response += (
                    f"\n📌 Total Assignments: "
                    f"{len(assignments)}\n"
                )

            else:

                response += (
                    f"\n{s['name']}: "
                    f"No assignments found\n"
                )

    # =====================================================
    # TIMETABLE
    # =====================================================

    elif any(word in query for word in timetable_keywords):

        response = "📅 Class Schedule:\n"

        for s in students:

            if subject_filter:

                cursor.execute(
                    """
                    SELECT day, subject, time
                    FROM timetable
                    WHERE class=? AND subject=?
                    """,
                    (
                        s["class"],
                        subject_filter
                    )
                )

            else:

                cursor.execute(
                    """
                    SELECT day, subject, time
                    FROM timetable
                    WHERE class=?
                    """,
                    (s["class"],)
                )

            timetable = cursor.fetchall()

            if timetable:

                response += f"\n{s['name']}:\n"

                for t in timetable:

                    response += (
                        f"• {t[0]} | "
                        f"{t[1]} at {t[2]}\n"
                    )

            else:

                response += (
                    f"\n{s['name']}: "
                    f"No timetable found\n"
                )

    # =====================================================
    # DEFAULT
    # =====================================================

    else:

        response = (
            "I can help you with:\n"
            "• Marks & Exam Performance\n"
            "• Assignments & Homework\n"
            "• Timetable & Schedule\n\n"
            "Try asking:\n"
            "- Show my unit test marks\n"
            "- Show my midterm marks\n"
            "- Show my final exam result\n"
            "- What is my improvement area?\n"
            "- Show previous exam marks\n"
            "- When is my Maths class?"
        )

    conn.close()

    return response
