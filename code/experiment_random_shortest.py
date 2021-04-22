from utils import read_input_file, get_file_names, view_graph
import networkx as nx
import random
import time
import sys
import os

untouchable_nodes = set()
vertices = set()

def next_pair_to_explore(query_dict):
    keys = list(query_dict.keys())
    random.shuffle(keys)
    for key in keys:
        if not query_dict[key]:
            return key
    return None

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


def path_count(graph):
    len_dict = {}
    paths_dict = {}
    for key in query_dict:
        source = key[0]
        destination = key[1]
        # Find mutually disjoint paths between a single source and sink
        paths = list(nx.all_simple_paths(graph, source, destination, cutoff=35))
        len_dict[key] = len(paths)
        paths_dict[key] = paths
    return list(dict(sorted(len_dict.items(), key=lambda item: item[1])).keys()), paths_dict


def find_path(graph, start, end, path=[]):
    path = path + [start]
    if start == end:
        return path
    if not graph.has_key(start):
        return None
    for node in graph[start]:
        if node not in path:
            newpath = find_path(graph, node, end, path)
            if newpath: return newpath
    return None


if __name__ == '__main__':
    inp_file, out_file = get_file_names(sys.argv[1:])
    for j in range(1000):
        print('Iteration ' + str(j))
        start_time = time.perf_counter()
        print('Starting time: ' + str(start_time))
        print(inp_file)
        graph, query_dict = read_input_file(inp_file)
        # print(nx.convert_matrix.to_numpy_matrix(graph))
        # view_graph(graph)
        # print(query_dict)
        # query_dict_keys, path_dict = path_count(graph)
        reset_query_dict(query_dict)

        key = next_pair_to_explore(query_dict)
        new_graph = graph.copy()
        i = 0
        while key and i < 20:
            source = key[0]
            destination = key[1]
            try:
                path = nx.shortest_path(new_graph, source, destination)
                if is_safe_to_add(path):
                    query_dict[key] = path
                    new_graph.remove_nodes_from(path)
            except nx.NetworkXNoPath:
                print('Couldnt find path between ' + str(source) + ' and ' + str(destination))
            key = next_pair_to_explore(query_dict)
            i += 1

        end_time = time.perf_counter()
        print('Ending time: ' + str(end_time))
        print('Time taken: ' + str(end_time - start_time) + ' seconds')
        count = 0
        for x in query_dict:
            if len(query_dict[x]) > 0:
                count += 1
        print('Unique paths: ' + str(count))
        print(query_dict)
        if not os.path.exists(out_file):
            with open(out_file, 'w') as file:
                for x in query_dict:
                    path = query_dict[x]
                    if len(path) > 0:
                        file.write(" ".join(repr(v) for v in path) + '\n')
                file.close()
        else:
            with open(out_file, 'r') as file:
                line_count = 0
                for line in file:
                    if line != "\n":
                        line_count += 1
                file.close()
            if count > line_count:
                with open(out_file, 'w') as file:
                    for x in query_dict:
                        path = query_dict[x]
                        if len(path) > 0:
                            file.write(" ".join(repr(v) for v in path) + '\n')
                    file.close()


    # count = 0
    # with open(out_file, 'w') as file:
    #     for key in result_query_dict:
    #         path = result_query_dict[key]
    #         if len(path) > 0:
    #             count += 1
    #             file.write(" ".join(repr(v) for v in path)+'\n')
    # file.close()
    # print('Backpropagation result: ' + str(result))
    # print('Unique paths: ' + str(count))