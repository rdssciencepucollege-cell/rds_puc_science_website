import logging
import os
import time
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask, abort, redirect, render_template, request, send_from_directory, session, url_for
from werkzeug.middleware.proxy_fix import ProxyFix
from werkzeug.security import check_password_hash, generate_password_hash

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent
LOG_PATH = BASE_DIR / "admin_activity.log"

logger = logging.getLogger("rds_admin")
logger.setLevel(logging.INFO)
logger.propagate = False
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_PATH, encoding="utf-8")
    file_handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    logger.addHandler(file_handler)


def write_audit_event(message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with LOG_PATH.open("a", encoding="utf-8") as fh:
        fh.write(f"{timestamp} {message}\n")


app = Flask(__name__, template_folder=str(BASE_DIR / "templates"), static_folder=str(BASE_DIR))
app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1, x_prefix=1)
app.config["SECRET_KEY"] = os.getenv("APP_SECRET", "replace-with-a-long-random-secret")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = os.getenv("USE_HTTPS", "false").lower() == "true"
app.config["SESSION_COOKIE_NAME"] = "rds_admin_session"
app.config["PERMANENT_SESSION_LIFETIME"] = timedelta(minutes=int(os.getenv("ADMIN_SESSION_MINUTES", "30")))

ADMIN_USERNAME = os.getenv("ADMIN_USERNAME", "owner")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") or "ChangeMe-StrongPassword-Now"
ADMIN_PASSWORD_HASH = os.getenv("ADMIN_PASSWORD_HASH") or generate_password_hash(ADMIN_PASSWORD, method="pbkdf2:sha256")
MAX_LOGIN_ATTEMPTS = int(os.getenv("MAX_LOGIN_ATTEMPTS", "5"))
LOCKOUT_SECONDS = int(os.getenv("LOCKOUT_SECONDS", "900"))
LOGIN_ATTEMPT_WINDOW_SECONDS = int(os.getenv("LOGIN_ATTEMPT_WINDOW_SECONDS", "900"))
FAILED_LOGIN_ATTEMPTS = defaultdict(list)


@app.after_request
def set_security_headers(response):
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Permissions-Policy"] = "geolocation=(), microphone=(), camera=()"
    response.headers["Cross-Origin-Opener-Policy"] = "same-origin"
    response.headers["Cross-Origin-Resource-Policy"] = "same-origin"

    if request.path.startswith("/admin"):
        response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
    return response


@app.route("/health")
def health_check():
    return {"status": "ok", "service": "rds-college-site"}, 200


@app.route("/admin")
def admin_root():
    return redirect(url_for("admin_login"))


def get_client_identifier():
    forwarded = request.headers.get("X-Forwarded-For")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.remote_addr or "unknown"


def get_locked_message(client_id):
    attempts = FAILED_LOGIN_ATTEMPTS.get(client_id, [])
    if not attempts:
        return "Too many failed attempts. Please try again later."
    now = time.time()
    attempts = [ts for ts in attempts if now - ts < LOGIN_ATTEMPT_WINDOW_SECONDS]
    if not attempts:
        FAILED_LOGIN_ATTEMPTS.pop(client_id, None)
        return "Too many failed attempts. Please try again later."

    remaining = int(max(0, LOCKOUT_SECONDS - (now - attempts[0])))
    return f"Too many failed attempts. Please try again in {remaining} seconds."


@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if session.get("admin_authenticated"):
        return redirect(url_for("admin_dashboard"))

    client_id = get_client_identifier()
    attempts = FAILED_LOGIN_ATTEMPTS.get(client_id, [])
    now = time.time()
    attempts = [ts for ts in attempts if now - ts < LOGIN_ATTEMPT_WINDOW_SECONDS]
    FAILED_LOGIN_ATTEMPTS[client_id] = attempts

    if len(attempts) >= MAX_LOGIN_ATTEMPTS:
        lock_error = get_locked_message(client_id)
        write_audit_event(f"admin_login_locked client_id={client_id} attempts={len(attempts)}")
        return render_template("admin/login.html", error=lock_error)

    error = None
    if request.method == "POST":
        username = (request.form.get("username") or "").strip()
        password = request.form.get("password") or ""

        if username == ADMIN_USERNAME and check_password_hash(ADMIN_PASSWORD_HASH, password):
            FAILED_LOGIN_ATTEMPTS.pop(client_id, None)
            session["admin_authenticated"] = True
            session.permanent = True
            write_audit_event(f"admin_login_success username={username} client_id={client_id}")
            return redirect(url_for("admin_dashboard"))

        attempts.append(time.time())
        FAILED_LOGIN_ATTEMPTS[client_id] = attempts
        write_audit_event(f"admin_login_failed username={username} client_id={client_id} attempts={len(attempts)}")
        error = "Invalid username or password. Please verify the owner credentials."

    return render_template("admin/login.html", error=error)


@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin_authenticated"):
        return redirect(url_for("admin_login"))
    return render_template("admin/dashboard.html")


@app.route("/admin/recovery")
def admin_recovery():
    return render_template("admin/recovery.html")


@app.route("/admin/logout")
def admin_logout():
    write_audit_event(f"admin_logout client_id={get_client_identifier()}")
    session.clear()
    return redirect(url_for("admin_login"))


@app.route("/", defaults={"path": "index.html"})
@app.route("/<path:path>")
def serve_public(path):
    if path.startswith("admin"):
        abort(404)

    safe_path = (BASE_DIR / path).resolve()
    if not str(safe_path).startswith(str(BASE_DIR)):
        abort(403)

    if safe_path.is_dir():
        safe_path = safe_path / "index.html"

    if not safe_path.is_file():
        abort(404)

    return send_from_directory(BASE_DIR, path)


if __name__ == "__main__":
    if not os.getenv("ADMIN_PASSWORD"):
        print("Warning: using a default demo admin password. Set ADMIN_PASSWORD in the environment for production.")
    app.run(host="0.0.0.0", port=5000, debug=False)
