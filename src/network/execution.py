

class Execution(object):
    def __init__(self, network, victim=None, attackers=None):
        self.network = network
        self.victim = victim
        self.attackers = attackers
        self.flows = None

    def set_flows(self, flows):
        self.flows = flows

    def __str__(self):
        s = self.network.__str__() + "\n"

        if self.victim:
            s += "victim: %s\n" % self.victim.name

        if self.attackers:
            attacker_str = ", ".join([str(h) for h in self.attackers])
            s += "attackers: [%s]\n" % attacker_str

        return s
