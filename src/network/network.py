import network.parse as parser


class Host(object):
    def __init__(self, name, r, s, a=1):
        self.name = name
        self.receiving_cap = r
        self.sending_cap = s
        self.amp_factor = a

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


# TODO: remove flow from this class
class Link(object):
    def __init__(self, h1, h2, c, f=None):
        self.h1 = h1
        self.h2 = h2
        self.capacity = c
        self.flow = f

    def __repr__(self):
        return "%s--%s" % (self.h1.name, self.h2.name)

    def __str__(self):
        return "%s:%d" % (self.__repr__(), self.capacity)


class Network(object):
    def __init__(self, hosts, links):
        self.hosts = hosts
        self.links = links

    def __str__(self):
        s = "hosts {\n"

        for h in self.hosts:
            s += "\t%s\n" % str(h)

        s += "}\nlinks {\n"
        for l in self.links:
            s += "\t%s\n" % str(l)

        return s + "}\n"

    @classmethod
    def from_string(cls, s):
        return parser.parse_network(s)
