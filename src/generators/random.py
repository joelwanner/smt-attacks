import subprocess
import os
from shutil import copyfile
from copy import copy

import string
import random

from network.topology import *

BRITE_DIRECTORY = "brite/"
CONF_FILE = "tmp.conf"
CONF_DEFAULT = "default.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"
SEED_DEFAULT = "seed.default"


class RandomTopology(Topology):
    def __init__(self, n, connectivity):
        with open(os.path.join(BRITE_DIRECTORY, CONF_DEFAULT), 'r') as f:
            config = f.read()

        n_routers = n * 3 // 5
        self.n_clients = n - n_routers

        # Configure BRITE
        # ------------------
        config = config.replace("<N_ROUTERS>", str(n_routers))
        config = config.replace("<CONNECTIVITY>", str(connectivity))

        tmp_conf = os.path.join(BRITE_DIRECTORY, CONF_FILE)
        with open(tmp_conf, 'w') as f:
            f.write(config)

        seed_path = os.path.join(BRITE_DIRECTORY, SEED_FILE)
        if not os.path.exists(seed_path):
            copyfile(os.path.join(BRITE_DIRECTORY, SEED_DEFAULT), seed_path)

        if 'BRITE' in os.environ:
            brite_bin = os.environ['BRITE']
        else:
            brite_bin = "brite"

        args = [brite_bin, CONF_FILE, TMP_FILE, SEED_FILE]
        dev_null = open("/dev/null", 'w')
        print("> %s" % " ".join(args))

        try:
            # Run BRITE
            # ------------------
            subprocess.check_call(args, env=os.environ, cwd=BRITE_DIRECTORY, stdout=dev_null)
            dev_null.close()

            output = os.path.join(BRITE_DIRECTORY, TMP_FILE)
            brite_file = "%s.brite" % output
            hosts, links = self.parse_brite_file(brite_file)
            os.remove(brite_file)

            super().__init__(hosts, links)
        except FileNotFoundError:
            print("BRITE binary was not found. Add it to the path or set the BRITE environment variable")
            super().__init__([], [])
        except subprocess.CalledProcessError:
            print("BRITE error")
            super().__init__([], [])
        finally:
            os.remove(tmp_conf)

    def parse_brite_file(self, path):
        with open(path, 'r') as f:
            s = f.read()
            paragraphs = s.split('\n\n')

            node_str = paragraphs[1]
            edge_str = paragraphs[2]

            node_id_map = {}
            routers = []
            links = []

            autonomous_systems = {}
            as_sizes = {}

            # Parse BRITE nodes
            for line in node_str.split('\n')[1:]:
                attrs = line.split(' ')
                i = int(attrs[0])
                as_id = int(attrs[5])

                if as_id not in as_sizes:
                    as_sizes[as_id] = 0
                    autonomous_systems[as_id] = []

                internal_address = as_sizes[as_id]
                as_sizes[as_id] += 1

                name = "%s%d" % (string.ascii_uppercase[as_id], internal_address + 1)
                r = random.randint(30, 100)
                s = random.randint(10, 100)

                if random.randint(0, 2) == 0:
                    a = random.randint(5, 40)
                    h = Server(name, r, s, a)
                else:
                    h = Router(name, r, s)

                routers.append(h)
                node_id_map[i] = h
                autonomous_systems[as_id].append(h)

            hosts = copy(routers)

            # Parse BRITE links
            for line in edge_str.split('\n')[1:]:
                if line:
                    attrs = line.split(' ')
                    src_id = int(attrs[1])
                    dest_id = int(attrs[2])
                    src_as = int(attrs[6])
                    dest_as = int(attrs[7])
                    capacity = int(float(attrs[5]))

                    src = node_id_map[src_id]
                    dest = node_id_map[dest_id]

                    # Inter-AS edges are assigned larger capacities
                    if src_as != dest_as:
                        capacity = random.randint(70, 200)

                    l = Link(src, dest, capacity)
                    links.append(l)

            # Create clients
            for i in range(self.n_clients):
                client = Host(str(i + 1), random.randint(5, 40), random.randint(1, 10))
                router = random.choice(routers)
                hosts.append(client)

                l = Link(client, router, random.randint(10, 40))
                links.append(l)

            return hosts, links
