import csv

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

def policz_wskazniki(sciezka, region=None):
    zamowienia = wczytaj_zamowienia(sciezka)
    if region is not None:
        zamowienia = [z for z in zamowienia if z["region"] == region]

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