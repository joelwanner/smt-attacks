import subprocess
import os
from shutil import copyfile
from copy import copy

import string
import math
import random

from network.topology import *

BRITE_DIRECTORY = "brite/"
CONF_FILE = "tmp.conf"
CONF_DEFAULT = "default.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"
SEED_DEFAULT = "seed.default"


class RandomTopology(Topology):
    def __init__(self, n):
        with open(os.path.join(BRITE_DIRECTORY, CONF_DEFAULT), 'r') as f:
            config = f.read()

        n_routers = n // 2
        self.n_systems = int(math.floor(math.sqrt(n_routers)))
        self.as_size = n_routers // self.n_systems
        self.n_routers = self.n_systems * self.as_size
        self.n_clients = n - self.n_routers

        # Configure BRITE
        # ------------------
        config = config.replace("<N_AS>", str(self.n_systems))
        config = config.replace("<AS_SIZE>", str(self.as_size))

        tmp_conf = os.path.join(BRITE_DIRECTORY, CONF_FILE)
        with open(tmp_conf, 'w') as f:
            f.write(config)

        seed_path = os.path.join(BRITE_DIRECTORY, SEED_FILE)
        if not os.path.exists(seed_path):
            copyfile(os.path.join(BRITE_DIRECTORY, SEED_DEFAULT), seed_path)

        brite = os.environ['BRITE_PATH']
        args = [brite, CONF_FILE, TMP_FILE, SEED_FILE]
        dev_null = open("/dev/null", 'w')
        print("> %s" % " ".join(args))

        try:
            # Run BRITE
            # ------------------
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
            routers = []
            links = []

            systems = [[]] * self.n_systems

            # Parse BRITE nodes
            for line in node_str.split('\n')[1:]:
                attrs = line.split(' ')

                i = int(attrs[0])
                as_id = i // self.as_size
                address = i % self.as_size

                name = "%s%d" % (string.ascii_uppercase[as_id], address + 1)
                r = random.randint(30, 100)
                s = random.randint(10, 100)

                if random.randint(0, 3) == 0:
                    a = random.randint(5, 40)
                    h = Server(name, r, s, a)
                else:
                    h = Router(name, r, s)

                routers.append(h)
                node_map[i] = h
                systems[as_id].append(h)

            hosts = copy(routers)

            # Parse BRITE links
            for line in edge_str.split('\n')[1:]:
                if line:
                    attrs = line.split(' ')
                    src_id = int(attrs[1])
                    dest_id = int(attrs[2])
                    capacity = float(attrs[5])

                    src = node_map[src_id]
                    dest = node_map[dest_id]

                    l = Link(src, dest, int(capacity))
                    links.append(l)

            # Create clients
            for i in range(self.n_clients):
                client = Host(str(i + 1), random.randint(5, 40), random.randint(1, 10))
                router = random.choice(routers)
                hosts.append(client)

                l = Link(client, router, random.randint(10, 40))
                links.append(l)

            return hosts, links
