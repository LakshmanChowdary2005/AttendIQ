import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )

def setup_admin_tables():
    con = get_db()
    cur = con.cursor(dictionary=True)
    print("🚀 Initializing Admin Portal Database Extension in attendance_db...")

    # 1. DEPARTMENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS departments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        short_code VARCHAR(20) UNIQUE NOT NULL,
        full_name VARCHAR(150) NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 2. DEPARTMENT SECTIONS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS department_sections (
        id INT AUTO_INCREMENT PRIMARY KEY,
        dept_code VARCHAR(20) NOT NULL,
        section_name VARCHAR(50) NOT NULL,
        INDEX (dept_code)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 3. ANNOUNCEMENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS announcements (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        severity VARCHAR(50) DEFAULT 'Info Notice',
        message TEXT NOT NULL,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 4. EMAIL LOGS TABLE (audit logs)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS email_audit_logs (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50) NOT NULL,
        student_name VARCHAR(150),
        email VARCHAR(150),
        attendance_pct DECIMAL(5, 2),
        sent_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        delivery_status VARCHAR(50) DEFAULT 'Delivered (Sent)'
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    con.commit()

    # Seed initial departments if empty
    cur.execute("SELECT COUNT(*) as cnt FROM departments")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding academic departments and sections...")
        depts = [
            ("IT", "Information Technology"),
            ("CSE", "Computer Science & Engineering"),
            ("AIDS", "Artificial Intelligence & Data Science"),
            ("ECE", "Electronics & Communication Engineering"),
            ("EEE", "Electrical & Electronics Engineering")
        ]
        for d in depts:
            cur.execute("INSERT INTO departments (short_code, full_name) VALUES (%s, %s)", d)
            for sec in ["Section A", "Section B", "Section C"]:
                cur.execute("INSERT INTO department_sections (dept_code, section_name) VALUES (%s, %s)", (d[0], sec))
        con.commit()

    # Seed sample announcements if empty
    cur.execute("SELECT COUNT(*) as cnt FROM announcements")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding sample announcement broadcast...")
        cur.execute("""
            INSERT INTO announcements (title, severity, message)
            VALUES ('Mid-Semester Attendance Threshold Warning', 'Info Notice', 'All students are reminded to maintain at least 75.0% cumulative attendance to be eligible for mid-semester examinations.')
        """)
        con.commit()

    # Seed sample email audit logs if empty
    cur.execute("SELECT COUNT(*) as cnt FROM email_audit_logs")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding sample email audit logs...")
        logs = [
            ("23501A1205", "Arjun Das", "arjun.d@student.edu", 33.33),
            ("23501A1204", "Sneha Patel", "sneha.p@student.edu", 73.33),
            ("23501A1203", "Karthik Nair", "karthik.n@student.edu", 33.33)
        ]
        for l in logs:
            cur.execute("""
                INSERT INTO email_audit_logs (student_id, student_name, email, attendance_pct)
                VALUES (%s, %s, %s, %s)
            """, l)
        con.commit()

    con.close()
    print("🎉 Admin Portal database setup complete!")

if __name__ == "__main__":
    setup_admin_tables()
