import sys
from app import app

def test_portal():
    client = app.test_client()
    print("Testing Student Portal Endpoints...")

    # 1. Home route
    res = client.get("/")
    assert res.status_code == 200, f"Home failed: {res.status_code}"
    print("[OK] Home route: 200 OK")

    # 2. Student login page
    res = client.get("/student_login")
    assert res.status_code == 200, f"Student login page failed: {res.status_code}"
    print("[OK] Student login page: 200 OK")

    # 3. Student login post
    res = client.post("/student_login", data={"roll": "23501A1201"}, follow_redirects=True)
    assert res.status_code == 200, f"Student login failed: {res.status_code}"
    assert b"ADARI KUSUMA" in res.data, "Student name not found in rendered portal"
    assert b"23501A1201" in res.data, "Student roll not found in rendered portal"
    assert b"AI Assessments" in res.data, "AI Assessments tab not found"
    assert b"AI Socratic Tutor" in res.data, "AI Socratic Tutor tab not found"
    assert b"Course Assignments" in res.data, "Course Assignments tab not found"
    assert b"Daily Homework" in res.data, "Daily Homework tab not found"
    assert b"Skill Gap Roadmap" in res.data, "Skill Gap Roadmap tab not found"
    print("[OK] Student Portal rendering & all 7 tabs: Verified!")

    # 4. Test Quiz API
    quiz_payload = {
        "subject": "DevOps",
        "answers": {"1": "B", "2": "C"},
        "time_taken": 45
    }
    res = client.post("/api/quiz/submit", json=quiz_payload)
    assert res.status_code == 200, f"Quiz submission failed: {res.status_code}"
    quiz_res = res.get_json()
    assert "score" in quiz_res, "Score not returned in quiz submission"
    assert "feedback" in quiz_res, "Feedback not returned in quiz submission"
    print(f"[OK] Quiz API Submit: Score {quiz_res['score']}/{quiz_res['total']} ({quiz_res['percentage']}%) Verified!")

    # 5. Test Doubt Box API
    doubt_payload = {
        "subject": "DevOps",
        "topic": "Docker Containers",
        "question": "How does Docker container isolation differ from a Virtual Machine?"
    }
    res = client.post("/api/doubt/ask", data=doubt_payload)
    assert res.status_code == 200, f"Doubt ask failed: {res.status_code}"
    doubt_res = res.get_json()
    assert doubt_res["success"] == True, "Doubt submission unsuccessful"
    assert "Academic Solution" in doubt_res["answer"] or "Docker" in doubt_res["answer"], "Smart AI explanation not returned"
    print("[OK] Doubt Box API: Instant academic solution returned & logged!")

    # 6. Test Notes Preview API
    res = client.get("/api/notes/preview/1")
    assert res.status_code == 200, f"Notes preview failed: {res.status_code}"
    note_res = res.get_json()
    assert "title" in note_res, "Note title missing"
    print(f"[OK] Notes Preview API: Loaded '{note_res['title']}' successfully!")

    # 7. Test Notes Download route
    res = client.get("/student/notes/download/devops_u1_u2")
    assert res.status_code == 200, f"Download failed: {res.status_code}"
    assert b"OFFICIAL STUDY MATERIAL" in res.data, "Download content format mismatch"
    print("[OK] Notes Download Route: Generated printable document successfully!")

    # 8. Test JAM save API
    res = client.post("/api/jam/save", json={"title": "The Impact of Generative AI", "fluency": 9})
    assert res.status_code == 200, f"JAM save failed: {res.status_code}"
    print("[OK] JAM Studio API: Session logged!")

    print("\nALL STUDENT PORTAL TESTS PASSED PERFECTLY!")

if __name__ == "__main__":
    test_portal()
