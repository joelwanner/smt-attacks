from z3 import *


class Model(object):
    def __init__(self, ctx, execution, n_flows):
        self.ctx = ctx
        self.victim = execution.victim
        self.attackers = execution.attackers
        self.network = execution.network

        int_sort = IntSort(ctx)

        # Hosts
        # --------------------------
        names = [h.name for h in self.network.hosts]
        self.Host, self.host_symbols = EnumSort('Host', names, ctx)
        self.host_map = dict(zip(self.host_symbols, self.network.hosts))

        # Flows
        # --------------------------
        ids = ['f%did' % i for i in range(n_flows)]
        self.FlowId, self.fids = EnumSort('FlowId', ids, ctx)
        self.FlowType, (self.REQUEST, self.RESPONSE) = EnumSort('FlowType', ['REQUEST', 'RESPONSE'], ctx)

        self.Flow = Datatype('Flow')
        args = [('id', self.FlowId), ('src', self.Host), ('dest', self.Host),
                ('size', int_sort), ('type', self.FlowType), ('req', self.FlowId)]
        self.Flow.declare('mk_flow', *args)
        self.Flow = self.Flow.create()

        self.flows = []
        for i in range(n_flows):
            id = self.fids[i]
            src = Const('f%d_src' % i, self.Host)
            dest = Const('f%d_dest' % i, self.Host)
            size = Const('f%d_size' % i, int_sort)
            ftype = Const('f%d_type' % i, self.FlowType)
            req = Const('f%d_req' % i, self.FlowId)
            self.flows[i] = self.Flow.mk_flow(id, src, dest, size, ftype, req)

        self.fpIdInv = Function('fpIdInv', self.FlowId, self.Flow)
        self.fSent = Function('sent', (self.Host, self.Host, self.FlowId), int_sort)

        Route = ArraySort(self.Host, BoolSort(ctx))
        self.fRoute = Function('route', (self.Host, self.Host), Route)
        self.fNext = Function('next', (self.Host, self.Host), self.Host)
