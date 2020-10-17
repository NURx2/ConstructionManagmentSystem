import lorem
from generator.Generator import Generator
from data.Task import Task
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
    queue = []
    blocker_to = dict()
    for task in tasks:
        if len(task.depends_on) == 0:
            queue.append(task.id) # using that id == index in the list (data design leak, but fine for now)
        for depends in task.depends_on:
            if depends in blocker_to:
                blocker_to[depends].add(task.id)
            else:
                blocker_to[depends] = set([task.id])
    
    used_links = dict()
    max_blocker_time_values = dict()
    visited = set()

    for i in range(len(tasks)):
        used_links[i] = 0
        max_blocker_time_values[i] = 0

    while len(queue) != 0:
        task_id = queue[0]
        queue = queue[1:]

        assert(task_id not in visited)
        visited.add(task_id)

        if not task_id in blocker_to:
            continue

        for blocked in blocker_to[task_id]:
            used_links[blocked] += 1
            max_blocker_time_values[blocked] = max(
                max_blocker_time_values[blocked],
                tasks[task_id].start + tasks[task_id].time)
            if used_links[blocked] == len(tasks[blocked].depends_on):
                queue.append(blocked)
                tasks[blocked].start = max_blocker_time_values[blocked] + 1


def create_graph_metadata(tasks):
    count_start_tasks = 0
    is_blocker = set()
    for task in tasks:
        if len(task.depends_on) == 0:
            count_start_tasks += 1
        for blocked in task.depends_on:
            is_blocker.add(blocked)
    count_end_tasks = len(tasks) - len(is_blocker)

    critical_path_time_length = 0
    for task in tasks:
        critical_path_time_length = max(
            critical_path_time_length,
            task.start + task.time)

    return {
        "start_tasks": count_start_tasks,
        "end_tasks": count_end_tasks,
        "critical_path_time_length": critical_path_time_length
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

        fill_start_poins(tasks)

        if print_metadata:
            metadata = create_graph_metadata(tasks)
            for field in metadata:
                print(field, ':', metadata[field])

        return tasks

