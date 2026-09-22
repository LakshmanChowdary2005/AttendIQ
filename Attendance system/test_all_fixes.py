from app import app, get_db

def run_tests():
    print("==================================================")
    print("RUNNING COMPREHENSIVE VERIFICATION FOR ALL FIXES")
    print("==================================================")
    client = app.test_client()

    # 1. VERIFY STU101 & STU999 REMOVAL
    con = get_db()
    cur = con.cursor(dictionary=True)
    cur.execute("SELECT student_id, name FROM students WHERE UPPER(student_id) IN ('STU101', 'STU999')")
    found_test_students = cur.fetchall()
    assert len(found_test_students) == 0, f"STU101/STU999 should be deleted, found: {found_test_students}"
    print("[PASS] Test students STU101 & STU999 are completely removed from database!")

    # 2. VERIFY ATTENDANCE SUBMISSION BUG FIX
    # Login as faculty
    with client.session_transaction() as sess:
        sess["role"] = "faculty"
        sess["faculty_id"] = 1
        sess["faculty_code"] = "FAC01"
        sess["faculty_name"] = "Dr. Ramesh Sharma"
        sess["faculty_subject"] = "Cloud Computing"

    cur.execute("SELECT * FROM faculty WHERE faculty_code='FAC01'")
    fac = cur.fetchone()
    subject_name = fac["subject"] if fac else "Cloud Computing"

    # Get two real student IDs from database
    cur.execute("SELECT student_id, name FROM students ORDER BY student_id LIMIT 5")
    students = cur.fetchall()
    assert len(students) >= 2, "At least 2 students required for test"
    
    absent_stu_1 = students[0]["student_id"]
    absent_stu_2 = students[1]["student_id"]

    post_data = {
        "hour": "2",
        "absent": [absent_stu_1, absent_stu_2]
    }

    res = client.post("/mark_attendance", data=post_data, follow_redirects=True)
    assert res.status_code == 200
    print(f"[OK] Submitted attendance with absent students: {absent_stu_1}, {absent_stu_2} for subject '{subject_name}'")

    # Check database records
    cur.execute("SELECT student_id, status FROM attendance WHERE date=CURDATE() AND hour='2' AND subject=%s", (subject_name,))
    att_records = {row["student_id"]: row["status"] for row in cur.fetchall()}

    assert att_records.get(absent_stu_1) == "Absent", f"{absent_stu_1} should be Absent but got {att_records.get(absent_stu_1)}"
    assert att_records.get(absent_stu_2) == "Absent", f"{absent_stu_2} should be Absent but got {att_records.get(absent_stu_2)}"
    
    # Check that other students are marked Present
    if len(students) > 2:
        present_stu = students[2]["student_id"]
        assert att_records.get(present_stu) == "Present", f"{present_stu} should be Present but got {att_records.get(present_stu)}"

    print(f"[PASS] Attendance marking bug FIXED! Checked absent students correctly saved as 'Absent' in database.")

    # 3. VERIFY STUDY NOTES PDF DOWNLOAD
    res_notes = client.get("/student/notes/download/devops_u1_u2")
    assert res_notes.status_code == 200
    assert "application/pdf" in res_notes.headers.get("Content-Type", "")
    assert res_notes.data.startswith(b"%PDF-"), "Notes response must be valid PDF binary starting with %PDF-"
    print(f"[PASS] Study Notes PDF download verified! Content-Type: application/pdf (Size: {len(res_notes.data)} bytes)")

    # 4. VERIFY FACULTY REPORT PDF IN ADMIN PORTAL
    res_fac_pdf = client.get("/export/faculty_pdf")
    assert res_fac_pdf.status_code == 200
    assert "application/pdf" in res_fac_pdf.headers.get("Content-Type", "")
    assert res_fac_pdf.data.startswith(b"%PDF-"), "Faculty report response must be valid PDF binary starting with %PDF-"
    print(f"[PASS] Admin Faculty Report PDF export verified! Content-Type: application/pdf (Size: {len(res_fac_pdf.data)} bytes)")

    con.close()
    print("\n==================================================")
    print("ALL VERIFICATION TESTS PASSED SUCCESSFULLY! (100%)")
    print("==================================================")

if __name__ == "__main__":
    run_tests()
