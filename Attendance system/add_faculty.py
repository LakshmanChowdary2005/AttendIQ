import sqlite3

con = sqlite3.connect("attendance.db")
cur = con.cursor()

faculty_data = [
    ("cloud", "123", "Ms. K. SRI VIJAYA", "Cloud Computing", 60),
    ("cns", "123", "Dr. Y. PADMA", "Cryptography & Network Security", 60),
    ("ml", "123", "Mrs. D. LEELA DHARANI", "Machine Learning", 60),
    ("devops", "123", "Mr. CH. PRANEETH", "DevOps", 60),
    ("spm", "123", "Dr. S. SAI KUMAR", "Software Project Management", 60),
    ("ewaste", "123", "Dr. B. SURYA PRASAD", "E-Waste Management", 30)
]

for f in faculty_data:
    cur.execute("""
        INSERT INTO faculty
        (username, password, faculty_name, subject, total_hours)
        VALUES (?, ?, ?, ?, ?)
    """, f)

con.commit()
con.close()

print("✅ Faculty Added Successfully")