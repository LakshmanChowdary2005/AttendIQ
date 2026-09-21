import mysql.connector

def remove_sample_students():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )
    cur = con.cursor()

    student_ids = ('STU101', 'STU102', 'STU103', 'STU104', 'STU105')
    cur.execute("DELETE FROM attendance WHERE student_id IN (%s, %s, %s, %s, %s)", student_ids)
    cur.execute("DELETE FROM email_audit_logs WHERE student_id IN (%s, %s, %s, %s, %s)", student_ids)
    cur.execute("DELETE FROM students WHERE student_id IN (%s, %s, %s, %s, %s)", student_ids)

    con.commit()
    con.close()
    print("Sample STU101-STU105 students removed.")

if __name__ == "__main__":
    remove_sample_students()
