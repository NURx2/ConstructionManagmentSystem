class Task:
    def __init__(self, id, name, description, is_veha, start, is_movable, costs, min_time, time, lower_time):
        self.id = id
        self.name = name
        self.description = description
        self.is_veha = is_veha
        self.start = start
        self.is_movable = is_movable
        self.costs = costs
        assert(len(costs) == 2)
        assert('moveBack' in costs)
        assert('moveForward' in costs)
        self.min_time = min_time
        self.time = time
        self.lower_time = lower_time
        self.depends_on = set()

    def add_depends_on(self, task_id):
        self.depends_on.add(task_id)

    def __str__(self):
        return "Task [id: {}, name: {}, isVeha: {}]".format(self.id, self.name, self.is_veha)
