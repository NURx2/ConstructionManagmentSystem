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

    dependencies = 0
    for task in tasks:
        dependencies += len(task.depends_on)

    return {
        "critical_path_time_length": critical_path_time_length,
        "end_tasks": count_end_tasks,
        "start_tasks": count_start_tasks,
        "total_dependencies": dependencies
    }

class BaseGenerator(Generator):
    def __init__(self, start_point_filler):
        self.start_point_filler = start_point_filler
        assert(isinstance(start_point_filler, StartPointFiller))

    def generate_data(self, size=1000, count_vehas=5, seed=0, print_metadata=True):
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

        edges = set()

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
                    edges.add((l, r))
            else:
                count_edges += 1
                dsu.merge(l, r)
                assert(dsu.is_same_group(l, r))
                edges.add((l, r))

        for (required, blocked) in edges:
            assert(required < blocked)
            tasks[blocked].add_depends_on(required)

        # now we need to generate some veha's!!!
        # we'll pick some random indices from 10%-90% range tasks

        middle_range = np.arange(size // 10, size * 9 // 10 + 1)
        p = np.zeros(len(middle_range))
        sum_deps = 0
        for index in middle_range:
            sum_deps += len(tasks[index].depends_on)
        for index in middle_range:
            p[index - size // 10] = len(tasks[index].depends_on) / sum_deps
        veha_indices = sorted(np.random.choice(middle_range, count_vehas, p=p))
        for veha_index in veha_indices:
            tasks[veha_index].time = 0
            tasks[veha_index].min_time = 0
            tasks[veha_index].is_movable = False
            tasks[veha_index].is_veha = True
            tasks[veha_index].costs = {'moveBack': 100 * 10000, 'moveForward': 100 * 10000}

        self.start_point_filler.fill_start_points(tasks)

        if print_metadata:
            metadata = create_graph_metadata(tasks)
            for field in metadata:
                print(field, ':', metadata[field])

        return tasks

