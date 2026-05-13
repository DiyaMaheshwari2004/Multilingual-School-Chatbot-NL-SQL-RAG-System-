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

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES ('rahul', '123', 'student', 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES ('riya', '123', 'student', 2)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES ('aman', '123', 'student', 3)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES ('rajesh', '123', 'parent', 1)
""")

cursor.execute("""
INSERT OR IGNORE INTO users
VALUES ('sunita', '123', 'parent', 2)
""")

# ---------------- MARKS ----------------

# Rahul Sharma

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Maths', 85, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Science', 78, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'English', 82, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Maths', 91, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Science', 88, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'English', 86, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Maths', 89, 'Unit Test')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'Science', 84, 'Unit Test')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (1, 'English', 80, 'Unit Test')
""")

# Riya Sharma

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'Maths', 90, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'English', 87, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'EVS', 85, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'Maths', 94, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'English', 91, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'EVS', 88, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'Maths', 88, 'Unit Test')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'English', 84, 'Unit Test')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (2, 'EVS', 82, 'Unit Test')
""")

# Aman Verma

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'Science', 88, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'Maths', 81, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'English', 79, 'Midterm')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'Science', 92, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'Maths', 86, 'Final')
""")

cursor.execute("""
INSERT OR IGNORE INTO marks
VALUES (3, 'English', 83, 'Final')
""")

# ---------------- ASSIGNMENTS ----------------

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (5, 'Maths', 'Complete chapter 3', '2026-05-01')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (5, 'Science', 'Prepare solar system model', '2026-05-03')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (5, 'English', 'Grammar worksheet', '2026-05-04')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (3, 'English', 'Write essay', '2026-05-02')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (3, 'Maths', 'Practice tables', '2026-05-05')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (3, 'EVS', 'Draw water cycle', '2026-05-06')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (8, 'Science', 'Read chapter 5', '2026-05-03')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (8, 'Maths', 'Solve algebra worksheet', '2026-05-05')
""")

cursor.execute("""
INSERT OR IGNORE INTO assignments
VALUES (8, 'English', 'Debate preparation', '2026-05-07')
""")

# ---------------- TIMETABLE ----------------

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (5, 'Maths', '10:00 AM', 'Monday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (5, 'Science', '11:00 AM', 'Tuesday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (5, 'English', '9:30 AM', 'Wednesday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (3, 'English', '9:00 AM', 'Tuesday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (3, 'Maths', '10:30 AM', 'Thursday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (3, 'EVS', '11:15 AM', 'Friday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (8, 'Science', '11:00 AM', 'Wednesday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (8, 'Maths', '1:00 PM', 'Thursday')
""")

cursor.execute("""
INSERT OR IGNORE INTO timetable
VALUES (8, 'English', '12:00 PM', 'Friday')
""")

# ---------------- FINALIZE ----------------

conn.commit()
conn.close()

print("Database ready with expanded academic data")
