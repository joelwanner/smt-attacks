import subprocess
import os

import string
import math
import random

from network.topology import *

BRITE_DIRECTORY = "brite/"
DEFAULT_CONF_FILE = "default.conf"
CONF_FILE = "tmp.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"


class RandomTopology(Topology):
    def __init__(self, n):
        with open(os.path.join(BRITE_DIRECTORY, DEFAULT_CONF_FILE), 'r') as f:
            config = f.read()

        self.n_systems = int(math.floor(math.sqrt(n)))
        self.as_size = n // self.n_systems

        config = config.replace("<N_AS>", str(self.n_systems))
        config = config.replace("<AS_SIZE>", str(self.as_size))

        tmp_conf = os.path.join(BRITE_DIRECTORY, CONF_FILE)
        with open(tmp_conf, 'w') as f:
            f.write(config)

        brite = os.environ['BRITE_PATH']
        args = [brite, CONF_FILE, TMP_FILE, SEED_FILE]
        dev_null = open("/dev/null", 'w')
        print("> %s" % " ".join(args))

        try:
            subprocess.check_call(args, env=os.environ, cwd=BRITE_DIRECTORY, stdout=dev_null)
            os.remove(tmp_conf)
            dev_null.close()

            output = os.path.join(BRITE_DIRECTORY, TMP_FILE)
            brite_file = "%s.brite" % output
            hosts, links = self.parse_brite_file(brite_file)
            os.remove(brite_file)

            super().__init__(hosts, links)
        except subprocess.CalledProcessError:
            print("Error generating BRITE topology")
            super().__init__([], [])

    def parse_brite_file(self, path):
        with open(path, 'r') as f:
            s = f.read()
            paragraphs = s.split('\n\n')

            node_str = paragraphs[1]
            edge_str = paragraphs[2]

            node_map = {}
            hosts = []
            links = []

            systems = [[]] * self.n_systems
            chosen_servers = []
            for i in range(self.n_systems):
                servers = [random.choice(range(0, self.as_size))]
                chosen_servers.append(servers)

            for line in node_str.split('\n')[1:]:
                attrs = line.split(' ')

                i = int(attrs[0])
                as_id = i // self.as_size
                address = i % self.as_size

                name = "%s%d" % (string.ascii_uppercase[as_id], address)

                if address in chosen_servers[as_id]:
                    h = Server(name, 1, 1, 2)
                else:
                    h = Host(name, 1, 1)

                hosts.append(h)
                node_map[i] = h
                systems[as_id].append(h)

            for line in edge_str.split('\n')[1:]:
                if line:
                    attrs = line.split(' ')
                    src_id = int(attrs[1])
                    dest_id = int(attrs[2])

                    src = node_map[src_id]
                    dest = node_map[dest_id]

                    if src_id // self.as_size == dest_id // self.as_size:
                        c = random.randint(1, 10)
                    else:
                        c = random.randint(10, 20)

                    l = Link(src, dest, c)
                    links.append(l)

            return hosts, links
