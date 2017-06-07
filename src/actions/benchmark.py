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


def benchmark_examples(out_path, sizes):
    with create_logfile(out_path) as logfile:
        log.print_header("Server Amplification Attacks")
        logfile.write("Server Amplification Attack\n")

        runtimes = []
        for n in sizes:
            attack = AmplificationAttack(n)
            checker = AttackChecker.from_execution(attack, n * 2)
            nc = NetworkChecker(checker)

            start_time = time.time()
            nc.check_attack(out_path)
            runtime = time.time() - start_time

            n_hosts = n + 2
            print("n = %d: %.3fs" % (n_hosts, runtime))
            runtimes.append(runtime)

        x_str = ", ".join(["%.3f" % n for n in sizes])
        y_str = ", ".join(["%.3f" % t for t in runtimes])
        logfile.write("x = [%s]\ny = [%s]\n" % (x_str, y_str))
