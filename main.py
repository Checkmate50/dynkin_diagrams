from src import diagram_manager
from src import cartan_generator


def main():
    print(diagram_manager.ddiagram("D", 6))
    print(cartan_generator.gen_cartan([[0, 1], [1, 0]]))


if __name__ == "__main__":
    main()

