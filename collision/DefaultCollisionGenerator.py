from collision.CollisionGenerator import CollisionGenerator
import copy
import numpy as np

class DefaultCollisionGenerator(CollisionGenerator):
    def __init__(self, collisions_needed=1, random_seed=0): # will generate at least collisions_needed collisions!
        self.collisions_needed = collisions_needed
        self.random_seed = random_seed

    def generate_collisions(self, tasks_from):
        tasks = copy.deepcopy(tasks_from)
        np.random.seed(self.random_seed)
        remaining_collisions = self.collisions_needed

        used = set()

        while remaining_collisions != 0:
            task_id = np.random.randint(0, len(tasks))
            if task_id in used:
                continue
            used.add(task_id)
            remaining_collisions -= 1

            for task in tasks:
                if task.is_depends_on(task_id):
                    tasks[task_id].time = task.start - tasks[task_id].start
                    break
        assert(remaining_collisions == 0)
        return tasks
