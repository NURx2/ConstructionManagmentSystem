from data.Task import Task
from generator.Generator import Generator
from generator.metadata.MetadataGenerator import MetadataGenerator
from generator.start_point.StartPointFiller import StartPointFiller
from structure.DSU import DSU
import lorem
import numpy as np

class WeightedGenerator(Generator):
    def __init__(self, start_point_filler, metadata_generator):
        self.start_point_filler = start_point_filler
        assert(isinstance(start_point_filler, StartPointFiller))
        self.metadata_generator = metadata_generator
        assert(isinstance(metadata_generator, MetadataGenerator))

    def generate_data(self, size=1000, count_vehas=5, seed=0, print_metadata=True):
        tasks = []
        np.random.seed(seed)
        for i in range(size):
            task_time = np.random.randint(1, 16)
            min_time = np.random.randint(task_time // 3 * 2, task_time + 1)
            tasks.append(Task(
                i,
                lorem.sentence().split()[0],
                lorem.sentence(),
                False,
                0,
                True,
                { 'moveBack': np.random.randint(0, 100), 'moveForward': np.random.randint(0, 100) },
                min_time,
                task_time,
                np.random.randint(0, 100)))

        middle_range = np.arange(size // 10, size * 9 // 10 + 1)
        veha_indices = sorted(np.random.choice(middle_range, count_vehas))
        for veha_index in veha_indices:
            tasks[veha_index].time = 0
            tasks[veha_index].min_time = 0
            tasks[veha_index].is_movable = False
            tasks[veha_index].is_veha = True
            tasks[veha_index].costs = {'moveBack': 100 * 10000, 'moveForward': 100 * 10000}

        # now we create propabilities array for edges generation
        p = [0] * size
        # we assume that propability of participation of veha is more in ten times than any other task
        default_task_propability = 1 / (size - count_vehas + count_vehas * 10)
        veha_propability = default_task_propability * 10

        for i in range(size):
            if i in veha_indices:
                p[i] = veha_propability
            else:
                p[i] = default_task_propability

        dsu = DSU(size)
        
        count_edges = 0

        edges = set()

        indices = list(np.arange(0, size))

        while dsu.number_components() != 1: # Processing until whole graph is somehow connected
            l, r = np.random.choice(indices, 2, p=p)
            while l == r:
                l, r = np.random.choice(indices, 2, p=p)
            if r < l:
                l, r = r, l
            assert(l < r)

            if tasks[l].is_veha and tasks[r].is_veha:
                continue

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

        self.start_point_filler.fill_start_points(tasks)

        if print_metadata:
            metadata = self.metadata_generator.generate_metadata(tasks)
            for field in metadata:
                print(field, ':', metadata[field])

        return tasks
