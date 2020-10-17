from collision.DefaultCollisionGenerator import DefaultCollisionGenerator
from generator.WeightedGenerator import WeightedGenerator
from generator.metadata.DefaultMetadataGenerator import DefaultMetadataGenerator
from generator.start_point.DefaultStartPointFiller import DefaultStartPointFiller
from solution.JustCopySolution import JustCopySolution
from validation.CollisionDetector import CollisionDetector


def main():
    data = WeightedGenerator(DefaultStartPointFiller(), DefaultMetadataGenerator()).generate_data()
    detector = CollisionDetector()
    print(len(data))
    assert(len(detector.get_collisions(data)) == 0)

    collision_generator = DefaultCollisionGenerator()
    new_tasks = collision_generator.generate_collisions(data)
    assert(len(detector.get_collisions(data)) == 0)
    assert(len(detector.get_collisions(new_tasks)) != 0)

    solutions = [
        JustCopySolution()
    ]

    for solution in solutions:
        result = solution.solve(new_tasks)
        if len(detector.get_collisions(result)) != 0:
            print("Solution", solution, "failed, still have:", len(detector.get_collisions(result)), "collisions")

if __name__ == '__main__':
    main()