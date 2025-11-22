"""
Simple auth routes (mocked for local development).

This module intentionally implements lightweight login/signup behavior
without persistence. It is meant for development and frontend integration
tests. Replace with real auth in production.
"""
from flask import Blueprint, request, jsonify

bp = Blueprint("auth", __name__, url_prefix="/api")


@bp.route("/auth/login", methods=["POST"])
def login():
	data = request.get_json() or {}
	email = data.get("email")
	password = data.get("password")
	if not email or not password:
		return jsonify({"error": "email and password required"}), 400

	# Mock authentication: accept any credentials and return a user object
	user = {
		"username": email.split("@")[0],
		"email": email,
		"avatarUrl": f"https://api.dicebear.com/7.x/avataaars/svg?seed={email}",
	}

	return jsonify({"user": user, "token": "dev-token"})


@bp.route("/auth/signup", methods=["POST"])
def signup():
	data = request.get_json() or {}
	email = data.get("email")
	password = data.get("password")
	if not email or not password:
		return jsonify({"error": "email and password required"}), 400

	# Mock signup: simply echo the created user
	user = {
		"username": email.split("@")[0],
		"email": email,
		"avatarUrl": f"https://api.dicebear.com/7.x/avataaars/svg?seed={email}",
	}

	return jsonify({"user": user, "token": "dev-token"}), 201

