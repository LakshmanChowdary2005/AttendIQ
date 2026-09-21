import mysql.connector

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )

def setup_faculty_tables():
    con = get_db()
    cur = con.cursor(dictionary=True)
    print("🚀 Extending database for Faculty Dashboard (Assignments, Homework & Reports)...")

    # 1. COURSE ASSIGNMENTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS course_assignments (
        id INT AUTO_INCREMENT PRIMARY KEY,
        faculty_id VARCHAR(50),
        department VARCHAR(100) DEFAULT 'IT - Information Technology',
        subject VARCHAR(100) NOT NULL,
        title VARCHAR(255) NOT NULL,
        due_date DATE,
        max_points INT DEFAULT 50,
        instructions TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 2. DAILY HOMEWORK TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS daily_homework (
        id INT AUTO_INCREMENT PRIMARY KEY,
        faculty_id VARCHAR(50),
        subject VARCHAR(100) NOT NULL,
        title VARCHAR(255) NOT NULL,
        due_date DATE,
        instructions TEXT,
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    con.commit()

    # SEED COURSE ASSIGNMENTS IF EMPTY
    cur.execute("SELECT COUNT(*) as cnt FROM course_assignments")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding active course assignments...")
        assignments = [
            ("devops", "IT - Information Technology", "Cloud Microservices & Kubernetes Architecture", "2026-09-28", 75, "Design a Kubernetes deployment manifest for a resilient multi-tier microservice with ingress routing and autoscaling policies."),
            ("ml", "IT - Information Technology", "Deep Learning Transformer Architecture Challenge", "2026-09-28", 100, "Build and train a multi-layer transformer model for text sentiment classification using PyTorch / TensorFlow."),
            ("cns", "IT - Information Technology", "Zero-Trust Network Protocol & RSA Cryptanalysis", "2026-09-25", 50, "Implement RSA key generation and execute a simulated mathematical factorization attack on small primes."),
            ("cloud", "IT - Information Technology", "AWS Multi-Region Infrastructure as Code with Terraform", "2026-09-22", 100, "Write Terraform HCL scripts provisioning VPC peering, S3 buckets, and EC2 auto-scaling groups across dual AWS regions.")
        ]
        for a in assignments:
            cur.execute("""
                INSERT INTO course_assignments
                (faculty_id, department, title, due_date, max_points, instructions, subject)
                VALUES (%s, %s, %s, %s, %s, %s, 'DevOps')
            """, a)
        con.commit()

    # SEED DAILY HOMEWORK IF EMPTY
    cur.execute("SELECT COUNT(*) as cnt FROM daily_homework")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding active daily homework tasks...")
        homeworks = [
            ("devops", "DevOps", "Daily Concept Check: Dockerfile Best Practices", "2026-09-18", "Write a multi-stage Dockerfile for a Node.js application minimizing final image size under 50MB."),
            ("ml", "Machine Learning", "Daily Concept Check: Gradient Descent Optimization", "2026-09-18", "Derive the weight update equation for SGD with Momentum and Adam optimizer.")
        ]
        for h in homeworks:
            cur.execute("""
                INSERT INTO daily_homework
                (faculty_id, subject, title, due_date, instructions)
                VALUES (%s, %s, %s, %s, %s)
            """, h)
        con.commit()

    con.close()
    print("✅ Faculty Dashboard database extension complete!")

if __name__ == "__main__":
    setup_faculty_tables()
