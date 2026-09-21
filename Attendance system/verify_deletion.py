import mysql.connector

def verify():
    con = mysql.connector.connect(host='localhost', user='root', password='lakshman8222', database='attendance_db')
    cur = con.cursor(dictionary=True)

    ids = ('STU101', 'STU102', 'STU103', 'STU104', 'STU105')
    cur.execute("SELECT COUNT(*) as c FROM students WHERE student_id IN (%s, %s, %s, %s, %s)", ids)
    c1 = cur.fetchone()['c']

    cur.execute("SELECT COUNT(*) as c FROM attendance WHERE student_id IN (%s, %s, %s, %s, %s)", ids)
    c2 = cur.fetchone()['c']

    print(f"Students table count for STU101-105: {c1}")
    print(f"Attendance table count for STU101-105: {c2}")

    con.close()

if __name__ == "__main__":
    verify()
