import argparse
import os

from actions.network import NetworkChecker
from actions.benchmark import Benchmark
from actions.generate import Generator


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

    args = parser.parse_args()

    if not os.path.exists(OUTPUT_PATH):
        os.makedirs(OUTPUT_PATH)

    if args.f:
        checker = NetworkChecker.from_file(args.f)

    if args.generate:
        if not os.path.exists(EXAMPLES_PATH):
            os.makedirs(EXAMPLES_PATH)

        g = Generator(EXAMPLES_PATH)
        g.generate_random(10, 6)
        g.generate_crafted(range(2, 6))

    if args.example:
        path = os.path.join(EXAMPLES_PATH, args.example + ".txt")
        checker = NetworkChecker.from_file(path)

    if args.benchmark:
        b = Benchmark()

    if args.random:
        n = int(args.random)
        # TODO: create random network and check for attack
