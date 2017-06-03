from z3 import *

from network.network import *


class Model(object):
    def __init__(self, execution, n_flows):
        self.victim = execution.victim
        self.attackers = execution.attackers
        self.network = execution.network

        int_sort = IntSort()

        # Hosts
        # --------------------------
        names = [h.name for h in self.network.hosts]
        self.s_Host, host_symbols = EnumSort('Host', names)
        self.host_map = dict(zip(self.network.hosts, host_symbols))

        # Flows
        # --------------------------
        ids = ['f%did' % i for i in range(n_flows)]
        self.s_FlowId, self.fids = EnumSort('FlowId', ids)
        s_FlowType, (self.REQUEST, self.RESPONSE) = EnumSort('FlowType', ['REQUEST', 'RESPONSE'])

        s_Flow = Datatype('Flow')
        args = [('id', self.s_FlowId), ('src', self.s_Host), ('dest', self.s_Host),
                ('size', int_sort), ('type', s_FlowType), ('req', self.s_FlowId)]
        s_Flow.declare('mk_flow', *args)
        self.s_Flow = s_Flow.create()

        self.flows = []
        for i in range(n_flows):
            id = self.fids[i]
            src = Const('f%d_src' % i, self.s_Host)
            dest = Const('f%d_dest' % i, self.s_Host)
            size = Const('f%d_size' % i, int_sort)
            ftype = Const('f%d_type' % i, s_FlowType)
            req = Const('f%d_req' % i, self.s_FlowId)
            self.flows.append(self.s_Flow.mk_flow(id, src, dest, size, ftype, req))

        # Functions
        # --------------------------
        self.fpIdInv = Function('fpIdInv', self.s_FlowId, self.s_Flow)
        self.fSent = Function('sent', self.s_Host, self.s_Host, self.s_FlowId, int_sort)

        s_Route = ArraySort(self.s_Host, BoolSort())
        self.fRoute = Function('route', self.s_Host, self.s_Host, s_Route)
        self.fNext = Function('next', self.s_Host, self.s_Host, self.s_Host)


class ModelEncoder(Model):
    def __init__(self, execution, n_flows):
        super().__init__(execution, n_flows)

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

    def __collect_assertions(self, *functions):
        assertions = []

        for f in functions:
            constraints = []
            for c in f():
                constraints.append(c)

            assertions.append(constraints)

        return assertions

    def get_assertions(self):
        a = self.__collect_assertions(self.__encode_f1, self.__encode_f2, self.__encode_f3,
                                      self.__encode_g1, self.__encode_g2)
        return a
