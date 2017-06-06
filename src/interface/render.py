import pydot

from network.network import *


class NetworkRenderer(object):
    accent_color = "#cc5555"
    host_color = "#f0f0f0"
    attacker_color = "#ffe6e6"
    server_color = "#bfbfbf"
    link_color = "#666666"
    light_color = "#bbbbbb"
    font_name = "Helvetica"
    label_size = 10
    node_fontsize = 8

    def __init__(self, network, execution=None):
        self.network = network
        self.execution = execution

        self.graph = self.create_graph()

    def render(self, output):
        self.graph.write_pdf(output + ".pdf")

    def __create_link_flow(self, h1, h2, f):
        e = pydot.Edge(h1, h2)
        e.set_fontname(self.font_name)
        e.set_fontsize(self.label_size)

        if f % 1 == 0:  # integer flow
            e.set_label(str(f))
        else:
            e.set_label("%.2f" % f)

        e.set_fontcolor(self.accent_color)
        e.set_color(self.accent_color)

        return e

    def create_graph(self):
        g = pydot.Dot(graph_type='digraph')
        node_map = {}

        for h in self.network.hosts:
            label = "<<B>%s</B><br/>%d  %d<br/>%d>" % (h.name, h.receiving_cap, h.sending_cap, h.amp_factor)

            n = pydot.Node(h.name, label=label, style='filled', margin=-0.8, width=0.5, height=0.5,
                           fontname=self.font_name, fontsize=self.node_fontsize)

            if type(h) is Server:
                if self.execution and h in self.execution.victims:
                    n.set_shape('doublecircle')
                else:
                    n.set_shape('Mcircle')

                n.set_fillcolor(self.server_color)
            elif type(h) is Router:
                if self.execution and h in self.execution.victims:
                    n.set_shape('doubleoctagon')
                else:
                    n.set_shape('octagon')

                n.set_fillcolor(self.server_color)
            else:
                if self.execution and h in self.execution.victims:
                    n.set_shape('doublecircle')
                else:
                    n.set_shape('circle')

                if self.execution and h in self.execution.attackers:
                    n.set_fillcolor(self.attacker_color)
                else:
                    n.set_fillcolor(self.host_color)

            g.add_node(n)
            node_map[h] = n

        for l in self.network.links:
            v1 = node_map[l.h1]
            v2 = node_map[l.h2]

            e = pydot.Edge(v1, v2, dir='none', label=str(l.capacity), color=self.link_color, fontcolor=self.link_color,
                           fontname=self.font_name, fontsize=self.label_size)
            g.add_edge(e)

            if self.execution:
                f1 = sum([f.get(l.h1, l.h2) for f in self.execution.flows])
                f2 = sum([f.get(l.h2, l.h1) for f in self.execution.flows])
                residual = l.capacity - f1 - f2

                if residual == l.capacity:
                    e.set_label(str(l.capacity))
                else:
                    e.set_label("%d/%d" % (residual, l.capacity))

                if residual <= 0:
                    e.set_color(self.light_color)
                    e.set_fontcolor(self.light_color)

                if f1 > 0:
                    g.add_edge(self.__create_link_flow(v1, v2, f1))

                if f2 > 0:
                    g.add_edge(self.__create_link_flow(v2, v1, f2))

        return g
