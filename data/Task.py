from typing import Dict, Set


class Task:
    def __init__(self, id, name, description, is_veha, start, is_movable, costs, min_time, time, lower_time, depends_on=set()):
        self.id: int = id
        self.name: str = name
        self.description: str = description
        self.is_veha: bool = is_veha
        self.start: int = start
        self.is_movable: bool = is_movable
        self.costs: Dict[str, int] = costs
        assert(len(costs) == 2)
        assert('moveBack' in costs)
        assert('moveForward' in costs)
        self.min_time: int = min_time
        self.time: int = time
        self.lower_time: int = lower_time
        self.depends_on: Set[int] = set(depends_on)

    def add_depends_on(self, task_id: int):
        self.depends_on.add(task_id)

    def is_depends_on(self, task_id: int):
        return task_id in self.depends_on

    def copy(self):
        return Task(
            self.id,
            self.name,
            self.description,
            self.is_veha,
            self.start,
            self.is_movable,
            self.costs,
            self.min_time,
            self.time,
            self.lower_time,
            self.depends_on)

    def __str__(self):
        return "Task [id: {}, name: {}, isVeha: {}]".format(self.id, self.name, self.is_veha)
