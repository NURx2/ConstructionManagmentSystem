from abc import ABC, abstractmethod
from data.Task import Task
from typing import List

class Solution(ABC):
    @abstractmethod
    def solve(self, tasks: List[Task]) -> List[Task]:
        pass

    def name(self):
        return self.__class__.__name__
