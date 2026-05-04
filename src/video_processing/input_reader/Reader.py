import abc
from abc import ABC, abstractmethod

class Reader(ABC):
    @abstractmethod
    def read_all(self):
        raise NotImplementedError

    @abstractmethod
    def read_with_gap(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

