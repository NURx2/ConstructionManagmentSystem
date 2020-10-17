from abc import ABC, abstractmethod

class MetadataGenerator(ABC):
    @abstractmethod
    def generate_metadata(self, tasks) -> dict:
        pass
