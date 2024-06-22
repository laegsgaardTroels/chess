import cProfile
from argparse import Namespace
from chess.__main__ import machine_vs_machine


def main() -> None:
    with cProfile.Profile() as profile:
        machine_vs_machine(args=Namespace(verbose=False))
        profile.print_stats(sort="time")


if __name__ == "__main__":
    main()
