from cache.Cache import Cache
from data.Task import Task
from typing import List
import json
import numpy as np

class TaskEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Task):
            return obj.__dict__
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, (set, int, str)):
            return list(obj)
        return json.JSONEncoder.default(self, obj)

def transform_into_tasks_list(json_tasks) -> List[Task]:
    result = []
    for json_task in json_tasks:
        depends_on = json_task['depends_on']
        del json_task['depends_on']
        task = Task(**json_task, depends_on=set(depends_on))
        result.append(task)
    result = sorted(result, key=lambda x: x.id)
    return result

class TaskCache(Cache): # extension for cache (just to load actual Tasks)
    def __init__(self, cache_class):
        self.cache = cache_class()

    def is_in_cache(self, key):
        return self.cache.is_in_cache(key)

    def load_from_cache(self, key):
        result = self.cache.load_from_cache(key)
        json_list = json.loads(result)
        return transform_into_tasks_list(json_list)

    def save(self, key, value: List[Task]):
        json_str = json.dumps(value, cls=TaskEncoder)
        self.cache.save(key, json_str)
