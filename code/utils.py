import matplotlib.pyplot as plt
import networkx as nx
import getopt
import sys


def create_graph(num_nodes, edge_present_prob):
    graph = nx.erdos_renyi_graph(num_nodes, edge_present_prob, directed=True)
    return graph


def view_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()


def save_graph(graph, path):
    nx.write_adjlist(graph, path)


def retrieve_graph(path):
    return nx.read_adjlist(path, create_using=nx.DiGraph, nodetype=int)


def get_vertex_disjoint_paths(graph, source, destination, aux, residual):
    return list(nx.node_disjoint_paths(graph, source, destination, auxiliary=aux, residual=residual))


def read_input_file(path):
    file = open(path, 'r')
    start_edges = False
    graph = nx.DiGraph()
    graph.add_nodes_from(node for node in range(1, 101))
    query_dict = {}
    for line in file:
        line = line.rstrip("\n")
        if line == 'EDGES':
            start_edges = True
        elif line == 'PAIRS':
            start_edges = False
        elif start_edges:
            pair = line.split(":")
            if len(pair[1].strip()) == 0:
                continue
            edge_nodes = pair[1].strip().split(" ")
            for node in edge_nodes:
                graph.add_edge(int(pair[0]), int(node))
        else:
            nodes = line.strip().split(" ")
            query_dict[(int(nodes[0]), int(nodes[1]))] = []
    file.close()
    return graph, query_dict


def read_output_file(path):
    result_dict = {}
    file = open(path, 'r')
    for line in file:
        line = line.rstrip("\n")
        nodes = line.strip().split(" ")
        nodes = [int(node) for node in nodes]
        result_dict[(nodes[0], nodes[-1])] = nodes
    file.close()
    return result_dict


def get_file_names(argv):
    inputfile = ''
    outputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:o:", ["ifile=","ofile="])
    except getopt.GetoptError:
        print('first_experiment.py -i <inputfile>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('test.py -i <inputfile> -o <outputfile>')
            sys.exit()
        elif opt in ["-i", "--ifile"]:
            inputfile = arg
        elif opt in ["-o", "--ofile"]:
            outputfile = arg
    return inputfile, outputfile
