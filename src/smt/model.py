from z3 import *


class Model(object):
    def __init__(self, execution, n_flows):
        self.victim = execution.victim
        self.attackers = execution.attackers
        self.network = execution.network

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
                ('size', IntSort()), ('type', s_FlowType), ('req', self.s_FlowId)]
        s_Flow.declare('mk_flow', *args)
        self.s_Flow = s_Flow.create()

        self.flows = []
        for i in range(n_flows):
            id = self.fids[i]
            src = Const('f%d_src' % i, self.s_Host)
            dest = Const('f%d_dest' % i, self.s_Host)
            size = Const('f%d_size' % i, IntSort())
            ftype = Const('f%d_type' % i, s_FlowType)
            req = Const('f%d_req' % i, self.s_FlowId)
            self.flows.append(self.s_Flow.mk_flow(id, src, dest, size, ftype, req))

        # Functions
        # --------------------------
        self.fpIdInv = Function('fpIdInv', self.s_FlowId, self.s_Flow)
        self.fSent = Function('sent', self.s_Host, self.s_Host, self.s_FlowId, IntSort())

        s_Route = ArraySort(self.s_Host, BoolSort())
        self.fRoute = Function('route', self.s_Host, self.s_Host, s_Route)
        self.fNext = Function('next', self.s_Host, self.s_Host, self.s_Host)

        self.state = Function('s', self.s_Flow, BoolSort())
