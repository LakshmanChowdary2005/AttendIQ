import re
from app import app

def check_no_duplicates():
    client = app.test_client()
    for roll in ['24505A1207', '23501A1201', 'STU101']:
        with client.session_transaction() as sess:
            sess['student_roll'] = roll
        res = client.get('/student_portal')
        assert res.status_code == 200
        html = res.data.decode('utf-8')
        
        # Extract subjects from marks table
        subjects = re.findall(r'<td style="padding:14px; color:#fff; font-weight:700;">(.*?)</td>', html)
        print(f"[{roll}] Rendered Marks Subjects ({len(subjects)}):", subjects)
        assert len(subjects) == len(set(subjects)), f"DUPLICATE SUBJECTS FOUND FOR {roll}!"
        print(f"[{roll}] SUCCESS: Each subject in Student Marks appears EXACTLY ONCE!")

if __name__ == "__main__":
    check_no_duplicates()
