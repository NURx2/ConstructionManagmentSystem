from data.DiffReport import DiffReport
from data.Task import Task
from diff.DiffGenerator import DiffGenerator
from solution.Solution import Solution
from typing import List
import copy
import numpy as np

from solution.utils import sort_uniq
from validation.CollisionDetector import CollisionDetector


class SimulatedAnnealingSolution(Solution):
    def __init__(self, K: int, temp: float, REDUCE: float, BOUND: float, VEHA_COST: int, MAX_VEHA_COUNT: int,
                 COLLISION_PENALTY: int = None, prestart: List[Task] = None):
        self.K = K
        self.temp = temp
        self.REDUCE = REDUCE
        self.BOUND = BOUND
        if COLLISION_PENALTY is not None:
            self.COLLISION_PENALTY = COLLISION_PENALTY
        else:
            self.COLLISION_PENALTY = VEHA_COST * (MAX_VEHA_COUNT + 5)
        self.prestart = prestart

    def calc_score(self, diff: DiffReport) -> int:
        return diff.now_collisions * self.COLLISION_PENALTY + diff.whole_cost

    def make_random_move(self, tasks: List[Task], steps: int):
        incident_tasks = []

        collisions = CollisionDetector.get_collisions(tasks)

        for collision in collisions:
            incident_tasks.append(collision.first_task_id)
            incident_tasks.append(collision.second_task_id)

        incident_tasks = list(sort_uniq(incident_tasks))
        if len(incident_tasks) == 0:
            incident_tasks = range(len(tasks))
        moves_in = np.random.choice(incident_tasks, steps)

        for id in moves_in:
            pos_moves = []

            if tasks[id].lower_time != -1 and tasks[id].time > tasks[id].min_time:
                pos_moves.append('lower')
            if tasks[id].costs['moveBack'] != -1:
                pos_moves.append('back')
            if tasks[id].costs['moveForward'] != -1:
                pos_moves.append('forward')

            action = np.random.choice(pos_moves)

            if action == 'lower':
                tasks[id].time -= 1
            elif action == 'back':
                tasks[id].start -= 1
            elif action == 'forward':
                tasks[id].start += 1

    def solve(self, tasks: List[Task]) -> List[Task]: # we need to copy tasks (to make previous tasks immutable)
        tasks_initial = copy.deepcopy(tasks)
        tasks = copy.deepcopy(tasks) if self.prestart is None else copy.deepcopy(self.prestart)

        score = self.calc_score(DiffGenerator().generate_diff(tasks_initial, tasks))
        best_score = score
        best_state = copy.deepcopy(tasks)

        while self.K * self.temp > self.BOUND:
            prev = copy.deepcopy(tasks)
            self.make_random_move(tasks, max(int(self.K * self.temp), 1))

            now_score = self.calc_score(DiffGenerator().generate_diff(tasks_initial, tasks))

            if now_score < score:
                score = now_score

                if score < best_score:
                    best_score = score
                    best_state = copy.deepcopy(tasks)
            else:
                p = np.exp((score - now_score) / self.temp)

                if np.random.uniform(0, 1) <= p:
                    score = now_score
                else:
                    tasks = prev

            self.temp *= self.REDUCE

        return best_state

