import subprocess
import os

from network.topology import *

BRITE_DIRECTORY = "brite/"
CONF_FILE = "default.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"


class RandomTopology(Topology):
    def __init__(self):
        try:
            brite = os.environ['BRITE_PATH']
            args = [brite, CONF_FILE, TMP_FILE, SEED_FILE]
            print("> %s" % " ".join(args))

            dev_null = open("/dev/null", 'w')
            subprocess.check_call(args, env=os.environ, cwd=BRITE_DIRECTORY, stdout=dev_null)
            dev_null.close()

            output = os.path.join(BRITE_DIRECTORY, TMP_FILE)
            brite_file = "%s.brite" % output
            hosts, links = self.parse_brite_file(brite_file)
            os.remove(brite_file)

            super().__init__(hosts, links)
        except subprocess.CalledProcessError:
            print("Error generating BRITE topology")
            super().__init__([], [])

    @staticmethod
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

            return hosts, links
