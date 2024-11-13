from abc import ABC, abstractmethod
from datetime import datetime


class ElPriceService(ABC):

    @abstractmethod
    def get_price(self, date: datetime, area: str) -> float:
        pass
