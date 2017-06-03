

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
        s = "(%s -> " % self.source.name

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
        self.__table = {}

        for h in self.network.hosts:
            self.__routes_from(h)

    def __routes_from(self, src):
        routes = {}

        for h in self.network.hosts:
            routes[h] = Route(src, h)

        visited = [src]
        current = [src]

        while current:
            h = current.pop()

            for l in h.links:
                neighbor = l.get_neighbor(h)
                if neighbor not in visited:
                    r = routes[neighbor]
                    r.add_route(routes[h])
                    r.add_hop(neighbor)

                    current.append(neighbor)
                    visited.append(neighbor)

        return routes
