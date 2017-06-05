import pydot

from network.network import *


class NetworkRenderer(object):
    accent_color = "#cc5555"
    host_color = "#f0f0f0"
    attacker_color = "#ffe6e6"
    server_color = "#bfbfbf"
    light_color = "#aaaaaa"
    font_name = "Helvetica"
    label_size = 10
    node_fontsize = 8

    def __init__(self, network, execution=None):
        self.network = network
        self.execution = execution

        self.graph = self.create_graph()

    def render(self, output):
        self.graph.write_pdf(output + ".pdf")

    def create_graph(self):
        g = pydot.Dot(graph_type='graph')
        node_map = {}

        for h in self.network.hosts:
            label = "<<B>%s</B><br/>%d  %d<br/>%d>" % (h.name, h.receiving_cap, h.sending_cap, h.amp_factor)

            n = pydot.Node(h.name, label=label, margin=-0.8, width=0.5, height=0.5)
            n.set_style("filled")
            n.set_fontname(self.font_name)
            n.set_fontsize(self.node_fontsize)

            if type(h) is Server:
                if self.execution and h == self.execution.victim:
                    n.set_shape("doublecircle")
                else:
                    n.set_shape("Mcircle")

                n.set_fillcolor(self.server_color)
            elif type(h) is Router:
                if self.execution and h == self.execution.victim:
                    n.set_shape("doubleoctagon")
                else:
                    n.set_shape("octagon")

                n.set_fillcolor(self.server_color)
            else:
                if self.execution and h == self.execution.victim:
                    n.set_shape("doublecircle")
                else:
                    n.set_shape("circle")

                if self.execution and h in self.execution.attackers:
                    n.set_fillcolor(self.attacker_color)
                else:
                    n.set_fillcolor(self.host_color)

            g.add_node(n)
            node_map[h] = n

        for l in self.network.links:
            if self.execution:
                flow = sum([f.across_link(l) for f in self.execution.flows])
            else:
                flow = 0

            h1 = node_map[l.h1]
            h2 = node_map[l.h2]

            e = pydot.Edge(h1, h2)
            e.set_fontname(self.font_name)
            e.set_fontsize(self.label_size)

            if flow > 0:
                if flow % 1 == 0:  # integer flow
                    e.set_label("%d/%d" % (flow, l.capacity))
                else:
                    e.set_label("%.2f/%d" % (flow, l.capacity))

                e.set_fontcolor(self.accent_color)
                e.set_color(self.accent_color)
            else:
                e.set_label(str(l.capacity))

            g.add_edge(e)

        return g
