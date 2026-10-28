from flask import request, abort


def parametr_int(nazwa: str, minimum: int, maksimum: int) -> int:
    if nazwa not in request.args:
        abort(400, description=f"Brak parametru {nazwa}")

    try:
        wartosc = int(request.args.get(nazwa))
    except (ValueError, TypeError):
        abort(400, description=f"Parametr {nazwa} nie jest liczba")

    if not (minimum <= wartosc <= maksimum):
        abort(422, description=f"Parametr {nazwa} poza zakresem {minimum}-{maksimum}")

    return wartosc