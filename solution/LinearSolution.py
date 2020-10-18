from data.Task import Task
from solution.Solution import Solution
from typing import List
import copy

from validation.CollisionDetector import CollisionDetector, Collision


class LinearSolution(Solution):
    def solve(self, tasks: List[Task]) -> List[Task]: # we need to copy tasks (to make previous tasks immutable)
        tasks = copy.deepcopy(tasks)

        collisions = CollisionDetector.get_collisions(tasks)
        while len(collisions) > 0:
            for collision in collisions:
                self.resolve_collision(tasks, collision)
            collisions = CollisionDetector.get_collisions(tasks)

        return tasks

    def resolve_collision(self, tasks: List[Task], collision: Collision) -> None:
        while (tasks[collision.first_task_id].lower_time != -1 and
            tasks[collision.first_task_id].min_time < tasks[collision.first_task_id].time and
            CollisionDetector.check_collision(tasks, collision)
        ):
            tasks[collision.first_task_id].time -= 1

        if not CollisionDetector.check_collision(tasks, collision):
            return

        if tasks[collision.second_task_id].costs['moveForward'] == -1:
            raise RuntimeError('Solution is too weak to resolve this conflict :(')

        while CollisionDetector.check_collision(tasks, collision):
            tasks[collision.second_task_id].start += 1

