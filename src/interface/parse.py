import re

from network.network import *
import smt.checker # TODO: remove this workaround for circular dependencies


def parse_network(s):
    hosts = []
    links = []

    # TODO: add exception handling and descriptive error messages
    host_search = re.search(r"hosts\s*{([^}]*)}", s)
    if host_search:
        host_block = host_search.groups()[0]
        host_strs = re.findall(r"\s*([^\s]+\([^)]*\))", host_block)

        for host_str in host_strs:
            name = re.search(r"(.*)\(", host_str).groups()[0]
            attr_search = re.search(r"\((.*)\)", host_str)

            if not attr_search:
                raise SyntaxError("Missing attributes for host " + host_str)

            attrs = [s.strip() for s in attr_search.groups()[0].split(',')]
            rc = int(attrs[0])
            sc = int(attrs[1])

            if len(attrs) > 2:
                amp = int(attrs[2])
            else:
                amp = 1

            if name[0] == '_':
                if len(attrs) == 3:
                    h = Server(name[1:], rc, sc, amp)
                else:
                    h = Switch(name[1:], rc, sc)
            else:
                h = Host(name, rc, sc, amp)

            hosts.append(h)

    link_search = re.search(r"links\s*{([^}]*)}", s)
    if link_search:
        link_block = link_search.groups()[0]
        link_strs = re.findall(r"\s*([^\s]+\s*--\s*[^\s]+:\s*\d+)", link_block)

        for link_str in link_strs:
            endpoints = re.search(r"([^\s]+)--([^\s]+)\s*:", link_str).groups()
            c = int(re.search(r".*:\s*(\d+)", link_str).groups()[0])
            h1 = None
            h2 = None

            for h in hosts:
                if h.name == endpoints[0]:
                    h1 = h
                elif h.name == endpoints[1]:
                    h2 = h

            if h1 is None:
                raise SyntaxError("Unknown host name '%s' specified in link '%s'" % (endpoints[0], link_str))
            if h2 is None:
                raise SyntaxError("Unknown host name '%s' specified in link '%s'" % (endpoints[1], link_str))

            links.append(Link(h1, h2, c))

    return Network(hosts, links)


def parse_attack(s):
    network = Network.from_string(s)
    victim = None
    attackers = None

    victim_search = re.search(r"victim\s*:\s*([^\s]*)", s)
    if victim_search:
        name = victim_search.groups()[0]
        matches = [h for h in network.hosts if h.name == name]

        if matches:
            victim = matches[0]

    attackers_search = re.search(r"attackers\s*:\s*\[([^\s]*)\]", s)
    if attackers_search:
        attackers_str = attackers_search.groups()[0]
        names = [x.strip() for x in attackers_str.split(',')]
        attackers = [h for h in network.hosts if h.name in names]

    return smt.checker.AttackChecker(network, victim, attackers)
