from network.execution import Execution
from network.network import *
from smt.encode import ModelEncoder
from smt.decode import ModelDecoder
from smt.solve import *


class AttackChecker:
    def __init__(self, network, n_flows, victims=None, attackers=None):
        if n_flows <= 0:
            raise ValueError("Invalid number of flows specified")

        self.network = network
        self.n_flows = n_flows
        self.victims = victims
        self.attackers = attackers

        self.attacks = []
        self.verbose = False

    def __check_execution(self, execution):
        encoder = ModelEncoder(execution, self.n_flows)
        assertions = encoder.get_assertions()

        solver = SmtSolver(verbose=self.verbose)
        result = solver.solve(assertions)

        if result == sat:
            decoder = ModelDecoder(encoder.model, solver.model)
            execution.flows = decoder.flows()
            execution.victims = decoder.victims()
            execution.attackers = decoder.attackers()

            return execution
        else:
            return None

    def check(self):
        if not self.attackers:
            potential_attackers = [h for h in self.network.hosts if not (isinstance(h, Server) or h == self.victims)]
        else:
            potential_attackers = self.attackers

        if self.victims and len(self.victims) == 1:
            # Check attack on single victim
            attack = self.__check_execution(Execution(self.network, self.n_flows, self.victims, potential_attackers))
            if attack:
                self.attacks.append(attack)
                return [attack]
            else:
                return []

        else:
            if self.victims:
                potential_victims = self.victims
            else:
                if self.attackers:
                    potential_victims = [h for h in self.network.hosts if h not in self.attackers]
                else:
                    potential_victims = self.network.hosts

            # Perform first check to see which hosts can be attacked
            print("Looking for attacks on potential victims %s" % potential_victims)
            attack = self.__check_execution(Execution(self.network, self.n_flows, potential_attackers, self.attackers))

            if attack:
                if len(attack.victims) == 1:
                    return [attack]

                # Fore more than one victim, there may be an attack possible -- check them individually
                for v in attack.victims:
                    print("Checking attack on victim %s" % v.__repr__())

                    attackers = [h for h in potential_attackers if h != v]
                    attack = self.__check_execution(Execution(self.network, self.n_flows, [v], attackers))

                    if attack:
                        self.attacks.append(attack)

            return self.attacks

    @classmethod
    def from_string(cls, s, n_flows):
        return parser.parse_attack(s, n_flows)
