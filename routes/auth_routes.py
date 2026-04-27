from flask import Blueprint, render_template, request, redirect, session
from werkzeug.security import generate_password_hash, check_password_hash

auth = Blueprint("auth", __name__)

# ⚠️ Temporary memory storage (server restart pe reset ho jayega)
users = {}


# ---------------- SIGNUP ----------------
@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users:
            return "User already exists"

        users[username] = generate_password_hash(password)
        return redirect("/login")

    return render_template("signup.html")


# ---------------- LOGIN ----------------
@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username in users and check_password_hash(users[username], password):
            session["user"] = username
            session["count"] = 0
            return redirect("/")

        return "Invalid username or password"

    return render_template("login.html")


# ---------------- LOGOUT ----------------
@auth.route("/logout")
def logout():
    session.clear()   # 🔥 logout
    return redirect("/login")