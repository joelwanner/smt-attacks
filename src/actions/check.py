import os

import interface.log as log
from network.network import Network
from interface.render import NetworkRenderer


class NetworkChecker(object):
    def __init__(self, checker, name=None, verbose=False):
        self.checker = checker
        checker.verbose = verbose

        self.name = name
        self.verbose = verbose

    def check_attack(self, out_path):
        if self.checker.target_links:
            attacks = self.checker.check_link_attack()
        else:
            attacks = self.checker.check_host_attacks()

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
                    path = "%sattack%d" % (out_prefix, i + 1)
                    nr = NetworkRenderer(a)
                    nr.render(path)
                    print("Attack rendering is located at:\n%s.pdf" % path)
            else:
                nr = NetworkRenderer(Network(self.checker.topology, 0))
                nr.render(out_prefix + "network")
                print("Network rendering is located at:\n%snetwork.pdf" % out_prefix)

        log.print_sep()

    @classmethod
    def from_file(cls, path, ac_cls, n_flows, render=True, verbose=False):
        file = open(path, "r")

        if render:
            filename = os.path.splitext(os.path.basename(path))[0]
        else:
            filename = None

        log.print_header("Running example '%s'" % filename, path)

        try:
            s = file.read()
            file.close()
            if verbose:
                print(s)

            checker = ac_cls.from_string(s, n_flows)
            return cls(checker, filename, verbose)

        except SyntaxError as e:
            print("Syntax error in file: " + str(e))
