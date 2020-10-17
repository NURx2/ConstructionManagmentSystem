from data.Task import Task
from solution.Solution import Solution
from typing import List

class JustCopySolution(Solution):
    def solve(self, tasks: List[Task]) -> List[Task]: # we need to copy tasks (to make previous tasks immutable)
        result = []
        for task in tasks:
            result.append(task.copy())
        return result

    def name(self):
        return "JustCopySolution"
