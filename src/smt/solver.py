import time

from z3 import *
from interface.log import *


class SmtSolver(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.model = None

    def solve(self, assertions):
        s = Solver()

        for a in assertions:
            s.add(a)

        start_time = time.time()
        result = s.check()
        runtime = time.time() - start_time

        if self.verbose:
            print_header("Done. Runtime: %.3fs" % runtime, "Statistics:")
            print(s.statistics())
        else:
            print_header("Done. Runtime: %.3fs" % runtime)

        if result == sat:
            print_header("Satisfiable")
            self.model = s.model()
        elif result == unsat:
            print_header("Unatisfiable")
        else:
            print_header("Unknown")

        return result
