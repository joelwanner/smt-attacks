import argparse
import os

from actions.check import NetworkChecker
from actions.generate import Generator
from actions.benchmark import Benchmark
from generators.random import RandomTopology
import smt.check
import max_flow.check


EXAMPLES_PATH = "examples/"
OUTPUT_PATH = "out/"
DEFAULT_N_FLOWS = 6

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('-f', '--file')
    parser.add_argument('-e', '--example', help="run using a topology from the examples directory")
    parser.add_argument('-g', '--generate', choices=['random', 'crafted'], help="generate an example topology")
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

    if args.maxflow:
        Checker = max_flow.check.AttackChecker
    else:
        Checker = smt.check.AttackChecker

    if args.file:
        checker = NetworkChecker.from_file(args.file, n_flows, verbose=args.debug)
        checker.check_attack(output)

    if args.generate:
        if not os.path.exists(EXAMPLES_PATH):
            os.makedirs(EXAMPLES_PATH)

        g = Generator(EXAMPLES_PATH)

        if args.generate == 'random':
            size = int(input("Number of hosts: "))
            n = int(input("Number of networks: "))
            c = int(input("Connectivity: "))
            try:
                g.generate_random(n, size, c)
            except ValueError:
                print("Invalid arguments")

        elif args.generate == 'crafted':
            lower = int(input("Smallest size: "))
            upper = int(input("Largest size: "))
            try:
                g.generate_crafted(range(lower, upper + 1))
            except ValueError:
                print("Invalid arguments")

    if args.example:
        path = os.path.join(EXAMPLES_PATH, args.example + ".txt")
        checker = NetworkChecker.from_file(path, Checker, n_flows, verbose=args.debug)
        checker.check_attack(output)

    if args.benchmark:
        try:
            k = int(input("Number of runs for each network: "))
            b = Benchmark(output, Checker, k)

            if args.benchmark == 'examples':
                b.run_files(EXAMPLES_PATH)

            elif args.benchmark == 'crafted':
                lower = int(input("Smallest size: "))
                upper = int(input("Largest size: "))
                b.run_examples(range(lower, upper + 1))

            print("Benchmark output stored in %s" % b.logfile)

        except ValueError:
            print("Input is not a number")

    if args.random:
        c = int(input("Connectivity: "))
        network = RandomTopology(int(args.random), c)
        checker = Checker(network, DEFAULT_N_FLOWS)
        nc = NetworkChecker(checker, "random", verbose=args.debug)
        nc.check_attack(output)
