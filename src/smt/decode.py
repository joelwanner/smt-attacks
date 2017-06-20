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

        for h in m.hosts:
            sent = m.mk_units_sent(h)

        for f in m.flows:
            fid = v.evaluate(m.Flow.id(f))
            size = v.evaluate(m.Flow.size(f)).as_long()

            if size > 0:
                id_str = str(v.evaluate(fid))
                src = v.evaluate(m.Flow.src(f))
                dest = v.evaluate(m.Flow.dest(f))

                # We may assume that the routes taken by flows are the pre-computed ones
                route = m.routes.get_route(self.__host_for_expr(src), self.__host_for_expr(dest))
                flows.append(Flow(route, size, id_str))

        return flows

    def victims(self):
        victims = set()

        for t in range(self.network.n_states):
            for h in self.network.hosts:
                r = self.network.mk_units_recvd(h, t)
                if self.model.evaluate(And(r > h.receiving_cap)):  # Hack to prevent AttributeError from Z3
                    victims.add(h)

            for l in self.network.links:
                s = self.network.mk_units_over_link(l, t)
                if self.model.evaluate(And(s > l.capacity)):  # Hack to prevent AttributeError from Z3
                    victims.add(l)

        return victims

    def attackers(self):
        # TODO: Implement attacker finding procedure
        return []
