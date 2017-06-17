

class Flow(object):
    def __init__(self):
        self.__map = {}

    def __repr__(self):
        s = "("
        for e in self.__map.keys():
            s += str(e) + ": " + str(self.__map[e]) + ", "

        return s + ")"

    def get(self, e):
        if e in self.__map:
            return self.__map[e]
        else:
            return 0

    def set(self, e, f):
        self.__map[e] = f
