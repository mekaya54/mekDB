from flask import Blueprint, request, jsonify
from backend.app.utils.db_update import create_user
from backend.app.utils.db_utils import get_db_connection
from backend.app.utils.auth_utils import verify_password, generate_token

bp = Blueprint("auth", __name__, url_prefix="/api")

@bp.route("/auth/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email")
    password = data.get("password")
    
    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    conn = get_db_connection()
    user = None
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
            user = cursor.fetchone()
        finally:
            conn.close()
    
    # Does user exist and password match?
    if user and verify_password(user["password_hash"], password):
        token = generate_token()
        # User object to return to frontend
        user_data = {
            "username": user["username"],
            "email": user["email"],
            "avatarUrl": user["avatar_url"] or f"https://api.dicebear.com/7.x/avataaars/svg?seed={user['username']}"
        }
        return jsonify({"user": user_data, "token": token})
    
    return jsonify({"error": "Invalid email or password"}), 401


@bp.route("/auth/signup", methods=["POST"])
def signup():
    data = request.get_json() or {}
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")
    
    if not all([username, email, password]):
        return jsonify({"error": "All fields are required"}), 400

    # Save user to database
    user_id = create_user(username, email, password)
    
    if user_id:
        token = generate_token()
        user_data = {
            "username": username,
            "email": email,
            "avatarUrl": f"https://api.dicebear.com/7.x/avataaars/svg?seed={username}"
        }
        return jsonify({"user": user_data, "token": token}), 201
    else:
        return jsonify({"error": "Registration failed. Email or username might be taken."}), 409