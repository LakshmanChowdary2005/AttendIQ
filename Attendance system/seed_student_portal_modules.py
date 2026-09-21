import mysql.connector

def seed_modules():
    con = mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )
    cur = con.cursor(dictionary=True)

    # 1. Student Marks
    cur.execute("SELECT COUNT(*) as c FROM student_marks")
    if cur.fetchone()['c'] == 0:
        cur.execute("SELECT student_id FROM students LIMIT 10")
        sample_students = [r['student_id'] for r in cur.fetchall()]
        subjects = ["Data Structures", "Database Systems", "Web Engineering", "DevOps", "Cloud Computing"]
        for sid in sample_students:
            for subj in subjects:
                i1, i2, ass, qz = 24, 26, 18, 9
                tot = i1 + i2 + ass + qz
                grade = 'A+' if tot >= 85 else ('A' if tot >= 75 else 'B')
                cur.execute("""
                    INSERT INTO student_marks (student_id, subject, internal_1, internal_2, assignments_score, quiz_score, total_marks, grade)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                """, (sid, subj, i1, i2, ass, qz, tot, grade))
        print("Seeded student_marks.")

    # 2. Student Doubts
    cur.execute("SELECT COUNT(*) as c FROM student_doubts")
    if cur.fetchone()['c'] == 0:
        sample_doubts = [
            ("STU101", "Data Structures", "AVL Trees", "How does double rotation LR work during AVL tree insertion?", "Double rotation (LR) occurs when an insertion happens in the right subtree of the left child. First perform a left rotation on the left child, then a right rotation on the root."),
            ("STU101", "Database Systems", "B+ Trees", "Why are B+ Trees preferred over B Trees for database indexing?", "B+ Trees store data pointers only at the leaf nodes, which are linked sequentially, enabling fast range queries and higher fan-out per disk block."),
            ("STU101", "Cloud Computing", "Kubernetes Pods", "What is the difference between a Deployment and a StatefulSet?", "Deployments handle stateless pods that can be replaced freely; StatefulSets maintain persistent pod identities and stable storage across restarts.")
        ]
        for sid, subj, top, q, a in sample_doubts:
            cur.execute("""
                INSERT INTO student_doubts (student_id, subject, topic, question, answer, answered_by, created_at)
                VALUES (%s, %s, %s, %s, %s, 'Dr. Rajesh Kumar (Faculty)', '2026-09-16')
            """, (sid, subj, top, q, a))
        print("Seeded student_doubts.")

    # 3. Subject Diagnostics (Strengths & Weaknesses)
    cur.execute("SELECT COUNT(*) as c FROM subject_diagnostics")
    if cur.fetchone()['c'] == 0:
        sample_diag = [
            ("STU101", "Data Structures", '["Array Operations", "Binary Search", "Hash Tables", "Stack Push/Pop"]', '["Graph Dijkstra Algorithm", "Dynamic Programming Knapsack", "Segment Trees"]', '["Solve 5 LeetCode Medium problems on Graph Traversal", "Review Dynamic Programming Memoization patterns"]'),
            ("STU101", "Database Systems", '["SQL SELECT Queries", "Normalization (1NF-3NF)", "ER Diagramming"]', '["B+ Tree Indexing", "Transaction Serializability & Locking"]', '["Practice SQL Window Functions and Lock Concurrency exercises"]'),
            ("STU101", "DevOps & Cloud", '["Docker Containerization", "Git Workflow", "CI/CD Pipeline"]', '["Kubernetes Ingress Controllers", "Terraform HCL State"]', '["Hands-on lab: Deploy Nginx ingress on Minikube cluster"]')
        ]
        for sid, subj, str_j, wk_j, rec_j in sample_diag:
            cur.execute("""
                INSERT INTO subject_diagnostics (student_id, subject, strengths_json, weaknesses_json, recommendations_json)
                VALUES (%s, %s, %s, %s, %s)
            """, (sid, subj, str_j, wk_j, rec_j))
        print("Seeded subject_diagnostics.")

    # 4. Study Materials / Notes PDF
    cur.execute("SELECT COUNT(*) as c FROM study_materials")
    if cur.fetchone()['c'] == 0:
        materials = [
            ("Data Structures", "Unit 1", "Comprehensive Guide to Linear Data Structures", "Complete breakdown of Arrays, Linked Lists, Stacks, Queues with complexity analysis and C++ implementations.", "/student/notes/download/ds_u1", "DS_Unit1_LectureNotes.pdf"),
            ("Data Structures", "Unit 2", "Non-Linear Structures: Trees & Binary Search Trees", "Detailed notes on BST Operations, AVL Balancing, Heaps, and Priority Queue applications.", "/student/notes/download/ds_u2", "DS_Unit2_Trees.pdf"),
            ("Database Systems", "Unit 1", "Relational Database Design & Normalization", "Covers Functional Dependencies, 1NF, 2NF, 3NF, BCNF, and ER Model mappings.", "/student/notes/download/db_u1", "DBMS_Unit1_Normalization.pdf"),
            ("DevOps & Cloud", "Unit 1", "Containerization & Docker Fundamentals", "Architecture of Containers vs Virtual Machines, Dockerfile best practices, and Docker Compose.", "/student/notes/download/devops_u1", "DevOps_Unit1_Docker.pdf")
        ]
        for subj, u, title, summ, url, fname in materials:
            cur.execute("""
                INSERT INTO study_materials (subject, unit, title, summary, download_url, file_name)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (subj, u, title, summ, url, fname))
        print("Seeded study_materials.")

    # 5. Active Teaching Activities
    cur.execute("SELECT COUNT(*) as c FROM active_teaching_activities")
    if cur.fetchone()['c'] == 0:
        acts = [
            ("Data Structures", "Flipped Classroom & Peer Code Review", "AVL Tree Rebalancing Sprints", "Students analyze broken AVL tree rotation code snippet in pairs and execute live debug demo.", "Dr. Rajesh Kumar"),
            ("Database Systems", "Problem-Based Learning (PBL)", "E-Commerce Database Schema Challenge", "Teams design BCNF normalized schema for a real-time order processing system.", "Prof. Anitha Sharma"),
            ("DevOps & Cloud", "Gamified Coding Sprint & Hackathon", "Kubernetes Deployment Speed Run", "Students deploy a multi-container microservice manifest within a 30-minute timed challenge.", "Prof. V. Srinivas")
        ]
        for subj, mname, top, desc, fac in acts:
            cur.execute("""
                INSERT INTO active_teaching_activities (subject, methodology_name, topic, activity_desc, faculty_name)
                VALUES (%s, %s, %s, %s, %s)
            """, (subj, mname, top, desc, fac))
        print("Seeded active_teaching_activities.")

    # 6. JAM Topics
    cur.execute("SELECT COUNT(*) as c FROM jam_topics")
    if cur.fetchone()['c'] == 0:
        jam_items = [
            ("Cloud Computing vs Edge Computing", "Cloud Computing", 60, "Key points: Latency, Bandwidth, Processing Power, IoT Devices"),
            ("Importance of Data Structures in AI Systems", "Data Structures", 60, "Key points: Search Trees, Graph Neural Networks, Memory Efficiency"),
            ("Microservices vs Monolithic Architecture", "Web Engineering", 60, "Key points: Scalability, Fault Isolation, Deployment Complexity")
        ]
        for t, subj, dur, h in jam_items:
            cur.execute("""
                INSERT INTO jam_topics (title, subject, duration_sec, hints)
                VALUES (%s, %s, %s, %s)
            """, (t, subj, dur, h))
        print("Seeded jam_topics.")

    con.commit()
    con.close()

if __name__ == "__main__":
    seed_modules()
