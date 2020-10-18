from abc import ABC, abstractmethod

class CacheMissException(Exception):
    pass

class Cache(ABC):
    @abstractmethod
    def save(self, key, value):
        pass

    @abstractmethod
    def is_in_cache(self, key):
        pass

    @abstractmethod
    def load_from_cache(self, key): # may throw exception if key isn't in cache (if not exception will return None)
        pass
