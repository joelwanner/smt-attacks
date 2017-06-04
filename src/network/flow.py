

class Flow(object):
    def __init__(self, fid, route, amount):
        self.id = fid
        self.route = route
        self.amount = amount

    def __repr__(self):
        return self.id

    def get(self, src, dest):
        if src in self.route and dest in self.route:
            return self.amount
        else:
            return 0

    def across_link(self, l):
        return self.get(l.h1, l.h2)
