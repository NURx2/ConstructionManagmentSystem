from abc import ABC, abstractmethod

class StartPointFiller(ABC):
    @abstractmethod
    def fill_start_points(self, tasks):
        pass
