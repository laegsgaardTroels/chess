import cProfile
from argparse import Namespace
from chess.__main__ import machine_vs_machine


def profiler():
    machine_vs_machine(args=Namespace(verbose=False))


if __name__ == "__main__":
    cProfile.run("profiler()", sort="time")
