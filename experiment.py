from utils import retrieve_graph, get_vertex_disjoint_paths, read_input_file
from networkx.algorithms.connectivity import build_auxiliary_node_connectivity
from networkx.algorithms.flow import build_residual_network
import random
import time

untouchable_nodes = set()
vertices = set()


def reset_query_dict(query_dict):
    for key in query_dict:
        vertices.add(key[0])
        vertices.add(key[1])
    untouchable_nodes.clear()


def next_pair_to_explore():
    keys = list(query_dict.keys())
    #random.shuffle(keys)
    for key in keys:
        if not query_dict[key]:
            return key
    return None


def is_safe_to_add(path):
    count = 0
    for v in path:
        if v in untouchable_nodes:
            return False
        elif v in vertices:
            count += 1
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


def backpropagation(graph, graph_aux, graph_residual, query_dict_keys, path_dict, query_dict, idx):
    if idx >= 10 or query_dict[query_dict_keys[idx]]:
        return True, query_dict
    '''pair = next_pair_to_explore()
    if not pair:
        return True'''
    pair = query_dict_keys[idx]
    #source = pair[0]
    #destination = pair[1]
    #paths = get_vertex_disjoint_paths(graph, source, destination, aux=graph_aux, residual=graph_residual)
    paths = path_dict[pair]
    path_select_keys, in_degree_map = path_sorter(graph, paths)
    for i in range(len(path_select_keys)):
        possible_paths = in_degree_map[path_select_keys[i]]
        for j in range(len(possible_paths)):
            path = paths[possible_paths[j]]
            if is_safe_to_add(path):
                add_to_nodes_used(path)
                query_dict[pair] = path
                res, temp_query_dict = backpropagation(graph, graph_aux, graph_residual, query_dict_keys,
                                                       path_dict, query_dict, idx+1)
                if res:
                    return True, temp_query_dict
                if j == len(possible_paths) - 1 and i == len(path_select_keys) - 1:
                    return True, query_dict
                remove_from_nodes_used(path)
                query_dict[pair] = []
    return False, query_dict

def path_count(graph, graph_aux, graph_residual):
    len_dict = {}
    path_dict = {}
    for key in query_dict:
        source = key[0]
        destination = key[1]
        paths = get_vertex_disjoint_paths(graph, source, destination, aux=graph_aux, residual=graph_residual)
        len_dict[key] = len(paths)
        path_dict[key] = paths
    print(len_dict)
    return list(dict(sorted(len_dict.items(), key=lambda item: item[1])).keys()), path_dict


if __name__ == '__main__':
    graph = retrieve_graph('0.9\\graph_store_30.txt')
    start_time = time.perf_counter()
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
    reset_query_dict(query_dict)
    graph_aux = build_auxiliary_node_connectivity(graph)
    graph_residual = build_residual_network(graph_aux, "capacity")
    query_dict_keys, path_dict = path_count(graph, graph_aux, graph_residual)
    print('Starting exploration')
    result, result_query_dict = backpropagation(graph, graph_aux, graph_residual, query_dict_keys, path_dict, query_dict, 0)
    end_time = time.perf_counter()
    count = 0
    for key in result_query_dict:
        if len(result_query_dict[key]) > 0:
            count += 1
    print('Backpropagation result: '+ str(result))
    print('Unique paths: ' + str(count))
    print(result_query_dict)
    print('Time taken: ' + str(end_time - start_time) + ' seconds')
    with open(str(0.9) + '\\graph_paths_found.txt', 'a+') as file:
        file.write(str(24) + ': ' + str(count) + ', ' + str(end_time - start_time) + ' seconds\n')
    file.close()
    '''
    graph, query_dict = read_input_file('samplein.txt')
    graph_aux = build_auxiliary_node_connectivity(graph)
    graph_residual = build_residual_network(graph_aux, "capacity")
    query_dict_keys, path_dict = path_count(graph, graph_aux, graph_residual)
    reset_query_dict(query_dict)
    start_time = time.perf_counter()
    print('Starting exploration')
    result, result_query_dict = backpropagation(graph, graph_aux, graph_residual, query_dict_keys,
                                                path_dict, query_dict, 0)
    end_time = time.perf_counter()
    count = 0
    for key in result_query_dict:
        if len(result_query_dict[key]) > 0:
            count += 1
    print('Backpropagation result: ' + str(result))
    print('Unique paths: ' + str(count))
    print(result_query_dict)
    print('Time taken: ' + str(end_time - start_time) + ' seconds')'''
