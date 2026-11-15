#set document(title: "Wskaźniki niezawodności obiektów nienaprawialnych")
#set page(paper: "a4", margin: 2.5cm, numbering: "1")
#set text(font: "Liberation Sans", lang: "pl", size: 11pt, hyphenate: false)
#set par(justify: false, linebreaks: "simple")
#set heading(numbering: "1.1")

#align(center)[
  #image("assets/logo-psk.png", width: 1.6cm)

  Politechnika Świętokrzyska \
  Wydział Elektrotechniki, Automatyki i Informatyki

  #v(0.6cm)
  #text(size: 16pt, weight: "bold")[NIEZAWODNOŚĆ SYSTEMÓW KOMPUTEROWYCH] \
  #text(size: 14pt, weight: "bold")[Laboratorium]
]

#v(2cm)
#text(size: 14pt)[
  Tytuł zadania: Wyznaczenie wartości wskaźników niezawodności obiektów
  nienaprawialnych dla rozkładu wykładniczego oraz rozkładu Erlanga r-tego rzędu
]

#v(1.5cm)
#grid(
  columns: (1fr, 1fr),
  column-gutter: 1cm,
  [], [
    *Wykonali:* xxx \
    #v(0.3cm)
    *Kierunek:* Informatyka \
    #v(0.3cm)
    *Grupa:* yyy
  ],
)

#pagebreak()

= Treść zadania laboratoryjnego

Napisać program komputerowy w dowolnym języku i środowisku wykonujący
obliczenia na wybrany z listy temat. Program winien być w wersji
wykonywalnej (np. exe).

Wykonać sprawozdanie z zadania zawierające:
+ Opis teoretyczny zagadnienia.
+ Algorytm działania programu.
+ Kod programu.
+ Opis i wyniki testowania aplikacji.
+ Instrukcja obsługi programu.

Zadanie realizowane jest w zespołach 2-osobowych. Należy przedstawić na
zajęciach funkcjonowanie programu oraz dostarczyć sprawozdanie i pliki
programu.

== Zadanie 2

Wyznaczenie wartości wskaźników niezawodności obiektów nienaprawialnych:
$F(t)$, $R(t)$, $f(t)$, $lambda(t)$, $overline(T)$, $sigma^2$ dla rozkładu
wykładniczego oraz rozkładu Erlanga $r$-tego rzędu.

= Opis teoretyczny zagadnienia

Rozważane są urządzenia elektroniczne nienaprawiane (UE) - po uszkodzeniu
nie są naprawiane, a jedynym analizowanym okresem jest czas od chwili
rozpoczęcia pracy $t = 0$ do chwili pierwszego uszkodzenia. Czas ten
oznaczamy jako zmienną losową $T$ (czas poprawnej pracy do pierwszego
uszkodzenia), typu ciągłego, o gęstości $f(t)$, dla której $Pr{T > 0} = 1$
oraz $E T < infinity$, $V T < infinity$.

Podstawowe charakterystyki niezawodnościowe UE nienaprawianego:

- *Funkcja zawodności* (dystrybuanta) $F(t) = Pr{T <= t}$ - prawdopodobieństwo
  uszkodzenia się obiektu do chwili $t$; $F(t) in [0, 1]$.
- *Funkcja niezawodności* $R(t) = 1 - F(t) = Pr{T > t}$ - prawdopodobieństwo
  bezawaryjnej pracy do chwili $t$; $R(t) in [0, 1]$.
- *Gęstość prawdopodobieństwa uszkodzenia* $f(t) = (d F(t)) / (d t) = -(d R(t))/(d t)$.
- *Intensywność uszkodzeń* $lambda(t) = f(t) / R(t)$ - warunkowa gęstość
  uszkodzenia w chwili $t$, pod warunkiem przeżycia do $t$.
- *Średni czas poprawnej pracy* $overline(T) = E T = integral_0^infinity R(t) dif t$
  (MTTF).
