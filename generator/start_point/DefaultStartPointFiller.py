from generator.start_point.StartPointFiller import StartPointFiller

class DefaultStartPointFiller(StartPointFiller):
    def fill_start_points(self, tasks):
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
