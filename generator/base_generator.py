import lorem
from generator.generator import Generator
from data.task import Task

class DSU:
    def __init__(self, size):
        self.size = size
        self.parent = [0] * size
        for i in range(size):
            self.parent[i] = i

    def get_group(self, node): # really shit
        while self.parent[node] != node:
            prev = node
            node = self.parent[node]
            self.parent[prev] = self.parent[node]
        return node

    def merge(self, l, r):
        l = self.get_group(l)
        r = self.get_group(r)
        if l == r:
            return False
        self.parent[l] = r # fuck optimizations
        return True

class BaseGenerator(Generator):
    def generate_data(self):
        return [Task(0, lorem.sentence(), lorem.text(), False, 0, True, {'moveBack': 100, 'moveForward': 10}, 15, 20, 5)]

