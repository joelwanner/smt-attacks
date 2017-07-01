from z3 import *


class Model(object):
    def __init__(self, execution, n_flows):
        self.hosts = execution.topology.hosts
        self.links = execution.topology.links
        self.routes = execution.topology.get_routes()

        self.victims = execution.victims
        self.attackers = execution.attackers

        # Hosts
        # --------------------------
        names = [h.name for h in self.hosts]
        Host, host_symbols = EnumSort('Host', names)
        self.host_map = dict(zip(self.hosts, host_symbols))

        # Flows
        # --------------------------
        ids = ['f%d' % i for i in range(n_flows)]
        FlowId, self.fids = EnumSort('FlowId', ids)
        FlowType, (self.REQUEST, self.RESPONSE) = EnumSort('FlowType', ['REQUEST', 'RESPONSE'])

        Flow = Datatype('Flow')
        args = [('id', FlowId), ('src', Host), ('dest', Host), ('size', IntSort()), ('type', FlowType)]
        Flow.declare('mk_flow', *args)
        Flow = Flow.create()

        self.flows = []
        for i in range(n_flows):
            fid = self.fids[i]
            src = Const('f%d_src' % i, Host)
            dest = Const('f%d_dest' % i, Host)
            size = Const('f%d_size' % i, IntSort())
            ftype = Const('f%d_type' % i, FlowType)
            self.flows.append(Flow.mk_flow(fid, src, dest, size, ftype))

        # Functions
        # --------------------------
        self.fpIdInv = Function('fpIdInv', FlowId, Flow)
        self.fReq = Function('req', Flow, FlowId)

        Route = ArraySort(Host, BoolSort())
        self.fRoute = Function('route', Host, Host, Route)
        self.fNext = Function('next', Host, Host, Host)

        self.fSent = Function('sent', Host, Host, Flow, IntSort())

        # Set public fields
        # --------------------------
        self.Flow = Flow

    # --------------------- #
    #    Helper Functions   #
    # --------------------- #

    def mk_units_sent_to(self, src, dest):
        return Sum([self.fSent(self.host_map[src], self.host_map[dest], f) for f in self.flows])

    def mk_units_sent(self, h):
        return Sum([self.mk_units_sent_to(h, l.neighbor(h)) for l in h.links])

    def mk_units_recvd(self, h):
        return Sum([self.mk_units_sent_to(l.neighbor(h), h) for l in h.links])
