from __future__ import annotations

import math
from dataclasses import dataclass

MAKSYMALNY_CZAS = 1.0e100
MAKSYMALNA_LAMBDA = 1.0e100
MAKSYMALNY_RZĄD_ERLANGA = 10_000

_BEZPIECZNY_WYKŁADNIK_DZIESIĘTNY = 300.0


@dataclass(frozen=True)
class Wskaźniki:

    zawodność: float
    niezawodność: float
    gęstość: float
    intensywność_uszkodzeń: float | None
    średni_czas_pracy: float
    wariancja: float


def _ogranicz_prawdopodobieństwo(wartość: float) -> float:
    return min(1.0, max(0.0, wartość))


def _sprawdź_dane_wspólne(lambda_: float, t: float) -> None:
    if lambda_ <= 0:
        raise ValueError("Parametr lambda musi być liczbą dodatnią (lambda > 0).")
    if t < 0:
        raise ValueError("Chwila czasu t nie może być ujemna.")
    if lambda_ > MAKSYMALNA_LAMBDA:
        raise ValueError(
            f"Lambda jest zbyt duża (maks. {MAKSYMALNA_LAMBDA:g} 1/h) -- "
            "większa wartość powodowałaby przepełnienie obliczeń."
        )
    if t > MAKSYMALNY_CZAS:
        raise ValueError(
            f"Czas t jest zbyt duży (maks. {MAKSYMALNY_CZAS:g} h) -- "
            "większa wartość powodowałaby przepełnienie obliczeń."
        )


def wskaźniki_wykładnicze(lambda_: float, t: float) -> Wskaźniki:
    _sprawdź_dane_wspólne(lambda_, t)

    try:
        niezawodność = _ogranicz_prawdopodobieństwo(math.exp(-lambda_ * t))
        gęstość = lambda_ * niezawodność
        średni_czas_pracy = 1.0 / lambda_
        wariancja = 1.0 / lambda_**2
    except OverflowError as błąd:
        raise ValueError(
            "Wprowadzone wartości są zbyt duże -- wystąpiłoby przepełnienie "
            "obliczeń. Wprowadź mniejsze t lub lambda."
        ) from błąd

    zawodność = _ogranicz_prawdopodobieństwo(1.0 - niezawodność)
    intensywność_uszkodzeń = lambda_

    return Wskaźniki(
        zawodność, niezawodność, gęstość, intensywność_uszkodzeń, średni_czas_pracy, wariancja
    )


def wskaźniki_erlanga(rząd: int, lambda_: float, t: float) -> Wskaźniki:
    _sprawdź_dane_wspólne(lambda_, t)
    if rząd < 1:
        raise ValueError("Rząd rozkładu Erlanga musi być liczbą całkowitą >= 1.")
    if rząd > MAKSYMALNY_RZĄD_ERLANGA:
        raise ValueError(
            f"Rząd rozkładu Erlanga jest zbyt duży (maks. {MAKSYMALNY_RZĄD_ERLANGA})."
        )

    lambda_t = lambda_ * t
    if lambda_t > 1 and (rząd - 1) * math.log10(lambda_t) > _BEZPIECZNY_WYKŁADNIK_DZIESIĘTNY:
        raise ValueError(
            "Takie połączenie t, lambda i rzędu Erlanga powoduje przepełnienie "
            "obliczeń (wartości pośrednie przekraczają zakres liczb "
            "zmiennoprzecinkowych). Zmniejsz t, lambda lub rząd r."
        )

    try:
        zanik = math.exp(-lambda_t)
        niezawodność = _ogranicz_prawdopodobieństwo(
            sum(zanik * lambda_t**k / math.factorial(k) for k in range(rząd))
        )
        zawodność = _ogranicz_prawdopodobieństwo(1.0 - niezawodność)
        gęstość = lambda_ * lambda_t ** (rząd - 1) / math.factorial(rząd - 1) * zanik
        średni_czas_pracy = rząd / lambda_
        wariancja = rząd / lambda_**2
    except OverflowError as błąd:
        raise ValueError(
            "Wprowadzone wartości są zbyt duże -- wystąpiłoby przepełnienie "
            "obliczeń. Wprowadź mniejsze t, lambda lub rząd r."
        ) from błąd

    intensywność_uszkodzeń = gęstość / niezawodność if niezawodność > 0 else None

    return Wskaźniki(
        zawodność, niezawodność, gęstość, intensywność_uszkodzeń, średni_czas_pracy, wariancja
    )
