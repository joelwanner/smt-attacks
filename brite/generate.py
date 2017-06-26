import argparse
import subprocess
import os

from network.topology import *


BRITE_DIRECTORY = "brite/"
CONF_FILE = "default.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"


def parse_brite_file(path):
    with open(path, 'r') as f:
        s = f.read()
        paragraphs = s.split('\n\n')

        node_str = paragraphs[1]
        edge_str = paragraphs[2]

        node_map = {}
        hosts = []
        links = []

        for line in node_str.split('\n')[1:]:
            attrs = line.split(' ')

            i = int(attrs[0])
            h = Host("H%d" % i, 1, 1)
            hosts.append(h)
            node_map[i] = h

        for line in edge_str.split('\n')[1:]:
            if line:
                attrs = line.split(' ')
                src_id = int(attrs[1])
                dest_id = int(attrs[2])

                src = node_map[src_id]
                dest = node_map[dest_id]

                l = Link(src, dest, 1)
                links.append(l)

        return Topology(hosts, links)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("brite", help="Path to BRITE binary")
    args = parser.parse_args()

    conf = os.path.join(BRITE_DIRECTORY, CONF_FILE)
    output = os.path.join(BRITE_DIRECTORY, TMP_FILE)
    seed = os.path.join(BRITE_DIRECTORY, SEED_FILE)
    exit_code = subprocess.call([args.brite, conf, output, seed], env=os.environ)

    if exit_code == 0:
        brite_file = "%s.brite" % output
        topology = parse_brite_file(brite_file)

        output_path = os.path.join("%s.txt" % output)
        with open(output_path, "w") as file:
            file.write(topology.__str__())
