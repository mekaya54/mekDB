from flask import Flask, jsonify, request
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

# ---------------- MOCK DATA ----------------- #

MOCK_MOVIES = [
    {
        "production_id": "1",
        "primary_title": "The Matrix",
        "start_year": 1999,
        "runtime_minutes": 136,
        "poster_url": "http://image.tmdb.org/t/p/original/2lECpi35Hnbpa4y46JX0aY3AWTy.jpg",
        "average_rating": 8.7,
        "num_votes": 1700000,
        "type": "movie",
        "genres": ["Action", "Sci-Fi"]
    },
    {
        "production_id": "2",
        "primary_title": "Breaking Bad",
        "start_year": 2008,
        "runtime_minutes": 49,
        "poster_url": "https://image.tmdb.org/t/p/original/5kAGbi9MFAobQTVfK4kWPnIfnP0.jpg",
        "average_rating": 9.5,
        "num_votes": 2000000,
        "type": "tvSeries",
        "genres": ["Crime", "Drama"]
    },
    {
        "production_id": "3",
        "primary_title": "Chernobyl",
        "start_year": 2019,
        "runtime_minutes": 60,
        "poster_url": "https://image.tmdb.org/t/p/original//hTP1DtLGFamjfu8WqjnuQdP1n4i.jpg",
        "average_rating": 9.4,
        "num_votes": 800000,
        "type": "tvMiniSeries",
        "genres": ["Drama", "History"]
    },
    {
        "production_id": "4",
        "primary_title": "Avengers: Endgame",
        "start_year": 2019,
        "runtime_minutes": 181,
        "poster_url": "https://image.tmdb.org/t/p/w500/or06FN3Dka5tukK1e9sl16pB3iy.jpg",
        "average_rating": 8.4,
        "num_votes": 1200000,
        "type": "movie",
        "genres": ["Action", "Adventure"]
    },
    {
        "production_id": "5",
        "primary_title": "Game of Thrones",
        "start_year": 2011,
        "runtime_minutes": 57,
        "poster_url": "https://image.tmdb.org/t/p/w1280/gwPSoYUHAKmdyVywgLpKKA4BjRr.jpg",
        "average_rating": 9.2,
        "num_votes": 2200000,
        "type": "tvSeries",
        "genres": ["Action", "Adventure"]
    },
    {
        "production_id": "6",
        "primary_title": "The Godfather",
        "start_year": 1972,
        "runtime_minutes": 175,
        "poster_url": "https://m.media-amazon.com/images/M/MV5BM2MyNjYxNmUtYTAwNi00MTYxLWJmNWYtYzZlODY3ZTk3OTFlXkEyXkFqcGdeQXVyNzkwMjQ5NzM@._V1_FMjpg_UX1000_.jpg",
        "average_rating": 9.2,
        "num_votes": 1700000,
        "type": "movie",
        "genres": ["Crime", "Drama"],
    }
]


TYPE_GROUPS = {
    "movie": ["movie", "tvMovie"],
    "tvseries": ["tvSeries", "tvMiniSeries"],
    "tvepisode": ["tvEpisode"],
}

TYPE_GROUPS = {
    "movie": ["movie", "tvMovie"],
    "tvseries": ["tvSeries", "tvMiniSeries"],
    "tvepisode": ["tvEpisode"],
}


def filter_data(search_query, filter_type):
    results = MOCK_MOVIES
    
    if search_query:
        q = search_query.lower()
        results = [m for m in results if q in m["primary_title"].lower()]

    ft = filter_type.lower() if filter_type else "all"
    if ft != "all" and ft in TYPE_GROUPS:
        allowed = set(TYPE_GROUPS[ft])
        results = [m for m in results if m["type"] in allowed]
    elif ft != "all":
        results = [m for m in results if m["type"].lower() == ft]

    return results


@app.route("/", methods=["GET"])
def index():
    return jsonify({"status": "ok", "message": "Backend is running in Mock Mode"})


@app.route("/api/movies", methods=['GET'])
def get_movies():
    search_query = request.args.get('search', '').strip()
    filter_type = request.args.get('type', 'all')
    
    movies = filter_data(search_query, filter_type)
    
    response = {
        "results": movies,
        "page": 1,
        "total_pages": 1,
        "total_results": len(movies)
    }
    return jsonify(response)


@app.route("/api/movies/home", methods=['GET'])
def get_home_movies():
    result = {}
    for key, types in {
        "movies": ["movie"], 
        "series": ["tvSeries", "tvMiniSeries"], 
        "episodes": ["tvEpisode"]
    }.items():
        items = [m for m in MOCK_MOVIES if m["type"] in types]
        items = sorted(items, key=lambda x: x["average_rating"], reverse=True)
        result[key] = items[:10]
    
    return jsonify(result)


@app.route("/api/movies/<production_id>", methods=['GET'])
def get_movie_detail(production_id):
    movie = next((m for m in MOCK_MOVIES if m["production_id"] == production_id), None)
    if movie:
        detail_response = movie.copy()
        detail_response["cast"] = [
            {"name": "Mock Actor 1", "characters": "Hero"},
            {"name": "Mock Actor 2", "characters": "Villain"}
        ]
        detail_response["crew"] = [
            {"name": "Mock Director", "job": "Director"}
        ]
        return jsonify(detail_response)
    return jsonify({"error": "Not found"}), 404


@app.route("/api/auth/login", methods=['POST'])
def login():
    data = request.json or {}
    email = data.get('email', 'user@example.com')
    return jsonify({
        "token": "mock-token-123",
        "user": {"username": email.split('@')[0], "email": email}
    })


if __name__ == "__main__":
    app.run(debug=True, port=5000)