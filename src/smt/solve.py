import time

from z3 import *
import interface.log as log


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
        # TODO: investigate performance with case_split option
        s.set('smt.case_split', 3)        # Case split based on relevancy (structural splitting)
        s.set('smt.delay_units', True)    # Prevent Z3 from restarting when a unit clause is learned
        s.set('sk_hack', True)            # Enable hack for VCC
        s.set('smt.qi.eager_threshold', 100.0)  # Increase threshold for eager quantifier instantiation (default: 10.0)

        for a in assertions:
            s.add(a)

        log.print_subsep()
        print("Solving formula...")

        if self.verbose:
            log.print_subsep()
            print(s)

        start_time = time.time()
        result = s.check()
        runtime = time.time() - start_time

        if self.verbose:
            log.print_subheader("Statistics:")
            print(s.statistics())

        if result == sat:
            print("Satisfiable.")
            log.print_subsep()
            self.model = s.model()

            if self.verbose:
                print(self.model)
                log.print_sep()
        elif result == unsat:
            print("Unatisfiable.")
            log.print_subsep()
        else:
            print("Unknown.")
            log.print_subsep()

        log.print_subsep()
        print("Runtime: %.3fs" % runtime)

        return result
