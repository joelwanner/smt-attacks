from network.flow import Flow


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
        x = self.model
        flows = []

        for f in m.flows:
            fid = x.evaluate(m.Flow.id(f))
            if x.evaluate(m.state(fid)):
                src = x.evaluate(m.Flow.src(f))
                dest = x.evaluate(m.Flow.dest(f))
                size = x.evaluate(m.Flow.size(f)).as_long()

                route = m.routes.get_route(self.__host_for_expr(src), self.__host_for_expr(dest))
                flows.append(Flow(route, size))

        return flows
