import math

from graphviz import Graph

"""
Takes in files representing the adjacency lists of networks and creates visualizations of the networks.
"""

out_root = "./Output/"
inp_root = "results_length/"
verts = 160
edge_w = "1"

import os

os.environ["PATH"] += os.pathsep + "C:/Users/om20fz/Downloads/Graphviz/bin"


def loadData(fName):
    data = []
    with open(fName) as f:
        lines = f.readlines()
        lines.__delitem__(0)
        for from_node, line in enumerate(lines):
            line = line.rstrip()
            line = line.split("\t")
            print(line)
            for to_node in line:
                if to_node == '':
                    continue
                print(to_node)
                data.append([int(from_node), int(to_node)])
                pass
            pass
        pass
    return data


def makeGraph():
    graph_root = "profile9/"
    theta_diff = 2 * math.pi / (verts / 2)
    inside_offset = theta_diff / 2
    radius = [3, 2.5]

    # inp_file = inp_root + graph_root + estr + ".dat"
    inp_file = inp_root + graph_root + "outGraph0" + ".dat"
    out_file = graph_root + "graph"
    data = loadData(inp_file)

    # if sidx == 0:
    # g = Graph(engine='neato')
    g = Graph(engine='sfdp')
    g.attr(size="5,5")
    g.graph_attr.update(dpi='600')
    g.node_attr.update(fixedsize='true', shape='circle')
    g.edge_attr.update(weight=edge_w)

    for n in range(verts):
        g.node(str(n))
        pass

    for d in data:
        if d[0] >= d[1]:
            g.edge(str(d[0]), str(d[1]))  # , penwidth=str(edge_w))
            pass
        pass

    g.render(filename=out_file, directory='results', cleanup=True, format='png')
    pass


def main():
    makeGraph()
    pass


main()
