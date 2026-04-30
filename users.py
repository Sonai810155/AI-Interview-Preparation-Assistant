def check_login(username, password):
    users = {
        "admin": "1234",
        "student": "5678"
    }

    if username in users and users[username] == password:
        return True
    return False