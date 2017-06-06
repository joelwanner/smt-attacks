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
        attacks = self.checker.check()

        if attacks:
            for a in attacks:
                print("Attack found on %s." % a.victims)
        else:
            print("No attack possible.")

        if self.name:
            out_prefix = os.path.join(out_path, self.name) + "-"
            log.print_subsep()

            if attacks:
                for i, a in enumerate(attacks):
                    nr = NetworkRenderer(self.checker.network, a)
                    nr.render("%sattack%d" % (out_prefix, i + 1))
            else:
                nr = NetworkRenderer(self.checker.network, None)
                nr.render(out_prefix + "network")
                print("Network rendering is located at:\n%s-network.pdf" % out_prefix)

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
