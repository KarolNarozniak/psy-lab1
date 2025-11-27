from __future__ import annotations
import math
import random
import sys
import time
from typing import Callable

# Stale przedzialu calkowania
PREDZIAL_A = 1.0
PREDZIAL_B = math.e


def konstrukcja_f_expr(wyrazenie: str) -> Callable[[float], float]:
    # Jesli wyrazenie jest niepoprawne, wyjatek przejdzie na zewnatrz i program sie zakonczy.
    globalns = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
    # Pozwalamy uzytkownikowi uzywac stalych typu 'e' czy 'pi' oraz funkcji math
    globalns['__builtins__'] = __builtins__
    kod = compile(wyrazenie, '<wyrazenie>', 'eval')

    def f(x: float) -> float:
        lokalne = {'x': x}
        wynik = eval(kod, globalns, lokalne)
        return float(wynik)

    return f


def calka_numeryczna(f: Callable[[float], float], a: float = PREDZIAL_A, b: float = PREDZIAL_B, kroki: int = 200000) -> float:
    """Przyblizona calka numeryczna metoda prostokatow (srodek) dla odniesienia. """
    if kroki <= 0:
        raise ValueError('kroki musi byc wieksze od 0')
    dx = (b - a) / kroki
    suma = 0.0
    for i in range(kroki):
        xi = a + (i + 0.5) * dx
        suma += f(xi) * dx
    return suma


def szacuj_mc_prostokaty(n: int, f: Callable[[float], float], a: float = PREDZIAL_A, b: float = PREDZIAL_B, ziarenko: int | None = None) -> float:
    """Oszacuj calke metoda Monte Carlo oparta na losowym podziale przedzialu i prostokatach."""
    if n < 0:
        raise ValueError('n musi byc nieujemne')
    rng = random.Random(ziarenko) if ziarenko is not None else random
    punkty = [rng.uniform(a, b) for _ in range(n)]
    punkty.sort()
    krawez = [a] + punkty + [b]
    wynik = 0.0
    for i in range(len(krawez) - 1):
        left = krawez[i]
        right = krawez[i + 1]
        szerokosc = right - left
        srodek = (left + right) / 2.0
        wysokosc = f(srodek)
        wynik += szerokosc * wysokosc
    return wynik


def wczytaj_wyrazenie_od_uzytkownika() -> tuple[str, Callable[[float], float]]:
    """Pytaj uzytkownika o wyrazenie f(x) az do momentu poprawnego wprowadzenia.

    Zwraca:
        (wyrazenie_lancuch, funkcja_f)
    """
    while True:
        try:
            wej = input("Podaj funkcje f(x) (np. 'x', 'x**2', 'sin(x)'): ").strip()
            if not wej:
                print('Nie podano wyrazenia. Sprobuj ponownie.')
                continue
            f = konstrukcja_f_expr(wej)
            return wej, f
        except Exception as e:
            print(f'Blad w wyrazeniu: {e}. Sprobuj ponownie.')


def ladny_raport(funkcja_nazwa: str, wyrazenie: str, f: Callable[[float], float], ziarno: int | None, ns_list: list[int], kroki_ref: int):
    """Wykonaj obliczenia i wypisz czytelny raport po polsku."""
    print('\n--- Wyniki:')
    print(f'Funkcja ({funkcja_nazwa}): {wyrazenie}')
    print(f'Przedzial calkowania: [{PREDZIAL_A}, {PREDZIAL_B}]')
    print('\nLicze wartosc referencyjna (calka numeryczna, metoda prostokatow)...')
    calka_ref = calka_numeryczna(f, PREDZIAL_A, PREDZIAL_B, kroki=kroki_ref)
    print(f'Wartosc referencyjna (numeryczna, kroki={kroki_ref}): {calka_ref:.12f}')

    print('\nEstymacje Monte Carlo (metoda prostokatow, losowy podzial):')
    print(' n    estymacja          blad_abs          blad_wzgledny [%]')
    for n in ns_list:
        est = szacuj_mc_prostokaty(n, f, PREDZIAL_A, PREDZIAL_B, ziarno)
        blad_abs = abs(calka_ref - est)
        blad_wzg = (blad_abs / abs(calka_ref) * 100.0) if calka_ref != 0 else float('inf')
        print(f'{n:3d}  {est:18.12f}  {blad_abs:13.12f}  {blad_wzg:15.6f}')


def main():
    """Glowna funkcja uruchamiana z konsoli. Prowadzi dialog z uzytkownikiem."""
    print('Program: Oszacowanie calki metoda Monte Carlo (metoda prostokatow)')
    print('Przedzial calkowania: a=1, b=e')

    ns_list = [10, 50, 100]      # liczby punktow do zbadania
    kroki_ref = 200_000         # liczba podprzedzialow do calki referencyjnej

    wyraz, f = wczytaj_wyrazenie_od_uzytkownika()
    ziarno = time.time_ns()
    print(f'Uzyte ziarno (time.time_ns): {ziarno}')
    ladny_raport('uzytkownika', wyraz, f, ziarno, ns_list, kroki_ref)


if __name__ == '__main__':
    main()
