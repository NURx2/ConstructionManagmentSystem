from generator.BaseGenerator import BaseGenerator
from validation.CollisionDetector import CollisionDetector
from collision.DefaultCollisionGenerator import DefaultCollisionGenerator
from generator.start_point.DefaultStartPointFiller import DefaultStartPointFiller


def main():
    data = BaseGenerator(DefaultStartPointFiller()).generate_data()
    detector = CollisionDetector()
    print(len(data))
    assert(len(detector.get_collisions(data)) == 0)

    collision_generator = DefaultCollisionGenerator()
    new_tasks = collision_generator.generate_collisions(data)
    assert(len(detector.get_collisions(data)) == 0)
    assert(len(detector.get_collisions(new_tasks)) != 0)

if __name__ == '__main__':
    main()