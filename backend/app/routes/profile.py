"""
Profile routes: return user profile and activity history.

This module provides a minimal profile endpoint used by the frontend.
Because this project does not implement persistent user accounts, the
endpoint returns mocked data or simple DB-derived history when possible.
"""
from flask import Blueprint, jsonify, request
from backend.app.db.connection import get_db_connection
from backend.app.services.profile_service import get_profile_for_email

bp = Blueprint("profile", __name__, url_prefix="/api")


@bp.route("/profile", methods=["GET"])
def get_profile():
	# Backwards-compatible endpoint: returns user + history when `email` param provided
	email = request.args.get("email") or "dev@local"
	result = get_profile_for_email(email)
	return jsonify(result)


@bp.route("/profile/me", methods=["GET"])
def get_profile_me():
	# In this simple dev implementation we read an `email` query param
	# to identify the user. In production, this would come from auth token.
	email = request.args.get("email") or "dev@local"
	result = get_profile_for_email(email)
	# Return only the user object for compatibility with frontend expectations
	return jsonify(result.get("user", {}))


@bp.route("/profile/ratings", methods=["GET"])
def get_profile_ratings():
	# Return user's ratings. In dev mode, return an empty list or a small mock.
	# If a DB table `ratings_user` or similar exists, attempt to read it.
	email = request.args.get("email")
	conn = get_db_connection()
	if not conn:
		# no DB -> return empty list so frontend can render a placeholder
		return jsonify([])

	try:
		cur = conn.cursor(dictionary=True)
		# best-effort: try a `user_ratings` table (adjust to your schema)
		try:
			cur.execute("SELECT production_id, user_rating, created_at FROM user_ratings WHERE user_email = %s ORDER BY created_at DESC LIMIT 50", (email,))
			rows = cur.fetchall()
			return jsonify(rows or [])
		except Exception:
			return jsonify([])
	finally:
		try:
			cur.close()
		except Exception:
			pass
		try:
			conn.close()
		except Exception:
			pass

