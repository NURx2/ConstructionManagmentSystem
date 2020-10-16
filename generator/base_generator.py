import lorem
from generator.generator import Generator
from data.task import Task
import numpy as np

class DSU:
    def __init__(self, size):
        self.size = size
        self.parent = [0] * size
        for i in range(size):
            self.parent[i] = i
        self.components = size

    def get_group(self, node): # really shit
        while self.parent[node] != node:
            prev = node
            node = self.parent[node]
            self.parent[prev] = self.parent[node]
        return node

    def is_same_group(self, l, r):
        return self.get_group(l) == self.get_group(r)

    def merge(self, l, r):
        l = self.get_group(l)
        r = self.get_group(r)
        if l == r:
            return False
        self.parent[l] = r # fuck optimizations
        self.components -= 1
        return True

    def number_components(self):
        return self.components

def fill_start_poins(tasks):
    pass

def create_graph_metadata(tasks):
    count_start_tasks = 0
    is_blocker = set()
    for task in tasks:
        if len(task.depends_on) == 0:
            count_start_tasks += 1
        for blocked in task.depends_on:
            is_blocker.add(blocked)
    count_end_tasks = len(tasks) - len(is_blocker)

    return {
        "start_tasks": count_start_tasks,
        "end_tasks": count_end_tasks
    }

class BaseGenerator(Generator):
    def generate_data(self, size=1000, seed=0, print_metadata=True):
        tasks = []
        np.random.seed(seed) # making this less random))
        for i in range(size):
            task_time = np.random.randint(1, 16)
            min_time = np.random.randint(task_time // 3 * 2, task_time + 1)
            tasks.append(Task(
                i,
                lorem.sentence().split()[0],
                lorem.sentence(),
                False,
                0, # start time, will be set after edges generation
                True,
                { 'moveBack': np.random.randint(0, 100), 'moveForward': np.random.randint(0, 100) },
                min_time,
                task_time,
                np.random.randint(0, 100)))

        dsu = DSU(size)
        
        count_edges = 0

        edges = []

        while dsu.number_components() != 1: # Processing until whole graph is somehow connected
            l = np.random.randint(0, size)
            r = np.random.randint(0, size)
            while l == r:
                l = np.random.randint(0, size)
                r = np.random.randint(0, size)
            if r < l:
                l, r = r, l
            assert(l < r)

            if count_edges > 3 * size:
                # if graph has more than V * 3 edges we want to connect large components, because as more edges
                # as more propability that we will connect tasks, that are already in same component
                # (in such case we can end up with too many edges)
                if not dsu.is_same_group(l, r):
                    count_edges += 1
                    assert(dsu.merge(l, r))
                    edges.append((l, r))
            else:
                count_edges += 1
                dsu.merge(l, r)
                assert(dsu.is_same_group(l, r))
                edges.append((l, r))

        for (required, blocked) in edges:
            assert(required < blocked)
            tasks[blocked].add_depends_on(required)

        if print_metadata:
            metadata = create_graph_metadata(tasks)
            for field in metadata:
                print(field, ':', metadata[field])

        fill_start_poins(tasks)

        return tasks

