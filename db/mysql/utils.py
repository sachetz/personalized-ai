import bcrypt

from db.mysql.client import MySQLClient

client = MySQLClient()

def validate_login(username, password):
    user = client.execute_query("SELECT * FROM users WHERE username = %s", (username,))[0]
    if bcrypt.checkpw(password.encode("utf-8"), user["password_hash"].encode("utf-8")):
        return user["id"]
    else:
        raise RuntimeError("User not found")

def register(username, password, email):
    try:
        password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        id = client.insert("users", {"username": username, "password_hash": password_hash, "email": email, "user_role": "user"})
        client.insert("gmail_integration", {"user_id": id})
        return id
    except Exception as e:
        raise RuntimeError("Unable to register")

def get_last_sync_at(user_id):
    try:
        rows = client.execute_query(f"SELECT last_sync_at FROM gmail_integration WHERE user_id={user_id}")
        return rows[0]["last_sync_at"]
    except Exception as e:
        raise RuntimeError("Unable to fetch last gmail sync at")
