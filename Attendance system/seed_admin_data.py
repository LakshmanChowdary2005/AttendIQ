import mysql.connector

def seed_admin_data():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )
    cur = con.cursor(dictionary=True)

    # Departments
    cur.execute("SELECT COUNT(*) as c FROM departments")
    if cur.fetchone()['c'] == 0:
        departments = [
            ("AIDS", "Artificial Intelligence & Data Science"),
            ("CSE", "Computer Science & Engineering"),
            ("ECE", "Electronics & Communication Engineering"),
            ("EEE", "Electrical & Electronics Engineering"),
            ("IT", "Information Technology")
        ]
        for code, name in departments:
            cur.execute("INSERT INTO departments (short_code, full_name) VALUES (%s, %s)", (code, name))
        print("Inserted default departments.")

    # Sections
    cur.execute("SELECT COUNT(*) as c FROM department_sections")
    if cur.fetchone()['c'] == 0:
        for code in ["AIDS", "CSE", "ECE", "EEE", "IT"]:
            for sec in ["Section A", "Section B", "Section C"]:
                cur.execute("INSERT INTO department_sections (dept_code, section_name) VALUES (%s, %s)", (code, sec))
        print("Inserted default sections.")

    # Email Audit Logs
    cur.execute("SELECT COUNT(*) as c FROM email_audit_logs")
    if cur.fetchone()['c'] == 0:
        sample_logs = [
            ('STU105', 'Arjun Das', 'arjun.d@student.edu', 33.33, 'Delivered (Sent)'),
            ('STU104', 'Sneha Patel', 'sneha.p@student.edu', 73.33, 'Delivered (Sent)'),
            ('STU103', 'Karthik Nair', 'karthik.n@student.edu', 33.33, 'Delivered (Sent)'),
            ('STU105', 'Arjun Das', 'arjun.d@student.edu', 33.33, 'Delivered (Sent)'),
            ('STU104', 'Sneha Patel', 'sneha.p@student.edu', 73.33, 'Delivered (Sent)'),
            ('STU103', 'Karthik Nair', 'karthik.n@student.edu', 33.33, 'Delivered (Sent)')
        ]
        for sid, sname, semail, spct, sstatus in sample_logs:
            cur.execute(
                "INSERT INTO email_audit_logs (student_id, student_name, email, attendance_pct, delivery_status) VALUES (%s, %s, %s, %s, %s)",
                (sid, sname, semail, spct, sstatus)
            )
        print("Inserted initial email audit logs.")

    con.commit()
    con.close()

if __name__ == "__main__":
    seed_admin_data()
