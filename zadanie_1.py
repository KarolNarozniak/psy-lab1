from __future__ import annotations
import math
import random
import sys
from typing import Callable

# Stale przedzialu calkowania
PREDZIAL_A = 1.0
PREDZIAL_B = math.e


def konstrukcja_f_expr(wyrazenie: str) -> Callable[[float], float]:

    dozwolone = {name: getattr(math, name) for name in dir(math) if not name.startswith('_')}
    dozwolone.update({'abs': abs, 'min': min, 'max': max, 'pow': pow})

    try:
        kod = compile(wyrazenie, '<wyrazenie>', 'eval')
    except Exception as e:
        raise ValueError(f"Niepoprawne wyrazenie: {e}") from e

    def f(x: float) -> float:
        lokalne = dict(dozwolone)
        lokalne['x'] = x
        try:
            wynik = eval(kod, {'__builtins__': None}, lokalne)
        except Exception as e:
            raise
        if not isinstance(wynik, (int, float)):
            raise ValueError('Wyrazenie nie zwraca liczby')
        return float(wynik)

    srodek = (PREDZIAL_A + PREDZIAL_B) / 2.0
    try:
        test = f(srodek)
    except Exception as e:
        raise ValueError(f"Wyrazenie nie moze byc ocenione: {e}") from e
    if not isinstance(test, (int, float)):
        raise ValueError('Wyrazenie nie zwraca liczby')

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


def wczytaj_ziarno() -> int | None:
    """Popros uzytkownika o opcjonalne ziarno (int). Zwraca None albo int."""
    wej = input('Opcjonalne ziarno (int) do powtarzalnosci, lub Enter: ').strip()
    if not wej:
        return None
    try:
        return int(wej)
    except ValueError:
        print('Niepoprawne ziarno. Pomijam i uzywam losowego.')
        return None


def ladny_raport(funkcja_nazwa: str, wyrazenie: str, f: Callable[[float], float], ziarno: int | None):
    """Wykonaj obliczenia i wypisz czytelny raport po polsku."""
    print('\n--- Wyniki:')
    print(f'Funkcja ({funkcja_nazwa}): {wyrazenie}')
    print(f'Przedzial calkowania: [{PREDZIAL_A}, {PREDZIAL_B}]')
    print('\nLicze wartosc referencyjna (calka numeryczna, metoda prostokatow)...')
    calka_ref = calka_numeryczna(f, PREDZIAL_A, PREDZIAL_B, kroki=200000)
    print(f'Wartosc referencyjna (numeryczna): {calka_ref:.12f}')

    ns = [10, 50, 100]
    print('\nEstymacje Monte Carlo (metoda prostokatow, losowy podzial):')
    print(' n    estymacja          blad_abs          blad_wzgledny [%]')
    for n in ns:
        est = szacuj_mc_prostokaty(n, f, PREDZIAL_A, PREDZIAL_B, ziarno)
        blad_abs = abs(calka_ref - est)
        blad_wzg = (blad_abs / abs(calka_ref) * 100.0) if calka_ref != 0 else float('inf')
        print(f'{n:3d}  {est:18.12f}  {blad_abs:13.12f}  {blad_wzg:15.6f}')


def main():
    """Glowna funkcja uruchamiana z konsoli. Prowadzi dialog z uzytkownikiem.

    Program prosci o wyrazenie f(x) i (opcjonalnie) ziarno. Wypisuje porownanie estymacji.
    """
    print('Program: Oszacowanie calki metoda Monte Carlo (metoda prostokatow)')
    print('Przedzial calkowania: a=1, b=e')
    wyraz, f = wczytaj_wyrazenie_od_uzytkownika()
    ziarno = wczytaj_ziarno()
    ladny_raport('uzytkownika', wyraz, f, ziarno)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nPrzerwane przez uzytkownika')
        sys.exit(1)
