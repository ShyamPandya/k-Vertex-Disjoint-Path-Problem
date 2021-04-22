from utils import read_input_file, get_file_names, view_graph
import random
import time
import sys

untouchable_nodes = set()
vertices = set()
max_val = 0


def reset_query_dict(query_dict):
    for key in query_dict:
        # Create disjoint vertices set based on input pair
        vertices.add(key[0])
        vertices.add(key[1])
    untouchable_nodes.clear()


def next_pair_to_explore(query_dict):
    keys = list(query_dict.keys())
    random.shuffle(keys)
    for key in keys:
        if not query_dict[key]:
            return key
    return None


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


def recursion(graph, u, d, path, final_paths, vertices):
    if len(final_paths) == 10:
        return final_paths, True
    vertices.add(u)
    path.append(u)
    if u == d:
        final_paths.append(list(path))
    else:
        adj = list(graph.adj[u])
        random.shuffle(adj)
        for i in adj:
            if i not in vertices:
                ret_final_paths, res = recursion(graph, i, d, path, final_paths, vertices)
                if res:
                    return ret_final_paths, res
    path.pop()
    vertices.remove(u)
    return final_paths, False

def find_limited_paths(graph, query_dict):
    paths_dict = {}
    for key in query_dict:
        s = key[0]
        d = key[1]
        print(key)
        final_paths, res = recursion(graph, s, d, [], [], set())
        print('Found all paths ' + str(res))
        paths_dict[key] = final_paths
    return paths_dict


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


def backpropagation(graph, path_dict, query_dict, out_file):
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
    pair = next_pair_to_explore(query_dict)
    if not pair:
        return True
    paths = path_dict[pair]
    path_select_keys, in_degree_map = path_sorter(graph, paths)
    for i in range(len(path_select_keys)):
        possible_paths = in_degree_map[path_select_keys[i]]
        for j in range(len(possible_paths)):
            path = paths[possible_paths[j]]
            if is_safe_to_add(path):
                add_to_nodes_used(path)
                query_dict[pair] = path
                res, temp_query_dict = backpropagation(graph, path_dict, query_dict, out_file)
                if res:
                    return True, temp_query_dict
                remove_from_nodes_used(path)
                query_dict[pair] = []
    return False, query_dict
if __name__ == '__main__':
    start_time = time.perf_counter()
    print('Starting time: ' + str(start_time))
    inp_file, out_file = get_file_names(sys.argv[1:])
    graph, query_dict = read_input_file(inp_file)
    paths_dict = find_limited_paths(graph, query_dict)
    reset_query_dict(query_dict)
    print('Started exploration')
    result, result_query_dict = backpropagation(graph, paths_dict, query_dict, out_file)
