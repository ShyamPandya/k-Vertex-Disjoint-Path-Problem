from utils import create_graph, save_graph, view_graph, retrieve_graph, get_vertex_disjoint_paths
from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
from networkx.algorithms.flow import build_residual_network
import networkx as nx
import time
import random
import os

query_dict = {
    (2, 17): [],
    (5, 19): [],
    (0, 18): [],
    (40, 97): [],
    (3, 85): [],
    (56, 57): [],
    (15, 37): [],
    (99, 79): [],
    (6, 66): [],
    (9, 69): []
}
untouchable_nodes = set()


def reset_query_dict():
    for key in query_dict:
        query_dict[key] = []
    untouchable_nodes.clear()


def next_pair_to_explore():
    keys = list(query_dict.keys())
    random.shuffle(keys)
    for key in keys:
        if not query_dict[key]:
            return key
    return None


def is_safe_to_add(path):
    for v in path:
        if v in untouchable_nodes:
            return False
    return True


def add_to_nodes_used(path):
    for v in path:
        untouchable_nodes.add(v)


def remove_from_nodes_used(path):
    for v in path:
        untouchable_nodes.remove(v)


def path_sorter(graph, initial_paths):
    in_degree_map = {}
    for i in range(len(initial_paths)):
        path = initial_paths[i]
        deg_val = 0
        for v in path[1:-1]:
            deg_val += graph.in_degree[v]
        deg_val /= len(path)
        if deg_val in in_degree_map:
            existing_paths = in_degree_map[deg_val]
            existing_paths.append(i)
            in_degree_map[deg_val] = existing_paths
        else:
            in_degree_map[deg_val] = [i]
    map_keys = list(in_degree_map.keys())
    map_keys.sort()
    '''for key in map_keys:
        print('Degree_Value: ' + str(key) + ' Paths: ' + str(in_degree_map[key]))'''
    return map_keys, in_degree_map


def backpropagation(graph, graph_aux, graph_residual):
    pair = next_pair_to_explore()
    if not pair:
        return True
    source = pair[0]
    destination = pair[1]
    paths = get_vertex_disjoint_paths(graph, source, destination, aux=graph_aux, residual=graph_residual)
    path_select_keys, in_degree_map = path_sorter(graph, paths)
    for i in range(len(path_select_keys)):
        possible_paths = in_degree_map[path_select_keys[i]]
        for j in range(len(possible_paths)):
            path = paths[possible_paths[j]]
            if is_safe_to_add(path):
                add_to_nodes_used(path)
                query_dict[pair] = path
                if backpropagation(graph, graph_aux, graph_residual):
                    return True
                if j == len(possible_paths) - 1 and i == len(path_select_keys) - 1:
                    return True
                remove_from_nodes_used(path)
                query_dict[pair] = []
    return False


if __name__ == '__main__':
    # graph = retrieve_graph('graph_store.txt')
    n = 100
    p = 0.60
    ps = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1]
    for p in ps:
        if not os.path.exists(str(p)):
            os.mkdir(str(p))
        for i in range(1, 50):
            start_time = time.perf_counter()
            reset_query_dict()
            graph = create_graph(n, p)
            save_graph(graph, str(p) + '\\graph_store_' + str(i) + '.txt')
            graph_aux = build_auxiliary_node_connectivity(graph)
            graph_residual = build_residual_network(graph_aux, "capacity")
            result = backpropagation(graph, graph_aux, graph_residual)
            end_time = time.perf_counter()
            count = 0
            for key in query_dict:
                if len(query_dict[key]) > 0:
                    count += 1
            print('Unique paths: ' + str(count))
            print('Time taken: ' + str(end_time - start_time) + ' seconds')
            with open(str(p) + '\\graph_paths_found.txt', 'a+') as file:
                file.write(str(i) + ': ' + str(count) + ', ' + str(end_time - start_time) + ' seconds\n')
            file.close()

    '''
    # graph = create_graph(5, 0.5)
    # save_graph(graph, 'graph_store.txt')
    # view_graph(graph)

    # Before reading make sure there aren't any empty lines in the file at the end or the library breaks
    graph = retrieve_graph('graph_store.txt')
    graph_aux = build_auxiliary_node_connectivity(graph)
    graph_residual = build_residual_network(graph_aux, "capacity")
    paths = get_vertex_disjoint_paths(graph, 0, 3, aux=graph_aux, residual=graph_residual)
    print(paths)
    path_sorter(graph, paths)
    paths2 = get_vertex_disjoint_paths(graph, 1, 4, aux=graph_aux, residual=graph_residual)
    print(paths2)
    path_sorter(graph, paths2)
    view_graph(graph)
    
    G = nx.icosahedral_graph()
    print(list(nx.node_disjoint_paths(G, 0, 6)))'''
