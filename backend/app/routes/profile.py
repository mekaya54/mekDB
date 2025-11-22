from flask import Blueprint, jsonify, request
from backend.app.db.connection import get_db_connection
from backend.app.services.profile_service import get_profile_for_email

bp = Blueprint("profile", __name__, url_prefix="/api")


@bp.route("/profile", methods=["GET"])
def get_profile():
	email = request.args.get("email") or "dev@local"
	result = get_profile_for_email(email)
	return jsonify(result)


@bp.route("/profile/me", methods=["GET"])
def get_profile_me():
	email = request.args.get("email") or "dev@local"
	result = get_profile_for_email(email)
	return jsonify(result.get("user", {}))


@bp.route("/profile/ratings", methods=["GET"])
def get_profile_ratings():
	email = request.args.get("email")
	conn = get_db_connection()
	if not conn:
		return jsonify([])

	try:
		cur = conn.cursor(dictionary=True)
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

