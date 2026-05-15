from abc import ABC, abstractmethod
from enum import Enum
from typing import List, Optional

class StatusUrzadzenia(Enum):
    WYLACZONE = "Wyłączone"
    WLACZONE = "Włączone"
    AWARIA = "Awaria"
    BRAK_DANYCH = "Brak danych"

class IPrzelaczalne(ABC):
    @abstractmethod
    def wlacz(self) -> None:
        pass

    @abstractmethod
    def wylacz(self) -> None:
        pass

class IRegulowalne(ABC):
    @abstractmethod
    def ustawWartosc(self, wartosc: float) -> None:
        pass

class Urzadzenie(ABC):
    def __init__(self, id_urzadzenia: str, nazwa_przyjazna: str, lokalizacja: str):
        self._id_urzadzenia = id_urzadzenia
        self._nazwa_przyjazna = nazwa_przyjazna
        self._lokalizacja = lokalizacja
        self._status = StatusUrzadzenia.WYLACZONE

    @property
    def id_urzadzenia(self) -> str:
        return self._id_urzadzenia

    def pobierzStatus(self) -> StatusUrzadzenia:
        return self._status

    def zmienStatus(self, nowy_status: StatusUrzadzenia) -> None:
        self._status = nowy_status

    @abstractmethod
    def pobierzSzczegolowyOpis(self) -> str:
        pass
  class Lampa(Urzadzenie, IPrzelaczalne, IRegulowalne):
    def __init__(self, id_urzadzenia: str, nazwa_przyjazna: str, lokalizacja: str):
        super().__init__(id_urzadzenia, nazwa_przyjazna, lokalizacja)
        self._poziom_jasnosci = 0

    def wlacz(self) -> None:
        self.zmienStatus(StatusUrzadzenia.WLACZONE)
        self._poziom_jasnosci = 100

    def wylacz(self) -> None:
        self.zmienStatus(StatusUrzadzenia.WYLACZONE)
        self._poziom_jasnosci = 0

    def ustawWartosc(self, wartosc: float) -> None:
        self._poziom_jasnosci = int(max(0, min(100, wartosc)))
        self.zmienStatus(StatusUrzadzenia.WLACZONE if self._poziom_jasnosci > 0 else StatusUrzadzenia.WYLACZONE)

    def pobierzSzczegolowyOpis(self) -> str:
        return f"Lampa '{self._nazwa_przyjazna}' ({self._lokalizacja}) | Status: {self._status.value} | Jasność: {self._poziom_jasnosci}%"


class Termostat(Urzadzenie, IRegulowalne):
    def __init__(self, id_urzadzenia: str, nazwa_przyjazna: str, lokalizacja: str, temp_poczatkowa: float = 21.0):
        super().__init__(id_urzadzenia, nazwa_przyjazna, lokalizacja)
        self._temperatura_docelowa = temp_poczatkowa
        self.zmienStatus(StatusUrzadzenia.WLACZONE)

    def ustawWartosc(self, wartosc: float) -> None:
        self._temperatura_docelowa = wartosc

    def pobierzSzczegolowyOpis(self) -> str:
        return f"Termostat '{self._nazwa_przyjazna}' ({self._lokalizacja}) | Status: {self._status.value} | Temp. docelowa: {self._temperatura_docelowa}°C"


class CzujnikRuchu(Urzadzenie):
    def __init__(self, id_urzadzenia: str, nazwa_przyjazna: str, lokalizacja: str):
        super().__init__(id_urzadzenia, nazwa_przyjazna, lokalizacja)
        self._czy_wykryto_ruch = False
        self.zmienStatus(StatusUrzadzenia.WLACZONE)

    def symulujRuch(self, wykryto: bool) -> None:
        self._czy_wykryto_ruch = wykryto

    def pobierzSzczegolowyOpis(self) -> str:
        stan_ruchu = "Tak" if self._czy_wykryto_ruch else "Nie"
        return f"Czujnik Ruchu '{self._nazwa_przyjazna}' ({self._lokalizacja}) | Status: {self._status.value} | Wykryto ruch: {stan_ruchu}"
    