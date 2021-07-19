from math import exp, log
from random import random

import numpy as np


class Graph:
    E: int = None  # Number edges
    V: int = None  # Number vertices
    nbr: dict = None  # Neighbour lists
    created: bool = None  # Colours
    epidemiced: bool = None

    #    COMMENT FROM MICHAEL TODO: Add functionality to catch if epidemic not run yet

    maxI: int = None  # Maximum infected at one time
    lengt: int = None  # Epidemic length
    totI: int = None  # Total people infected

    def __init__(self, max_verts=128):
        self.clr = []
        self.initialize_graph(max_verts)

    def initialize_graph(self, maximum: int):
        self.V = 0
        self.E = 0
        # self.nbr = dict.fromkeys(range(0, maximum), [])
        self.nbr = [[] for _ in range(maximum)]

        self.clr = np.zeros(maximum)
        self.created = False
        self.epidemiced = False

    # Ring of 128 nod
    # es, where each vertex has 2m neighbours (m before and m after)
    def RNGnm(self, n: int, m: int):
        self.initialize_graph(n)  # Check for storage

        if m > n:
            m %= n  # Fail safe

        self.V = n
        self.E = 2 * m * n
        for i in range(n):
            for j in range(1, m + 1):
                self.nbr[i].append((i + j) % n)
                self.nbr[i].append((i - j + n) % n)

    # Hop edge
    def hop(self, v: int, n1: int, n2: int):
        nb1: int = 0  # Neighbour of v for consideration
        nb2: int = 0  # Neighbour of nb1 for consideration
        d1: int = 0  # Degree of v
        d2: int = 0  # Degree of nb1

        if self.V == 0:  # Empty graph
            return

        v = self.normalize(v, self.V)
        d1 = self.degree(v)  # Get degree of neighbour
        if d1 < 1:  # No neighbours
            return

        n1 = self.normalize(n1, d1)
        nb1 = self.nbrMod(v, n1)  # Get neighbour
        d2 = self.degree(nb1)  # Get degree of neighbour
        if d2 < 2:  # No place to hop
            return
        n2 = self.normalize(n2, d2)
        nb2 = self.nbrMod(nb1, n2)  # Get neighbour of neighbour
        if self.edgeP(v, nb2):  # Triangle, no hop possible
            return
        if v == nb2:  # Trying to add a loop
            return

        # MICHAEL TODO: Remove duplicate code above
        # Process hop # FIXME
        # del(v, nb1)
        # add(v, nb2)

    # Local Toggle
    def ltog(self, v: int, n1: int, n2: int):
        if self.V == 0:
            return  # Empty graph
        v = self.normalize(v, self.V)
        d1 = self.degree(v)
        if d1 < 1:
            return  # No neighbours

        n1 = self.normalize(n1, d1)
        nb1 = self.nbrMod(v, n1)  # Get neighbour
        d2 = self.degree(nb1)
        if d2 < 2:
            return  # No place to toggle
        n2 = self.normalize(n2, d2)
        nb2 = self.nbrMod(nb1, n2)  # Get neighbour of neighbour
        if v == nb2:
            return  # Trying to add a loop
        self.toggle(v, nb2)  # Apply toggle

    # Toggle edge
    def toggle(self, a: int, b: int):
        if self.V == 0:
            return
        a = int(self.normalize(a, self.V))
        b = int(self.normalize(b, self.V))
        if a == b:
            return
        if b in self.nbr[a]:  # Edge exists
            self.nbr[a].remove(b)
            self.nbr[b].remove(a)
            self.E -= 1
        else:  # # Edge doesn't exist
            self.nbr[a].append(b)
            self.nbr[b].append(a)
            self.E += 1

    # Returns the (n % degree)th neighbour of v
    def nbrMod(self, v: int, n: int) -> int:
        return self.nbr[v][n % self.degree(v)]

    # Takes in orig and returns orig if 0 <= orig < max.  Otherwise, it returns
    # / ((orig % max) + max) % max, this forces correct vertex numbers
    def normalize(self, orig: int, max: int) -> int:
        if (orig < 0) or (orig >= self.V):
            orig = ((orig % max) + max) % max
        return int(orig)

    def degree(self, v: int) -> int:
        return len(self.nbr[v])

    # Local Add
    def ladd(self, v: int, n1: int, n2: int):

        if self.V == 0:
            return  # Empty graph
        v = self.normalize(v, self.V)
        d1 = self.degree(v)
        if d1 < 1:
            return  # No neighbours
        n1 = self.normalize(n1, d1)
        nb1 = self.nbrMod(v, n1)  # Get neighbour
        d2 = self.degree(nb1)
        if d2 < 2:
            return  # No place to toggle

        n2 = self.normalize(n2, d2)
        nb2 = self.nbrMod(nb1, n2)  # Get neighbour of neighbour
        if v == nb2:
            return  # Trying to add a loop

        self.add(v, nb2)  # Apply add

    # Add edge
    def add(self, a: int, b: int):
        a = self.normalize(a, self.V)
        b = self.normalize(b, self.V)
        if a == b:
            return
        # fixme check contains
        if b not in self.nbr[a]:
            self.toggle(a, b)

    # Local Del
    def ldel(self, v: int, n1: int, n2: int):
        if self.V == 0:
            return  # Empty graph

        v = self.normalize(v, self.V)
        d1 = self.degree(v)
        if d1 < 1:
            return  # No neighbours

        n1 = self.normalize(n1, d1)
        nb1 = self.nbrMod(v, n1)  # Get neighbour
        d2 = self.degree(nb1)
        if d2 < 2:
            return  # No place to toggle

        n2 = self.normalize(n2, d2)
        nb2 = self.nbrMod(nb1, n2)  # Get neighbour of neighbour
        if v == nb2:
            return  # Trying to add a loop

        self.gdel(v, nb2)  # Apply del

    # Del edge
    def gdel(self, a: int, b: int):
        a = self.normalize(a, self.V)
        b = self.normalize(b, self.V)
        if a == b:  # Same vertex
            return

        if self.nbr[a].__contains__(str(b)):
            self.toggle(a, b)

    # Swap
    def swap(self, a: int, b: int, k: int):

        # Check degree bound
        v1 = a % self.V
        if len(self.nbr[v1]) < k:
            return

        v2 = b % self.V
        if len(self.nbr[v2]) < k:
            return

        if self.edgeP(v1, v2):
            return  # Already edge from v1 to v2

        n1 = int(a / self.V) % self.degree(v1)  # First neighbour's index
        n1 = self.nbr[v1][n1]  # First neighbour
        n2 = int(b / self.V) % self.degree(v2)  # Second neighbour's index
        n2 = self.nbr[v2][n2]  # Second neighbour

        if self.edgeP(v1, n2) or self.edgeP(v2, n1) or self.edgeP(n1, n2):  # Edges already exist
            return

        # Process swap
        self.toggle(v1, n1)
        self.toggle(v2, n2)
        self.toggle(v1, n2)
        self.toggle(v2, n1)

    # Is a to b an edge
    def edgeP(self, a: int, b: int) -> bool:
        if (a < 0) or (b < 0) or (a >= self.V) or (b >= self.V):  # Not a vertex
            return False
        return b in self.nbr[a]

    # def SIRLength(self, alpha: float, sirs: bool, removedLength: int):
    #
    #     if not self.created:
    #         print("ERROR: SIRLength not created")
    #
    #     maxI = 0
    #     totI = 0
    #     # int NI # Number of infected individuals
    #     # ArrayList<Integer> nin # Number of Infected Neighbors
    #
    #     if (self.V == 0):
    #         print("ERROR: SIRLength on Graph with 0 Nodes")
    #
    #     # fixme what's this ?
    #     self.setClr(0)  # Susceptible
    #     self.clr.set(0, 1)  # Infect node with index 0
    #     NI = 1
    #     len = 0
    #
    #     while (NI > 0):  # Still infected
    #         nin = []  # size of self.V
    #         for i in range(self.V):  # Clear nin
    #             nin.append(0)
    #
    #         for i in range(self.V):  # Fill nin
    #             if self.clr[i] == 1:  # Infected individual found (node i)
    #                 for j in range(len(self.nbr.get(i))):  # For each neighbour
    #                     neighbour = self.nbr.get(i).get(j)
    #                     nin[neighbour] = nin.get(neighbour) + 1  # Increase nin
    #
    #         # Check for transmission
    #         for i in range(self.V):
    #             if (self.clr[i] == 0) and (nin.get(i) > 0):
    #                 infected_var = 0
    #                 if self.infected(nin.get(i), alpha):
    #                     infected_var = 4
    #                 self.clr[i] = infected_var
    #
    #         if NI > maxI:
    #             maxI = NI
    #
    #         totI += NI
    #         NI = 0
    #
    #         # MICHAEL TODO: correct below
    #         if sirs:
    #             cap = removedLength + 3  # SIR and Newly Infected (0-3)
    #             for i in range(self.V):
    #                 colour: int = self.clr[i]
    #                 if colour == 1:
    #                     self.clr[i] = 2  # Infected, move to removed
    #                 elif colour == 2:
    #                     self.clr[i] = 4  # Removed, move to next day of resistance
    #                 elif colour == 3:
    #                     self.clr[i] = 1  # Newly infected, move to infected
    #                     NI += 1
    #                 elif colour == cap:
    #                     self.clr[i] = 0  # End of resistance, move to susceptible
    #                 elif colour != 0:
    #                     self.clr[i] = colour + 1
    #         else:
    #             for i in range(self.V):
    #                 if self.clr[i] == 0:  # Susceptible, do nothing
    #                     break
    #                 if self.clr[i] == 1:  # Infected, move to removed
    #                     self.clr.set(i, 2)
    #                     break
    #                 if self.clr[i] == 2:  # Removed, do nothing
    #                     break
    #                 if self.clr[i] == 3:  # Newly infected, move to infected
    #                     self.clr.set(i, 1)
    #                     NI += 1
    #                     break
    #
    #         len += 1
    #     self.epidemiced = True
    #     return len

    # END  SIRLength
    def probability(self, percent):
        rnd = random()
        return rnd < percent

    # Returns true if node would become infected given strength alpha
    def infected(self, n: int, alpha: float):
        inf_rnd = random()
        beta = 1 - exp(n * log(1 - alpha))
        return inf_rnd < beta

    # Set all colours to c
    def setClr(self, c: int):
        self.clr = []
        for i in range(self.V):
            self.clr.append(c)
        self.clr = np.array(self.clr)

    def SIRProfile(self, alpha: float):
        if not self.created:
            print("ERROR: SIRProfile not created")
        prof = np.zeros(self.V)  # size of double[V]
        maxI = 0
        totI = 0
        self.lengt = 0

        # nin # Number of Infected Neighbors

        if self.V == 0:
            print("ERROR: SIRProfile on Graph with 0 Nodes")
        for i in range(self.V):
            prof[i] = 0

        self.setClr(0)  # Susceptible
        self.clr[0] = 1  # Infect node with index 0
        NI = 1
        prof[self.lengt] = 1.0
        while NI > 0:  # Still infected
            nin = []  # size of V
            for i in range(self.V):
                nin.append(0)

            for i in range(self.V):
                if self.clr[i] == 1:  # Infected individual found (node i)
                    for j in range(len(self.nbr[i])):  # For each neighbour
                        neighbour = self.nbr[i][j]
                        nin[neighbour] = nin[neighbour] + 1  # Increase nin

            # Check for transmission
            for i in range(self.V):
                infected_var = 0
                if (self.clr[i] == 0) and (nin[i] > 0):
                    # send Susceptible for vaccination
                    prb = self.probability(0.2)
                    if prb:
                        infected_var = 5
                        self.clr[i] = infected_var
                        continue
                    #     todo what if got vaccinated and infected at the same day ?
                    inf_prob = self.infected(nin[i], alpha)
                    if inf_prob:
                        infected_var = 4
                    self.clr[i] = infected_var
                elif self.clr[i] == 5 and (nin[i] > 0):
                    if self.infected(nin[i], 0.3):
                        infected_var = 4
                    self.clr[i] = infected_var

            if NI > maxI:
                maxI = NI

            totI += NI
            NI = 0

            for i in range(self.V):
                if self.clr[i] == 0 or self.clr[i] == 5:  # Susceptible, do nothing
                    continue
                # if self.clr[i] == 1:  # Infected day 1, move to day 2
                #     self.clr[i] = 2
                #     continue
                if self.clr[i] == 1:  # Infected day 2, move to removed
                    self.clr[i] = 3
                    continue
                if self.clr[i] == 3:  # Removed, do nothing
                    continue
                if self.clr[i] == 4:  # Newly infected, move to infected
                    self.clr[i] = 1
                    NI += 1
                    prof[self.lengt + 1] += 1.0
                    continue

            self.lengt += 1

        self.epidemiced = True
        return prof

    def SIRLength(self, alpha: float):
        if not self.created:
            print("ERROR: SIRProfile not created")
        maxI = 0
        totI = 0
        self.lengt = 0

        # nin # Number of Infected Neighbors

        if self.V == 0:
            print("ERROR: SIRProfile on Graph with 0 Nodes")

        self.setClr(0)  # Susceptible
        self.clr[0] = 1  # Infect node with index 0
        NI = 1
        while NI > 0:  # Still infected
            nin = []  # size of V
            for i in range(self.V):
                nin.append(0)

            for i in range(self.V):
                if self.clr[i] == 1:  # Infected individual found (node i)
                    for j in range(len(self.nbr[i])):  # For each neighbour
                        neighbour = self.nbr[i][j]
                        nin[neighbour] = nin[neighbour] + 1  # Increase nin

            # Check for transmission
            for i in range(self.V):
                infected_var = 0
                if (self.clr[i] == 0) and (nin[i] > 0):
                    # send Susceptible for vaccination
                    prb = self.probability(0.2)
                    if prb:
                        infected_var = 5
                        self.clr[i] = infected_var
                        continue
                    #     todo what if got vaccinated and infected at the same day ?
                    inf_prob = self.infected(nin[i], alpha)
                    if inf_prob:
                        infected_var = 4
                    self.clr[i] = infected_var
                elif self.clr[i] == 5 and (nin[i] > 0):
                    if self.infected(nin[i], 0.3):
                        infected_var = 4
                    self.clr[i] = infected_var

            if NI > maxI:
                maxI = NI

            totI += NI
            NI = 0

            for i in range(self.V):
                if self.clr[i] == 0 or self.clr[i] == 5:  # Susceptible, do nothing
                    continue
                # if self.clr[i] == 1:  # Infected day 1, move to day 2
                #     self.clr[i] = 2
                #     continue
                if self.clr[i] == 1:  # Infected day 2, move to removed
                    self.clr[i] = 3
                    continue
                if self.clr[i] == 3:  # Removed, do nothing
                    continue
                if self.clr[i] == 4:  # Newly infected, move to infected
                    self.clr[i] = 1
                    NI += 1
                    continue

            self.lengt += 1

        self.epidemiced = True

    def write(self):
        output = ''  # new StringBuilder()
        output += str(self.V)
        output += "\t"
        output += str(self.E)
        output += "\n"

        for l in range(len(self.nbr)):
            for n in self.nbr[l]:
                output += str(n)
                output += "\t"
            output += "\n"
        return output

    def getLen(self):
        if not self.created or not self.epidemiced:
            print("ERROR: getLen")

        return self.lengt

    def setLen(self, l: int):
        if not self.created or not self.epidemiced:
            print("ERROR: setLen")

        self.lengt = l

    def getTotI(self) -> int:
        if not self.created or not self.epidemiced:
            print("ERROR: getTotI")

        return self.totI

    def setCreated(self):
        self.created = True
        self.epidemiced = False
# 4.406920000000008 0.023422362516864553 0.37770903298696124 3.28
#
# 0 3.0
# 4.3544600000000075 0.02398728422130284 0.38681896075548144 3.28
#
# 0 4.0
# 4.315099999999999 0.025289109710188228 0.40781219942517744 3.28
#

# 0 5.0
# 4.27759999999999 0.02499940814483045 0.4031404717961943 3.28