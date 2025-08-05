from flask import Flask
from flask_cors import CORS
from flask_smorest import Api
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

from .routes.health import blp as health_blp

# Load environment variables
load_dotenv()

def create_app():
    """Factory to create app and register blueprints/models."""
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    # CORS
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Config
    app.config["API_TITLE"] = "My Flask API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = ""
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["OPENAPI_URL_PREFIX"] = "/docs"
    # JWT Secret Key
    app.config["JWT_SECRET_KEY"] = os.environ.get("JWT_SECRET_KEY", "dev-secret")
    # Database config (default sqlite for demo)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "DATABASE_URL", "sqlite:///notes.db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Extensions
    from .models import db
    db.init_app(app)

    api = Api(app)
    # Register blueprints
    api.register_blueprint(health_blp)
    from .routes.notes import blp as notes_blp
    api.register_blueprint(notes_blp)
    from .routes.auth import blp as auth_blp
    api.register_blueprint(auth_blp)

    # Create tables on first launch (for demo)
    @app.before_first_request
    def create_tables():
        db.create_all()

    return app

# Allow for 'from app import app' usage in run.py
app = create_app()
