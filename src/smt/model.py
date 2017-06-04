from z3 import *


class Model(object):
    def __init__(self, execution, n_flows):
        self.hosts = execution.network.hosts
        self.links = execution.network.links
        self.routes = execution.network.get_routes()

        self.victim = execution.victim
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
        args = [('id', FlowId), ('src', Host), ('dest', Host),
                ('size', IntSort()), ('type', FlowType), ('req', FlowId)]
        Flow.declare('mk_flow', *args)
        Flow = Flow.create()

        self.flows = []
        for i in range(n_flows):
            fid = self.fids[i]
            src = Const('f%d_src' % i, Host)
            dest = Const('f%d_dest' % i, Host)
            size = Const('f%d_size' % i, IntSort())
            ftype = Const('f%d_type' % i, FlowType)
            req = Const('f%d_req' % i, FlowId)
            self.flows.append(Flow.mk_flow(fid, src, dest, size, ftype, req))

        # Functions
        # --------------------------
        self.fpIdInv = Function('fpIdInv', FlowId, Flow)
        self.fSent = Function('sent', Host, Host, FlowId, IntSort())

        Route = ArraySort(Host, BoolSort())
        self.fRoute = Function('route', Host, Host, Route)
        self.fNext = Function('next', Host, Host, Host)

        self.state = Function('s', FlowId, BoolSort())

        # Set public fields
        # --------------------------
        self.Flow = Flow
