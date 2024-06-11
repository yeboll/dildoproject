from abc import ABC, abstractmethod

class Platform(ABC):
    @abstractmethod
    def get_avaliable_tikers(self) -> []:
        ...

    @abstractmethod
    def get_last_candles(self, tiker, tf, time = 0) -> []:
        ...
