import os
import time

import interface.log as log
from actions.check import NetworkChecker
from generators.crafted import AmplificationNetwork, CoremeltNetwork


class Benchmark(object):
    def __init__(self, output_path, ac_cls, n_runs):
        self.ac_cls = ac_cls
        self.n_runs = n_runs
        self.out_path = output_path
        self.logfile = output_path

    def run_files(self, directory):
        with self.create_logfile() as logfile:
            logfile.write("Runtimes\n-------------------\n")

            # Run all benchmarks in directory
            files = os.listdir(directory)
            n = len(files)

            for i, filename in enumerate(files):
                if filename.endswith(".txt"):
                    print()
                    log.print_header("BENCHMARK %d/%d" % (i + 1, n), filename)

                    runs = []
                    for k in range(self.n_runs):
                        checker = NetworkChecker.from_file(os.path.join(directory, filename), self.ac_cls,
                                                           10, render=False, verbose=False)

                        start_time = time.time()
                        checker.check_attack(out_path=None)
                        runs.append(time.time() - start_time)

                    runtime_str = ", ".join(["%.3f" % r for r in runs])
                    logfile.write("%s: %s\n" % (filename, runtime_str))

    def run_examples(self, sizes):
        with self.create_logfile() as logfile:
            log.print_header("Server Amplification Attacks")
            logfile.write("Server Amplification Attack\n")
            self.__run_example(AmplificationNetwork, sizes, [2 * n for n in sizes], logfile)

            log.print_header("Coremelt Attacks")
            logfile.write("\nCoremelt Attack\n")
            self.__run_example(CoremeltNetwork, sizes, [2 * n for n in sizes], logfile)

    def __run_example(self, attack_cls, sizes, n_flows, logfile):
        x = []
        runtimes = []

        for size, n in zip(sizes, n_flows):
            runs = []
            n_hosts = None

            for k in range(self.n_runs):
                print("Run %d/%d of network %s(%d)" % (k + 1, self.n_runs, attack_cls, size))
                attack = attack_cls(size)
                checker = self.ac_cls.from_network(attack, n)
                nc = NetworkChecker(checker)

                start_time = time.time()
                nc.check_attack(out_path=None)
                runs.append(time.time() - start_time)

                if not n_hosts:
                    n_hosts = len(attack.topology.hosts)

            runtime_str = ", ".join(["%.3f" % r for r in runs])
            x.append(n_hosts)
            runtimes.append("[%s]" % runtime_str)

        x_str = ", ".join(["%d" % n for n in x])
        y_str = ", ".join(runtimes)
        logfile.write("x = [%s]\ny = [%s]\n" % (x_str, y_str))

    def create_logfile(self):
        if os.path.isdir(self.out_path):
            i = 1
            file = None
            while not file or os.path.exists(file):
                file = os.path.join(self.out_path, "benchmark%d.txt" % i)
                i += 1

            self.logfile = file
            return open(file, 'w')
        else:
            return open(self.out_path, 'w')
