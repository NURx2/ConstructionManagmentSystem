from generator.base_generator import BaseGenerator


def main():
    data = BaseGenerator().generate_data()
    print(len(data))

if __name__ == '__main__':
    main()