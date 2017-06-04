import os

from generators.random import *
from generators.crafted import *


class Generator(object):
    def __init__(self, path):
        self.path = path

    def __generate(self, cls, name, sizes):
        for n in sizes:
            network = cls(n)
            path = os.path.join(self.path, "%s%d.txt" % (name, n))

            with open(path, "w") as file:
                file.write(network.__str__())

    def generate_random(self, n_networks, n_hosts):
        for n in range(n_networks):
            network = RandomNetwork(n_hosts)
            path = os.path.join(self.path, "random%d.txt" % n)

            with open(path, "w") as file:
                file.write(network.__str__())

    def generate_crafted(self, sizes):
        self.__generate(AmplificationAttack, "amplification", sizes)
        self.__generate(CoremeltAttack, "coremelt", sizes)
