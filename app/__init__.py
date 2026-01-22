# Student ID: 24071105
# Student Name: Riya Adhikari

from flask import Flask
from config import Config
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    csrf.init_app(app)

    # Initialize Database Connection
    from app.db import init_app
    init_app(app)
    
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
