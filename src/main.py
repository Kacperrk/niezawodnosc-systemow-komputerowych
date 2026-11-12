from __future__ import annotations

import re
import tkinter as tk
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from tkinter import messagebox, ttk

from niezawodnosc import Wskaźniki, wskaźniki_erlanga, wskaźniki_wykładnicze

WZORZEC_ZMIENNOPRZECINKOWY = re.compile(r"^\d*([.,]\d*)?$")
WZORZEC_CAŁKOWITY = re.compile(r"^\d*$")

KATALOG_WYNIKÓW = Path(__file__).resolve().parent / "wyniki"
PLIK_WYNIKÓW = KATALOG_WYNIKÓW / "wyniki_niezawodnosc.txt"

DANE_TESTOWE: list[tuple[str, str, str, str]] = [
    ("Test 1", "10", "0.1", "2"),
    ("Test 2", "100", "0.01", "5"),
    ("Test 3", "20", "0.05", "4"),
]

WIERSZE: list[tuple[str, str, str]] = [
    ("Funkcja zawodności F(t)", "-", "zawodność"),
    ("Funkcja niezawodności R(t)", "-", "niezawodność"),
    ("Gęstość prawdopodobieństwa f(t)", "1/h", "gęstość"),
    ("Intensywność uszkodzeń λ(t)", "1/h", "intensywność_uszkodzeń"),
    ("Średni czas poprawnej pracy T", "h", "średni_czas_pracy"),
    ("Wariancja czasu pracy σ²", "h²", "wariancja"),
]


@dataclass
class WynikObliczeń:

    t: float
    lambda_: float
    rząd: int
    wykładniczy: Wskaźniki
    erlanga: Wskaźniki


def formatuj_wartość(wartość: float | None) -> str:
    if wartość is None:
        return "brak danych (R(t)=0)"
    return f"{wartość:.6g}"


