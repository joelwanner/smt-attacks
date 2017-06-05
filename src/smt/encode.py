from smt.model import *
from network.network import *


class ModelEncoder(object):
    def __init__(self, execution, n_flows):
        self.model = Model(execution, n_flows)

    # --------------------- #
    #      Constraints      #
    # --------------------- #

    # (F1) Inverse fId projection function
    # -------------------------------------------
    def __encode_f1(self):
        m = self.model

        for i, f in enumerate(m.flows):
            yield m.fpIdInv(m.fids[i]) == f

    # (F2) Routing table setup
    # -------------------------------------------
    def __encode_f2(self):
        m = self.model
        table = m.routes

        for h_src in m.hosts:
            for h_dest in m.hosts:
                src = m.host_map[h_src]
                dest = m.host_map[h_dest]
                r = m.fRoute(src, dest)

                route = table.get_route(h_src, h_dest)
                hops = route.hops

                if hops:
                    next_hop = m.host_map[hops[0]]
                else:  # This case may occur in disconnected networks
                    next_hop = src

                set_constraints = []
                for host in m.hosts:
                    h = m.host_map[host]
                    membership = Select(r, h)

                    if host in hops or host == h_src:
                        set_constraints.append(membership)
                    else:
                        set_constraints.append(Not(membership))

                rule_next = m.fNext(src, dest) == next_hop
                rule_route = And(set_constraints)

                yield And(rule_next, rule_route)

    # (F3) Flow request field constraints
    # -------------------------------------------
    def __encode_f3(self):
        m = self.model

        for f in m.flows:
            rid = m.Flow.req(f)
            r = m.fpIdInv(rid)

            f_is_response = m.Flow.type(f) == m.RESPONSE
            r_is_request = m.Flow.type(r) == m.REQUEST
            host_matches = m.Flow.src(f) == m.Flow.dest(r)
            distinct = Not(f == r)

            # Ensure that there is no other response that is mapped to the same request
            is_lone_response = And([Not(m.Flow.req(g) == rid) for g in m.flows if not g == f])

            yield Implies(f_is_response, And(r_is_request, host_matches, distinct, is_lone_response))

    # (G1) General rules for instances of flows
    # -------------------------------------------
    def __encode_g1(self):
        m = self.model

        servers = [h for h in m.hosts if type(h) is Server]
        switches = [h for h in m.hosts if type(h) is Router]

        for f in m.flows:
            src = m.Flow.src(f)
            dest = m.Flow.dest(f)

            distinct = Not(src == dest)
            positive_size = m.Flow.size(f) >= 0

            is_request = m.Flow.type(f) == m.REQUEST
            not_from_server = And([Not(src == m.host_map[s]) for s in servers])
            server_rule = Implies(is_request, not_from_server)

            switch_rule = And([Not(src == m.host_map[s]) for s in switches])

            yield And(distinct, positive_size, server_rule, switch_rule)

    # (G2) Amplification factor constraints
    # -------------------------------------------
    def __encode_g2(self):
        m = self.model

        for host in m.hosts:
            h = m.host_map[host]

            if len(m.flows) > 1:
                for f in m.flows:
                    r = m.fpIdInv(m.Flow.req(f))

                    is_response = m.Flow.type(f) == m.RESPONSE
                    belongs_to_host = m.Flow.src(f) == h
                    amp_constraint = m.Flow.size(f) <= m.Flow.size(r) * host.amp_factor

                    yield Implies(And(is_response, belongs_to_host), amp_constraint)

    # (C1) Definition of sent() function
    # -------------------------------------------
    def __encode_c1(self):
        m = self.model

        for host in m.hosts:
            h = m.host_map[host]
            for l in host.links:
                n = m.host_map[l.neighbor(host)]

                for i, f in enumerate(m.flows):
                    fid = m.fids[i]
                    src = m.Flow.src(f)
                    dest = m.Flow.dest(f)

                    size = m.Flow.size(f)
                    result = m.fSent(h, n, fid)

                    h_in_route = Select(m.fRoute(src, dest), h)
                    n_is_next_hop = n == m.fNext(h, dest)
                    condition = And(h_in_route, n_is_next_hop)

                    yield result == If(condition, size, 0)

    # (C2) Host sending and receiving capacities
    # -------------------------------------------
    def __encode_c2(self):
        m = self.model

        for h in m.hosts:
            if not h == m.victim:
                yield self.__mk_units_recvd(h) <= h.receiving_cap
            else:  # Attack property
                yield self.__mk_units_recvd(h) > h.receiving_cap

            if h not in m.attackers:
                yield self.__mk_units_sent(h) <= h.sending_cap
            else:  # Continuous sending property
                yield self.__mk_units_sent(h) == h.sending_cap

    # (C3) Link capacities
    # -------------------------------------------
    def __encode_c3(self):
        m = self.model
        for l in m.links:
            yield self.__mk_units_sent_to(l.h1, l.h2) + self.__mk_units_sent_to(l.h2, l.h1) <= l.capacity

    # --------------------- #
    #    Helper Functions   #
    # --------------------- #

    def __mk_units_sent_to(self, src, dest):
        m = self.model
        return Sum([m.fSent(m.host_map[src], m.host_map[dest], fid) for fid in m.fids])

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
