from flask import Blueprint, request, jsonify
from backend.app.db.connection import get_db_connection

bp = Blueprint("people", __name__, url_prefix="/api")


@bp.route("/people", methods=["GET"])
def search_people():
	q = request.args.get("search", "").strip()
	conn = get_db_connection()
	if conn is None:
		return jsonify([])

	try:
		cursor = conn.cursor(dictionary=True)
		sql = "SELECT person_id, primary_name, birth_year, death_year, primary_profession FROM people WHERE 1=1"
		params = []
		if q:
			sql += " AND primary_name LIKE %s"
			params.append(f"%{q}%")
		sql += " LIMIT 50"
		cursor.execute(sql, tuple(params))
		rows = cursor.fetchall()
		return jsonify(rows)
	except Exception as e:
		return jsonify({"error": str(e)}), 500
	finally:
		try:
			cursor.close()
		except Exception:
			pass
		try:
			conn.close()
		except Exception:
			pass


@bp.route("/people/<person_id>", methods=["GET"])
def get_person(person_id):
	conn = get_db_connection()
	if conn is None:
		return jsonify({}), 404

	try:
		cursor = conn.cursor(dictionary=True)
		cursor.execute("SELECT person_id, primary_name, birth_year, death_year, primary_profession FROM people WHERE person_id = %s LIMIT 1", (person_id,))
		row = cursor.fetchone()
		if not row:
			return jsonify({}), 404
		return jsonify(row)
	except Exception as e:
		return jsonify({"error": str(e)}), 500
	finally:
		try:
			cursor.close()
		except Exception:
			pass
		try:
			conn.close()
		except Exception:
			pass

