import mysql.connector

def clean_test_students():
    try:
        con = mysql.connector.connect(
            host="localhost",
            user="root",
            password="lakshman8222",
            database="attendance_db"
        )
        cur = con.cursor()
        
        target_ids = ('STU101', 'STU999', 'STU102', 'STU103', 'STU104', 'STU105')
        format_strings = ','.join(['%s'] * len(target_ids))
        
        tables = [
            'students',
            'attendance',
            'student_marks',
            'student_doubts',
            'subject_diagnostics',
            'risk_predictions',
            'homework_submissions',
            'assignment_submissions'
        ]
        
        for t in tables:
            try:
                cur.execute(f"DELETE FROM {t} WHERE UPPER(student_id) IN ({format_strings})", target_ids)
                print(f"Cleaned {cur.rowcount} rows from table '{t}'")
            except Exception as e:
                print(f"Table '{t}' cleanup note: {e}")

        # Notifications table uses recipient_id
        try:
            cur.execute(f"DELETE FROM notifications WHERE UPPER(recipient_id) IN ({format_strings})", target_ids)
            print(f"Cleaned {cur.rowcount} rows from table 'notifications'")
        except Exception as e:
            print(f"Notifications cleanup note: {e}")
                
        con.commit()
        con.close()
        print("Database cleanup completed successfully!")
    except Exception as e:
        print("Database connection/cleanup error:", e)

if __name__ == "__main__":
    clean_test_students()
