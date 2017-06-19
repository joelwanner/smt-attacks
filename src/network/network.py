

class Network(object):
    def __init__(self, topology, n_flows, victims=None, attackers=None):
        self.topology = topology
        self.victims = victims
        self.attackers = attackers

        self.n_flows = n_flows
        self.flows = None

    def __str__(self):
        s = "%s\nflows: %d\n" % (self.topology.__str__(), self.n_flows)

        if self.victims:
            victims_str = ", ".join([v.__repr__() for v in self.victims])
            s += "victims: [%s]\n" % victims_str

        if self.attackers:
            attacker_str = ", ".join([h.name for h in self.attackers])
            s += "attackers: [%s]\n" % attacker_str

        return s
