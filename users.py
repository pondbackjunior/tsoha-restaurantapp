from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text

def login(username, password):
    sql = text("SELECT id, password, role FROM users WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if username == "admin" and password == "admin":
            session["user_id"] = user.id
            session["username"] = username
            session["user_role"] = user.role
            return True
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["user_role"] = user.role
            return True
        else:
            return False

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO users (username,password,role) VALUES (:username,:password,:role)")
        db.session.execute(sql, {"username":username, "password":hash_value, "role":"user"})
        db.session.commit()
    except:
        return False
    return login(username, password)

def user_id():
    return session.get("user_id",0)

def user_role():
    return session.get("user_role",0)

def generate_default_admin():
    if not db.session.execute(text("SELECT id FROM users WHERE username='admin'")).fetchone():
        db.session.execute(text("INSERT INTO users (username,password,role) VALUES ('admin', 'admin', 'admin')"))
        db.session.commit()