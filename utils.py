import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms.flow import shortest_augmenting_path


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
        elif start_edges == True:
            pair = line.split(":")
            edge_nodes = pair[1].strip().split(" ")
            for node in edge_nodes:
                graph.add_edge(int(pair[0]), int(node))
        else:
            nodes = line.strip().split(" ")
            query_dict[(int(nodes[0]), int(nodes[1]))] = []
    return graph, query_dict
