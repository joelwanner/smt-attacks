import os

from smt.checker import AttackChecker
from interface.render import NetworkRenderer


# TODO: add checking routine
class NetworkChecker(object):
    def __init__(self, checker, path, name=None, verbose=False):
        self.checker = checker
        self.path = path
        self.name = name
        self.verbose = verbose

    def check_attack(self):
        attack_found = self.checker.check()

        if attack_found:
            print("Attack found.")
        else:
            print("No attack possible.")

        if self.name:
            out_prefix = os.path.join(self.path, self.name) + "-"
            nr = NetworkRenderer(self.checker.network, self.checker.victim, self.checker.attackers)
            nr.render(out_prefix + "network")
            print("Network rendering is located at " + out_prefix + "network.pdf")

    @classmethod
    def from_file(cls, path):
        file = open(path, "r")
        filename = os.path.splitext(os.path.basename(path))[0]

        try:
            checker = AttackChecker.from_string(file.read())
            return cls(checker, filename)

        except SyntaxError as e:
            print("Syntax error in file: " + str(e))
