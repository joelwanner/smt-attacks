from network.flow import Flow
from z3 import *


class ModelDecoder(object):
    def __init__(self, network_model, smt_model):
        self.network = network_model
        self.model = smt_model

    def __host_for_expr(self, h):
        host_map = self.network.host_map

        for host in host_map.keys():
            if host_map[host] == h:
                return host

        return None

    def flows(self):
        m = self.network
        v = self.model
        flows = []

        for f in m.flows:
            fid = v.evaluate(m.Flow.id(f))
            size = v.evaluate(m.Flow.size(f)).as_long()

            if size > 0:
                id_str = str(v.evaluate(fid))
                src = v.evaluate(m.Flow.src(f))
                dest = v.evaluate(m.Flow.dest(f))

                # We may assume that the routes taken by flows are the pre-computed ones
                route = m.routes.get_route(self.__host_for_expr(src), self.__host_for_expr(dest))
                flows.append(Flow(id_str, route, size))

        return flows
