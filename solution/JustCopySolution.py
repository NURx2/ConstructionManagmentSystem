from data.Task import Task
from solution.Solution import Solution
from typing import List
import copy

class JustCopySolution(Solution):
    def solve(self, tasks: List[Task]) -> List[Task]: # we need to copy tasks (to make previous tasks immutable)
        return copy.deepcopy(tasks)

    def name(self):
        return "JustCopySolution"
