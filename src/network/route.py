

class Route(object):
    def __init__(self, src, dest, hops=None):
        self.source = src
        self.destination = dest

        if hops:
            self.hops = hops
        else:
            self.hops = []

    def add_hop(self, h):
        self.hops.append(h)

    def add_route(self, route):
        self.hops.extend(route.hops)

    def __repr__(self):
        s = "(%s -> " % self.source

        for h in self.hops:
            if not h == self.destination:
                s += "%s -> " % h.name

        s += "%s)" % self.destination.name
        return s


class RoutingTable(object):
    def __init__(self, network):
        self.network = network
        self.__compute_routes()

    def __compute_routes(self):
        n = self.network.hosts
