from typing import List

from data.Task import Task

class Collision:
    def __init__(self, first_task_id, second_task_id):
        self.first_task_id = first_task_id
        self.second_task_id = second_task_id

class CollisionDetector:
    def __init__(self):
        pass # Lol, why the hell we need class?!?!?

    @staticmethod
    def get_collisions(tasks: List[Task]) -> List[Collision]:
        collisions = []
        for task in tasks:
            for depends in task.depends_on:
                if tasks[depends].start + tasks[depends].time >= task.start:
                    collisions.append(Collision(depends, task.id))
        return collisions

    @staticmethod
    def get_collisions_from(tasks: List[Task], from_task: Task) -> List[int]:
        collisions = []
        for task in tasks:
            for depend in task.depends_on:
                if depend == from_task.id and from_task.start + from_task.time >= task.start:
                    collisions.append(task.id)
        return collisions
