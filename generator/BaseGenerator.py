from data.Task import Task
from generator.Generator import Generator
from generator.start_point.StartPointFiller import StartPointFiller
from structure.DSU import DSU
import lorem
import numpy as np

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
    def __init__(self, start_point_filler):
        self.start_point_filler = start_point_filler
        assert(isinstance(start_point_filler, StartPointFiller))

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

        self.start_point_filler.fill_start_points(tasks)

        if print_metadata:
            metadata = create_graph_metadata(tasks)
            for field in metadata:
                print(field, ':', metadata[field])

        return tasks

