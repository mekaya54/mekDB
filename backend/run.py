from flask import Flask, jsonify
from flask_cors import CORS
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

try:
    from backend.app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
except Exception as e:
    print(f"Error registering auth blueprint: {e}")

try:
    from backend.app.routes.people import bp as people_bp
    app.register_blueprint(people_bp)
except Exception as e:
    print(f"Error registering people blueprint: {e}")

try:
    from backend.app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp)
except Exception as e:
    print(f"Error registering profile blueprint: {e}")

try:
    from backend.app.routes.movies import bp as movies_bp
    app.register_blueprint(movies_bp)
except Exception as e:
    print(f"Error registering movies blueprint: {e}")

# ---------------- MOCK DATA ---------------- #

# MOCK_MOVIES = [
#    {
#       "production_id": 1,
#        "primary_title": "The Matrix",
#        "start_year": 1999,
#        "runtime_minutes": 136,
#        "poster_url": "https://example.com/matrix.jpg",
#        "average_rating": 8.7,
#        "num_votes": 1700000,
#        "type": "movie",
#    },
# {
#     "production_id": 2,
#     "primary_title": "Breaking Bad",
#     "start_year": 2008,
#     "runtime_minutes": 49,
#     "poster_url": "https://example.com/breakingbad.jpg",
#     "average_rating": 9.5,
#     "num_votes": 2000000,
#     "type": "tvSeries",
# },
# {
#     "production_id": 3,
#     "primary_title": "Chernobyl",
#     "start_year": 2019,
#     "runtime_minutes": 60,
#     "poster_url": "https://example.com/chernobyl.jpg",
#     "average_rating": 9.4,
#     "num_votes": 800000,
#     "type": "tvMiniSeries",
# },
# {
#     "production_id": 4,
#     "primary_title": "The Matrix Reloaded",
#     "start_year": 2003,
#     "runtime_minutes": 138,
#     "poster_url": "https://example.com/matrix2.jpg",
#     "average_rating": 7.2,
#     "num_votes": 600000,
#     "type": "movie",
# },
# {
#     "production_id": 5,
#     "primary_title": "Breaking Bad: Ozymandias",
#     "start_year": 2013,
#     "runtime_minutes": 47,
#     "poster_url": "https://example.com/ozymandias.jpg",
#     "average_rating": 10.0,
#     "num_votes": 500000,
#     "type": "tvEpisode",
# },
# ]

@app.route("/", methods=["GET"])
def index():
    return jsonify({
        "status": "active",
        "message": "ByteSizedDB API is running",
        "version": "1.0.0"
    })


if __name__ == "__main__":
    debug_mode = os.getenv("FLASK_DEBUG", "True") == "True"
    app.run(debug=debug_mode, port=5000)
