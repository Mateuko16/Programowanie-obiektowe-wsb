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