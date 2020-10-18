from data.Task import Task

def calculate_move_cost(before: Task, after: Task) -> int:
    if before.start < after.start:
        return before.costs['moveForward'] * (after.start - before.start)
    return before.costs['moveBack'] * (before.start - after.start)

def calculate_shrink_cost(before: Task, after: Task):
    assert(before.time > after.time)
    return before.lower_time * (before.time - after.time)

class Diff:
    def __init__(self, before: Task, after: Task):
        assert(before != after)
        assert(before.id == after.id)
        self.was_moved = before.start != after.start
        self.was_shrinked = before.time != after.time
        self.move_cost = 0 if not self.was_moved else calculate_move_cost(before, after)
        self.shrink_cost = 0 if not self.was_shrinked else calculate_shrink_cost(before, after)
        self.whole_cost = self.move_cost + self.shrink_cost