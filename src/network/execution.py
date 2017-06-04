

class Execution(object):
    def __init__(self, network, n_flows, victim=None, attackers=None):
        self.network = network
        self.victim = victim
        self.attackers = attackers

        self.n_flows = n_flows
        self.flows = None

    def set_flows(self, flows):
        self.flows = flows

    def __str__(self):
        s = "%s\nflows: %d\n" % (self.network.__str__(), self.n_flows)

        if self.victim:
            s += "victim: %s\n" % self.victim.name

        if self.attackers:
            attacker_str = ", ".join([str(h) for h in self.attackers])
            s += "attackers: [%s]\n" % attacker_str

        return s
