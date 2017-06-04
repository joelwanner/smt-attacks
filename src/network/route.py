

class Route(object):
    def __init__(self, src, dest, hops=None):
        self.source = src
        self.destination = dest

        if hops:
            self.hops = hops
        else:
            self.hops = []

    def __contains__(self, item):
        return item in self.hops or item == self.source

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

    def get_route(self, src, dest):
        return self.__table[(src, dest)]

    def __compute_routes(self):
        self.__table = {}

        for src in self.network.hosts:
            routes = self.__routes_from(src)
            for r in routes.values():
                self.__table[(src, r.destination)] = r

    def __routes_from(self, src):
        routes = {}

        for h in self.network.hosts:
            routes[h] = Route(src, h)

        visited = [src]
        current = [src]

        while current:
            h = current.pop()

            for l in h.links:
                neighbor = l.neighbor(h)
                if neighbor not in visited:
                    r = routes[neighbor]
                    r.add_route(routes[h])
                    r.add_hop(neighbor)

                    current.append(neighbor)
                    visited.append(neighbor)

        return routes
