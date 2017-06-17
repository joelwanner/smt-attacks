from smt.check import AttackChecker
from max_flow.algorithm import MaxFlow


class MaxFlowChecker(AttackChecker):
    def __init__(self, network, victims=None, links=None, attackers=None):
        super().__init__(network, 0, victims, links, attackers)

    def check_network(self, network):
        mf = MaxFlow(network)
        mf.compute_flow()

        for v in network.victims:
            if mf.flow_to_victim(v) > v.receiving_cap:
                return True

        return False
