import subprocess
import os

from network.topology import *

BRITE_DIRECTORY = "brite/"
CONF_FILE = "default.conf"
TMP_FILE = "tmp"
SEED_FILE = "seed"


class RandomTopology(Topology):
    def __init__(self, n):
        conf = os.path.join(BRITE_DIRECTORY, CONF_FILE)
        output = os.path.join(BRITE_DIRECTORY, TMP_FILE)
        seed = os.path.join(BRITE_DIRECTORY, SEED_FILE)

        try:
            brite = os.environ['BRITE_PATH']
            subprocess.check_call([brite, conf, output, seed], env=os.environ)
            brite_file = "%s.brite" % output

            hosts, links = parser.parse_brite_file(brite_file)
            os.remove(brite_file)

            super().__init__(hosts, links)
        except subprocess.CalledProcessError:
            print("Error generating BRITE topology")
            super().__init__([], [])
