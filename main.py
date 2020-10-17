from collision.DefaultCollisionGenerator import DefaultCollisionGenerator
from generator.WeightedGenerator import WeightedGenerator
from generator.metadata.DefaultMetadataGenerator import DefaultMetadataGenerator
from generator.start_point.DefaultStartPointFiller import DefaultStartPointFiller
from solution.JustCopySolution import JustCopySolution
from solution.NaiveSolution import NaiveSolution
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
    assert(len(data) == len(new_tasks))

    solutions = [
        JustCopySolution(),
        NaiveSolution()
    ]

    for solution in solutions:
        result = solution.solve(new_tasks)
        collisions_count = len(detector.get_collisions(result))
        if collisions_count != 0:
            print("Solution", solution.name(), "failed, still have:", collisions_count, "collisions")

if __name__ == '__main__':
    main()