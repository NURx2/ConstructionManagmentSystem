from data.Task import Task
from solution.Solution import Solution
from typing import List
import copy

from validation.CollisionDetector import CollisionDetector, Collision


class NaiveSolution(Solution):
    def solve(self, tasks: List[Task]) -> List[Task]: # we need to copy tasks (to make previous tasks immutable)
        tasks = copy.deepcopy(tasks)

        for collision in CollisionDetector.get_collisions(tasks):
            self.resolve_collision(tasks, collision)

        return tasks

    def resolve_collision(self, tasks: List[Task], collision: Collision, known_cost: int = None) -> int:
        pass


