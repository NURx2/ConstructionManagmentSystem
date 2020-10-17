from cache.OfflineCache import OfflineCache
from cache.TaskCache import TaskCache
from generator.Generator import Generator

class GeneratorWithCache(Generator):
    def __init__(self, generator):
        assert(isinstance(generator, Generator))
        self.generator = generator
        self.task_cache = TaskCache(OfflineCache)

    def generate_data(self, *args, **kwargs):
        key = str(args) + "-" + str(kwargs)
        if self.task_cache.is_in_cache(key):
            print("Got from cache")
            return self.task_cache.load_from_cache(key)

        result = self.generator.generate_data(*args, **kwargs)
        self.task_cache.save(key, result)
        return result
