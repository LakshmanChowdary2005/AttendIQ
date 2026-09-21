import mysql.connector
import datetime
import random

def get_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="lakshman8222",
        database="attendance_db"
    )

def setup_database():
    con = get_db()
    cur = con.cursor(dictionary=True)
    print("🚀 Initializing Student Portal Database Extension in attendance_db...")

    # 1. STUDENT MARKS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_marks (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(20) NOT NULL,
        subject VARCHAR(100) NOT NULL,
        exam_type VARCHAR(50) NOT NULL,
        marks_obtained DECIMAL(5, 2) NOT NULL,
        max_marks DECIMAL(5, 2) NOT NULL,
        grade VARCHAR(5) NOT NULL,
        semester VARCHAR(10) DEFAULT 'Sem-4',
        exam_date DATE,
        INDEX (student_id),
        INDEX (subject)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 2. STUDENT DOUBTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS student_doubts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(20) NOT NULL,
        student_name VARCHAR(150),
        subject VARCHAR(100) NOT NULL,
        topic VARCHAR(150),
        question TEXT NOT NULL,
        answer TEXT,
        status VARCHAR(20) DEFAULT 'Answered',
        answered_by VARCHAR(100) DEFAULT 'AI Academic Assistant & Faculty',
        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX (student_id),
        INDEX (subject)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 3. QUIZ QUESTIONS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_questions (
        id INT AUTO_INCREMENT PRIMARY KEY,
        subject VARCHAR(100) NOT NULL,
        topic VARCHAR(100) NOT NULL,
        difficulty VARCHAR(20) DEFAULT 'Medium',
        question TEXT NOT NULL,
        option_a VARCHAR(255) NOT NULL,
        option_b VARCHAR(255) NOT NULL,
        option_c VARCHAR(255) NOT NULL,
        option_d VARCHAR(255) NOT NULL,
        correct_option CHAR(1) NOT NULL,
        explanation TEXT,
        INDEX (subject)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 4. QUIZ ATTEMPTS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS quiz_attempts (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(20) NOT NULL,
        subject VARCHAR(100) NOT NULL,
        score INT NOT NULL,
        total_questions INT NOT NULL,
        percentage DECIMAL(5, 2) NOT NULL,
        time_taken_seconds INT DEFAULT 60,
        attempted_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        INDEX (student_id)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 5. JAM (JUST-A-MINUTE) TOPICS TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS jam_topics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        category VARCHAR(50) NOT NULL,
        title VARCHAR(200) NOT NULL,
        description TEXT,
        suggested_points TEXT,
        vocabulary_hints VARCHAR(255),
        target_skills VARCHAR(150)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 6. ACTIVE TEACHING METHODOLOGY ACTIVITIES TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS active_teaching_activities (
        id INT AUTO_INCREMENT PRIMARY KEY,
        subject VARCHAR(100) NOT NULL,
        methodology_type VARCHAR(150) NOT NULL,
        title VARCHAR(200) NOT NULL,
        scenario_description TEXT NOT NULL,
        student_task TEXT NOT NULL,
        deliverable VARCHAR(255),
        learning_outcome TEXT
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    cur.execute("ALTER TABLE active_teaching_activities MODIFY COLUMN methodology_type VARCHAR(150);")
    cur.execute("ALTER TABLE active_teaching_activities MODIFY COLUMN deliverable VARCHAR(255);")


    # 7. STUDY MATERIALS & NOTES TABLE
    cur.execute("""
    CREATE TABLE IF NOT EXISTS study_materials (
        id INT AUTO_INCREMENT PRIMARY KEY,
        subject VARCHAR(100) NOT NULL,
        unit VARCHAR(20) NOT NULL,
        title VARCHAR(200) NOT NULL,
        doc_type VARCHAR(30) DEFAULT 'PDF Notes',
        file_name VARCHAR(150),
        file_size VARCHAR(20) DEFAULT '1.8 MB',
        summary TEXT,
        content_preview LONGTEXT,
        download_url VARCHAR(255),
        INDEX (subject)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    # 8. SUBJECT DIAGNOSTICS (STRENGTHS & WEAKNESSES)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS subject_diagnostics (
        id INT AUTO_INCREMENT PRIMARY KEY,
        student_id VARCHAR(20) NOT NULL,
        subject VARCHAR(100) NOT NULL,
        mastery_score INT DEFAULT 75,
        strong_topics TEXT,
        weak_topics TEXT,
        action_plan TEXT,
        recommended_hours INT DEFAULT 4,
        UNIQUE KEY student_subject (student_id, subject)
    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)

    con.commit()
    print("✅ All tables created successfully!")

    # Fetch all students from MySQL
    cur.execute("SELECT student_id, name FROM students")
    students = cur.fetchall()
    print(f"📌 Found {len(students)} registered students.")

    subjects = [
        "DevOps",
        "Machine Learning",
        "Cloud Computing",
        "Cryptography & Network Security",
        "Software Project Management",
        "Soft Skills",
        "CRT",
        "E-Waste Management",
        "Machine Learning Lab",
        "Cloud Computing Lab"
    ]

    # SEED QUIZ QUESTIONS (if empty)
    cur.execute("SELECT COUNT(*) as cnt FROM quiz_questions")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding Quiz Questions...")
        quiz_data = [
            # DevOps
            ("DevOps", "CI/CD Pipelines", "Medium", "What is the primary role of a Jenkinsfile in a pipeline?", "To define deployment infrastructure as code", "To script and version the build/deploy workflow steps", "To monitor memory usage of containers", "To act as the MySQL database adapter", "B", "A Jenkinsfile is a text file that contains the definition of a Jenkins Pipeline and is checked into source control."),
            ("DevOps", "Docker & Containers", "Easy", "Which command is used to build a Docker image from a Dockerfile?", "docker compile .", "docker make -f Dockerfile", "docker build -t app:v1 .", "docker start --new .", "C", "'docker build' builds Docker images from a Dockerfile and a context."),
            ("DevOps", "Kubernetes Orchestration", "Hard", "What Kubernetes component manages pod replica counts according to declared spec?", "kube-proxy", "kube-scheduler", "kube-controller-manager (ReplicaSet Controller)", "kubelet", "C", "The controller manager continuously reconciles the desired replica state with the actual running pods."),
            ("DevOps", "GitOps & Version Control", "Medium", "What is the key advantage of GitOps?", "Manual approval via email", "Single source of truth in Git with declarative infrastructure automated reconciliation", "Elimination of CI pipelines", "Direct SSH to production clusters", "B", "GitOps uses Git repositories as the single source of truth for all infrastructure and application code."),
            ("DevOps", "Continuous Monitoring", "Medium", "Prometheus primarily gathers metrics via which communication model?", "Pull / Scraping HTTP endpoints", "Push via UDP sockets only", "FTP polling", "Direct kernel memory hooks", "A", "Prometheus scrapes metrics from instrumented jobs either directly or via an intermediary push gateway for short-lived jobs."),

            # Machine Learning
            ("Machine Learning", "Supervised Learning", "Easy", "Which algorithm is commonly used for classification when features are conditionally independent?", "K-Means", "Naive Bayes", "Linear Regression", "DBSCAN", "B", "Naive Bayes is a probabilistic classifier based on Bayes theorem with the strong naive independence assumption."),
            ("Machine Learning", "Model Evaluation", "Medium", "What metric is preferred when evaluating a highly imbalanced fraud detection dataset?", "Accuracy", "F1-Score and PR-AUC", "Mean Squared Error", "Explained Variance", "B", "When classes are highly imbalanced, accuracy is misleading; F1-score and Precision-Recall AUC reflect false positive and false negative trade-offs accurately."),
            ("Machine Learning", "Overfitting Prevention", "Medium", "Which technique adds a penalty proportional to the absolute value of coefficients?", "L2 Regularization (Ridge)", "L1 Regularization (Lasso)", "Dropout only", "Min-Max Normalization", "B", "L1 (Lasso) regularization adds penalty |w| which induces sparsity by driving coefficients strictly to zero."),
            ("Machine Learning", "Neural Networks", "Hard", "Why is the ReLU activation function widely preferred over Sigmoid in deep networks?", "ReLU limits outputs strictly between 0 and 1", "ReLU mitigates the vanishing gradient problem for positive activations", "ReLU requires trigonometric operations", "ReLU is differentiable everywhere including x=0", "B", "ReLU avoids saturation for positive values, maintaining a constant gradient of 1 and reducing vanishing gradients."),
            ("Machine Learning", "Unsupervised Learning", "Medium", "What does the 'Elbow Method' identify in K-Means clustering?", "The learning rate", "The optimal number of clusters k via WCSS reduction rate", "The convergence speed of PCA", "The outlier threshold distance", "B", "The elbow method plots within-cluster sum of squares against k to spot the point where diminishing returns start."),

            # Cloud Computing
            ("Cloud Computing", "Virtualization & Hypervisors", "Medium", "What is a Type-1 Hypervisor?", "Runs on top of a conventional host operating system", "Runs directly on the host hardware (Bare-Metal)", "Software container engine like Docker", "A browser virtual machine plugin", "B", "Type-1 (Bare Metal) hypervisors like VMware ESXi or KVM run directly on hardware without a guest OS underneath."),
            ("Cloud Computing", "Cloud Service Models", "Easy", "Which cloud service model provides hardware, networking, and OS while developer only manages code and runtime?", "IaaS", "PaaS", "SaaS", "FaaS only", "B", "Platform-as-a-Service (PaaS) abstracts away OS and infrastructure management so developers can focus solely on deployment."),
            ("Cloud Computing", "Auto Scaling & Elasticity", "Hard", "What is the difference between Scalability and Elasticity in Cloud Computing?", "They are identical terms", "Scalability is adapting capacity statically to peak load; Elasticity is dynamic automated real-time provisioning & de-provisioning based on demand", "Scalability applies only to RAM", "Elasticity applies only to network bandwidth", "B", "Elasticity is the degree to which a system can adapt to workload changes by provisioning and de-provisioning resources automatically."),
            ("Cloud Computing", "Serverless Architecture", "Medium", "In AWS Lambda or Google Cloud Functions, what triggers billing?", "Always-on 24/7 server reservation", "Exact millisecond execution duration and memory allocated per invocation", "Static monthly license", "Number of lines of code in repo", "B", "Serverless follows an event-driven pay-per-use model billing only execution time and memory consumed."),

            # Cryptography & Network Security
            ("Cryptography & Network Security", "Public Key Cryptography", "Hard", "The mathematical security of the RSA encryption algorithm relies on:", "Discrete Logarithm problem over elliptic curves", "Difficulty of factoring the product of two large prime numbers", "Quantum entanglement entanglement", "Fast Fourier transform matrices", "B", "RSA relies on the computational difficulty of factoring very large semiprime integers into their two prime factors."),
            ("Cryptography & Network Security", "Symmetric Ciphers", "Medium", "Which of the following block sizes does the Advanced Encryption Standard (AES) utilize?", "64 bits", "128 bits", "256 bits", "512 bits", "B", "AES specifies a fixed block size of 128 bits, while its key sizes can be 128, 192, or 256 bits."),
            ("Cryptography & Network Security", "Digital Signatures", "Medium", "To generate a digital signature on a document, the sender encrypts the document hash with:", "The receiver's public key", "The sender's private key", "The sender's public key", "A shared symmetric session key", "B", "A digital signature is created by signing the cryptographic digest with the sender's private key, verifiable by anyone with the sender's public key."),
            ("Cryptography & Network Security", "Network Attacks", "Easy", "What type of attack intercepts and alters communication between two unsuspecting parties?", "DDoS", "Man-in-the-Middle (MitM)", "SQL Injection", "Buffer Overflow", "B", "In a Man-in-the-Middle (MitM) attack, the attacker secretly relays and possibly alters communications between two entities.")
        ]

        for q in quiz_data:
            cur.execute("""
                INSERT INTO quiz_questions
                (subject, topic, difficulty, question, option_a, option_b, option_c, option_d, correct_option, explanation)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, q)
        con.commit()

    # SEED JAM TOPICS
    cur.execute("SELECT COUNT(*) as cnt FROM jam_topics")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding JAM Topics...")
        jam_topics = [
            ("Non-Technical", "Work-Life Balance & Digital Wellbeing in the Modern Era", "Speak on managing screen time, avoiding burnout, and establishing healthy boundaries between study/work and personal relaxation.", "1. Impact of continuous connectivity & screen fatigue\n2. Importance of physical exercise & mindfulness\n3. Setting clear boundaries between study/work and personal time\n4. Actionable habits for digital detox", "Burnout, Mindfulness, Equilibrium, Digital Detox", "Personal Reflection, Persuasive Speaking, Tone Modulation"),
            ("Non-Technical", "The Power of Daily Habits & Discipline over Fleeting Motivation", "Discuss how small 1% atomic habit improvements compounded daily build long-term success compared to sporadic spikes of motivation.", "1. Motivation vs Systems\n2. The 1% compounding rule of daily habits\n3. Overcoming procrastination\n4. Consistency over intensity", "Compounding, Discipline, Procrastination, Consistency", "Structured Argumentation, Clarity of Thought, Conviction"),
            ("Non-Technical", "Climate Action & Individual Responsibility for Sustainability", "Explore practical actions individuals and student communities can take to reduce carbon footprints and protect local ecosystems.", "1. Understanding global climate trends & emissions\n2. Reducing single-use plastics and e-waste\n3. Renewable energy transition\n4. Everyday eco-friendly choices", "Ecosystem, Sustainability, Renewable, Carbon Footprint", "Societal Awareness, Rhetorical Impact, Actionability"),
            ("Non-Technical", "Public Speaking & Overcoming Stage Fright in Everyday Life", "Share techniques for conquering performance anxiety, projecting vocal confidence, and delivering clear impromptu presentations.", "1. Understanding performance anxiety & stage fright\n2. Pacing, deep breathing, and vocal projection\n3. Structuring impromptu thoughts logically\n4. Building confidence through practice", "Articulation, Composure, Eloquence, Impromptu", "Vocal Clarity, Confidence, Eye Contact"),
            ("Technical & Emerging Tech", "The Impact of Generative AI on Modern Software Engineering", "Speak on how tools like GitHub Copilot and LLMs transform coding speed, code reviews, and what future engineers must learn.", "1. Introduction to AI coding tools\n2. Boost in developer productivity\n3. Quality, security, and hallucination risks\n4. Evolving role of software engineers", "Synergy, Automate, Paradigm, Augmentation", "Extempore Fluency, Technical Accuracy, Coherence"),
            ("Technical & Emerging Tech", "Microservices vs Monoliths: When Simplicity Beats Hype", "Discuss architectural tradeoffs, scalability challenges, distributed debugging, and organizational alignment.", "1. Definition of monolithic vs microservices\n2. Hidden operational overhead of microservices\n3. Start with monolith, scale when needed\n4. Real-world architectural takeaway", "Decoupling, Latency, Overhead, Scalability", "Structure, Clarity, Architectural Insight"),
            ("Soft Skills & Leadership", "The Importance of Emotional Intelligence (EQ) in Tech Teams", "Explain why high IQ is not enough and how empathy, conflict resolution, and active listening drive high-performing teams.", "1. EQ vs IQ in engineering\n2. Empathy during code reviews and outages\n3. Psychological safety in team culture\n4. Personal teamwork takeaway", "Empathy, Collaboration, Resilience, Constructive", "Body Language, Vocal Modulation, Conviction"),
            ("Career & Placement", "Preparing for Tech Interviews: Coding vs System Design vs Communication", "Detail how an undergraduate should balance algorithmic practice, foundational CS knowledge, and verbal articulation during campus placements.", "1. Problem solving under pressure\n2. Articulating thought process out loud\n3. Core CS subjects (OS, DBMS, Networks)\n4. Behavioural interview readiness", "Articulation, Rigor, Optimization, Composure", "Time Management, Persuasiveness, Structured Thinking")
        ]
        for t in jam_topics:
            cur.execute("""
                INSERT INTO jam_topics (category, title, description, suggested_points, vocabulary_hints, target_skills)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, t)
        con.commit()

    # SEED ACTIVE TEACHING ACTIVITIES
    cur.execute("SELECT COUNT(*) as cnt FROM active_teaching_activities")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding Active Teaching Methodology Activities...")
        activities = [
            ("DevOps", "Flipped Classroom & Live Incident Response", "Production Deployment Outage: Rollback or Hotfix?", "Your team deployed a new Kubernetes release at 2:00 AM; checkout service latency spiked by 800% and error rate hit 14%. Analyze the deployment YAML, Prometheus grafana alerts, and formulate a 5-minute incident command decision.", "Present a 3-step triage plan with exact kubectl rollback commands and post-mortem template.", "Executive Incident Summary", "Mastery of incident mitigation, canary releases, and zero-downtime deployment pipelines."),
            ("Machine Learning", "Case Study & Think-Pair-Share", "Detecting Bias in Algorithmic Credit Scoring", "A bank deployed an XGBoost model for credit limit approvals. Audit data reveals applicants from specific zip codes get 40% lower limits despite identical income and repayment histories. Investigate proxy feature correlations and bias mitigation.", "Identify the root cause of disparate impact; suggest pre-processing or fair-metric objective rewrites.", "Bias Audit & Fairness Report", "Understanding ethical AI, disparate impact, demographic parity, and feature fairness constraints."),
            ("Cloud Computing", "Architectural Challenge & Group Discussion", "Designing a 99.999% SLA Multi-Region Cloud Architecture", "An e-commerce giant expects 50,000 requests/sec on Black Friday. Draft a multi-region cloud deployment on AWS/GCP addressing database replication, RTO/RPO limits, CDN edge caching, and cost optimization.", "Diagram the cloud architecture with VPC peering, Route 53 latency routing, and DynamoDB Global Tables.", "High-Availability System Blueprint", "Real-world cloud topology, failure-domain isolation, and disaster recovery strategies."),
            ("Cryptography & Network Security", "Red Team vs Blue Team Simulation", "Zero-Trust Network Perimeter & TLS 1.3 Audit", "A corporate internal network relies on legacy perimeter firewalls with plain HTTP internal microservice calls. Simulate a lateral movement attacker scenario and design a Zero-Trust migration.", "Map out mTLS (mutual TLS) certificates, identity-based access proxies, and secret vault rotation policies.", "Zero-Trust Defense Matrix", "Implementing defensive cryptography, certificate authorities, and end-to-end encryption standards."),
            ("Software Project Management", "Role-Playing Simulation: Agile Sprint Retrospective", "Resolving Sprint Scope Creep & Velocity Drop", "Sprint 4 ended with only 55% of story points completed. The Product Owner added 4 unplanned high-priority features mid-sprint while developers faced tech debt blockers. Conduct an Agile Retrospective.", "Role-play as Scrum Master, Lead Developer, and Product Owner to negotiate working agreements and sprint buffer.", "Agile Sprint Agreement", "Sprint velocity forecasting, boundary negotiation, and stakeholder conflict resolution.")
        ]
        for a in activities:
            cur.execute("""
                INSERT INTO active_teaching_activities
                (subject, methodology_type, title, scenario_description, student_task, deliverable, learning_outcome)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, a)
        con.commit()

    # SEED STUDY MATERIALS & PDF NOTES
    cur.execute("SELECT COUNT(*) as cnt FROM study_materials")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding Study Materials & PDFs...")
        materials = [
            ("DevOps", "Unit 1 & 2", "DevOps Foundations & CI/CD Master Blueprint", "PDF Notes", "devops_complete_notes_u1_u2.pdf", "3.4 MB", "Comprehensive guide covering DevOps culture, Continuous Integration with Jenkins/GitHub Actions, Docker containerization, and automated pipeline scripts.", """
# DevOps Foundations & CI/CD Pipeline Blueprint

### 1. What is DevOps?
DevOps is a set of practices, cultural philosophies, and tools that increases an organization's ability to deliver applications and services at high velocity.

### 2. The Continuous Integration Cycle
- **Source Control**: Centralized repository with branch protection rules.
- **Automated Builds**: Unit testing, linting, and compilation on every commit.
- **Feedback Loops**: Immediate build notifications to prevent broken trunk integration.

### 3. Containerization with Docker
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```
Containers package application code, dependencies, and environment configurations into an immutable, portable artifact.

### 4. Key Takeaways for Examinations
- Compare Monolithic vs Microservices deployment models.
- Explain Blue-Green vs Canary deployment strategies with architectural diagrams.
- Write a sample declarative Jenkinsfile pipeline script.
            """, "/student/notes/download/devops_u1_u2"),

            ("Machine Learning", "Unit 1 to 3", "Machine Learning Core Algorithms & Mathematical Foundations", "Lecture Slides & PDF", "ml_core_algorithms_handbook.pdf", "4.1 MB", "Detailed lecture summaries covering Supervised vs Unsupervised models, Cost functions, Gradient Descent, Decision Trees, and Evaluation Metrics.", """
# Machine Learning Algorithmic Handbook

### 1. Cost Function & Gradient Descent
For linear regression with parameter vector $\\theta$:
$$J(\\theta) = \\frac{1}{2m} \\sum_{i=1}^m (h_\\theta(x^{(i)}) - y^{(i)})^2$$

### 2. Regularization (L1 vs L2)
- **L1 (Lasso)**: Adds $\\lambda \\sum |w_i|$ penalty. Enforces sparsity, driving non-essential coefficients strictly to zero (feature selection).
- **L2 (Ridge)**: Adds $\\lambda \\sum w_i^2$ penalty. Shrinks large weights smoothly, combating multicollinearity.

### 3. Confusion Matrix Metrics
- **Precision**: $\\frac{TP}{TP + FP}$
- **Recall (Sensitivity)**: $\\frac{TP}{TP + FN}$
- **F1 Score**: $2 \\times \\frac{Precision \\times Recall}{Precision + Recall}$

### 4. Essential Exam Topics
- Bias-Variance tradeoff and learning curves.
- Support Vector Machine maximum margin hyperplanes and Kernel trick.
- Random Forests ensemble bootstrapping and bagging principles.
            """, "/student/notes/download/ml_handbook"),

            ("Cloud Computing", "Unit 1 & 2", "Cloud Computing Architecture, Virtualization & Storage Systems", "PDF Notes", "cloud_computing_architecture.pdf", "2.8 MB", "In-depth notes on Hypervisor architectures, NIST Cloud Model, AWS/Azure service hierarchies, Object vs Block storage, and Auto-scaling.", """
# Cloud Computing Architecture & Services

### 1. NIST Definition of Cloud Computing
Five Essential Characteristics:
1. On-demand self-service
2. Broad network access
3. Resource pooling
4. Rapid elasticity
5. Measured service

### 2. Hypervisors & Virtualization
- **Type 1 (Bare Metal)**: Direct execution on hardware (VMware ESXi, KVM). Lower latency, production hypervisors.
- **Type 2 (Hosted)**: Runs atop a host OS (VirtualBox, VMware Workstation). Ideal for local development.

### 3. Storage Models in the Cloud
- **Block Storage** (AWS EBS): Raw block volumes mounted like internal hard drives to virtual machines.
- **Object Storage** (AWS S3): REST API access, high durability (99.999999999%), unlimited scalability, metadata tagging.
            """, "/student/notes/download/cloud_u1_u2"),

            ("Cryptography & Network Security", "Unit 1 to 4", "CNS Security Protocols, RSA, AES & Modern Cryptosystems", "Formula Sheet & PDF", "cns_complete_security_notes.pdf", "3.6 MB", "Complete cryptosystem reference: Classical ciphers, DES/AES mechanics, Diffie-Hellman Key Exchange, RSA step-by-step numerical examples, and SHA-256.", """
# Cryptography & Network Security Complete Notes

### 1. The RSA Algorithm
1. Select two large primes: $p$ and $q$.
2. Compute modulus $n = p \\times q$.
3. Compute Euler's totient: $\\phi(n) = (p-1)(q-1)$.
4. Choose integer $e$ such that $1 < e < \\phi(n)$ and $\\gcd(e, \\phi(n)) = 1$.
5. Compute private key $d$ such that $d \\times e \\equiv 1 \\pmod{\\phi(n)}$.
- **Encryption**: $C = M^e \\pmod{n}$
- **Decryption**: $M = C^d \\pmod{n}$

### 2. Diffie-Hellman Key Exchange
Allows two parties to negotiate a shared secret over an insecure channel using modular exponentiation and primitive roots.

### 3. SHA-256 & Message Digests
One-way cryptographic hash functions producing fixed 256-bit signatures. Resistant to preimage and collision attacks.
            """, "/student/notes/download/cns_notes"),

            ("Software Project Management", "Unit 1 & 2", "SPM Agile Methodologies, Effort Estimation & Risk Management", "PDF Notes", "spm_agile_risk_estimation.pdf", "2.2 MB", "Guide to Agile Scrum ceremonies, COCOMO model calculations, Work Breakdown Structure (WBS), Critical Path Method (CPM), and PERT diagrams.", """
# Software Project Management Comprehensive Notes

### 1. Effort Estimation - COCOMO Model
Basic COCOMO effort equation:
$$Effort (E) = a \\times (KLOC)^b \\text{ person-months}$$
- Organic, Semidetached, and Embedded project categories determine constants $a$ and $b$.

### 2. Critical Path Method (CPM)
- Determine the longest sequence of dependent activities in project network diagram.
- Activities on the critical path have zero float (slack time); any delay delays overall project delivery.

### 3. Scrum Framework
- **Sprint Planning**: Commit to Sprint Backlog from prioritized Product Backlog.
- **Daily Standup**: 15-minute sync on yesterday, today, and blockers.
- **Sprint Review & Retrospective**: Inspect product increment and team process.
            """, "/student/notes/download/spm_notes")
        ]

        for m in materials:
            cur.execute("""
                INSERT INTO study_materials
                (subject, unit, title, doc_type, file_name, file_size, summary, content_preview, download_url)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, m)
        con.commit()

    # SEED SAMPLE DOUBTS
    cur.execute("SELECT COUNT(*) as cnt FROM student_doubts")
    if cur.fetchone()["cnt"] == 0:
        print("🌱 Seeding Sample Student Doubts...")
        sample_doubts = [
            ("23501A1201", "ADARI KUSUMA", "DevOps", "Kubernetes Pod Lifecycle", "What happens when a pod enters CrashLoopBackOff state, and how do we debug it?", "When a container fails to start and repeatedly restarts, Kubernetes applies an exponential backoff delay (10s, 20s, 40s... up to 5 mins). To troubleshoot: 1) Run 'kubectl describe pod <pod-name>' to check Events. 2) Run 'kubectl logs <pod-name> --previous' to inspect error logs from the crashed container. Common culprits include missing environment variables, failing DB connections, or invalid startup commands.", "Answered", "Prof. CH. Praneeth & AI Tutor"),
            ("23501A1201", "ADARI KUSUMA", "Machine Learning", "Overfitting vs Underfitting", "How do I choose the regularization parameter lambda in Ridge Regression?", "You typically find the optimal lambda via k-fold cross-validation (using RidgeCV in scikit-learn). Plot the validation error against a log-scale range of lambda values. The optimal lambda minimizes cross-validation Mean Squared Error while preserving generalizability on unseen test folds.", "Answered", "Mrs. D. Leela Dharani"),
            ("23501A1202", "AKULA RUSHITHA", "Cloud Computing", "S3 Storage Classes", "When should we transition objects from S3 Standard to S3 Glacier Flexible Retrieval?", "If files are accessed less than once a quarter or stored for compliance/audit archiving where 3-5 hour retrieval latency is acceptable, transitioning reduces monthly GB storage costs by over 75% compared to S3 Standard.", "Answered", "Ms. K. Sri Vijaya"),
            ("23501A1203", "ALURI SREYA", "Cryptography & Network Security", "Public Key Distribution", "Why do we need Certificate Authorities (CAs) if public keys can already be freely shared?", "Anyone could create an impostor public key claiming to be your bank or server (Man-in-the-Middle attack). A Certificate Authority digitally signs the public key bound to the server's identity, allowing clients to verify trust through standard browser root certificates.", "Answered", "Dr. Y. Padma")
        ]
        for d in sample_doubts:
            cur.execute("""
                INSERT INTO student_doubts
                (student_id, student_name, subject, topic, question, answer, status, answered_by)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, d)
        con.commit()

    # SEED STUDENT MARKS & STRENGTHS/WEAKNESSES FOR ALL 72 STUDENTS
    cur.execute("SELECT COUNT(*) as cnt FROM student_marks")
    marks_exist = cur.fetchone()["cnt"] > 0

    if not marks_exist:
        print("🌱 Seeding Realistic Student Marks and Diagnostics for all students...")
        
        subject_diagnostics_templates = {
            "DevOps": {
                "strong": ["Docker Containerization", "Git & GitHub Versioning", "CI Pipeline Setup"],
                "weak": ["Kubernetes Ingress & Helm Charts", "Prometheus Alertmanager Rules"],
                "plan": "Review Kubernetes networking architecture and deploy a 3-tier microservice with Helm."
            },
            "Machine Learning": {
                "strong": ["Supervised Classification", "Data Preprocessing & Scaling", "Scikit-Learn Workflows"],
                "weak": ["Vanishing Gradients in Deep Networks", "Hyperparameter Tuning with Optuna"],
                "plan": "Complete 3 hands-on notebooks implementing backpropagation and Bayesian optimization."
            },
            "Cloud Computing": {
                "strong": ["IaaS vs PaaS Fundamentals", "AWS S3 & IAM Policies", "Virtualization Models"],
                "weak": ["VPC Subnetting & CIDR Calculation", "Multi-Region Disaster Recovery"],
                "plan": "Practice designing dual-tier private/public subnets with NAT Gateways on AWS Cloud."
            },
            "Cryptography & Network Security": {
                "strong": ["Symmetric AES Encryption", "Hash Functions & SHA-256", "Firewall Principles"],
                "weak": ["RSA Key Generation Mathematics", "Elliptic Curve Cryptography (ECC)"],
                "plan": "Solve 5 numerical problems calculating private exponent d and modular inverse in RSA."
            },
            "Software Project Management": {
                "strong": ["Agile Scrum Ceremonies", "Work Breakdown Structure", "Team Collaboration"],
                "weak": ["COCOMO Effort Calculations", "CPM Critical Path Float Calculations"],
                "plan": "Draw network diagrams and calculate early/late start dates for 3 sample project schedules."
            },
            "Soft Skills": {
                "strong": ["Interpersonal Communication", "Professional Email Etiquette", "Teamwork"],
                "weak": ["Impromptu Public Speaking (JAM)", "Negotiation Tactics in Conflict"],
                "plan": "Record three 60-second extempore speeches weekly using the JAM studio."
            },
            "CRT": {
                "strong": ["Quantitative Aptitude", "Logical Reasoning Patterns", "Number Systems"],
                "weak": ["Time & Distance Complex Problems", "Data Interpretation Speed"],
                "plan": "Attempt 20 timed aptitude questions daily focusing on shortcuts and elimination strategies."
            },
            "E-Waste Management": {
                "strong": ["E-Waste Legislation & Rules", "Hazardous Material Identification"],
                "weak": ["Recycling Plant Recovery Yield Calculations", "Extended Producer Responsibility (EPR)"],
                "plan": "Summarize India E-Waste Management Rules 2022 and international Basel convention directives."
            },
            "Machine Learning Lab": {
                "strong": ["Pandas & NumPy Manipulations", "Model Training Scripts"],
                "weak": ["Model Serialization & Flask API Deployment"],
                "plan": "Deploy a trained Random Forest pickle model behind a lightweight REST endpoint."
            },
            "Cloud Computing Lab": {
                "strong": ["EC2 Instance Provisioning", "SSH Keypair Configuration"],
                "weak": ["Terraform Infrastructure-as-Code Declarations"],
                "plan": "Write and apply a Terraform script to create an S3 bucket and EC2 instance automatically."
            }
        }

        # Seed realistic exam scores for each student
        exam_types = [
            ("Mid-Term 1", 30),
            ("Mid-Term 2", 30),
            ("Assignment & Lab Internal", 20),
            ("End-Semester Project / Exam", 50)
        ]

        for s in students:
            sid = s["student_id"]
            # Seed reproducible pseudo-random seed per student so their scores stay steady
            student_seed = sum(ord(c) for c in sid)
            rnd = random.Random(student_seed)

            # Insert marks for top subjects
            for sub in subjects:
                base_pct = rnd.randint(65, 94) # Student baseline performance

                for exam_name, max_m in exam_types:
                    score = round((base_pct + rnd.randint(-8, 6)) / 100 * max_m, 1)
                    score = max(min(score, max_m), 10.0)
                    pct = (score / max_m) * 100
                    if pct >= 85:
                        grade = "A+"
                    elif pct >= 75:
                        grade = "A"
                    elif pct >= 65:
                        grade = "B+"
                    elif pct >= 55:
                        grade = "B"
                    else:
                        grade = "C"

                    cur.execute("""
                        INSERT INTO student_marks
                        (student_id, subject, exam_type, marks_obtained, max_marks, grade, semester, exam_date)
                        VALUES (%s, %s, %s, %s, %s, %s, 'Sem-4', '2026-03-01')
                    """, (sid, sub, exam_name, score, max_m, grade))

                # Insert Diagnostics (Strengths & Weaknesses)
                diag = subject_diagnostics_templates.get(sub, {
                    "strong": ["Core Concepts", "Problem Solving"],
                    "weak": ["Advanced Edge Cases"],
                    "plan": "Review unit textbook notes and practice previous year question sets."
                })
                mastery = min(max(base_pct + rnd.randint(-5, 5), 50), 98)
                cur.execute("""
                    INSERT INTO subject_diagnostics
                    (student_id, subject, mastery_score, strong_topics, weak_topics, action_plan, recommended_hours)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON DUPLICATE KEY UPDATE mastery_score=VALUES(mastery_score)
                """, (
                    sid,
                    sub,
                    mastery,
                    ", ".join(diag["strong"]),
                    ", ".join(diag["weak"]),
                    diag["plan"],
                    rnd.randint(3, 6)
                ))

            # Add an initial quiz attempt record for the student
            cur.execute("""
                INSERT INTO quiz_attempts
                (student_id, subject, score, total_questions, percentage, time_taken_seconds)
                VALUES (%s, 'DevOps', %s, 5, %s, %s)
            """, (sid, rnd.randint(3, 5), rnd.randint(70, 100), rnd.randint(85, 160)))

        con.commit()
        print("✅ Student Marks, Diagnostics, and Quiz Attempts populated for all students!")

    con.close()
    print("🎉 Student Portal Database Setup Complete!")

if __name__ == "__main__":
    setup_database()
