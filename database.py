import sqlite3

conn = sqlite3.connect("school.db")
cursor = conn.cursor()

# ==================================================
# DROP OLD TABLES
# ==================================================

cursor.execute("DROP TABLE IF EXISTS users")
cursor.execute("DROP TABLE IF EXISTS parents")
cursor.execute("DROP TABLE IF EXISTS students")
cursor.execute("DROP TABLE IF EXISTS marks")
cursor.execute("DROP TABLE IF EXISTS assignments")
cursor.execute("DROP TABLE IF EXISTS timetable")

# ==================================================
# CREATE TABLES
# ==================================================

# USERS
cursor.execute("""
CREATE TABLE users (
    username TEXT PRIMARY KEY,
    password TEXT,
    role TEXT,
    ref_id INTEGER
)
""")

# PARENTS
cursor.execute("""
CREATE TABLE parents (
    id INTEGER PRIMARY KEY,
    name TEXT
)
""")

# STUDENTS
cursor.execute("""
CREATE TABLE students (
    id INTEGER PRIMARY KEY,
    name TEXT,
    class INTEGER,
    section TEXT,
    parent_id INTEGER
)
""")

# MARKS
cursor.execute("""
CREATE TABLE marks (
    student_id INTEGER,
    subject TEXT,
    marks INTEGER,
    exam TEXT
)
""")

# ASSIGNMENTS
cursor.execute("""
CREATE TABLE assignments (
    class INTEGER,
    subject TEXT,
    assignment TEXT,
    due_date TEXT
)
""")

# TIMETABLE
cursor.execute("""
CREATE TABLE timetable (
    class INTEGER,
    subject TEXT,
    time TEXT,
    day TEXT
)
""")

# ==================================================
# PARENTS
# ==================================================

cursor.execute("""
INSERT INTO parents VALUES
(1, 'Rajesh Sharma')
""")

cursor.execute("""
INSERT INTO parents VALUES
(2, 'Sunita Verma')
""")

# ==================================================
# STUDENTS
# ==================================================

cursor.execute("""
INSERT INTO students VALUES
(1, 'Rahul Sharma', 5, 'A', 1)
""")

cursor.execute("""
INSERT INTO students VALUES
(2, 'Riya Sharma', 3, 'B', 1)
""")

cursor.execute("""
INSERT INTO students VALUES
(3, 'Aman Verma', 8, 'A', 2)
""")

# ==================================================
# USERS
# ==================================================

users = [
    ('rahul', '123', 'student', 1),
    ('riya', '123', 'student', 2),
    ('aman', '123', 'student', 3),
    ('rajesh', '123', 'parent', 1),
    ('sunita', '123', 'parent', 2),
]

cursor.executemany(
    "INSERT INTO users VALUES (?, ?, ?, ?)",
    users
)

# ==================================================
# MARKS DATA
# ==================================================

marks_data = [

    # RAHUL
    (1, 'Maths', 89, 'Unit Test'),
    (1, 'Science', 84, 'Unit Test'),
    (1, 'English', 80, 'Unit Test'),

    (1, 'Maths', 85, 'Midterm'),
    (1, 'Science', 78, 'Midterm'),
    (1, 'English', 82, 'Midterm'),

    (1, 'Maths', 91, 'Final'),
    (1, 'Science', 88, 'Final'),
    (1, 'English', 86, 'Final'),

    # RIYA
    (2, 'Maths', 88, 'Unit Test'),
    (2, 'English', 84, 'Unit Test'),
    (2, 'EVS', 82, 'Unit Test'),

    (2, 'Maths', 90, 'Midterm'),
    (2, 'English', 87, 'Midterm'),
    (2, 'EVS', 85, 'Midterm'),

    (2, 'Maths', 94, 'Final'),
    (2, 'English', 91, 'Final'),
    (2, 'EVS', 88, 'Final'),

    # AMAN
    (3, 'Maths', 75, 'Unit Test'),
    (3, 'Science', 82, 'Unit Test'),
    (3, 'English', 78, 'Unit Test'),

    (3, 'Maths', 79, 'Midterm'),
    (3, 'Science', 84, 'Midterm'),
    (3, 'English', 81, 'Midterm'),

    (3, 'Maths', 85, 'Final'),
    (3, 'Science', 89, 'Final'),
    (3, 'English', 86, 'Final'),
]

cursor.executemany(
    "INSERT INTO marks VALUES (?, ?, ?, ?)",
    marks_data
)

# ==================================================
# ASSIGNMENTS
# ==================================================

assignment_data = [

    # CLASS 5
    (5, 'Maths', 'Complete chapter 3', '2026-05-01'),
    (5, 'Science', 'Prepare solar system chart', '2026-05-04'),
    (5, 'English', 'Write paragraph on nature', '2026-05-07'),

    # CLASS 3
    (3, 'English', 'Write essay', '2026-05-02'),
    (3, 'Maths', 'Practice tables', '2026-05-05'),
    (3, 'EVS', 'Draw water cycle', '2026-05-06'),

    # CLASS 8
    (8, 'Science', 'Read chapter 5', '2026-05-03'),
    (8, 'Maths', 'Solve algebra worksheet', '2026-05-08'),
    (8, 'English', 'Grammar exercises', '2026-05-10'),
]

cursor.executemany(
    "INSERT INTO assignments VALUES (?, ?, ?, ?)",
    assignment_data
)

# ==================================================
# TIMETABLE
# ==================================================

timetable_data = [

    # CLASS 5
    (5, 'Maths', '10:00 AM', 'Monday'),
    (5, 'Science', '11:00 AM', 'Wednesday'),
    (5, 'English', '9:30 AM', 'Friday'),

    # CLASS 3
    (3, 'English', '9:00 AM', 'Tuesday'),
    (3, 'Maths', '10:30 AM', 'Thursday'),
    (3, 'EVS', '11:15 AM', 'Friday'),

    # CLASS 8
    (8, 'Science', '11:00 AM', 'Wednesday'),
    (8, 'Maths', '9:45 AM', 'Monday'),
    (8, 'English', '1:00 PM', 'Thursday'),
]

cursor.executemany(
    "INSERT INTO timetable VALUES (?, ?, ?, ?)",
    timetable_data
)

# ==================================================
# SAVE
# ==================================================

conn.commit()
conn.close()

print("✅ Database Ready Successfully")
