from flask import Flask
from flask_cors import CORS

# Route imports
from backend.app.routes import auth, movies, people, profile

def create_app():
    app = Flask(__name__)
    
    # CORS settings (To allow Frontend to access Backend)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Register blueprints
    app.register_blueprint(auth.bp)
    app.register_blueprint(movies.bp)
    app.register_blueprint(people.bp)
    app.register_blueprint(profile.bp)
    
    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="127.0.0.1", port=5000, debug=True)