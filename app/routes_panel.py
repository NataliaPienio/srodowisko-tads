from flask import Blueprint, request, abort, current_app
from .services import policz_wskazniki, dostepne_regiony

panel_bp = Blueprint("panel", __name__)

@panel_bp.get("/")
def index():
    return "Panel wskaźników"

@panel_bp.get("/kpi")
def kpi():
    region = request.args.get("region")
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    
    # 1. Sprawdzamy błąd 404 TYLKO wtedy, gdy parametr region został w ogóle podany
    if region is not None and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")
    
    # 2. Jeśli region to None, policz_wskazniki policzy marżę dla całej bazy
    dane = policz_wskazniki(sciezka, region)
    
    # 3. Zapis do dziennika
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", dane["region"])
    
    nazwa_regionu = dane["region"] if dane["region"] else "Wszystkie"
    return f"<h1>Wskaźniki: {nazwa_regionu}</h1><p>Marża: {dane['marza']:.2%}</p>"