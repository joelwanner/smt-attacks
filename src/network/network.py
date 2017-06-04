from network.route import *


class Host(object):
    def __init__(self, name, r, s, a=1):
        self.name = name
        self.receiving_cap = r
        self.sending_cap = s
        self.amp_factor = a

        self.links = []

    def add_link(self, l):
        self.links.append(l)

    def __str__(self):
        if self.amp_factor == 1:
            return "%s(%d,%d)" % (self.name, self.receiving_cap, self.sending_cap)
        else:
            return "%s(%d,%d,%d)" % (self.name, self.receiving_cap, self.sending_cap, self.amp_factor)

    def __repr__(self):
        return self.name


class Server(Host):
    def __init__(self, name, r, s, a):
        super().__init__(name, r, s, a)

    def __str__(self):
        return "_" + super().__str__()


class Switch(Server):
    def __init__(self, name, r, s):
        super().__init__(name, r, s, 1)


class Link(object):
    def __init__(self, h1, h2, c):
        self.h1 = h1
        self.h2 = h2
        self.capacity = c

    def neighbor(self, h):
        if h == self.h1:
            return self.h2
        elif h == self.h2:
            return self.h1
        else:
            return None

    def __repr__(self):
        return "%s--%s" % (self.h1.name, self.h2.name)

    def __str__(self):
        return "%s:%d" % (self.__repr__(), self.capacity)


class Network(object):
    def __init__(self, hosts, links):
        self.hosts = hosts
        self.links = links
        self.__routes = None

        for l in links:
            l.h1.add_link(l)
            l.h2.add_link(l)

    def get_routes(self):
        if not self.__routes:
            self.__routes = RoutingTable(self)

        return self.__routes

    def __str__(self):
        host_str = ",\n\t".join([str(h) for h in self.hosts])
        link_str = ",\n\t".join([str(l) for l in self.links])
        return "hosts {\n\t%s\n}\nlinks {\n\t%s\n}" % (host_str, link_str)

    @classmethod
    def from_string(cls, s):
        return parser.parse_network(s)


# TODO: remove workaround for circular dependencies
import interface.parse as parser
