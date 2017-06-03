import time

from z3 import *
from interface.log import *


class SmtSolver(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.model = None

    def solve(self, assertions):
        s = Solver()

        # Parameters
        # -----------------------------
        s.set('smt.ematching', False)     # Disable E-matching based quantifier instantiation
        s.set('smt.phase_selection', 0)   # Phase selection heuristic: always false
        s.set('smt.restart_strategy', 0)  # Restart strategy: geometric
        s.set('smt.restart_factor', 1.5)  # Increase restart threshold multiplication factor (geometric progression)
        s.set('smt.arith.random_initial_value', True)  # Use random initial values in procedure for linear arithmetic
        s.set('smt.case_split', 3)        # Case split based on relevancy (structural splitting)
        s.set('smt.delay_units', True)    # Prevent Z3 from restarting when a unit clause is learned
        s.set('sk_hack', True)            # Enable hack for VCC
        s.set('smt.qi.eager_threshold', 100.0)  # Increase threshold for eager quantifier instantiation (default: 10.0)

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
