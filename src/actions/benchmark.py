import os
import time

import interface.log as log
from actions.check import NetworkChecker


def run_benchmarks(directory, out_path):
    # Create logfile (not replacing existing ones)
    i = 1
    path = None
    while not path or os.path.exists(path):
        path = os.path.join(out_path, "benchmark%d.txt" % i)
        i += 1

    with open(path, 'w') as logfile:
        logfile.write("Runtimes\n-------------------\n")

        # Run all benchmarks in directory
        files = os.listdir(directory)
        n = len(files)

        for i, filename in enumerate(files):
            if filename.endswith(".txt"):
                print()
                log.print_header("BENCHMARK %d/%d" % (i + 1, n), filename)

                checker = NetworkChecker.from_file(os.path.join(directory, filename), 10, verbose=False)

                start_time = time.time()
                checker.check_attack(out_path)
                runtime = time.time() - start_time

                logfile.write("%s: %.3f\n" % (filename, runtime))
