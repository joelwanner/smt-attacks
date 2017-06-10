from network.topology import *
from network.network import Network


class AmplificationTopology(Topology):
    def __init__(self, n_servers):
        amp_factor = 3
        hosts = []
        links = []

        a = Host("A", 0, n_servers)
        b = Host("B", n_servers * amp_factor - 1, 0)
        hosts.extend([a, b])
        self.victim = b

        for i in range(n_servers):
            s = Server("S" + str(i + 1), 1, amp_factor + 1, amp_factor)
            l1 = Link(a, s, 1)
            l2 = Link(s, b, amp_factor)

            hosts.append(s)
            links.extend([l1, l2])

        super().__init__(hosts, links)


class AmplificationNetwork(Network):
    def __init__(self, n_servers):
        network = AmplificationTopology(n_servers)
        super().__init__(network, n_servers * 2, [network.victim])


class CoremeltTopology(Topology):
    def __init__(self, n):
        hosts = []
        links = []

        s1 = Router("S1", 100, 100)
        s2 = Router("S2", 100, 100)
        hosts.extend([s1, s2])

        l = Link(s1, s2, 2 * n)
        links.append(l)
        self.victim = l

        for i in range(n):
            a = Host("A" + str(i + 1), 10, 10)
            hosts.append(a)
            links.append(Link(a, s1, 20))

            b = Host("B" + str(i + 1), 20, 10)
            hosts.append(b)
            links.append(Link(s2, b, 10))

        super().__init__(hosts, links)


class CoremeltNetwork(Network):
    def __init__(self, n):
        network = CoremeltTopology(n)
        super().__init__(network, n * 2, [network.victim])
