import network.parse as parser

from network.network import *


# TODO: extend class to include flow
class Execution(object):
    def __init__(self, network, victim=None, attackers=None):
        self.__network = network
        self.victim = victim
        self.attackers = attackers

    @classmethod
    def from_string(cls, s):
        return parser.parse_attack(s)