- *Wariancja czasu pracy* $sigma^2 = V T = 2 integral_0^infinity R(t) dif t - overline(T)^2$.

== Rozkład wykładniczy

Dla czasu pracy $T$ o rozkładzie wykładniczym z parametrem (intensywnością
uszkodzeń) $lambda > 0$ (str. 315, wzory z Przykładu 7.1a):

$ F(t) = 1 - e^(-lambda t), quad R(t) = e^(-lambda t), quad f(t) = lambda e^(-lambda t) $
$ lambda(t) = lambda, quad overline(T) = 1 / lambda, quad sigma^2 = 1 / lambda^2 $

Intensywność uszkodzeń jest stała w czasie - konsekwencja własności braku
pamięci rozkładu wykładniczego.

== Rozkład Erlanga rzędu $r$

Dla czasu pracy $T$ o rozkładzie Erlanga $r$-tego rzędu ($r >= 1$, liczba
całkowita) z parametrem $lambda > 0$ (str. 316, Przykład 7.1b):

$ F(t) = 1 - sum_(k=0)^(r-1) e^(-lambda t) (lambda t)^k / k!, quad
  R(t) = sum_(k=0)^(r-1) e^(-lambda t) (lambda t)^k / k! $
$ f(t) = lambda (lambda t)^(r-1) / (r-1)! e^(-lambda t), quad
  lambda(t) = f(t) / R(t) $
$ overline(T) = r / lambda, quad sigma^2 = r / lambda^2 $

Rozkład Erlanga rzędu $r=1$ pokrywa się z rozkładem wykładniczym - jest to
suma $r$ niezależnych zmiennych losowych o rozkładzie wykładniczym $lambda$
(np. czas do $r$-tego uszkodzenia w ciągu zdarzeń Poissona).

= Algorytm działania programu

+ Użytkownik wprowadza z klawiatury w oknie programu: chwilę czasu $t$ [h],
  intensywność uszkodzeń $lambda$ [1/h] oraz rząd rozkładu Erlanga $r$
  (liczba całkowita).
+ Program waliduje dane: pola numeryczne akceptują tylko cyfry (i separator
  dziesiętny) podczas wpisywania, a po kliknięciu "Oblicz" sprawdzane jest,
  czy $t >= 0$, $lambda > 0$ oraz $r >= 1$ i całkowite. Błędne dane
  skutkują czytelnym komunikatem, bez przerwania programu.
+ Po poprawnej walidacji program oblicza niezależnie sześć wskaźników
  ($F$, $R$, $f$, $lambda(t)$, $overline(T)$, $sigma^2$) dla rozkładu
  wykładniczego oraz dla rozkładu Erlanga, według wzorów z rozdziału 2.
+ Prawdopodobieństwa $F(t)$ i $R(t)$ są obcinane do przedziału $[0, 1]$, aby
  zabezpieczyć się przed błędami zaokrągleń zmiennoprzecinkowych.
+ Jeżeli $R(t)$ jest numerycznie równe zero (np. dla bardzo dużego $t$),
  intensywność uszkodzeń $lambda(t) = f(t)/R(t)$ nie jest wyznaczana (dzielenie
  przez zero) - program wyświetla w tym miejscu czytelną informację zamiast
  ulegać awarii.
+ Dane wejściowe są dodatkowo ograniczone od góry ($t$, $lambda$ - do
  $10^(100)$; rząd Erlanga $r$ - do 10 000), a dla rozkładu Erlanga program
  sprawdza z góry, czy składnik $(lambda t)^(r-1)$ zmieści się w liczbie
  zmiennoprzecinkowej, zanim przystąpi do sumowania. Chroni to przed
  przepełnieniem przy bardzo dużych danych wejściowych -
  zamiast awarii program zgłasza czytelny komunikat o zbyt dużych wartościach.
+ Wyniki są wyświetlane w tabeli (wskaźnik, jednostka, wartość dla rozkładu
  wykładniczego, wartość dla rozkładu Erlanga).
