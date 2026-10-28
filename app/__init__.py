import logging
import time
from flask import Flask, g
from .config import KONFIGURACJE
from app.converters import RegionConverter
from app.errors import zarejestruj_obsluge_bledow


def create_app(nazwa_konfiguracji="rozwojowa"):
    app = Flask(__name__)
    app.config.from_object(KONFIGURACJE[nazwa_konfiguracji])
    app.logger.setLevel(logging.INFO)

    from .routes_api import api_bp
    from .routes_panel import panel_bp

    # Rejestracja konwertera (przed blueprintami)
    app.url_map.converters["region"] = RegionConverter

    # Procedury cyklu żądania: pomiar czasu i nagłówek X-Czas-Ms
    @app.before_request
    def before_request():
        g.start = time.perf_counter()

    @app.after_request
    def after_request(response):
        czas = (time.perf_counter() - g.start) * 1000
        response.headers["X-Czas-Ms"] = f"{czas:.2f}"
        return response

    # Rejestracja centralnej obsługi błędów
    zarejestruj_obsluge_bledow(app)

    # Rejestracja blueprintów (w tym wersja v2 pod przedrostkiem /api/v2)
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")

    return app