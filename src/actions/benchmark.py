import os
import time

import interface.log as log
from actions.check import NetworkChecker
from generators.crafted import AmplificationAttack, CoremeltAttack
from smt.check import AttackChecker


def create_logfile(directory):
    i = 1
    path = None
    while not path or os.path.exists(path):
        path = os.path.join(directory, "benchmark%d.txt" % i)
        i += 1

    return open(path, 'w')


def benchmark_files(directory, out_path):
    with create_logfile(out_path) as logfile:
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


def __benchmark_example(cls, sizes, n_flows, logfile):
    runtimes = []
    for i, n in enumerate(sizes):
        attack = cls(n)
        checker = AttackChecker.from_execution(attack, n_flows[i])
        nc = NetworkChecker(checker)

        start_time = time.time()
        nc.check_attack(out_path=None)
        runtime = time.time() - start_time

        print("Runtime for %d hosts: %.3fs" % (len(attack.network.hosts), runtime))

    x_str = ", ".join(["%.3f" % n for n in sizes])
    y_str = ", ".join(["%.3f" % t for t in runtimes])
    logfile.write("x = [%s]\ny = [%s]\n" % (x_str, y_str))


def benchmark_examples(out_path, sizes):
    with create_logfile(out_path) as logfile:
        log.print_header("Server Amplification Attacks")

        logfile.write("Server Amplification Attack\n")
        __benchmark_example(AmplificationAttack, sizes, [2 * n for n in sizes], logfile)

        logfile.write("Coremelt Attack\n")
        __benchmark_example(CoremeltAttack, sizes, [2 * n for n in sizes], logfile)
