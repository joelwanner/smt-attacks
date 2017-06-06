

class Flow(object):
    def __init__(self, fid, route, amount):
        self.id = fid
        self.route = route
        self.amount = amount

    def __repr__(self):
        return self.id

    def get(self, src, dest):
        if self.route.successor(src) == dest:
            return self.amount
        else:
            return 0
