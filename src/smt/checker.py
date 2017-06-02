from network.network import *


# TODO: refactor class such that it uses the new Execution class
# TODO: outsource string parsing
class AttackChecker:
    def __init__(self, network, victim=None, attackers=None):
        self.__network = network
        self.victim = victim
        self.attackers = attackers

    def __check(self, victim, attackers):
        raise NotImplementedError

    def check_attack(self):
        if not self.attackers or not self.victim:
            regular_hosts = []
            for h in self.__network.hosts:
                if not (isinstance(h, Server) or h == self.victim):
                    regular_hosts.append(h)
        else:
            regular_hosts = self.attackers

        if self.victim:
            self.attackers = regular_hosts
            return self.__check(self.victim, regular_hosts)
        else:
            for v in self.__network.hosts:
                a = [h for h in regular_hosts if h != v]
                if self.__check(v, a):
                    self.victim = v
                    self.attackers = a
                    return True

            return False

    def get_execution(self):
        raise NotImplementedError

    def to_string(self):
        network_str = self.__network.to_string()
        if self.victim:
            # TODO: include attackers
            victim_ln = "victim: %s\n" % self.victim.name
            return network_str + victim_ln
        else:
            return network_str

    @classmethod
    def from_string(cls, s):
        raise NotImplementedError