+ Na żądanie użytkownika (przycisk "Zapisz wynik do druku") dane
  wejściowe i wyniki są zapisywane do pliku PDF
  `wynik_niezawodnosc.pdf`, w tym samym katalogu co program. Każdy zapis
  zastępuje poprzedni plik, więc plik zawiera tylko wynik ostatniego
  obliczenia.

= Kod programu

Program napisano w języku Python z interfejsem graficznym w bibliotece
`tkinter`. Kod podzielono na dwa pliki: `niezawodnosc.py` (obliczenia
niezawodnościowe) oraz `main.py`
(okno programu).

== niezawodnosc.py

#block(fill: luma(245), stroke: 0.5pt + luma(180), inset: 8pt, radius: 2pt, width: 100%)[
  #raw(read("niezawodnosc.py"), lang: "python", block: true)
]

== main.py

#block(fill: luma(245), stroke: 0.5pt + luma(180), inset: 8pt, radius: 2pt, width: 100%)[
  #raw(read("main.py"), lang: "python", block: true)
]

= Opis i wyniki testowania programu

Strony 315-316 książki źródłowej podają wzory Przykładu 7.1 w postaci
symbolicznej, dlatego poprawność programu zweryfikowano w dwóch krokach:

+ *Tożsamość Erlang-wykładniczy.* Rozkład Erlanga rzędu $r = 1$ jest z
  definicji równoważny rozkładowi wykładniczemu. Dla danych wejściowych
  $t = 100$ h, #box["$lambda = 0.001$ 1/h"], $r = 1$ program zwraca dokładnie
  takie same wartości wskaźników dla obu rozkładów, co potwierdza poprawność
  implementacji wzorów Erlanga.
+ *Przykład liczbowy.* Dla danych wejściowych $t = 100$ h,
  #box["$lambda = 0.001$ 1/h"], $r = 3$ program zwraca poniższe wyniki:

#table(
  columns: (auto, auto, auto, auto),
  align: (left, center, right, right),
  table.header([*Wskaźnik*], [*Jednostka*], [*Wykładniczy*], [*Erlang (r=3)*]),
  [Funkcja zawodności $F(t)$], [-], [0,095163], [0,000155],
  [Funkcja niezawodności $R(t)$], [-], [0,904837], [0,999845],
  [Gęstość $f(t)$], [1/h], [9,0484 dot 10^(-4)], [4,5242 dot 10^(-6)],
  [Intensywność $lambda(t)$], [1/h], [0,001], [4,5249 dot 10^(-6)],
  [Średni czas pracy $overline(T)$], [h], [1000], [3000],
  [Wariancja $sigma^2$], [h#super[2]], [$10^6$], [$3 dot 10^6$],
)

+ *Przyciski "Test".* Program zawiera trzy przyciski wklejające gotowe
  dane wejściowe:

#let wiersz_testu(nazwa, t, lam, r, wyniki) = {
  [*#nazwa* - dane: $t = #t$ h, $lambda = #lam$ 1/h, $r = #r$:]
  table(
    columns: (auto, auto, auto, auto),
    align: (left, center, right, right),
    table.header([*Wskaźnik*], [*Jednostka*], [*Wykładniczy*], [*Erlang*]),
    ..wyniki
  )
}

#wiersz_testu("Test 1", 10, 0.1, 2, (
  [$F(t)$], [-], [0,632121], [0,264241],
  [$R(t)$], [-], [0,367879], [0,735759],
  [$f(t)$], [1/h], [0,0367879], [0,0367879],
  [$lambda(t)$], [1/h], [0,1], [0,05],
  [$overline(T)$], [h], [10], [20],
  [$sigma^2$], [h#super[2]], [100], [200],
))

