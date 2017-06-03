from z3 import *


class Model(object):
    def __init__(self, execution, n_flows):
        self.victim = execution.victim
        self.attackers = execution.attackers
        self.network = execution.network

        int_sort = IntSort()

        # Hosts
        # --------------------------
        names = [h.name for h in self.network.hosts]
        s_Host, host_symbols = EnumSort('Host', names)
        host_map = dict(zip(host_symbols, self.network.hosts))

        # Flows
        # --------------------------
        ids = ['f%did' % i for i in range(n_flows)]
        self.s_FlowId, self.fids = EnumSort('FlowId', ids)
        s_FlowType, (REQUEST, RESPONSE) = EnumSort('FlowType', ['REQUEST', 'RESPONSE'])

        s_Flow = Datatype('Flow')
        args = [('id', self.s_FlowId), ('src', s_Host), ('dest', s_Host),
                ('size', int_sort), ('type', s_FlowType), ('req', self.s_FlowId)]
        s_Flow.declare('mk_flow', *args)
        s_Flow = s_Flow.create()

        self.flows = []
        for i in range(n_flows):
            id = self.fids[i]
            src = Const('f%d_src' % i, s_Host)
            dest = Const('f%d_dest' % i, s_Host)
            size = Const('f%d_size' % i, int_sort)
            ftype = Const('f%d_type' % i, s_FlowType)
            req = Const('f%d_req' % i, self.s_FlowId)
            self.flows.append(s_Flow.mk_flow(id, src, dest, size, ftype, req))

        self.fpIdInv = Function('fpIdInv', self.s_FlowId, s_Flow)
        self.fSent = Function('sent', s_Host, s_Host, self.s_FlowId, int_sort)

        s_Route = ArraySort(s_Host, BoolSort())
        self.fRoute = Function('route', s_Host, s_Host, s_Route)
        self.fNext = Function('next', s_Host, s_Host, s_Host)


class ModelEncoder(Model):
    def __init__(self, execution, n_flows):
        super().__init__(execution, n_flows)

    def constraint_f1(self):
        constraints = []

        for i, f in enumerate(self.flows):
            fid = self.fids[i]
            constraints.append(self.fpIdInv(fid) == f)

        return And(constraints)

    def get_assertions(self):
        a = [self.constraint_f1()]
        return a
