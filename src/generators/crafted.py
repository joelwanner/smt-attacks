from network.network import *
from network.execution import Execution


class AmplificationNetwork(Network):
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


class AmplificationAttack(Execution):
    def __init__(self, n_servers):
        network = AmplificationNetwork(n_servers)
        super().__init__(network, n_servers * 2, network.victim)


class CoremeltNetwork(Network):
    def __init__(self, n):
        hosts = []
        links = []

        s = Switch("S", 100, 100)
        hosts.append(s)
        self.victim = s

        for i in range(n):
            a = Host("A" + str(i + 1), 10 + i/2, 2 + i/3)
            hosts.append(a)
            links.append(Link(a, s, 20))

            b = Host("B" + str(i + 1), 5 + i/4, 3 + i/4)
            hosts.append(b)
            links.append(Link(s, b, 10))

        super().__init__(hosts, links)


class CoremeltAttack(Execution):
    def __init__(self, n):
        network = CoremeltNetwork(n)
        super().__init__(network, n * 2, network.victim)
