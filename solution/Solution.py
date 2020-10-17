from abc import ABC, abstractmethod

class Solution(ABC):
    @abstractmethod
    def solve(self, tasks):
        pass

    @abstractmethod
    def name(self):
        pass
