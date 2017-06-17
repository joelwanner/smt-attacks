import smt.check
from max_flow.algorithm import MaxFlow
from network.network import Network


class AttackChecker(smt.check.AttackChecker):
    def __init__(self, topology, _, victims=None, links=None, attackers=None):
        super().__init__(topology, 0, victims, links, attackers)

    def check_network(self, network):
        mf = MaxFlow(network)
        mf.compute_flow()

        attacked_hosts = []

        for v in network.victims:
            if mf.flow_to_victim(v) > v.receiving_cap:
                attacked_hosts.append(v)

        return Network(self.topology, 0, attacked_hosts, self.attackers)
