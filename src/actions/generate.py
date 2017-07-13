import os

from generators.random import *
from generators.crafted import *


class Generator(object):
    def __init__(self, path):
        self.path = path

    def __generate(self, cls, name, sizes):
        for n in sizes:
            topology = cls(n)
            path = os.path.join(self.path, "%s%d.txt" % (name, n))

            with open(path, "w") as file:
                file.write(topology.__str__())

    def generate_random(self, n_networks, n_hosts, connectivity):
        for n in range(n_networks):
            topology = RandomTopology(n_hosts, connectivity)
            path = os.path.join(self.path, "random%d.txt" % n)

            with open(path, "w") as file:
                file.write(topology.__str__())

    def generate_crafted(self, sizes):
        self.__generate(AmplificationNetwork, "amplification", sizes)
        self.__generate(CoremeltNetwork, "coremelt", sizes)
