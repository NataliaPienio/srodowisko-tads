import csv
import io

_RAPORTY = []

def wczytaj_zamowienia(sciezka):
    zamowienia = []
    with open(sciezka, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_clean = {k.strip(): v.strip() for k, v in row.items()}
            zamowienia.append({
                "data": row_clean["data"],
                "region": row_clean["region"],
                "przychod": float(row_clean["przychod"]),
                "koszt": float(row_clean["koszt"]),
            })
    return zamowienia


def dostepne_regiony(sciezka):
    zamowienia = wczytaj_zamowienia(sciezka)
    regiony = sorted(list({z["region"] for z in zamowienia}))
    return regiony


def policz_wskazniki(sciezka, region=None, rok=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    if region is not None:
        zamowienia = [z for z in zamowienia if z["region"] == region]
    if rok is not None:
        zamowienia = [z for z in zamowienia if z["data"].startswith(str(rok))]

    liczba = len(zamowienia)
    przychod = sum(z["przychod"] for z in zamowienia)
    koszt = sum(z["koszt"] for z in zamowienia)

    if przychod == 0.0:
        marza = 0.0
    else:
        marza = round((przychod - koszt) / przychod, 4)

    return {
        "region": region,
        "liczba_zamowien": liczba,
        "przychod": przychod,
        "koszt": koszt,
        "marza": marza,
    }
def zestawienie_regionow(sciezka):
    regiony = dostepne_regiony(sciezka)
    return [policz_wskazniki(sciezka, region=r) for r in regiony]

def zapisz_raport(rok, region, uwagi=""):
    rekord = {"rok": int(rok), "region": str(region), "uwagi": str(uwagi)}
    _RAPORTY.append(rekord)
    return rekord


def raporty_roku(rok):
    return [r for r in _RAPORTY if r["rok"] == int(rok)]


def wykaz_raportow():
    return list(_RAPORTY)

def wczytaj_zbior(strumien):
    # Odczyt bajtów i dekodowanie UTF-8 (błąd automatycznie rzuci UnicodeDecodeError, który dziedziczy po ValueError)
    zawartosc = strumien.read().decode("utf-8")
    
    czytnik = csv.DictReader(io.StringIO(zawartosc))
    wymagane = {"data", "region", "przychod", "koszt"}
    obecne = set(czytnik.fieldnames or [])
    brakujace = sorted(wymagane - obecne)
    
    if brakujace:
        raise ValueError(f"brak kolumn: {', '.join(brakujace)}")
        
    wiersze = list(czytnik)
    return len(wiersze)