class AplikacjaNiezawodność(ttk.Frame):

    def __init__(self, nadrzędne: tk.Tk) -> None:
        super().__init__(nadrzędne, padding=12)
        self.nadrzędne = nadrzędne
        self.ostatni_wynik: WynikObliczeń | None = None

        self._zbuduj_sekcję_danych_wejściowych()
        self._zbuduj_tabelę_wyników()
        self._zbuduj_przyciski()

        self.grid(sticky="nsew")
        nadrzędne.columnconfigure(0, weight=1)
        nadrzędne.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)

    def _zbuduj_sekcję_danych_wejściowych(self) -> None:
        waliduj_float = (self.register(self._waliduj_zmiennoprzecinkowy), "%P")
        waliduj_int = (self.register(self._waliduj_całkowity), "%P")

        ramka = ttk.LabelFrame(self, text="Dane wejściowe", padding=10)
        ramka.grid(row=0, column=0, sticky="ew", pady=(0, 10))
        ramka.columnconfigure(1, weight=1)

        ttk.Label(ramka, text="Chwila czasu t [godziny]:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.zmienna_t = tk.StringVar()
        ttk.Entry(
            ramka, textvariable=self.zmienna_t, validate="key", validatecommand=waliduj_float
        ).grid(row=0, column=1, sticky="ew", padx=(8, 0))

        ttk.Label(ramka, text="Intensywność uszkodzeń lambda [1/godziny]:").grid(
            row=1, column=0, sticky="w", pady=2
        )
        self.zmienna_lambda = tk.StringVar()
        ttk.Entry(
            ramka, textvariable=self.zmienna_lambda, validate="key", validatecommand=waliduj_float
        ).grid(row=1, column=1, sticky="ew", padx=(8, 0))

        ttk.Label(ramka, text="Rząd rozkładu Erlanga r (dodatnia liczba całkowita):").grid(
            row=2, column=0, sticky="w", pady=2
        )
        self.zmienna_rząd = tk.StringVar()
        ttk.Entry(
            ramka, textvariable=self.zmienna_rząd, validate="key", validatecommand=waliduj_int
        ).grid(row=2, column=1, sticky="ew", padx=(8, 0))

        ramka_testów = ttk.Frame(ramka)
        ramka_testów.grid(row=3, column=0, columnspan=2, sticky="w", pady=(8, 0))
        ttk.Label(ramka_testów, text="Dane przykładowe:").grid(row=0, column=0, padx=(0, 8))
        for indeks, (etykieta, t, lambda_, rząd) in enumerate(DANE_TESTOWE):
            ttk.Button(
                ramka_testów,
                text=etykieta,
                command=lambda t=t, lambda_=lambda_, rząd=rząd: self.wklej_dane_testowe(
                    t, lambda_, rząd
                ),
            ).grid(row=0, column=indeks + 1, padx=(0, 6))

    def _zbuduj_tabelę_wyników(self) -> None:
        ramka = ttk.LabelFrame(self, text="Wyniki obliczeń", padding=10)
        ramka.grid(row=1, column=0, sticky="nsew", pady=(0, 10))
        self.rowconfigure(1, weight=1)
        ramka.columnconfigure(0, weight=1)

        kolumny = ("wskaźnik", "jednostka", "wykładniczy", "erlanga")
        self.tabela = ttk.Treeview(ramka, columns=kolumny, show="headings", height=len(WIERSZE))
        self.tabela.heading("wskaźnik", text="Wskaźnik")
        self.tabela.heading("jednostka", text="Jednostka")
        self.tabela.heading("wykładniczy", text="Rozkład wykładniczy")
        self.tabela.heading("erlanga", text="Rozkład Erlanga")
        self.tabela.column("wskaźnik", width=260, anchor="w")
        self.tabela.column("jednostka", width=70, anchor="center")
        self.tabela.column("wykładniczy", width=160, anchor="center")
        self.tabela.column("erlanga", width=160, anchor="center")
        self.tabela.grid(row=0, column=0, sticky="nsew")

        for etykieta, jednostka, _pole in WIERSZE:
            self.tabela.insert("", "end", values=(etykieta, jednostka, "-", "-"))

    def _zbuduj_przyciski(self) -> None:
        ramka = ttk.Frame(self)
        ramka.grid(row=2, column=0, sticky="ew")

        ttk.Button(ramka, text="Oblicz", command=self.oblicz).grid(row=0, column=0, padx=(0, 8))
        self.przycisk_zapisz = ttk.Button(
            ramka,
            text="Zapisz wynik do pliku wyników",
            command=self.zapisz_do_pliku,
            state="disabled",
        )
        self.przycisk_zapisz.grid(row=0, column=1)

        self.etykieta_status = ttk.Label(ramka, text="", foreground="#1a7a1a")
        self.etykieta_status.grid(row=0, column=2, padx=(12, 0), sticky="w")

    @staticmethod
    def _waliduj_zmiennoprzecinkowy(proponowana: str) -> bool:
        return bool(WZORZEC_ZMIENNOPRZECINKOWY.match(proponowana))

    @staticmethod
    def _waliduj_całkowity(proponowana: str) -> bool:
        return bool(WZORZEC_CAŁKOWITY.match(proponowana))

    def wklej_dane_testowe(self, t: str, lambda_: str, rząd: str) -> None:
        self.zmienna_t.set(t)
        self.zmienna_lambda.set(lambda_)
        self.zmienna_rząd.set(rząd)

    def _wczytaj_dane_wejściowe(self) -> tuple[float, float, int]:
        tekst_t = self.zmienna_t.get().strip().replace(",", ".")
        tekst_lambda = self.zmienna_lambda.get().strip().replace(",", ".")
        tekst_rząd = self.zmienna_rząd.get().strip()

        if not tekst_t:
            raise ValueError("Wprowadź chwilę czasu t w godzinach [h].")
        if not tekst_lambda:
            raise ValueError("Wprowadź intensywność uszkodzeń lambda w [1/h].")
        if not tekst_rząd:
            raise ValueError("Wprowadź rząd rozkładu Erlanga r (liczba całkowita >= 1).")

        try:
            t = float(tekst_t)
        except ValueError as błąd:
            raise ValueError("Czas t musi być liczbą, np. 100 lub 100.5 [h].") from błąd

        try:
            lambda_ = float(tekst_lambda)
        except ValueError as błąd:
            raise ValueError("Lambda musi być liczbą, np. 0.001 [1/h].") from błąd

        try:
            rząd = int(tekst_rząd)
        except ValueError as błąd:
            raise ValueError("Rząd rozkładu Erlanga musi być liczbą całkowitą, np. 3.") from błąd

        return t, lambda_, rząd

    def oblicz(self) -> None:
        try:
            t, lambda_, rząd = self._wczytaj_dane_wejściowe()
            wykładniczy = wskaźniki_wykładnicze(lambda_, t)
            erlanga = wskaźniki_erlanga(rząd, lambda_, t)
        except ValueError as błąd:
            messagebox.showerror("Błąd danych wejściowych", str(błąd))
            return

        for id_wiersza, (_etykieta, _jednostka, pole) in zip(self.tabela.get_children(), WIERSZE):
            wartość_wykładnicza = formatuj_wartość(getattr(wykładniczy, pole))
            wartość_erlanga = formatuj_wartość(getattr(erlanga, pole))
            self.tabela.set(id_wiersza, "wykładniczy", wartość_wykładnicza)
            self.tabela.set(id_wiersza, "erlanga", wartość_erlanga)

        self.ostatni_wynik = WynikObliczeń(t, lambda_, rząd, wykładniczy, erlanga)
        self.przycisk_zapisz.state(["!disabled"])

    def zapisz_do_pliku(self) -> None:
        if self.ostatni_wynik is None:
            return

        KATALOG_WYNIKÓW.mkdir(parents=True, exist_ok=True)
        numer_testu = self._następny_numer_testu()

        with open(PLIK_WYNIKÓW, "a", encoding="utf-8") as plik:
            plik.write(self._renderuj_wpis(numer_testu))

        self.etykieta_status.config(text=f"Zapisano test nr {numer_testu}")

    @staticmethod
    def _następny_numer_testu() -> int:
        if not PLIK_WYNIKÓW.exists():
            return 1
        treść = PLIK_WYNIKÓW.read_text(encoding="utf-8")
        return treść.count("Test nr ") + 1

    def _renderuj_wpis(self, numer_testu: int) -> str:
        wynik = self.ostatni_wynik
        assert wynik is not None

        linie = [
            "=" * 84,
            f"Test nr {numer_testu} -- {datetime.now():%Y-%m-%d %H:%M:%S}",
            "Wskaźniki niezawodności obiektów nienaprawialnych",
            "",
            "Dane wejściowe:",
            f"  Chwila czasu t = {wynik.t:g} h",
            f"  Intensywność uszkodzeń lambda = {wynik.lambda_:g} 1/h",
            f"  Rząd rozkładu Erlanga r = {wynik.rząd}",
            "",
            f"{'Wskaźnik':38}{'Jednostka':10}{'Wykładniczy':18}{'Erlang':18}",
            "-" * 84,
        ]
        for etykieta, jednostka, pole in WIERSZE:
            wartość_wykładnicza = formatuj_wartość(getattr(wynik.wykładniczy, pole))
            wartość_erlanga = formatuj_wartość(getattr(wynik.erlanga, pole))
            linie.append(f"{etykieta:38}{jednostka:10}{wartość_wykładnicza:18}{wartość_erlanga:18}")

        return "\n".join(linie) + "\n\n"


def main() -> None:
    okno = tk.Tk()
    okno.title("Wskaźniki niezawodności - rozkład wykładniczy i Erlanga")
    okno.minsize(760, 420)
    AplikacjaNiezawodność(okno)
    okno.mainloop()


if __name__ == "__main__":
    main()
