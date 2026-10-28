import logging
from flask import Flask
from .config import KONFIGURACJE
from app.converters import RegionConverter

def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    from .routes_api import api_bp
    from .routes_panel import panel_bp

    app.url_map.converters["region"] = RegionConverter

    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    return app