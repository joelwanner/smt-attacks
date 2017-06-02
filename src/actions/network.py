import os
import time

from smt.checker import AttackChecker


# TODO: add checking routine
class NetworkChecker(object):
    def __init__(self, checker, name=None, render=True, verbose=False):
        self.checker = checker
        self.name = name

    def check_attack(self):
        start_time = time.time()
        attack_found = self.checker.check_attack()
        runtime = time.time() - start_time
        print("Algorithm runtime: %.5fs" % runtime)

        if attack_found:
            print("Attack found.")
        else:
            print("No attack possible.")

        # if name:
        #     out_prefix = os.path.join(OUTPUT_PATH, name) + "-"
        #     render_network(checker.get_network(), out_prefix + "network", checker.victim, checker.attackers)
        #     print("Network rendering is located at " + out_prefix + "network.pdf")
        #
        #     if debug:
        #         graph, flow = checker.get_graph()
        #         render_graph(graph, out_prefix + "graph")
        #         render_graph(graph, out_prefix + "graph_flow", flow)

    @classmethod
    def from_file(cls, path):
        file = open(path, "r")
        filename = os.path.splitext(os.path.basename(path))[0]

        try:
            checker = AttackChecker.from_string(file.read())
            return cls(checker, filename)

        except SyntaxError as e:
            print("Syntax error in file: " + str(e))
