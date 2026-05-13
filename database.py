import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# ---------------- TABLES ----------------

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT,
    ref_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class INTEGER,
    section TEXT,
    parent_id INTEGER
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    exam TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    class INTEGER,
    subject TEXT,
    assignment TEXT,
    due_date TEXT
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    class INTEGER,
    subject TEXT,
    time TEXT,
    day TEXT
)
""")

# ---------------- CLEAR OLD DATA ----------------

cursor.execute("DELETE FROM users")
cursor.execute("DELETE FROM parents")
cursor.execute("DELETE FROM students")
cursor.execute("DELETE FROM marks")
cursor.execute("DELETE FROM assignments")
cursor.execute("DELETE FROM timetable")

# ---------------- PARENTS ----------------

cursor.execute(
    "INSERT INTO parents VALUES (1, 'Rajesh Sharma')"
)

# ---------------- STUDENTS ----------------

cursor.execute(
    "INSERT INTO students VALUES (1, 'Rahul Sharma', 5, 'A', 1)"
)

cursor.execute(
    "INSERT INTO students VALUES (2, 'Riya Sharma', 3, 'B', 1)"
)

# ---------------- USERS ----------------

cursor.execute(
    "INSERT INTO users VALUES ('rahul', '123', 'student', 1)"
)

cursor.execute(
    "INSERT INTO users VALUES ('riya', '123', 'student', 2)"
)

cursor.execute(
    "INSERT INTO users VALUES ('rajesh', '123', 'parent', 1)"
)

# ---------------- MARKS ----------------

rahul_marks = [

    (1, "Maths", 89, "Unit Test"),
    (1, "Science", 84, "Unit Test"),
    (1, "English", 80, "Unit Test"),

    (1, "Maths", 85, "Midterm"),
    (1, "Science", 78, "Midterm"),
    (1, "English", 82, "Midterm"),

    (1, "Maths", 91, "Final"),
    (1, "Science", 88, "Final"),
    (1, "English", 86, "Final"),
]

riya_marks = [

    (2, "Maths", 88, "Unit Test"),
    (2, "English", 84, "Unit Test"),
    (2, "EVS", 82, "Unit Test"),

    (2, "Maths", 90, "Midterm"),
    (2, "English", 87, "Midterm"),
    (2, "EVS", 85, "Midterm"),

    (2, "Maths", 94, "Final"),
    (2, "English", 91, "Final"),
    (2, "EVS", 88, "Final"),
]

cursor.executemany(
    "INSERT INTO marks VALUES (?, ?, ?, ?)",
    rahul_marks
)

cursor.executemany(
    "INSERT INTO marks VALUES (?, ?, ?, ?)",
    riya_marks
)

# ---------------- ASSIGNMENTS ----------------

assignments = [

    (5, "Maths", "Complete Chapter 3", "2026-05-12"),
    (5, "Science", "Prepare Solar System Model", "2026-05-14"),
    (5, "English", "Write Essay on Nature", "2026-05-15"),

    (3, "Maths", "Practice Tables", "2026-05-10"),
    (3, "English", "Write Essay", "2026-05-11"),
    (3, "EVS", "Draw Water Cycle", "2026-05-13"),
]

cursor.executemany(
    "INSERT INTO assignments VALUES (?, ?, ?, ?)",
    assignments
)

# ---------------- TIMETABLE ----------------

timetable = [

    (5, "Maths", "10:00 AM", "Monday"),
    (5, "Science", "11:00 AM", "Tuesday"),
    (5, "English", "9:30 AM", "Wednesday"),

    (3, "Maths", "10:30 AM", "Thursday"),
    (3, "English", "9:00 AM", "Tuesday"),
    (3, "EVS", "11:15 AM", "Friday"),
]

cursor.executemany(
    "INSERT INTO timetable VALUES (?, ?, ?, ?)",
    timetable
)

conn.commit()
conn.close()

print("✅ Database Ready")
