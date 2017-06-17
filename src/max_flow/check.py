import smt.check
from max_flow.algorithm import MaxFlow
from network.network import Network
from network.topology import *


class AttackChecker(smt.check.AttackChecker):
    def __init__(self, topology, _, victims=None, links=None, attackers=None):
        super().__init__(topology, 0, victims, links, attackers)

    def check_network(self, network):
        mf = MaxFlow(network)
        mf.compute_flow()

        attacked_hosts = []

        for v in network.victims:
            if isinstance(v, Host) and mf.flow_to_victim(v) > v.receiving_cap:
                attacked_hosts.append(v)

        if attacked_hosts:
            return Network(self.topology, 0, attacked_hosts, network.attackers)
        else:
            return None

    def check_host_attacks(self):
        if not self.attackers:
            potential_attackers = [h for h in self.topology.hosts
                                   if not (isinstance(h, Server) or (self.victims and h in self.victims))]
        else:
            potential_attackers = self.attackers

        if self.victims:
            potential_victims = self.victims
        else:
            if self.attackers:
                potential_victims = [h for h in self.topology.hosts if h not in self.attackers]
            else:
                potential_victims = self.topology.hosts

        for v in potential_victims:
            n = Network(self.topology, 0, [v], potential_attackers)
            attack = self.check_network(n)
            if attack:
                self.attacks.append(attack)

        return self.attacks
