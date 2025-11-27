from __future__ import annotations
import math
import statistics
import time
from rn_generator_20251120 import RNGenerator


def normal_probe_generator(gen: RNGenerator, mu: float, sigma: float) -> float:
    """Wygeneruj pojedyncza wartosc z rozkladu normalnego N(mu, sigma^2)."""
    # zabezpieczenie: u1 nie moze byc 0
    u1 = 0.0
    while u1 <= 0.0:
        u1 = gen.random()
    u2 = gen.random()
    r = math.sqrt(-2.0 * math.log(u1))
    theta = 2.0 * math.pi * u2
    z = r * math.cos(theta)
    return mu + sigma * z


def generuj_probe_normalna(gen: RNGenerator, mu: float, sigma: float, n: int) -> list[float]:
    """Generuj probe 'n' wartosci z rozkladu normalnego."""
    return [normal_probe_generator(gen, mu, sigma) for _ in range(n)]


def analizuj_probe(probka: list[float]) -> tuple[float, float]:
    """Oblicz statystyki empiryczne: srednia i wariancja (estymator nieobciazony)."""
    if len(probka) < 2:
        return (statistics.mean(probka) if probka else 0.0, 0.0)
    srednia_emp = statistics.mean(probka)
    wariancja_emp = statistics.variance(probka)
    return srednia_emp, wariancja_emp


def main() -> None:
    print('Test generatora - rozklad normalny')
    # Ustawienia testu
    srodkowa_teoretyczna = 2.5
    odchylenie_teoretyczne = 1.7
    N = 1000

    ziarno = time.time_ns()
    print(f'Uzyte ziarno (time.time_ns): {ziarno}')
    gen = RNGenerator(ziarno)

    # Generuj probe
    print(f'Generuje probe N={N} z N({srodkowa_teoretyczna}, {odchylenie_teoretyczne}^2) ...')
    probka = generuj_probe_normalna(gen, srodkowa_teoretyczna, odchylenie_teoretyczne, N)

    # Analiza
    srednia_emp, wariancja_emp = analizuj_probe(probka)

    print('\nWyniki:')
    print(f' Srednia teoretyczna  = {srodkowa_teoretyczna:.6f}')
    print(f' Srednia empiryczna  = {srednia_emp:.6f}')
    print(f' Wariancja teoretyczna = {odchylenie_teoretyczne**2:.6f}')
    print(f' Wariancja empiryczna  = {wariancja_emp:.6f}')

    # raport bledu
    blad_sredniej = abs(srednia_emp - srodkowa_teoretyczna)
    blad_wariancji = abs(wariancja_emp - odchylenie_teoretyczne ** 2)
    print(f' Blad sredniej = {blad_sredniej:.6f}')
    print(f' Blad wariancji = {blad_wariancji:.6f}')


if __name__ == '__main__':
    main()
