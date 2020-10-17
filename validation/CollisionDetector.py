from data.task import Task

class Collision:
    def __init__(self, first_task_id, second_task_id):
        self.first_task_id = first_task_id
        self.second_task_id = second_task_id

class CollisionDetector:
    def __init__(self):
        pass # Lol, why the hell we need class?!?!?

    def get_collisions(self, tasks):
        collisions = []
        for task in tasks:
            for depends in task.depends_on:
                if tasks[depends].start + tasks[depends].time >= task.start:
                    collisions.append(Collision(depends, task.id))
        return collisions