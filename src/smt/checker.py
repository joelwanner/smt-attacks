from network.network import *
from network.execution import Execution

class AttackChecker:
    def __init__(self, network, victim, attackers):
        self.network = network
        self.victim = victim
        self.attackers = attackers

    def __check(self, execution):
        raise NotImplementedError

    def check_attack(self):
        if not self.attackers or not self.victim:
            regular_hosts = []
            for h in self.network.hosts:
                if not (isinstance(h, Server) or h == self.victim):
                    regular_hosts.append(h)
        else:
            regular_hosts = self.attackers

        if self.victim:
            self.attackers = regular_hosts
            e = Execution(self.network, self.victim, regular_hosts)
            return self.__check(e)
        else:
            for v in self.network.hosts:
                a = [h for h in regular_hosts if h != v]
                e = Execution(self.network, v, a)

                if self.__check(e):
                    self.victim = v
                    self.attackers = a
                    return True

            return False

    def get_execution(self):
        raise NotImplementedError

    def to_string(self):
        network_str = self.network.to_string()
        if self.victim:
            # TODO: include attackers
            victim_ln = "victim: %s\n" % self.victim.name
            return network_str + victim_ln
        else:
            return network_str

    @classmethod
    def from_string(cls, s):
        return parser.parse_attack(s)
