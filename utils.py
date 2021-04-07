import networkx as nx
import matplotlib.pyplot as plt


def create_graph(num_nodes, edge_present_prob):
    graph = nx.erdos_renyi_graph(num_nodes, edge_present_prob, directed=True)
    return graph


def view_graph(graph):
    nx.draw(graph, with_labels=True)
    plt.show()


def save_graph(graph, path):
    nx.write_adjlist(graph, path)


def retrieve_graph(path):
    return nx.read_adjlist(path, create_using=nx.DiGraph,nodetype = int)
