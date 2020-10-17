from generator.BaseGenerator import BaseGenerator
from validation.CollisionDetector import CollisionDetector


def main():
    data = BaseGenerator().generate_data()
    detector = CollisionDetector()
    print('Collisions:', len(detector.get_collisions(data)))
    print(len(data))
    assert(len(detector.get_collisions(data)) == 0)
    for collision in detector.get_collisions(data):
        first, second = collision.first_task_id, collision.second_task_id
        print(first, second)
        print(data[first].start + data[first].time, data[second].time)

if __name__ == '__main__':
    main()