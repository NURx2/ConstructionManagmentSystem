from collision.DefaultCollisionGenerator import DefaultCollisionGenerator
from generator.DefaultGenerator import DefaultGenerator
from generator.metadata.DefaultMetadataGenerator import DefaultMetadataGenerator
from generator.start_point.DefaultStartPointFiller import DefaultStartPointFiller
from validation.CollisionDetector import CollisionDetector


def main():
    data = DefaultGenerator(DefaultStartPointFiller(), DefaultMetadataGenerator()).generate_data()
    detector = CollisionDetector()
    print(len(data))
    assert(len(detector.get_collisions(data)) == 0)

    collision_generator = DefaultCollisionGenerator()
    new_tasks = collision_generator.generate_collisions(data)
    assert(len(detector.get_collisions(data)) == 0)
    assert(len(detector.get_collisions(new_tasks)) != 0)

if __name__ == '__main__':
    main()