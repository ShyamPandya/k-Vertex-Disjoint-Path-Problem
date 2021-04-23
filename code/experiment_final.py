from utils import read_input_file, get_file_names, view_graph
import networkx as nx
import random
import time
import sys
import os

untouchable_nodes = set()
vertices = set()
max_val = 0


def reset_query_dict(query_dict):
    for key in query_dict:
        # Create disjoint vertices set based on input pair
        vertices.add(key[0])
        vertices.add(key[1])
    untouchable_nodes.clear()


def is_safe_to_add(path):
    count = 0
    for v in path:
        # If a node conflicts with already chosen paths
        if v in untouchable_nodes:
            return False
        elif v in vertices:
            count += 1
    # If a node is part of the input nodes then don't choose the path
    if count > 2:
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
        # For all nodes between source and sink
        for v in path[1:-1]:
            deg_val += graph.in_degree[v]
        # deg_val is the ratio of sum of incoming edges of intermediate nodes
        # to the total number of nodes in the path
        deg_val /= len(path)
        if deg_val in in_degree_map:
            existing_paths = in_degree_map[deg_val]
            existing_paths.append(i)
            in_degree_map[deg_val] = existing_paths
        else:
            in_degree_map[deg_val] = [i]
    map_keys = list(in_degree_map.keys())
    map_keys.sort()
    return map_keys, in_degree_map


def recursion(graph, u, d, path, final_paths, vs):
    if len(final_paths) == 500000:
        return final_paths, True
    vs.add(u)
    path.append(u)
    if u == d:
        final_paths.append(list(path))
    else:
        adj = list(graph.adj[u])
        random.shuffle(adj)
        for i in adj:
            if i not in vs:
                ret_final_paths, res = recursion(graph, i, d, path, final_paths, vs)
                if res:
                    return ret_final_paths, res
    path.pop()
    vs.remove(u)
    return final_paths, False


def path_count(graph):
    temp_graph = graph.copy()
    len_dict = {}
    paths_dict = {}
    for key in query_dict:
        source = key[0]
        destination = key[1]
        #view_graph(temp_graph)
        final_destinations = []
        edge_dict = {}
        for node in vertices:
            if node == destination or node == source:
                continue
            final_destinations.append(node)
            edge_dict[node] = []
            edge_dict[node].extend(list(temp_graph.in_edges(node)))
            edge_dict[node].extend(list(temp_graph.out_edges(node)))
        temp_graph.remove_nodes_from(final_destinations)
        #view_graph(temp_graph)
        # Find mutually disjoint paths between a single source and sink
        #paths = list(nx.all_simple_paths(temp_graph, source, destination))
        paths, result = recursion(temp_graph, source, destination,[], [], set())
        len_dict[key] = len(paths)
        paths_dict[key] = paths
        temp_graph.add_nodes_from(final_destinations)
        for node in edge_dict:
            temp_graph.add_edges_from(edge_dict[node])
    print(len_dict)
    return list(dict(sorted(len_dict.items(), key=lambda item: item[1])).keys()), paths_dict


def backpropagation(graph, query_dict_keys, path_dict, query_dict, idx, out_file):
    c = 0
    for k in query_dict:
        if query_dict[k]:
            c += 1
    global max_val
    if c > max_val:
        max_val = c
        print('Max found: ' + str(max_val))
        with open(out_file, 'w') as file:
            for key in query_dict:
                p = query_dict[key]
                if len(p) > 0:
                    file.write(" ".join(repr(v) for v in p) + '\n')
        file.close()
    if idx >= 10 or query_dict[query_dict_keys[idx]]:
        return True, query_dict
    pair = query_dict_keys[idx]
    paths = path_dict[pair]
    path_select_keys, in_degree_map = path_sorter(graph, paths)
    for i in range(len(path_select_keys)):
        possible_paths = in_degree_map[path_select_keys[i]]
        for j in range(len(possible_paths)):
            path = paths[possible_paths[j]]
            if is_safe_to_add(path):
                add_to_nodes_used(path)
                query_dict[pair] = path
                res, temp_query_dict = backpropagation(graph, query_dict_keys,
                                                       path_dict, query_dict, idx+1, out_file)
                if res:
                    return True, temp_query_dict
                remove_from_nodes_used(path)
                query_dict[pair] = []
    return False, query_dict


if __name__ == '__main__':
    inp_file, out_file = get_file_names(sys.argv[1:])
    start_time = time.perf_counter()
    print('Starting time: ' + str(start_time))
    graph, query_dict = read_input_file(inp_file)
    reset_query_dict(query_dict)
    query_dict_keys, path_dict = path_count(graph)
    print('Starting exploration ')
    result, result_query_dict = backpropagation(graph, query_dict_keys, path_dict,
                                                query_dict, 0, out_file)
    end_time = time.perf_counter()
    print('Ending time: ' + str(end_time))
    print('Time taken: ' + str(end_time - start_time) + ' seconds')