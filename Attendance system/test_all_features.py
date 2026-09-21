import urllib.request
import json

def test():
    base = "http://127.0.0.1:5000"

    print("--- TESTING ALL ROUTES & FEATURES ---")

    # 1. Home
    res = urllib.request.urlopen(f"{base}/")
    print("Home page HTTP status:", res.status)

    # 2. Admin Dashboard
    res_admin = urllib.request.urlopen(f"{base}/admin_dashboard")
    print("Admin dashboard HTTP status:", res_admin.status)

    # 3. Export PDF
    res_pdf = urllib.request.urlopen(f"{base}/export/pdf")
    print("PDF export HTTP status:", res_pdf.status, "Content-Type:", res_pdf.headers.get("Content-Type"))

    # 4. Export Excel
    res_excel = urllib.request.urlopen(f"{base}/export")
    print("Excel export HTTP status:", res_excel.status)

    # 5. Smart Edu Tutor Chat API
    req_tutor = urllib.request.Request(
        f"{base}/api/smart_edu/tutor_chat",
        data=json.dumps({"message": "Explain binary search trees", "subject": "Data Structures"}).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    res_tutor = urllib.request.urlopen(req_tutor)
    print("Smart Tutor Chat API response:", json.loads(res_tutor.read().decode('utf-8'))['success'])

    print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY!")

if __name__ == "__main__":
    test()
