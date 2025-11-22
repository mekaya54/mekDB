"""
Database connection helper.

Provides `get_db_connection()` which returns a mysql.connector connection
or `None` if a connection cannot be established.
"""
import mysql.connector
from mysql.connector import Error
from backend.app.config import settings


def get_db_connection():
	try:
		conn = mysql.connector.connect(
			host=settings.DB_HOST,
			database=settings.DB_NAME,
			user=settings.DB_USER,
			password=settings.DB_PASS,
			autocommit=True,
		)
		if conn.is_connected():
			return conn
	except Error as e:
		# leave printing to the caller or logs; return None for fallback behaviour
		print(f"DB connection error: {e}")
	return None
