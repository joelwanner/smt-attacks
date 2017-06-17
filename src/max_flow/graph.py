

class Vertex(object):
    def __init__(self, name):
        self.name = name
        self.out_edges = []
        self.in_edges = []

    def __repr__(self):
        return self.name

    def add_edge(self, e):
        if e.src == self:
            self.out_edges.append(e)
        elif e.dest == self:
            self.in_edges.append(e)


class Edge(object):
    def __init__(self, u, v, c):
        self.src = u
        self.dest = v
        self.capacity = c

        u.add_edge(self)
        v.add_edge(self)

    def __repr__(self):
        if self.capacity is None:
            c = "∞"
        else:
            c = str(self.capacity)
        return "%s -(%s)-> %s" % (self.src, c, self.dest)


class DirectedWeightedGraph(object):
    def __init__(self, vertices, edges):
        self.vertices = vertices
        self.edges = edges

    def get_edge(self, u, v):
        for e in self.edges:
            if e.src == u and e.dest == v:
                return e


class FlowGraph(DirectedWeightedGraph):
    def __init__(self, vertices, edges, s, t, amp_factors):
        super().__init__(vertices, edges)

        self.source = s
        self.sink = t
        self.vertices.extend([s, t])
        self.amp_factors = amp_factors

    # Compute all cycle-free paths from src to dest using DFS
    def paths(self, src, dest, f):
        stack = [(src, Path([], self.amp_factors))]
        paths = []

        while stack:
            (u, path) = stack.pop()

            for e in u.out_edges:
                if e.capacity is None or e.capacity - f.get(e) > 0:
                    v = e.dest
                    if v == dest:
                        p = Path(path.edges + [e], self.amp_factors)
                        paths.append(p)
                    elif not path.visits(v):
                        # TODO: Implement joining / extending paths more efficiently
                        # (without recomputing amplification)
                        stack.append((e.dest, Path(path.edges + [e], self.amp_factors)))

        return paths


class Path(object):
    def __init__(self, edges, amp_factors):
        self.edges = edges
        self.a = self.__compute_amplification(amp_factors)

    def __repr__(self):
        if not self.edges:
            return "()"

        s = "(" + self.edges[0].src.name
        for e in self.edges:
            s += " -> " + e.dest.name

        return s + ")"

    def __compute_amplification(self, amp_factors):
        amplification = {}
        a = 1

        for e in self.edges:
            if amplification:
                if e.src in amp_factors:
                    factor = amp_factors[e.src]
                else:
                    factor = 1
                a *= factor

            amplification[e] = a

        return amplification

    def visits(self, v):
        if not self.edges:
            return False

        if v == self.edges[0].src:
            return True

        for e in self.edges:
            if e.dest == v:
                return True

        return False

    def potential(self, f):
        min_residual = None
        for e in self.edges:
            if e.capacity is not None:
                r = (e.capacity - f.get(e)) / self.a[e]
                if min_residual is None or r < min_residual:
                    min_residual = r

        last_edge = self.edges[-1]
        benefit = self.a[last_edge] * min_residual

        return min_residual, benefit

    # Computes the amplification factor that would be assigned to the edge
    def next_amplification(self, e, amp_factors):
        last_edge = self.edges[-1]

        if e.src in amp_factors:
            a = amp_factors[e.src]
        else:
            a = 1

        return self.a[last_edge] * a
