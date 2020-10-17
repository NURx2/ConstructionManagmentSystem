from data.Diff import Diff
from typing import List

class DiffReport:
    def __init__(self, diff_list: List[Diff], was_collisions: int, now_collisions):
        self.diff_list = diff_list
        self.was_collisions = was_collisions
        self.now_collisions = now_collisions
        self.whole_cost = 0
        for diff in self.diff_list:
            self.whole_cost += diff.whole_cost