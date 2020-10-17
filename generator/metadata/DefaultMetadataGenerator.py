from data.Task import Task
from generator.metadata.MetadataGenerator import MetadataGenerator

class DefaultMetadataGenerator(MetadataGenerator):
    def generate_metadata(self, tasks):
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

        vehas = 0
        for task in tasks:
            if task.is_veha:
                vehas += 1

        return {
            "critical_path_time_length": critical_path_time_length,
            "end_tasks": count_end_tasks,
            "start_tasks": count_start_tasks,
            "total_dependencies": dependencies,
            "vehas_count": vehas
        }
