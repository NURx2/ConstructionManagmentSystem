from abc import ABC, abstractmethod
from data.task import Task

# Generates valid tasks list (no collisions)
# Collisions will be added later
class Generator(ABC):
    @abstractmethod
    def generate_data(self) -> [Task]:
        pass