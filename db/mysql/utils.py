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
        return client.insert("users", {"username": username, "password_hash": password_hash, "email": email, "user_role": "user"})
    except Exception as e:
        raise RuntimeError("Unable to register")
