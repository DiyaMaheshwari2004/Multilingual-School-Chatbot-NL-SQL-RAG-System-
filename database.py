import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# ---------------- TABLES ----------------

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT,
    ref_id INTEGER
)
""")

# PARENTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

# STUDENTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class INTEGER,
    section TEXT,
    parent_id INTEGER
)
""")

# MARKS
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    exam TEXT,
    UNIQUE(student_id, subject, exam)
)
""")

# ASSIGNMENTS
cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    class INTEGER,
    subject TEXT,
    assignment TEXT,
    due_date TEXT,
    UNIQUE(class, subject, assignment)
)
""")

# TIMETABLE
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    class INTEGER,
    subject TEXT,
    time TEXT,
    day TEXT,
    UNIQUE(class, subject, time, day)
)
""")

# ---------------- PARENTS ----------------

cursor.execute("""
INSERT OR IGNORE INTO parents
VALUES (1, 'Rajesh Sharma')
""")

cursor.execute("""
INSERT OR IGNORE INTO parents
VALUES (2, 'Sunita Verma')
""")

# ---------------- STUDENTS ----------------

cursor.execute("""
INSERT OR IGNORE INTO students
VALUES (1, 'Rahul Sharma', 5, 'A', 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO students
VALUES (2, 'Riya Sharma', 3, 'B', 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO students
VALUES (3, 'Aman Verma', 8, 'A', 2)
""")

# ---------------- USERS ----------------

users = [
    ("rahul", "123", "student", 1),
    ("riya", "123", "student", 2),
    ("aman", "123", "student", 3),
    ("rajesh", "123", "parent", 1),
    ("sunita", "123", "parent", 2),
]

for user in users:
    cursor.execute("""
    INSERT OR IGNORE INTO users
    VALUES (?, ?, ?, ?)
    """, user)

# ---------------- MARKS ----------------

marks_data = [

    # Rahul
    (1, "Maths", 85, "Midterm"),
    (1, "Science", 78, "Midterm"),
    (1, "English", 82, "Midterm"),

    (1, "Maths", 91, "Final"),
    (1, "Science", 88, "Final"),
    (1, "English", 86, "Final"),

    (1, "Maths", 89, "Unit Test"),
    (1, "Science", 84, "Unit Test"),
    (1, "English", 80, "Unit Test"),

    # Riya
    (2, "Maths", 90, "Midterm"),
    (2, "English", 87, "Midterm"),
    (2, "EVS", 85, "Midterm"),

    (2, "Maths", 94, "Final"),
    (2, "English", 91, "Final"),
    (2, "EVS", 88, "Final"),

    (2, "Maths", 88, "Unit Test"),
    (2, "English", 84, "Unit Test"),
    (2, "EVS", 82, "Unit Test"),

    # Aman
    (3, "Science", 88, "Midterm"),
    (3, "Maths", 81, "Midterm"),
    (3, "English", 79, "Midterm"),

    (3, "Science", 92, "Final"),
    (3, "Maths", 86, "Final"),
    (3, "English", 83, "Final"),
]

for mark in marks_data:
    cursor.execute("""
    INSERT OR IGNORE INTO marks
    VALUES (?, ?, ?, ?)
    """, mark)

# ---------------- ASSIGNMENTS ----------------

assignments = [

    (5, "Maths", "Complete chapter 3", "2026-05-01"),
    (5, "Science", "Prepare solar system model", "2026-05-03"),
    (5, "English", "Grammar worksheet", "2026-05-04"),

    (3, "English", "Write essay", "2026-05-02"),
    (3, "Maths", "Practice tables", "2026-05-05"),
    (3, "EVS", "Draw water cycle", "2026-05-06"),

    (8, "Science", "Read chapter 5", "2026-05-03"),
    (8, "Maths", "Solve algebra worksheet", "2026-05-05"),
    (8, "English", "Debate preparation", "2026-05-07"),
]

for assignment in assignments:
    cursor.execute("""
    INSERT OR IGNORE INTO assignments
    VALUES (?, ?, ?, ?)
    """, assignment)

# ---------------- TIMETABLE ----------------

timetable = [

    (5, "Maths", "10:00 AM", "Monday"),
    (5, "Science", "11:00 AM", "Tuesday"),
    (5, "English", "9:30 AM", "Wednesday"),

    (3, "English", "9:00 AM", "Tuesday"),
    (3, "Maths", "10:30 AM", "Thursday"),
    (3, "EVS", "11:15 AM", "Friday"),

    (8, "Science", "11:00 AM", "Wednesday"),
    (8, "Maths", "1:00 PM", "Thursday"),
    (8, "English", "12:00 PM", "Friday"),
]

for entry in timetable:
    cursor.execute("""
    INSERT OR IGNORE INTO timetable
    VALUES (?, ?, ?, ?)
    """, entry)

# ---------------- FINALIZE ----------------

conn.commit()
conn.close()

print("Database ready with expanded academic records")
