from flask import Flask
from app.config import Config
from app.models.db import mysql

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    mysql.init_app(app)

    from app.home.routes import home_bp
    from app.analytics.routes import analytics_bp
    from app.inventory.routes import inventory_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(analytics_bp)
    app.register_blueprint(inventory_bp)

    return app
