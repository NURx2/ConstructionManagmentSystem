import lorem
from generator.generator import Generator
from data.task import Task

class BaseGenerator(Generator):
    def generate_data(self):
        return [Task(0, lorem.sentence(), lorem.text(), False, 0, True, {'moveBack': 100, 'moveForward': 10}, 15, 20, 5)]

