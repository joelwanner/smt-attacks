import networkx as nx
import random
import string

from network.network import *


class RandomNetwork(Network):
    # TODO: add random seed
    def __init__(self, n):
        hosts = []
        links = []

        g = nx.gnp_random_graph(n, 0.6)
        node_map = {}

        for node in g.nodes():
            name = string.ascii_uppercase[node]
            r = random.randint(6, 8)
            s = random.randint(1, 2)

            kind = random.randint(0, 5)
            if kind == 2:
                h = Server(name, r * 4, s * 2, random.randint(1, 4))
            elif kind == 1:
                h = Switch(name, r * 2, s * 2)
            else:
                h = Host(name, r, s)

            hosts.append(h)
            node_map[node] = h

        for edge in g.edges():
            h1 = node_map[edge[0]]
            h2 = node_map[edge[1]]

            l = Link(h1, h2, random.randint(1, 4))
            links.append(l)

        super().__init__(hosts, links)