from flask import Blueprint, jsonify, request
from backend.app.utils.db_utils import get_db_connection

bp = Blueprint("profile", __name__, url_prefix="/api")

@bp.route("/profile/me", methods=["GET"])
def get_profile_me():
    # Taking email from query param or mock since auth is not fully set up
    email = request.args.get("email") or "user@example.com"
    
    conn = get_db_connection()
    if not conn:
        return jsonify({})
        
    try:
        cursor = conn.cursor(dictionary=True)
        # Find user from users table
        cursor.execute("SELECT username, email, created_at, avatar_url FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
        
        if user:
            # Stats (total ratings/reviews) - Extra query needed
            # Note: Returning 0 if user_ratings table is not fully defined.
            stats = {"total_ratings": 0, "reviews": 0}
            
            return jsonify({
                "username": user["username"],
                "email": user["email"],
                "member_since": user["created_at"],
                "stats": stats
            })
            
        return jsonify({"error": "User not found"}), 404
    except Exception as e:
        print(f"Profile error: {e}")
        return jsonify({"error": "Internal error"}), 500
    finally:
        if conn: conn.close()

@bp.route("/profile/ratings", methods=["GET"])
def get_profile_ratings():
    # Endpoint to fetch user rated movies
    # Returning empty list as user_ratings table is not ready
    return jsonify([])