import argparse
import os

from actions.check import NetworkChecker
from actions.generate import Generator
from actions.benchmark import benchmark_files, benchmark_examples
from generators.random import RandomTopology
from smt.check import AttackChecker


EXAMPLES_PATH = "examples/"
OUTPUT_PATH = "out/"
DEFAULT_N_FLOWS = 10

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file')
    parser.add_argument('-e', '--example', help="run a network from the examples directory")
    parser.add_argument('-g', '--generate', choices=['random', 'crafted'])
    parser.add_argument('-b', '--benchmark', choices=['examples', 'crafted'])
    parser.add_argument('-r', '--random')

    parser.add_argument('-d', '--debug', action='store_true')
    parser.add_argument('-n', help="number of flows in the model")
    parser.add_argument('-o', help="output path")

    parser.add_argument('--maxflow', action='store_true')

    args = parser.parse_args()

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    if args.n:
        n_flows = int(args.n)
    else:
        n_flows = DEFAULT_N_FLOWS

    if args.o:
        output = args.o
    else:
        output = OUTPUT_PATH

    if args.file:
        checker = NetworkChecker.from_file(args.file, n_flows, verbose=args.debug)
        checker.check_attack(output)

    if args.generate:
        if not os.path.exists(EXAMPLES_PATH):
            os.makedirs(EXAMPLES_PATH)

        clear = input("Remove existing examples? (y/N) ")

        if clear == 'y' or clear == 'Y':
            # Delete previous examples
            for f in os.listdir(EXAMPLES_PATH):
                path = os.path.join(EXAMPLES_PATH, f)
                try:
                    if os.path.isfile(path):
                        os.unlink(path)
                except OSError as e:
                    pass

        g = Generator(EXAMPLES_PATH)

        if args.generate == 'random':
            size = input("Number of hosts: ")
            n = input("Number of networks: ")
            try:
                g.generate_random(int(n), int(size))
            except ValueError:
                print("Invalid arguments")

        elif args.generate == 'crafted':
            lower = input("Smallest size: ")
            upper = input("Largest size: ")
            try:
                g.generate_crafted(range(int(lower), int(upper) + 1))
            except ValueError:
                print("Invalid arguments")

    if args.example:
        path = os.path.join(EXAMPLES_PATH, args.example + ".txt")
        checker = NetworkChecker.from_file(path, n_flows, verbose=args.debug)
        checker.check_attack(output)

    if args.benchmark:
        if args.benchmark == 'examples':
            benchmark_files(EXAMPLES_PATH, output)

        elif args.benchmark == 'crafted':
            lower = input("Smallest size: ")
            upper = input("Largest size: ")
            try:
                benchmark_examples(output, range(int(lower), int(upper) + 1))
            except ValueError:
                print("Invalid arguments")

    if args.random:
        network = RandomTopology(int(args.random))
        checker = AttackChecker(network, 10)
        nc = NetworkChecker(checker, "random", verbose=args.debug)
        nc.check_attack(output)
