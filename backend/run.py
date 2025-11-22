from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Register modular routes if available
try:
    from backend.app.routes.auth import bp as auth_bp
    app.register_blueprint(auth_bp)
except Exception:
    pass

try:
    from backend.app.routes.people import bp as people_bp
    app.register_blueprint(people_bp)
except Exception:
    pass

try:
    from backend.app.routes.profile import bp as profile_bp
    app.register_blueprint(profile_bp)
except Exception:
    pass

# ---------------- MOCK DATA ---------------- #

MOCK_MOVIES = [
    {
        "production_id": 1,
        "primary_title": "The Matrix",
        "start_year": 1999,
        "runtime_minutes": 136,
        "poster_url": "https://example.com/matrix.jpg",
        "average_rating": 8.7,
        "num_votes": 1700000,
        "type": "movie",
    },
    {
        "production_id": 2,
        "primary_title": "Breaking Bad",
        "start_year": 2008,
        "runtime_minutes": 49,
        "poster_url": "https://example.com/breakingbad.jpg",
        "average_rating": 9.5,
        "num_votes": 2000000,
        "type": "tvSeries",
    },
    {
        "production_id": 3,
        "primary_title": "Chernobyl",
        "start_year": 2019,
        "runtime_minutes": 60,
        "poster_url": "https://example.com/chernobyl.jpg",
        "average_rating": 9.4,
        "num_votes": 800000,
        "type": "tvMiniSeries",
    },
    {
        "production_id": 4,
        "primary_title": "The Matrix Reloaded",
        "start_year": 2003,
        "runtime_minutes": 138,
        "poster_url": "https://example.com/matrix2.jpg",
        "average_rating": 7.2,
        "num_votes": 600000,
        "type": "movie",
    },
    {
        "production_id": 5,
        "primary_title": "Breaking Bad: Ozymandias",
        "start_year": 2013,
        "runtime_minutes": 47,
        "poster_url": "https://example.com/ozymandias.jpg",
        "average_rating": 10.0,
        "num_votes": 500000,
        "type": "tvEpisode",
    },
]

TYPE_GROUPS = {
    "movie": ["movie", "tvMovie"],
    "tvseries": ["tvSeries", "tvMiniSeries"],
    "tvepisode": ["tvEpisode"],
}


def filter_mock_movies(search_query: str, filter_type: str):
    movies = MOCK_MOVIES

    # search filter
    if search_query:
        q = search_query.lower()
        movies = [m for m in movies if q in m["primary_title"].lower()]

    # type filter
    ft = filter_type.lower()
    if ft in TYPE_GROUPS:
        allowed = set(TYPE_GROUPS[ft])
        movies = [m for m in movies if m["type"] in allowed]

    # sort by rating then votes
    movies = sorted(
        movies,
        key=lambda m: (
            m.get("average_rating") or 0,
            m.get("num_votes") or 0,
        ),
        reverse=True,
    )

    return movies


# ---------------- DB CONNECTION ---------------- #

def get_db_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            database=os.getenv('DB_NAME', 'imdb_project'),
            user=os.getenv('DB_USER', 'root'),
            password=os.getenv('DB_PASS', '')
        )
        if connection.is_connected():
            return connection
    except Error as e:
        print(f"Database Error: {e}")
        return None


# ---------------- ROUTES ---------------- #

@app.route("/api/movies", methods=['GET'])
def get_movies():
    search_query = request.args.get('search', '').strip()
    filter_type = request.args.get('type', 'all')

    conn = get_db_connection()
    if conn is None:
        # fallback to mock data
        movies = filter_mock_movies(search_query, filter_type)
        return jsonify(movies[:50])

    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            SELECT 
                p.production_id,
                p.primary_title,
                p.start_year,
                p.runtime_minutes,
                p.poster_url,
                r.average_rating,
                r.num_votes,
                t.type_name AS type
            FROM productions p
            LEFT JOIN title_types t ON p.type_id = t.type_id
            LEFT JOIN ratings r ON p.production_id = r.rating_id
            WHERE 1=1
        """
        params = []

        if search_query:
            sql += " AND p.primary_title LIKE %s"
            params.append(f"%{search_query}%")

        ft = filter_type.lower()
        if ft in TYPE_GROUPS:
            allowed = TYPE_GROUPS[ft]
            placeholders = ",".join(["%s"] * len(allowed))
            sql += f" AND t.type_name IN ({placeholders})"
            params.extend(allowed)

        sql += " ORDER BY r.average_rating DESC, r.num_votes DESC LIMIT 50"

        cursor.execute(sql, tuple(params))
        movies = cursor.fetchall()
        return jsonify(movies)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


@app.route("/api/movies/top", methods=['GET'])
def get_top_movies():
    conn = get_db_connection()

    groups = {
        "movies": ["movie", "tvMovie"],
        "series": ["tvSeries", "tvMiniSeries"],
        "episodes": ["tvEpisode"],
    }

    if conn is None:
        # fallback to mock data
        result = {}
        for key, types in groups.items():
            items = [m for m in MOCK_MOVIES if m["type"] in types]
            items = sorted(
                items,
                key=lambda m: (
                    m.get("average_rating") or 0,
                    m.get("num_votes") or 0,
                ),
                reverse=True,
            )
            result[key] = items[:10]
        return jsonify(result)

    cursor = conn.cursor(dictionary=True)

    try:
        result = {}

        base_sql = """
            SELECT 
                p.production_id,
                p.primary_title,
                p.start_year,
                p.runtime_minutes,
                p.poster_url,
                r.average_rating,
                r.num_votes,
                t.type_name AS type
            FROM productions p
            LEFT JOIN title_types t ON p.type_id = t.type_id
            LEFT JOIN ratings r ON p.production_id = r.rating_id
            WHERE t.type_name IN ({placeholders})
            ORDER BY r.average_rating DESC, r.num_votes DESC
            LIMIT 10
        """

        for key, types in groups.items():
            placeholders = ",".join(["%s"] * len(types))
            sql = base_sql.format(placeholders=placeholders)
            cursor.execute(sql, types)
            result[key] = cursor.fetchall()

        return jsonify(result)

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()


if __name__ == "__main__":
    app.run(debug=True)
