import app

def test_login():
    client = app.app.test_client()

    # Test correct password
    res = client.post('/admin_login', data={'username': 'admin', 'password': '500452'})
    print("Login with 500452 status code (expect 302 redirect):", res.status_code)
    print("Redirect location:", res.headers.get('Location'))

    # Test wrong password
    res_wrong = client.post('/admin_login', data={'username': 'admin', 'password': 'wrongpassword'})
    print("Login with wrong password status code (expect 200 with error):", res_wrong.status_code)
    print("Error message in page:", "Invalid Admin Credentials" in res_wrong.data.decode('utf-8'))

if __name__ == "__main__":
    test_login()
