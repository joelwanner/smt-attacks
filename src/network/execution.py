from network.network import *


# TODO: extend class to include flow
class Execution(object):
    def __init__(self, network, victim=None, attackers=None):
        self.__network = network
        self.victim = victim
        self.attackers = attackers
