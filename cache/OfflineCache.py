from cache.Cache import Cache, CacheMissException
from pathlib import Path
import os

class OfflineCache(Cache):
    def __init__(self):
        self.working_dir = "./tmp/"
        Path(self.working_dir).mkdir(parents=True, exist_ok=True)

    def save(self, key, value):
        with open(self.working_dir + str(key), 'w') as out:
            out.write(str(value))
            out.flush()

    def is_in_cache(self, key):
        return str(key) in os.listdir(self.working_dir)

    def load_from_cache(self, key):
        with open(self.working_dir + str(key), 'r') as inp:
            return inp.read()
        raise CacheMissException()
