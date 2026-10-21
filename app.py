from flask import Flask, request, abort, jsonify
from services import policz_wskazniki, dostepne_regiony

app = Flask(__name__)
SCIEZKA_DANYCH = "dane/zamowienia.csv"

@app.get("/")
def index():
    return "Panel wskaźników"

@app.get("/kpi")
def kpi():
    region = request.args.get("region")
    
    # Sprawdzamy region TYLKO gdy został podany w adresie URL
    if region is not None and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    
    dane = policz_wskazniki(SCIEZKA_DANYCH, region)
    
    # Etykieta nagłówka zależna od tego, czy wybrano region
    nazwa_regionu = dane["region"] if dane["region"] else "Wszystkie"
    return f"<h1>Wskaźniki: {nazwa_regionu}</h1><p>Marża: {dane['marza']:.2%}</p>"

@app.get("/api/kpi")
def api_kpi():
    region = request.args.get("region")
    
    if region is not None and region not in dostepne_regiony(SCIEZKA_DANYCH):
        abort(404, description=f"Nieznany region: {region}")
    
    dane = policz_wskazniki(SCIEZKA_DANYCH, region)
    return jsonify(dane)