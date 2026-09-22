from app import app, get_db

def test_targeted_low_attendance():
    print("--- TESTING TARGETED LOW ATTENDANCE NOTIFICATIONS & ALERT BANNER ---")
    client = app.test_client()

    try:
        # 1. Login as Student STU101 (Low Attendance < 75%)
        with client.session_transaction() as sess:
            sess["role"] = "student"
            sess["student_roll"] = "STU101"
            sess["user_id"] = "STU101"
            sess["student_name"] = "Test Low Attendance Student"

        # Make student STU101 have low attendance (< 75%) in database
        con = get_db()
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE UPPER(student_id)='STU101'")
        cur.execute("INSERT INTO students (student_id, name, email, department, section) VALUES ('STU101', 'Test Low Attendance Student', 'low@example.com', 'IT', 'A')")
        cur.execute("DELETE FROM attendance WHERE UPPER(student_id)='STU101'")
        # Insert 10 total classes: 5 Present, 5 Absent -> 50% attendance
        for i in range(5):
            cur.execute("INSERT INTO attendance (student_id, date, subject, hour, status) VALUES ('STU101', '2026-09-19', 'DevOps', 1, 'Present')")
        for i in range(5):
            cur.execute("INSERT INTO attendance (student_id, date, subject, hour, status) VALUES ('STU101', '2026-09-19', 'DevOps', 2, 'Absent')")
        con.commit()
        con.close()

        # Fetch notification bell API for STU101
        res = client.get('/api/notifications')
        assert res.status_code == 200
        notifs = res.json
        print(f"[OK] Low attendance student (50%) bell notifications count: {len(notifs)}")
        has_low_att_notif = any("low attendance" in (n.get("title") or "").lower() or "shortage" in (n.get("title") or "").lower() for n in notifs)
        assert has_low_att_notif, "Low attendance student MUST receive low attendance notification in bell!"
        print("[OK] Low attendance student RECEIVED low attendance notification in bell!")

        # Render student portal for STU101
        portal_res = client.get('/student_portal')
        assert portal_res.status_code == 200
        html = portal_res.get_data(as_text=True)
        assert "low-att-alert-banner" in html, "Low attendance student MUST get scrollable alert banner!"
        assert "marqueeScroll" in html
        print("[OK] Low attendance student portal DISPLAYED scrollable alert marquee banner!")

        # 2. Login as Student STU999 (Safe Attendance >= 75%)
        with client.session_transaction() as sess:
            sess["role"] = "student"
            sess["student_roll"] = "STU999"
            sess["user_id"] = "STU999"
            sess["student_name"] = "Test Safe Student"

        # Insert safe student STU999
        con = get_db()
        cur = con.cursor()
        cur.execute("DELETE FROM students WHERE student_id='STU999'")
        cur.execute("INSERT INTO students (student_id, name, email, department, section) VALUES ('STU999', 'Test Safe Student', 'safe@example.com', 'IT', 'A')")
        cur.execute("DELETE FROM attendance WHERE student_id='STU999'")
        # Insert 10 total classes: 9 Present, 1 Absent -> 90% attendance
        for i in range(9):
            cur.execute("INSERT INTO attendance (student_id, date, subject, hour, status) VALUES ('STU999', '2026-09-19', 'DevOps', 1, 'Present')")
        cur.execute("INSERT INTO attendance (student_id, date, subject, hour, status) VALUES ('STU999', '2026-09-19', 'DevOps', 2, 'Absent')")
        # Add a dummy warning notification to test filtering
        cur.execute("INSERT INTO notifications (recipient_id, recipient_role, title, message, type, is_read) VALUES ('STU999', 'student', 'Low Attendance Alert', 'Test Warning', 'warning', 0)")
        con.commit()
        con.close()

        # Fetch notification bell API for STU999
        res_safe = client.get('/api/notifications')
        assert res_safe.status_code == 200
        safe_notifs = res_safe.json
        has_low_att_notif_safe = any("low attendance" in (n.get("title") or "").lower() for n in safe_notifs)
        assert not has_low_att_notif_safe, "Safe attendance student MUST NOT receive low attendance notification in bell!"
        print("[OK] Safe student (90%) DOES NOT receive low attendance notification in bell!")

        # Render student portal for STU999
        portal_safe_res = client.get('/student_portal')
        assert portal_safe_res.status_code == 200
        safe_html = portal_safe_res.get_data(as_text=True)
        assert "low-att-alert-banner" not in safe_html, "Safe attendance student MUST NOT get scrollable alert banner!"
        print("[OK] Safe student portal DOES NOT display scrollable alert banner!")

        print("\nALL TARGETED LOW ATTENDANCE TESTS PASSED PERFECTLY!")
    finally:
        # Tear down test records so they don't persist in live DB
        con = get_db()
        cur = con.cursor()
        for test_id in ['STU101', 'STU999']:
            cur.execute("DELETE FROM students WHERE UPPER(student_id)=%s", (test_id,))
            cur.execute("DELETE FROM attendance WHERE UPPER(student_id)=%s", (test_id,))
            cur.execute("DELETE FROM notifications WHERE UPPER(recipient_id)=%s", (test_id,))
            cur.execute("DELETE FROM risk_predictions WHERE UPPER(student_id)=%s", (test_id,))
        con.commit()
        con.close()
        print("[CLEANUP] Purged temporary test student records (STU101, STU999).")

if __name__ == "__main__":
    test_targeted_low_attendance()
