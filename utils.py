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
