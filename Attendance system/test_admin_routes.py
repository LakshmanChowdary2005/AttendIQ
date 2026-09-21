import urllib.request

def test_admin():
    try:
        req = urllib.request.urlopen("http://127.0.0.1:5000/admin_dashboard")
        html = req.read().decode('utf-8')
        print(f"HTTP Status: {req.status}")
        print("Admin Control Center found:", "Admin Control Center" in html)
        print("AI Attendance Risk Audit found:", "AI Attendance Risk Audit" in html)
        print("Outgoing Student Email Alert Audit Log found:", "Outgoing Student Email Alert Audit Log" in html)
        print("User Management Portal found:", "User Management Portal" in html)
        print("Departments & Sections Management found:", "Departments & Sections Management" in html)
        print("STU101 found:", "STU101" in html)
        print("STU105 found:", "STU105" in html)
    except Exception as e:
        print("Error fetching /admin_dashboard:", e)

if __name__ == "__main__":
    test_admin()
