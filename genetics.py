import math
import os
from random import randint, uniform, random
import random
from Dataset import Dataset
from Graph import Graph
import numpy as np


class GET:
    # constant parameters
    verbose = True  # Print running output
    alpha = 0.5  # Probability of Epidemic Spread
    profile_length = 16  # Profile Length
    num_epidemics = 50  # Number of Sampled Epidemics
    short_epidemic = 3  # Meaningful Epidemic Length
    short_retries = 5  # Retry Short Epidemics
    final_test_len = 50  # Final Test Length
    runs = 30  # Number of Runs
    mating_events = 40000  # Number of Mating Events
    reporting_interval = 400  # Reporting Interval
    num_commands = 9  # Number of commands
    min_deg_swap = 2  # Minimum degree for swap
    popsize = 1000  # Number of chromosomes
    verts = 128  # Number of nodes
    gene_length = 256  # Gene length
    nodes_cubed = 2097152  # Nodes cubed
    max_mutations = 3  # Maximum number of mutations
    tourn_size = 7  # Tournament Size
    seed = 91207819  # Random Number Seed
    # pop = dict.fromkeys(range(0, popsize), [])  # Population of command strings
    pop = [[] for _ in range(popsize)]  # Population of command strings
    profile_path = None
    profile = None
    fitness = None
    sort_index = None
    cmd_density = None
    out_path = None
    profile_num = 0
    """
         Runs one iteration of the Graph Evolution Tool with the provided profile number, output
         folder and command densities.  Uses the profile matching fitnessPM.
              @param profileNum Epidemic profile number (1-9)
         @param outputPath Output location
         @param densities  Command densities
    
    """

    def __init__(self, densities: list, output_path: str, profile_num: int = None):
        self.profile_num = profile_num
        # self.profile = np.zeros(self.verts)
        self.fitness = np.zeros(self.popsize)  # float list
        self.sort_index = [i for i in range(self.popsize)]  # int list
        self.cmd_density = densities
        self.out_path = output_path

        if self.verbose:
            print("CORE")
            # print("\tProfile Number: " + str(profile_num))
            print("\tOutput Location: " + self.out_path)
            print("\tCommand Densities : ")
            for i in range(self.num_commands):
                print(str(densities[i]) + " ")
            print()

            # Grab information from command line arguments

        # profile_path = "./Profiles/Profile" + str(profile_num) + ".dat"  # Profile name
        # self.profile_path = "Profiles/Profile" + str(profile_num) + ".dat"  # Profile name
        # self.initalg()

    def run(self):
        print("profile_num", self.profile_num)
        for run in range(self.runs):
            run_output = ''
            self.init_pop()
            run_output += self.report()
            for mev in range(self.mating_events):
                self.mating_event()
                if (mev + 1) % self.reporting_interval == 0:
                    if self.verbose:
                        print(str(run) + " " + str((mev + 1) / self.reporting_interval) + " ")
                    run_output += self.report()
            # print(self.out_path + "run" + str(run) + ".dat", ''.join(run_output), False)
            self.print_to_file(self.out_path + "run" + str(run) + ".dat", run_output)
            self.report_best(run, is_pm=False)

    #  Facilitates one mating event
    def mating_event(self):
        # for length, higher is better, so the parents will be the two highest fitness genes
        ## the children are the lower value genes.
        self.t_select(is_pm=False)  # places first 7 peeps as the tourn (best at end)
        cp1 = abs(randint(0, 10000000) % self.gene_length)  # Crossover Points
        cp2 = abs(randint(0, 10000000) % self.gene_length)  # Crossover Points
        if cp1 > cp2:
            cp1, cp2 = cp2, cp1
        # Crossover
        parent1 = self.pop[int(self.sort_index[self.tourn_size - 2])]
        parent2 = self.pop[int(self.sort_index[self.tourn_size - 1])]

        child1 = parent1[0: cp1]
        child2 = parent2[0: cp1]

        child1.extend(parent2[cp1: cp2])
        child2.extend(parent1[cp1: cp2])

        child1.extend(parent1[cp2: self.gene_length])
        child2.extend(parent2[cp2: self.gene_length])

        muts = abs(randint(0, 1000000) % (self.max_mutations + 1))  # Number of Mutations
        for i in range(muts):
            r = abs(randint(0, 100000) % self.gene_length)  # Location of mutation
            child1[r] = self.valid_loci()

        muts = abs(randint(0, 100000) % (self.max_mutations + 1))
        for i in range(muts):
            r = abs(randint(0, 100000) % self.gene_length)
            child2[r] = self.valid_loci()

        # Update Fitness
        # fixme Profile matching
        # self.fitness[int(self.sort_index[0])] = self.fitness_pm(child1)
        # self.fitness[int(self.sort_index[1])] = self.fitness_pm(child2)
        self.fitness[int(self.sort_index[0])] = self.fitness_length(child1)
        self.fitness[int(self.sort_index[1])] = self.fitness_length(child2)

        self.pop[int(self.sort_index[0])] = child1
        self.pop[int(self.sort_index[1])] = child2

    def report(self) -> str:
        data = Dataset()
        data.add(self.fitness)

        new_data = data.getReport()
        if self.verbose:
            print(new_data)
        return new_data

    def init_pop(self):
        for i in range(self.popsize):
            # add "gene_length" number of valid_loci() to pop[i]
            self.pop[i] = [self.valid_loci() for _ in range(self.gene_length)]
            # fixme
            # self.fitness[i] = self.fitness_pm(self.pop[i])
            self.fitness[i] = self.fitness_length(self.pop[i])
            self.sort_index[i] = i  # Initialize order

    def valid_loci(self):
        # uniform: Return a random floating point number N
        dart = uniform(0, 1) - self.cmd_density[0]  # Throw the dart
        cmd = 0
        while dart > 0 and (cmd < self.num_commands - 1):
            cmd += 1
            dart -= self.cmd_density[cmd]

        cmd += self.num_commands * abs(randint(0, 100000000) % self.nodes_cubed)
        return cmd

    # Initialize the algorithm by seeding the random number generator and reading profile
    def init_algorithm(self):
        random.seed(self.seed)  # seed for rand ints
        # try:
        # input_file = open(self.profile_path)
        # for i in range(self.verts):
        #     self.profile[i] = 0  # Clear profile
        # self.profile[0] = 1  # Patient zero
        # i = 0
        # for tokens in input_file.readlines():
        #     for token in tokens.split():
        #         self.profile[i] = int(float(token))
        #         i += 1
        # # for i in range(1, self.profile_length):
        # #
        # # Print profile
        # if self.verbose:
        #     print("\tProfile: ")
        #
        #     for i in range(self.profile_length):
        #         print(str(self.profile[i]) + " ")
        #
        #     print()
        # except:
        #     print("ERROR: File '" + self.profile_path + "' Not Found")

    def initalg(self):
        self.init_algorithm()

    def t_select(self, is_pm=True):
        for i in range(self.tourn_size):
            r = abs(randint(1, 10000000) % self.popsize)
            tmp = self.sort_index[i]
            self.sort_index[i] = self.sort_index[r]
            self.sort_index[r] = int(tmp)
        if is_pm:
            not_sorted = True
            while not_sorted:
                not_sorted = False
                # Ensure decreasing fitnessPM (lower better)
                for i in range(self.tourn_size - 1):
                    for j in range(self.tourn_size - i - 1):
                        if self.fitness[self.sort_index[i]] < self.fitness[self.sort_index[i + 1]]:
                            self.sort_index[i], self.sort_index[i + 1] = self.sort_index[i + 1], self.sort_index[i]
                            not_sorted = True
        else:
            not_sorted = True
            while not_sorted:
                not_sorted = False
                # Ensure decreasing fitnessPM (lower better)
                for i in range(self.tourn_size - 1):
                    for j in range(self.tourn_size - i - 1):
                        if self.fitness[self.sort_index[i]] > self.fitness[self.sort_index[i + 1]]:
                            self.sort_index[i], self.sort_index[i + 1] = self.sort_index[i + 1], self.sort_index[i]
                            not_sorted = True

    def fitness_length(self, cmd):
        acc = 0
        G = Graph()  # Graph
        self.express(G, cmd)
        for e in range(self.num_epidemics):
            # Epidemic Length
            G.SIRLength(self.alpha)
            acc += G.getLen()

        return acc / self.num_epidemics

    def fitness_pm(self, cmd):
        trials = []
        G = Graph()  # Graph
        self.express(G, cmd)
        for e in range(self.num_epidemics):
            # Epidemic Profile
            rsltProfile = G.SIRProfile(self.alpha)
            error = 0.0  # Zero squared error
            if G.getLen() < self.profile_length + 1:
                G.setLen(self.profile_length + 1)

            for i in range(G.getLen()):
                delta = rsltProfile[i] - self.profile[i]
                error += delta * delta

            trials.append(math.sqrt(error / G.getLen()))

        trials.sort()  # Ascending order
        accu = 0.0
        for i in range(self.num_epidemics):
            accu += trials[i] / (i + 1)
        return accu

    def express(self, G, cmd):

        G.RNGnm(self.verts, 2)

        for i in cmd:
            block = i
            cdv = block % self.num_commands
            block /= self.num_commands
            a = int(block % self.verts)
            b = int((block / self.verts) % self.verts)
            c = int((block / self.verts / self.verts) % self.verts)
            if cdv == 0:  # Toggle
                G.toggle(a, b)
                continue
            if cdv == 1:  # Hop
                G.hop(a, b, c)
                continue
            if cdv == 2:  # Add
                G.add(a, b)
                continue
            if cdv == 3:  # Delete
                G.gdel(a, b)
                continue
            if cdv == 4:  # Swap
                a = int(block % (self.verts * 10))
                b = int((block / (self.verts * 10)) % (self.verts * 10))
                G.swap(a, b, self.min_deg_swap)
                continue
            if cdv == 5:  # Local Toggle
                G.ltog(a, b, c)
                continue
            if cdv == 6:  # Local Add
                G.ladd(a, b, c)
                continue
            if cdv == 7:  # Local Delete
                G.ldel(a, b, c)
                continue
            if cdv == 8:  # Null
                continue
        G.setCreated()

    def report_best(self, run, is_pm=True):
        # StringBuilder output = new StringBuilder(); // What this method outputs
        output = ''
        G = Graph(self.verts)  # To hold final graph from run
        if is_pm:
            b = 0  # Index of best fitnessPM found
            for i in range(1, self.popsize):
                if self.fitness[i] < self.fitness[b]:
                    b = i

            output += str(self.fitness[b])
            output += " -fitnessPM"
            output += "\n"
        else:
            b = 0  # Index of best fitnessPM found
            for i in range(1, self.popsize):
                if self.fitness[i] > self.fitness[b]:
                    b = i

            output += str(self.fitness[b])
            output += " -fitnessEL"
            output += "\n"

        # // Place best graph and fitness in best.lint

        output += str(self.pop[b][0])
        for i in range(1, self.gene_length):
            output += " "
            output += str(self.pop[b][i])
        output += "\n"

        self.express(G, self.pop[b])  # // Create graph
        self.print_to_file(self.out_path + "Graph" + str(run) + ".dat", G.write())
        self.print_to_file(self.out_path + "best.lint", output)

    def print_to_file(self, path: str, to_write: str):
        f = open("results_length/profile" + str(self.profile_num) + "/" + path, "a")
        # f = open("results/profile" + str(self.profile_num) + "/" + path, "a")
        f.write(to_write)
        f.close()


param_file = open('params.txt')
for param_line in param_file.readlines():
    params = [float(param) for param in param_line.split()]
    a = GET(densities=params,
            output_path='out', profile_num=1)
    a.run()
