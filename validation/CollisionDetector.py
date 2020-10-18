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
    def check_tasks_collision(task_a: Task, task_b: Task) -> bool:
        return task_a.start + task_a.time >= task_b.start

    @staticmethod
    def check_collision(tasks: List[Task], collision: Collision):
        return CollisionDetector.check_tasks_collision(tasks[collision.first_task_id], tasks[collision.second_task_id])

    @staticmethod
    def get_collisions(tasks: List[Task]) -> List[Collision]:
        collisions = []
        for task in tasks:
            for depends in task.depends_on:
                if CollisionDetector.check_tasks_collision(tasks[depends], task):
                    collisions.append(Collision(depends, task.id))
        return collisions

    @staticmethod
    def get_collisions_from(tasks: List[Task], from_task: Task) -> List[int]:
        collisions = []
        for task in tasks:
            for depend in task.depends_on:
                if depend == from_task.id and CollisionDetector.check_tasks_collision(from_task, task):
                    collisions.append(task.id)
        return collisions
