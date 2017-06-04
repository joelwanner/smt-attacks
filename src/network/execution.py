

class Execution(object):
    def __init__(self, network, victim=None, attackers=None):
        self.network = network
        self.victim = victim
        self.attackers = attackers
        self.flows = None

    def set_flows(self, flows):
        self.flows = flows
