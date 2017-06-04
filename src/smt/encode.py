from z3 import *

from smt.model import Model
from network.network import *


class ModelEncoder(Model):
    def __init__(self, execution, n_flows):
        super().__init__(execution, n_flows)

    # --------------------- #
    #      Constraints      #
    # --------------------- #

    # (F1) Inverse fId projection function
    # -------------------------------------------
    def __encode_f1(self):
        for i, f in enumerate(self.flows):
            yield self.fpIdInv(self.fids[i]) == f

    # (F2) Routing table setup
    # -------------------------------------------
    def __encode_f2(self):
        constraints = []
        table = self.network.get_routes()

        for h_src in self.network.hosts:
            for h_dest in self.network.hosts:
                if not h_src == h_dest:
                    src = self.host_map[h_src]
                    dest = self.host_map[h_dest]
                    r = self.fRoute(src, dest)

                    route = table.get_route(h_src, h_dest)
                    hops = route.hops

                    if hops:
                        next_hop = self.host_map[hops[0]]
                    else:  # This case may occur in disconnected networks
                        next_hop = src

                    set_constraints = []
                    for host in self.network.hosts:
                        h = self.host_map[host]
                        membership = Select(r, h)

                        if host in hops or host == h_src:
                            set_constraints.append(membership)
                        else:
                            set_constraints.append(Not(membership))

                    rule_next = self.fNext(src, dest) == next_hop
                    rule_route = And(set_constraints)

                    yield And(rule_next, rule_route)

    # (F3) Flow request field constraints
    # -------------------------------------------
    def __encode_f3(self):
        Flow = self.s_Flow

        for f in self.flows:
            rid = Flow.req(f)
            r = self.fpIdInv(rid)

            f_is_response = Flow.type(f) == self.RESPONSE
            r_is_request = Flow.type(r) == self.REQUEST
            host_matches = Flow.src(f) == Flow.dest(r)
            distinct = Not(f == r)

            # Ensure that there is no other response that is mapped to the same request
            is_lone_response = And([Not(Flow.req(g) == rid) for g in self.flows if not g == f])

            yield Implies(f_is_response, And(r_is_request, host_matches, distinct, is_lone_response))

    # (G1) General rules for instances of flows
    # -------------------------------------------
    def __encode_g1(self):
        Flow = self.s_Flow

        servers = [h for h in self.network.hosts if type(h) is Server]
        switches = [h for h in self.network.hosts if type(h) is Switch]

        for f in self.flows:
            src = Flow.src(f)
            dest = Flow.dest(f)

            distinct = Not(src == dest)
            positive_size = Flow.size(f) > 0

            is_request = Flow.type(f) == self.REQUEST
            not_from_server = And([Not(src == self.host_map[s]) for s in servers])
            server_rule = Implies(is_request, not_from_server)

            switch_rule = And([Not(src == self.host_map[s]) for s in switches])

            yield And(distinct, positive_size, server_rule, switch_rule)

    # (G2) Amplification factor constraints
    # -------------------------------------------
    def __encode_g2(self):
        Flow = self.s_Flow

        for host in self.network.hosts:
            h = self.host_map[host]

            if len(self.flows) > 1:
                for f in self.flows:
                    r = self.fpIdInv(Flow.req(f))

                    is_response = Flow.type(f) == self.RESPONSE
                    belongs_to_host = Flow.src(f) == h
                    amp_constraint = Flow.size(f) <= Flow.size(r) * host.amp_factor

                    yield Implies(And(is_response, belongs_to_host), amp_constraint)

    # (C1) Definition of sent() function
    # -------------------------------------------
    def __encode_c1(self):
        Flow = self.s_Flow

        for host in self.network.hosts:
            h = self.host_map[host]
            for l in host.links:
                n = self.host_map[l.neighbor(host)]

                for i, f in enumerate(self.flows):
                    fid = self.fids[i]
                    src = Flow.src(f)
                    dest = Flow.dest(f)

                    size = Flow.size(f)
                    result = self.fSent(h, n, fid)

                    f_is_active = self.state(f)
                    h_in_route = Select(self.fRoute(src, dest), h)
                    n_is_next_hop = n == self.fNext(h, dest)
                    condition = And(f_is_active, h_in_route, n_is_next_hop)

                    # TODO: compare efficiency
                    # yield And(Implies(condition, result == size), Implies(Not(condition), result == 0))
                    yield result == If(condition, size, 0)

    # (C2) Host sending and receiving capacities
    # -------------------------------------------
    def __encode_c2(self):
        for h in self.network.hosts:
            if not h == self.victim:
                yield self.__mk_units_recvd(h) <= h.receiving_cap

            if h not in self.attackers:
                yield self.__mk_units_sent(h) <= h.sending_cap
            else:  # Continuous sending property
                yield self.__mk_units_sent(h) == h.sending_cap

    # (C3) Link capacities
    # -------------------------------------------
    def __encode_c3(self):
        for l in self.network.links:
            yield self.__mk_units_sent_to(l.h1, l.h2) + self.__mk_units_sent_to(l.h2, l.h1) <= l.capacity

    # --------------------- #
    #    Helper Functions   #
    # --------------------- #

    def __mk_units_sent_to(self, src, dest):
        return Sum([self.fSent(self.host_map[src], self.host_map[dest], fid) for fid in self.fids])

    def __mk_units_sent(self, host):
        # TODO: does this work for disconnected hosts?
        return Sum([self.__mk_units_sent_to(host, l.neighbor(host)) for l in host.links])

    def __mk_units_recvd(self, host):
        return Sum([self.__mk_units_sent_to(l.neighbor(host), host) for l in host.links])

    @staticmethod
    def __collect_assertions(*functions):
        assertions = []
        for f in functions:
            constraints = []
            generator = f()

            if generator:
                for c in generator:
                    constraints.append(c)
                assertions.append(constraints)

        return assertions

    # ---------------------- #
    #    Public Functions    #
    # ---------------------- #
    def get_assertions(self):
        a = self.__collect_assertions(self.__encode_f1, self.__encode_f2, self.__encode_f3,
                                      self.__encode_g1, self.__encode_g2,
                                      self.__encode_c1, self.__encode_c2, self.__encode_c3)
        return a
