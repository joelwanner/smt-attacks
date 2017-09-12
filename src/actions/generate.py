from generators.random import *
from generators.crafted import *


class Generator(object):
    def __init__(self, path):
        self.path = path

    def __generate(self, cls, name, ids, params):
        for i, p in enumerate(zip(*params)):
            topology = cls(*p)
            path = os.path.join(self.path, "%s%d.txt" % (name, ids[i]))

            with open(path, "w") as file:
                file.write(topology.__str__())
                print("Generated %s" % path)

    def generate_random(self, n_networks, n_hosts, connectivity):
        self.__generate(RandomTopology, "random", range(n_networks), [[n_hosts]*n_networks, [connectivity]*n_networks])

    def generate_crafted(self, sizes):
        self.__generate(AmplificationNetwork, "amplification", sizes, [sizes])
        self.__generate(CoremeltNetwork, "coremelt", sizes, [sizes])
