class DSU:
    def __init__(self, size):
        self.size = size
        self.parent = [0] * size
        for i in range(size):
            self.parent[i] = i
        self.components = size

    def get_group(self, node): # really shit
        while self.parent[node] != node:
            prev = node
            node = self.parent[node]
            self.parent[prev] = self.parent[node]
        return node

    def is_same_group(self, l, r):
        return self.get_group(l) == self.get_group(r)

    def merge(self, l, r):
        l = self.get_group(l)
        r = self.get_group(r)
        if l == r:
            return False
        self.parent[l] = r # fuck optimizations
        self.components -= 1
        return True

    def number_components(self):
        return self.components
