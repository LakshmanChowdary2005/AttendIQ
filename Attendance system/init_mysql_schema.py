import mysql.connector

def init_mysql_tables():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )
    cur = con.cursor()

    # 1. Students Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS students (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(150) NOT NULL,
        email VARCHAR(150),
        password VARCHAR(100) DEFAULT '123456',
        department VARCHAR(100) DEFAULT 'Information Technology',
        section VARCHAR(50) DEFAULT 'Section A'
    )
    """)

    # 2. Faculty Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS faculty (
        id INT AUTO_INCREMENT PRIMARY KEY,
        faculty_code VARCHAR(50) UNIQUE NOT NULL,
        name VARCHAR(150) NOT NULL,
        password VARCHAR(100) NOT NULL DEFAULT '500452',
        subject VARCHAR(150) NOT NULL DEFAULT 'Data Structures',
        department VARCHAR(100) DEFAULT 'Information Technology',
        section VARCHAR(50) DEFAULT 'Section A',
        email VARCHAR(150),
        total_classes INT DEFAULT 60
    )
    """)

    # 3. Admin Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS admin (
        admin_id VARCHAR(50) PRIMARY KEY,
        name VARCHAR(150) NOT NULL,
        password VARCHAR(100) NOT NULL,
        email VARCHAR(150)
    )
    """)

    # Seed Admin if not present (Password 500452)
    cur.execute("SELECT COUNT(*) FROM admin WHERE admin_id='admin'")
    if cur.fetchone()[0] == 0:
        cur.execute("INSERT INTO admin (admin_id, name, password, email) VALUES ('admin', 'System Administrator', '500452', 'admin@attend-iq.ai')")

    # 4. Attendance Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS attendance (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50),
        faculty_code VARCHAR(50),
        subject VARCHAR(150),
        date VARCHAR(20),
        hour VARCHAR(10) DEFAULT '1',
        status VARCHAR(20)
    )
    """)

    # 5. Homework Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS homework (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        description TEXT,
        due_date VARCHAR(20),
        created_by VARCHAR(150),
        created_at VARCHAR(30)
    )
    """)

    # 6. Homework Submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS homework_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        homework_id INT,
        student_id VARCHAR(50),
        submission_text TEXT,
        status VARCHAR(50) DEFAULT 'Completed',
        submitted_at VARCHAR(30)
    )
    """)

    # 7. Assignments Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        department VARCHAR(100) DEFAULT 'IT',
        description TEXT,
        due_date VARCHAR(20),
        points INT DEFAULT 50,
        created_by VARCHAR(150),
        created_at VARCHAR(30)
    )
    """)

    # 8. Assignment Submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS assignment_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        assignment_id INT,
        student_id VARCHAR(50),
        submission_text TEXT,
        file_link VARCHAR(255),
        status VARCHAR(50) DEFAULT 'Submitted',
        submitted_at VARCHAR(30)
    )
    """)

    # 9. AI Assignments Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS ai_assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        topic VARCHAR(150) NOT NULL,
        difficulty VARCHAR(50) NOT NULL,
        content TEXT NOT NULL,
        created_by VARCHAR(150),
        created_at VARCHAR(30)
    )
    """)

    # 10. Notifications Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS notifications (
        id INT AUTO_INCREMENT PRIMARY KEY,
        recipient_id VARCHAR(50),
        recipient_role VARCHAR(50),
        title VARCHAR(255) NOT NULL,
        message TEXT NOT NULL,
        type VARCHAR(50) DEFAULT 'info',
        is_read INT DEFAULT 0,
        created_at VARCHAR(30)
    )
    """)

    # 11. Risk Predictions Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS risk_predictions (
        student_id VARCHAR(50) PRIMARY KEY,
        current_pct DECIMAL(5,2),
        predicted_pct DECIMAL(5,2),
        risk_level VARCHAR(50),
        ai_recommendation TEXT,
        updated_at VARCHAR(30)
    )
    """)

    # 12. System Settings Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS system_settings (
        setting_key VARCHAR(100) PRIMARY KEY,
        setting_value TEXT
    )
    """)
    cur.execute("INSERT IGNORE INTO system_settings (setting_key, setting_value) VALUES ('ALERT_EMAIL_SENDER', 'lakshmanchowdary2005@gmail.com')")
    cur.execute("INSERT IGNORE INTO system_settings (setting_key, setting_value) VALUES ('ALERT_EMAIL_PASSWORD', 'ytfjjwkrjjzyrrpt')")

    # 13. Smart Education: Tutor Sessions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_tutor_sessions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50) NOT NULL,
        subject VARCHAR(150) DEFAULT 'General Science & Engineering',
        topic VARCHAR(150),
        history_json TEXT,
        created_at VARCHAR(30)
    )
    """)

    # 14. Smart Education: Flashcards
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_study_flashcards (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        topic VARCHAR(150) NOT NULL,
        cards_json TEXT NOT NULL,
        created_at VARCHAR(30)
    )
    """)

    # 15. Smart Education: Assessments
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_assessments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        title VARCHAR(255) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        difficulty VARCHAR(50) DEFAULT 'Intermediate',
        questions_json TEXT NOT NULL,
        created_by VARCHAR(150),
        created_at VARCHAR(30)
    )
    """)

    # 16. Smart Education: Assessment Submissions
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_assessment_submissions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        assessment_id INT NOT NULL,
        student_id VARCHAR(50) NOT NULL,
        score DECIMAL(5,2) DEFAULT 0.0,
        max_score DECIMAL(5,2) DEFAULT 100.0,
        feedback_json TEXT,
        submitted_at VARCHAR(30)
    )
    """)

    # 17. Smart Education: Skill Roadmaps
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_skill_roadmaps (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(50) UNIQUE NOT NULL,
        target_role VARCHAR(150) NOT NULL,
        skills_json TEXT NOT NULL,
        completed_pct DECIMAL(5,2) DEFAULT 0.0,
        updated_at VARCHAR(30)
    )
    """)

    # 18. Smart Education: Classroom Polls
    cur.execute("""
    CREATE TABLE IF NOT EXISTS smart_classroom_polls (
        id INT AUTO_INCREMENT PRIMARY KEY,
        faculty_code VARCHAR(50) NOT NULL,
        subject VARCHAR(150) NOT NULL,
        question TEXT NOT NULL,
        options_json TEXT NOT NULL,
        results_json TEXT,
        status VARCHAR(50) DEFAULT 'Active',
        created_at VARCHAR(30)
    )
    """)

    con.commit()

    cur.execute("SELECT COUNT(*) FROM students")
    st_cnt = cur.fetchone()[0]
    cur.execute("SELECT COUNT(*) FROM faculty")
    fa_cnt = cur.fetchone()[0]
    print(f"MySQL tables verified! Students count: {st_cnt}, Faculty count: {fa_cnt}")

    con.close()

if __name__ == "__main__":
    init_mysql_tables()
