import sqlite3

con = sqlite3.connect("attendance.db")
cur = con.cursor()

# STUDENTS
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll TEXT UNIQUE,
    name TEXT
)
""")

# FACULTY
cur.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT,
    faculty_name TEXT,
    subject TEXT,
    total_hours INTEGER
)
""")

# ATTENDANCE (WITH faculty_id COLUMN)
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    subject TEXT,
    date TEXT,
    hour INTEGER,
    status TEXT
)
""")

con.commit()
con.close()

print("✅ Fresh Database Created Successfully")
