"""
Flask Blueprint providing movies-related API endpoints.

The endpoints mirror those implemented in the project's top-level `run.py`,
but are provided here as a modular blueprint so `run.py` or another
application factory can register them.
"""
from flask import Blueprint, request, jsonify
from backend.app.services.movie_service import search_movies, get_movie_by_id, get_top_by_groups
from backend.app.config.settings import DEFAULT_LIMIT

bp = Blueprint("movies", __name__, url_prefix="/api")


@bp.route("/movies", methods=["GET"])
def api_search_movies():
    q = request.args.get("search", "").strip()
    t = request.args.get("type", "all")
    try:
        limit = int(request.args.get("limit", DEFAULT_LIMIT))
    except Exception:
        limit = DEFAULT_LIMIT

    movies = search_movies(q, t, limit)
    return jsonify(movies)


@bp.route("/movies/home", methods=["GET"])
def api_home_movies():
    # returns grouped top items for home page
    top = get_top_by_groups(limit=10)
    return jsonify(top)


@bp.route("/movies/<production_id>", methods=["GET"])
def api_movie_detail(production_id):
    movie = get_movie_by_id(production_id)
    if movie is None:
        return jsonify({}), 404
    return jsonify(movie)
