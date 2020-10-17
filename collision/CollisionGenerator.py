from data.Task import Task
from abc import ABC, abstractmethod

class CollisionGenerator(ABC):
    @abstractmethod
    def generate_collisions(self, tasks) -> [Task]:
        return tasks
