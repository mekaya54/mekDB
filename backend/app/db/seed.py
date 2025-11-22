"""
Database seeding helpers.

This script provides a programmatic way to execute SQL files found in
the repository `database/table_creation` folder. It is intentionally
minimal and intended for local development only.
"""
import os
from glob import glob
from backend.app.db.connection import get_db_connection


def _read_sql_file(path: str) -> str:
	with open(path, "r", encoding="utf-8") as f:
		return f.read()


def apply_all_sql(folder: str = None):
	folder = folder or os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "database", "table_creation"))
	sql_files = sorted(glob(os.path.join(folder, "*.sql")))
	if not sql_files:
		print("No SQL files found in:", folder)
		return

	conn = get_db_connection()
	if conn is None:
		print("DB connection unavailable; cannot apply SQL files.")
		return

	try:
		cursor = conn.cursor()
		for p in sql_files:
			print("Applying:", p)
			sql = _read_sql_file(p)
			try:
				cursor.execute(sql)
			except Exception as e:
				# If file contains multiple statements, try executing via executescript-like loop
				statements = [s.strip() for s in sql.split(";") if s.strip()]
				for stmt in statements:
					try:
						cursor.execute(stmt)
					except Exception as e2:
						print(f"Failed statement in {p}:", e2)
		conn.commit()
	finally:
		try:
			cursor.close()
		except Exception:
			pass
		try:
			conn.close()
		except Exception:
			pass


if __name__ == "__main__":
	apply_all_sql()

