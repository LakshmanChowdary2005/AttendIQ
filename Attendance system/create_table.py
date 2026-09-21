import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "attendance.db")

con = sqlite3.connect(DB_PATH)
cur = con.cursor()

# STUDENTS TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    roll TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL
)
""")

# FACULTY TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS faculty (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    faculty_name TEXT NOT NULL
)
""")

# FACULTY SUBJECT + HOURS
cur.execute("""
CREATE TABLE IF NOT EXISTS faculty_hours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    faculty_id INTEGER,
    subject TEXT,
    total_hours INTEGER,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
)
""")

# ATTENDANCE TABLE
cur.execute("""
CREATE TABLE IF NOT EXISTS attendance (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    student_id INTEGER,
    faculty_id INTEGER,
    subject TEXT,
    date TEXT,
    status TEXT,
    FOREIGN KEY (student_id) REFERENCES students(id),
    FOREIGN KEY (faculty_id) REFERENCES faculty(id)
)
""")

con.commit()
con.close()

print("✅ Database and ALL tables created successfully")
