from abc import ABC, abstractmethod
from data.task import Task

class Generator(ABC):
    @abstractmethod
    def generate_data(self) -> [Task]:
        pass