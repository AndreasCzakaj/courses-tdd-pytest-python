"""The "app": prints a new UUID. Run it with `python -m funwithflags`."""

from funwithflags.uuid_generator import UuidGeneratorNaiveRandomImpl


def main() -> None:
    print(UuidGeneratorNaiveRandomImpl().create())


if __name__ == "__main__":
    main()