#wiersz_testu("Test 2", 100, 0.01, 5, (
  [$F(t)$], [-], [0,632121], [0,00365985],
  [$R(t)$], [-], [0,367879], [0,99634],
  [$f(t)$], [1/h], [0,00367879], [0,000153283],
  [$lambda(t)$], [1/h], [0,01], [0,000153846],
  [$overline(T)$], [h], [100], [500],
  [$sigma^2$], [h#super[2]], [10000], [50000],
))

#wiersz_testu("Test 3", 20, 0.05, 4, (
  [$F(t)$], [-], [0,632121], [0,0189882],
  [$R(t)$], [-], [0,367879], [0,981012],
  [$f(t)$], [1/h], [0,018394], [0,00306566],
  [$lambda(t)$], [1/h], [0,05], [0,003125],
  [$overline(T)$], [h], [20], [80],
  [$sigma^2$], [h#super[2]], [400], [1600],
))

Dodatkowo sprawdzono zachowanie przy danych brzegowych i błędnych: $t = 0$
daje $F(0) = 0$, $R(0) = 1$ dla obu rozkładów; wpisanie litery, przecinka w
polu rzędu Erlanga lub wartości ujemnej jest odrzucane przez walidację pól
albo zgłaszane czytelnym komunikatem po kliknięciu "Oblicz", bez przerwania
działania programu.

= Instrukcja obsługi programu

+ Należy uruchomić program poleceniem `python main.py` albo uruchamiając plik `niezawodnosc.exe` na Windows. Otworzy się okno programu.
+ W sekcji *Dane wejściowe* należy wprowadzić:
  - *Chwila czasu t [godziny]* - czas, dla którego mają zostać wyznaczone
    wskaźniki, w godzinach (liczba nieujemna, np. `100`).
  - *Intensywność uszkodzeń lambda [1/godziny]* - parametr rozkładu
    wykładniczego/Erlanga, w odwrotności godzin (liczba dodatnia,
    np. `0.001`).
  - *Rząd rozkładu Erlanga r (dodatnia liczba całkowita)*, np. `3`.

  Zamiast wpisywać dane ręcznie, można kliknąć jeden z przycisków *Test 1*,
  *Test 2*, *Test 3* - wklejają one do pól gotowy zestaw danych.

  Jeżeli interesuje nas wyłącznie rozkład wykładniczy, należy w polu *Rząd
  rozkładu Erlanga r* wpisać `1` - rozkład Erlanga rzędu $r=1$ pokrywa się
  z rozkładem wykładniczym, więc obie kolumny wyników będą identyczne.
+ Należy kliknąć przycisk *Oblicz*. Wyniki dla obu rozkładów pojawią się
  w tabeli poniżej, wraz z jednostkami.
+ W przypadku błędu (np. wartość ujemna, brak danych) program wyświetli
  okno z komunikatem opisującym, co i w jakich jednostkach należy poprawić.
+ Aby udokumentować test, należy kliknąć *Zapisz wynik do druku*.
  W tym samym katalogu co program zostanie utworzony plik
  `wynik_niezawodnosc.pdf` z danymi wejściowymi i wynikami ostatniego
  obliczenia. Każdy zapis zastępuje poprzedni plik wynikowy.

= Zrzuty ekranu działania programu

#figure(
  image("assets/okno-programu.png", width: 90%),
  caption: [Okno programu bezpośrednio po uruchomieniu, przed wprowadzeniem danych.],
)

#figure(
  image("assets/wykonane-obliczenia.png", width: 90%),
  caption: [Okno programu po wprowadzeniu danych testowych i kliknięciu przycisku "Oblicz".],
)

#figure(
  image("assets/wynik-do-druku.png", width: 90%),
  caption: [Plik PDF `wynik_niezawodnosc.pdf` wygenerowany po kliknięciu przycisku "Zapisz wynik do druku".],
)

= Literatura

+ _Niezawodność urządzeń elektronicznych._ Pr. zb. pod red. M. Prażewskiej,
  WKiŁ, Warszawa 1987, str. 313-316.
