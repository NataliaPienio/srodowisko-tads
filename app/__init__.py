from datetime import date
import logging
import time
from flask import Flask, g
from flask_wtf.csrf import CSRFProtect
from .config import KONFIGURACJE
from app.converters import RegionConverter
from app.errors import zarejestruj_obsluge_bledow
from app.filters import zarejestruj_filtry
from app.services import dostepne_regiony

csrf = CSRFProtect()


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

    # Włączenie ochrony CSRF (po procedurach before_request i after_request)
    csrf.init_app(app)

    # Rejestracja centralnej obsługi błędów
    zarejestruj_obsluge_bledow(app)

    # Zadanie 2: Rejestracja filtrów Jinja2
    zarejestruj_filtry(app)

    # Zadanie 2: Procesor kontekstu dostarczający wspólne dane do szablonów
    @app.context_processor
    def dane_wspolne():
        return {
            "regiony": dostepne_regiony(app.config["SCIEZKA_DANYCH"]),
            "rok_biezacy": date.today().year,
        }

    # Rejestracja blueprintów (w tym wersja v2 pod przedrostkiem /api/v2)
    app.register_blueprint(panel_bp)
    app.register_blueprint(api_bp, url_prefix="/api")
    app.register_blueprint(api_bp, url_prefix="/api/v2", name="api_v2")

    return app