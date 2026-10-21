from flask import Blueprint, request, abort, jsonify, current_app
from .services import policz_wskazniki, dostepne_regiony

api_bp = Blueprint("api", __name__)

# Zauważ: reguła trasy to "/kpi", przedrostek "/api" dodawany jest przy rejestracji
@api_bp.get("/kpi")
def kpi():
    region = request.args.get("region")
    sciezka = current_app.config["SCIEZKA_DANYCH"]

    if region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")

    dane = policz_wskazniki(sciezka, region)
    return jsonify(dane)