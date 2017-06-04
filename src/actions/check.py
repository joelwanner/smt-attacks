import os

import interface.log as log
from smt.check import AttackChecker
from interface.render import NetworkRenderer


class NetworkChecker(object):
    def __init__(self, checker, name=None, verbose=False):
        self.checker = checker
        checker.verbose = verbose

        self.name = name
        self.verbose = verbose

    def check_attack(self, out_path):
        attack_found = self.checker.check()

        if attack_found:
            print("Attack found on %s." % self.checker.attack.victim.__repr__())
        else:
            print("No attack possible.")

        if self.name:
            if attack_found:
                attack = self.checker.attack
            else:
                attack = None

            out_prefix = os.path.join(out_path, self.name) + "-"
            nr = NetworkRenderer(self.checker.network, attack)
            nr.render(out_prefix + "network")

            log.print_subsep()
            print("Network rendering is located at:\n" + out_prefix + "network.pdf")

        log.print_sep()

    @classmethod
    def from_file(cls, path, n_flows, verbose=False):
        file = open(path, "r")
        filename = os.path.splitext(os.path.basename(path))[0]

        log.print_header("Running example '%s'" % filename, path)

        try:
            s = file.read()
            if verbose:
                print(s)

            checker = AttackChecker.from_string(s, n_flows)
            return cls(checker, filename, verbose)

        except SyntaxError as e:
            print("Syntax error in file: " + str(e))
