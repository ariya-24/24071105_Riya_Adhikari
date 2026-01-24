# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect
from datetime import timedelta
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

csrf = CSRFProtect()
db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    csrf.init_app(app)

    # Session security settings
    app.config['SESSION_COOKIE_SECURE'] = True  # Only send cookies over HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True  # Prevent JS access to cookies
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
    app.permanent_session_lifetime = timedelta(minutes=30)  # Session timeout

    # Initialize SQLAlchemy and Flask-Migrate
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    from app.main.routes import main
    from app.auth.routes import auth
    from app.booking.routes import booking
    from app.admin.routes import admin

    app.register_blueprint(main)
    app.register_blueprint(auth, url_prefix='/auth')
    app.register_blueprint(booking, url_prefix='/booking')
    app.register_blueprint(admin, url_prefix='/admin')

    return app