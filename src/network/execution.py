

class Execution(object):
    def __init__(self, network, n_flows, victims=None, attackers=None):
        self.network = network
        self.victims = victims
        self.attackers = attackers

        self.n_flows = n_flows
        self.flows = None

    def set_flows(self, flows):
        self.flows = flows

    def __str__(self):
        s = "%s\nflows: %d\n" % (self.network.__str__(), self.n_flows)

        if self.victims:
            victims_str = ", ".join([h.name for h in self.victims])
            s += "victims: [%s]\n" % victims_str

        if self.attackers:
            attacker_str = ", ".join([h.name for h in self.attackers])
            s += "attackers: [%s]\n" % attacker_str

        return s
