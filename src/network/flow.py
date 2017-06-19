

class Flow(object):
    def __init__(self, route, amount, fid="f"):
        self.route = route
        self.amount = amount
        self.id = fid

    def __repr__(self):
        return self.id

    def get(self, src, dest):
        if self.route.successor(src) == dest:
            return self.amount
        else:
            return 0
