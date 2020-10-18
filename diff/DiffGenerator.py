from validation.CollisionDetector import CollisionDetector
from data.Diff import Diff
from data.DiffReport import DiffReport
from data.Task import Task
from typing import List

class DiffGenerator:
    def __init__(self):
        self.collision_detector = CollisionDetector()

    def generate_diff(self, before_tasks: List[Task], after_tasks: List[Task]) -> DiffReport:
        diff_list = []
        for i in range(len(before_tasks)):
            assert(before_tasks[i].id == after_tasks[i].id)
            if before_tasks[i] != after_tasks[i]:
                diff_list.append(Diff(before_tasks[i], after_tasks[i]))
        was_collisions = len(self.collision_detector.get_collisions(before_tasks))
        after_collisions = len(self.collision_detector.get_collisions(after_tasks))
        return DiffReport(diff_list, was_collisions, after_collisions)
