import os
from flask import Flask, request, render_template, redirect, url_for, session, abort

app = Flask(__name__)

app.secret_key = os.environ.get("APP_SECRET", "dev-unsafe-secret-change-me")

DEMO_USER = os.environ.get("DEMO_USER", "admin")
DEMO_PASS = os.environ.get("DEMO_PASS", "password")

@app.get("/")
def index():
    if session.get("user"):
        return redirect(url_for("dashboard"))
    return redirect(url_for("login"))

@app.get("/login")
def login():
    return render_template("login.html")

@app.post("/login")
def login_post():
    username = request.form.get("username", "")
    password = request.form.get("password", "")

    if username == DEMO_USER and password == DEMO_PASS:
        session["user"] = username
        return redirect(url_for("dashboard"))

    return render_template("login.html", error="Invalid credentials")

@app.get("/dashboard")
def dashboard():
    user = session.get("user")
    if not user:
        return redirect(url_for("login"))
    return render_template("dashboard.html", user=user)

@app.post("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.get("/debug-env")
def debug_env():
    """
    Intentionally dangerous for demos:
    shows how secrets in env vars can leak if an attacker hits an internal/debug endpoint.
    In hardened deployments, you would remove this or protect it.
    """
    if os.environ.get("ENABLE_DEBUG_ENV") != "1":
        abort(404)

    # Return only a few keys to keep the demo simple
    keys = ["DEMO_USER", "DEMO_PASS", "APP_SECRET"]
    return {k: os.environ.get(k) for k in keys}

if __name__ == "__main__":
    # Insecure Dockerfile runs this (debug server)
    app.run(host="0.0.0.0", port=5000, debug=True)