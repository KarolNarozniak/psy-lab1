import time
import math
import random
import sys
from datetime import datetime


class RNGSeeds:
    """
    Klasa RNGSeeds.
    Używa aktualnego czasu zegarowego jako ziarna (ms od epoki).
    """

    @staticmethod
    def ClockSeed(d=None):
        """
        Zwraca wartość typu "long integer" jako ziarno zbudowane
        na podstawie aktualnego czasu zegarowego lub podanej daty.
        Jeżeli d jest None, używana jest bieżąca data/czas.
        """
        if d is None:
            # ms od 1.1.1970
            return int(time.time() * 1000)
        if isinstance(d, datetime):
            return int(d.timestamp() * 1000)
        raise TypeError("ClockSeed oczekuje obiektu datetime lub None")


class RNGenerator(random.Random):
    """
    Klasa RNGenerator.
    Dziedziczy po random.Random i dodaje generowanie z wielu rozkładów.
    """

    cof = [76.18009173, -86.50532033, 24.01409822,
           -1.231739516, 0.120858003e-2, -0.536382e-5]
    PI = math.pi

    def __init__(self, seed=None):
        """
        Konstruktor generatora liczb losowych.
        Jeżeli seed jest None, użyte zostanie domyślne ziarno random.Random.
        """
        super().__init__(seed)

    # ======================================================================
    @staticmethod
    def generateSeed():
        """
        Tworzy ziarno na podstawie aktualnego czasu zegarowego,
        korzystając z RNGSeeds.ClockSeed().
        """
        return RNGSeeds.ClockSeed()

    # ======================================================================
    '''
    
    '''

    def uniform(self, a, b):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'jednostajnego' (inaczej: jednorodny, równomierny, prostokątny albo płaski).
         @param a Najmniejsza wartość generowanej zmiennej. Poprawny zakres wartości: liczby rzeczywiste, z warunkiem: a<b.
         @param b Największa wartość generowanej zmiennej. Poprawny zakres wartości: liczby rzeczywiste, z warunkiem: a<b.
         @return Zwraca liczbę rzeczywistą w przedziale [a, b)
        """
        if b < a:
            print("RNGenerator.uniform: give b>a", file=sys.stderr)
            return -1.0
        return self.random() * (b - a) + a

    # Rozkład jednostajny (całkowity)
    def uniformInt(self, a, b=None):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'równomierny'.
         @param b Największa wartość generowanej zmiennej. Poprawny zakres wartości: liczby całkowite dodatnie.
         @return Zwraca liczbę całkowitą nieujemną w przedziale [0, b).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład wykładniczy

    def exponential(self, lam):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'wykładniczy'.
         @param lambda Parametr skali. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale [0 ; ∞).
        """
        if lam < 0:
            print("RNGenerator.exponential: a must be >0", file=sys.stderr)
            return -1.0
        u = self.random()
        return (1.0 / lam) * (-math.log(1.0 - u))

    # ======================================================================
    # Rozkład Erlanga

    def erlang(self, k, lam):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'erlanga'.
         @param k Parametr kształtu. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @param lambda Parametr częstości. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale [0 ; ∞).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład gamma

    def gamma(self, k, b):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'gamma'.
         @param k Parametr kształtu. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @param b Parametr zakresu. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale [0 ; ∞).
        """
        if (k < 0.0) or (b < 0.0):
            print("RNGenerator.gamma: k and b be >0 and k<=1", file=sys.stderr)

        # k < 1
        if k < 1.0:
            while True:
                xx = self.random() ** (1.0 / k)
                yy = self.random() ** (1.0 / (1.0 - k))
                if xx + yy <= 1.0:
                    break
            xx = xx / (xx + yy)
            yy = self.exponential(1.0)
            return xx * yy / b

        # k == 1
        if k == 1.0:
            return self.exponential(1.0) / b

        # k > 1: metoda odrzucania
        while True:
            while True:
                while True:
                    v1 = 2.0 * self.random() - 1.0
                    v2 = 2.0 * self.random() - 1.0
                    if v1 * v1 + v2 * v2 <= 1.0:
                        break
                yy = v2 / v1
                am = k - 1.0
                s = math.sqrt(2.0 * am + 1.0)
                avg = s * yy + am
                if avg > 0.0:
                    break
            e = (1.0 + yy * yy) * math.exp(am * math.log(avg / am) - s * yy)
            if self.random() <= e:
                break
        return avg / b

    # ======================================================================
    # Rozkład normalny

    def normal(self, a, b):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'normalny'.
         @param a Parametr położenia. Poprawny zakres wartości: liczba rzeczywista.
         @param b Parametr skali. Poprawny zakres wartości: liczba rzeczywista, różna od 0.
         @return Zwraca liczbę rzeczywistą w przedziale (-∞ ; ∞).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład chi-kwadrat

    def chisquare(self, k):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'Chi kwadrat'.
         @param k Parametr swobody. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale [0 ; ∞).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład beta

    def beta(self, a, b):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'beta'.
         @param a Parametr kształtu. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @param b Parametr kształtu. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale [0 ; 1].
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład studenta

    def student(self, n):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'studenta'. Wartość oczekiwana równa jest 0 dla n>1, w przeciwnym wypadku wartość jest nieznana.
         @param n Parametr swobody. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale (-∞ ; ∞).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład lognormalny

    def lognormal(self, average, std_dev):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'lognormal'.
         @param average Wartość oczekiwana. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @param stdDev Odchylenie standardowe. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale (0 ; ∞).
        """
        if std_dev <= 0.0:
            print("RNGenerator:lognormal: b must be >0", file=sys.stderr)
            return -1.0
        return math.exp(self.normal(average, std_dev))

    # ======================================================================
    # Rozkład F-Snedecora

    def fdistribution(self, n, m):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'F Snedecora'.
         @param n Parametr stopnia swobody. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @param m Parametr stopnia swobody. Poprawny zakres wartości: liczba całkowita, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale (0 ; ∞).
        """

        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład Weibulla

    def weibull(self, m, k):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'weibulla'.
         @param m Parametr charakterystycznego czasu życia. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @param k Parametr kształtu. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę rzeczywistą w przedziale (0 ; ∞).
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład Poissona

    def poisson(self, a):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'poissona'.
         @param a Parametr oczekiwanej liczby zdarzeń w danym przedziale czasu. Poprawny zakres wartości: liczba rzeczywista, większa od 0.
         @return Zwraca liczbę całkowitą nieujemną.
        """
        sq = -1.0
        alxm = -1.0
        g = -1.0
        oldm = -1.0

        if a < 12.0:
            if a != oldm:
                oldm = a
                g = math.exp(-a)
            em = -1.0
            t = 1.0
            while True:
                em += 1.0
                t *= self.random()
                if t <= g:
                    break
        else:
            if a != oldm:
                oldm = a
                sq = math.sqrt(2.0 * a)
                alxm = math.log(a)
                g = a * alxm - self._lngamma(a + 1.0)
            while True:
                while True:
                    yy = math.tan(self.PI * self.random())
                    em = sq * yy + a
                    if em >= 0.0:
                        break
                em = math.floor(em)
                t = 0.9 * (1.0 + yy * yy) * math.exp(
                    em * alxm - self._lngamma(em + 1.0) - g
                )
                if self.random() <= t:
                    break
        return int(em)

    # ======================================================================
    # Rozkład geometryczny

    def geometric(self, p):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'geometryczny'.
         @param p Parametr prawdopodobieństwa sukcesu. Poprawny zakres wartości: liczba rzeczywista z przedziału (0;1).
         @return Zwraca liczbę całkowitą dodatnią.
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Rozkład dwumianowy

    def binomial(self, p, n):
        """
	 Metoda generująca wartość pseudolosową jako realizację rozkładu 'dwumianowy'.
	 @param p Parametr prawdopodobieństwa sukcesu. Poprawny zakres wartości: liczba rzeczywista z przedziału [0;1].
	 @param n Parametr liczby prób. Poprawny zakres wartości: liczba całkowita nieujemna.
	 @return Zwraca liczbę całkowitą nieujemną ze zbioru liczb {0,...,n}
        """
        if (p <= 0.0) or (p >= 1.0):
            print("RNGenerator.binomial: p must be from range (0,1)",
                  file=sys.stderr)
            return -1

        nold = -1
        pold = -1.0
        pc = 0.0
        en = 0.0
        oldg = 0.0
        plog = 0.0
        pclog = 0.0

        prob = p if p <= 0.5 else 1.0 - p
        am = n * prob

        # prosta metoda dla małego n
        if n < 25:
            bnl = 0.0
            for _ in range(1, n + 1):
                if self.random() < prob:
                    bnl += 1.0

        # metoda Poissona dla małej wartości oczekiwanej
        elif am < 10.0:
            g = math.exp(-am)
            t = 1.0
            for j in range(0, n + 1):
                t *= self.random()
                if t < g:
                    break
            bnl = float(j if j <= n else n)

        # metoda odrzucania
        else:
            if n != nold:
                en = float(n)
                oldg = self._lngamma(en + 1.0)
                nold = n
            if prob != pold:
                pc = 1.0 - prob
                plog = math.log(prob)
                pclog = math.log(pc)
                pold = prob
            sq = math.sqrt(2.0 * am * pc)
            while True:
                while True:
                    angle = self.PI * self.random()
                    yy = math.tan(angle)
                    em = sq * yy + am
                    if 0.0 <= em < (en + 1.0):
                        break
                em = math.floor(em)
                t = 1.2 * sq * (1.0 + yy * yy) * math.exp(
                    oldg - self._lngamma(em + 1.0)
                    - self._lngamma(en - em + 1.0)
                    + em * plog
                    + (en - em) * pclog
                )
                if self.random() <= t:
                    break
            bnl = em

        if prob != p:
            bnl = n - bnl
        return int(bnl)

    # ======================================================================
    # Rozkład trójkątny

    def triangular(self, a):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'trójkątny'.
         @param a Parametr kształtu. Poprawny zakres wartości: liczba rzeczywista z przedziału [0;1].
         @return Zwraca liczbę rzeczywistą nieujemną.
        """
        raise Exception('Not implemented.')

    # ======================================================================
    # Prawdopodobieństwo p

    def probability(self, p):
        """
         Metoda generująca wartość pseudolosową jako realizację rozkładu 'prawdopodobieństwo p'.
         @param a Parametr prawdopodobieństwa. Poprawny zakres wartości: liczba rzeczywista z przedziału (0;1).
         @return Zwraca TRUE lub FALSE.
        """
        if (p < 0.0) or (p > 1.0):
            print("RNGenerator.propability: p must be from range (0,1)",
                  file=sys.stderr)
            return False
        return p >= self.random()

    # ======================================================================
    # Prywatna implementacja funckji pomocniczej

    @classmethod
    def _lngamma(cls, xx):
        x = xx - 1.0
        tmp = x + 5.5
        tmp -= (x + 0.5) * math.log(tmp)
        ser = 1.0
        for j in range(6):
            x += 1.0
            ser += cls.cof[j] / x
        return -tmp + math.log(2.50662827465 * ser)
