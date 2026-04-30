import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# USERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT,
    ref_id INTEGER
)
""")

# Parents
cursor.execute("""
CREATE TABLE IF NOT EXISTS parents (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

# Students
cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class INTEGER,
    section TEXT,
    parent_id INTEGER
)
""")

# Marks
cursor.execute("""
CREATE TABLE IF NOT EXISTS marks (
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    exam TEXT
)
""")

# Assignments
cursor.execute("""
CREATE TABLE IF NOT EXISTS assignments (
    class INTEGER,
    subject TEXT,
    assignment TEXT,
    due_date TEXT
)
""")

# Timetable
cursor.execute("""
CREATE TABLE IF NOT EXISTS timetable (
    class INTEGER,
    subject TEXT,
    time TEXT,
    day TEXT
)
""")

# -------- REAL DATA --------

# Parents
cursor.execute("INSERT OR IGNORE INTO parents VALUES (1, 'Rajesh Sharma')")
cursor.execute("INSERT OR IGNORE INTO parents VALUES (2, 'Sunita Verma')")

# Students
cursor.execute("INSERT OR IGNORE INTO students VALUES (1, 'Rahul Sharma', 5, 'A', 1)")
cursor.execute("INSERT OR IGNORE INTO students VALUES (2, 'Riya Sharma', 3, 'B', 1)")
cursor.execute("INSERT OR IGNORE INTO students VALUES (3, 'Aman Verma', 8, 'A', 2)")

# Users
cursor.execute("INSERT OR IGNORE INTO users VALUES ('rahul', '123', 'student', 1)")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('riya', '123', 'student', 2)")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('aman', '123', 'student', 3)")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('rajesh', '123', 'parent', 1)")
cursor.execute("INSERT OR IGNORE INTO users VALUES ('sunita', '123', 'parent', 2)")

# Marks
cursor.execute("INSERT INTO marks VALUES (1, 'Maths', 85, 'Midterm')")
cursor.execute("INSERT INTO marks VALUES (1, 'Science', 78, 'Midterm')")
cursor.execute("INSERT INTO marks VALUES (2, 'Maths', 90, 'Midterm')")
cursor.execute("INSERT INTO marks VALUES (3, 'Science', 88, 'Midterm')")

# Assignments
cursor.execute("INSERT INTO assignments VALUES (5, 'Maths', 'Complete chapter 3', '2026-05-01')")
cursor.execute("INSERT INTO assignments VALUES (3, 'English', 'Write essay', '2026-05-02')")
cursor.execute("INSERT INTO assignments VALUES (8, 'Science', 'Read chapter 5', '2026-05-03')")

# Timetable
cursor.execute("INSERT INTO timetable VALUES (5, 'Maths', '10:00 AM', 'Monday')")
cursor.execute("INSERT INTO timetable VALUES (3, 'English', '9:00 AM', 'Tuesday')")
cursor.execute("INSERT INTO timetable VALUES (8, 'Science', '11:00 AM', 'Wednesday')")

conn.commit()
conn.close()

setup_db()

print("✅ Realistic database ready!")
