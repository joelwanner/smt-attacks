

class Flow(object):
    def __init__(self, route, amount):
        self.route = route
        self.amount = amount

    def get(self, src, dest):
        if src in self.route and dest in self.route:
            return self.amount
        else:
            return 0

    def across_link(self, l):
        return self.get(l.h1, l.h2)
