from cache.OfflineCache import OfflineCache
from cache.TaskCache import TaskCache
from collision.DefaultCollisionGenerator import DefaultCollisionGenerator
from diff.DiffGenerator import DiffGenerator
from generator.GeneratorWithCache import GeneratorWithCache
from generator.metadata.DefaultMetadataGenerator import DefaultMetadataGenerator
from generator.start_point.DefaultStartPointFiller import DefaultStartPointFiller
from generator.WeightedGenerator import WeightedGenerator
from solution.JustCopySolution import JustCopySolution
from solution.NaiveSolution import NaiveSolution
from validation.CollisionDetector import CollisionDetector
import json


def main():
    generator = GeneratorWithCache(WeightedGenerator(DefaultStartPointFiller(), DefaultMetadataGenerator()))
    data = generator.generate_data()
    detector = CollisionDetector()
    print(len(data))
    assert(len(detector.get_collisions(data)) == 0)

    cache = TaskCache(OfflineCache)
    cache.save(len(data), data)
    assert(cache.is_in_cache(len(data)))
    assert(len(cache.load_from_cache(len(data))) == len(data))
    index = 0
    for cached in cache.load_from_cache(len(data)):
        assert(data[index] == cached)
        index += 1

    collision_generator = DefaultCollisionGenerator(collisions_needed=100)
    new_tasks = collision_generator.generate_collisions(data)
    assert(len(detector.get_collisions(data)) == 0)
    assert(len(detector.get_collisions(new_tasks)) != 0)
    assert(len(data) == len(new_tasks))

    solutions = [
        JustCopySolution(),
        NaiveSolution()
    ]
    
    diff_generator = DiffGenerator()

    for solution in solutions:
        result = solution.solve(new_tasks)
        collisions_count = len(detector.get_collisions(result))
        if collisions_count != 0:
            print("Solution", solution.name(), "failed, still have:", collisions_count, "collisions")
        else:
            print("Success")
            report = diff_generator.generate_diff(new_tasks, result)
            print("Solution whole cost:", report.whole_cost)
            print("Moved tasks:", len(report.diff_list))

if __name__ == '__main__':
    main()