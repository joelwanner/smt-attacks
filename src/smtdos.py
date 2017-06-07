import argparse
import os

from actions.check import NetworkChecker
from actions.generate import Generator
from actions.benchmark import benchmark_files, benchmark_examples
from generators.random import RandomNetwork
from smt.check import AttackChecker


EXAMPLES_PATH = "examples/"
OUTPUT_PATH = "out/"

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # TODO: add descriptions for arguments
    parser.add_argument("-f", action='store_true')
    parser.add_argument("--example")
    parser.add_argument("--generate", action='store_true')
    parser.add_argument("--benchmark", action='store_true')
    parser.add_argument("--random")

    parser.add_argument("--debug", action='store_true')
    parser.add_argument("-n")

    args = parser.parse_args()

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    if args.n:
        n_flows = int(args.n)
    else:
        n_flows = 10

    if args.f:
        checker = NetworkChecker.from_file(args.f, n_flows, verbose=args.debug)
        checker.check_attack(OUTPUT_PATH)

    if args.generate:
        if not os.path.exists(EXAMPLES_PATH):
            os.makedirs(EXAMPLES_PATH)

        g = Generator(EXAMPLES_PATH)
        # TODO: allow input to specify these parameters
        g.generate_random(10, 6)
        g.generate_crafted(range(3, 10))

    if args.example:
        path = os.path.join(EXAMPLES_PATH, args.example + ".txt")
        checker = NetworkChecker.from_file(path, n_flows, verbose=args.debug)
        checker.check_attack(OUTPUT_PATH)

    if args.benchmark:
        # TODO: add parameters to choose what happens
        # benchmark_files(EXAMPLES_PATH, OUTPUT_PATH)
        benchmark_examples(OUTPUT_PATH, range(3, 11))

    if args.random:
        network = RandomNetwork(int(args.random))
        checker = AttackChecker(network, 10)
        nc = NetworkChecker(checker, "random", verbose=args.debug)
        nc.check_attack(OUTPUT_PATH)
