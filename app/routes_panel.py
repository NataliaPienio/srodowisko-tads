from flask import Blueprint, request, abort, current_app, redirect, url_for
from .services import (
    policz_wskazniki,
    dostepne_regiony,
    raporty_roku,
    zapisz_raport,
    wczytaj_zamowienia,
)

panel_bp = Blueprint("panel", __name__)

ROK_DOMYSLNY = 2026


@panel_bp.get("/")
def index():
    return "Panel wskaźników"


@panel_bp.get("/kpi")
def kpi():
    region = request.args.get("region")
    sciezka = current_app.config["SCIEZKA_DANYCH"]

    if region is not None and region not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {region}")

    dane = policz_wskazniki(sciezka, region)
    current_app.logger.info("Obliczono wskaźniki dla regionu %s", dane["region"])

    nazwa_regionu = dane["region"] if dane["region"] else "Wszystkie"
    return f"<h1>Wskaźniki: {nazwa_regionu}</h1><p>Marża: {dane['marza']:.2%}</p>"


@panel_bp.get("/regiony/<region:kod>")
def region(kod):
    sciezka = current_app.config["SCIEZKA_DANYCH"]
    if kod not in dostepne_regiony(sciezka):
        abort(404, description=f"Nieznany region: {kod}")

    wszystkie_zamowienia = wczytaj_zamowienia(sciezka)
    liczba = len([z for z in wszystkie_zamowienia if z["region"] == kod])

    return f"<h1>Region {kod}</h1><p>Zamówień: {liczba}</p>"


@panel_bp.get("/raporty/", defaults={"rok": ROK_DOMYSLNY})
@panel_bp.get("/raporty/<int(min=2020, max=2030):rok>")
def raport(rok):
    n = len(raporty_roku(rok))
    return f"<h1>Raport {rok}</h1><p>Zapisane raporty: {n}</p>"


@panel_bp.route("/raporty/nowy", methods=["GET", "POST"])
def nowy_raport():
    if request.method == "GET":
        return "<p>Instrukcja zapisu raportu</p>"

    sciezka = current_app.config["SCIEZKA_DANYCH"]
    rok = request.form.get("rok", type=int)
    kod_regionu = request.form.get("region")

    if rok is None or kod_regionu not in dostepne_regiony(sciezka):
        abort(400, description="Niepoprawne dane formularza")

    if not (2020 <= rok <= 2030):
        abort(422, description="Rok poza zakresem 2020-2030")

    zapisz_raport(rok, kod_regionu)
    return redirect(url_for("panel.raport", rok=rok), code=303)


@panel_bp.get("/stary-panel")
def stary_panel():
    return redirect(url_for("panel.kpi"), code=301)