from utils import read_input_file, get_file_names, view_graph
import networkx as nx
import time
import sys

untouchable_nodes = set()
vertices = set()


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
        paths = list(nx.all_simple_paths(graph, source, destination,cutoff=35))
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
    start_time = time.perf_counter()
    print('Starting time: ' + str(start_time))
    inp_file, out_file = get_file_names(sys.argv[1:])
    print(inp_file)
    graph, query_dict = read_input_file(inp_file)
    # print(nx.convert_matrix.to_numpy_matrix(graph))
    # view_graph(graph)
    # print(query_dict)
    # query_dict_keys, path_dict = path_count(graph)
    reset_query_dict(query_dict)
    
    for key in query_dict:
        source = key[0]
        destination = key[1]
        H = graph.copy()
        for keys in query_dict:
            if keys != key:
                # print("true")
                try:
                    H.remove_node(keys[0])
                except:
                    pass
                try:
                    H.remove_node(keys[1])
                except:
                    pass
        try:
            path = nx.shortest_path(H,source, destination)
        except nx.NetworkXNoPath:
            continue
        print(path)
        for x in path:
            graph.remove_node(x)
        
        
    print('Starting exploration ')
    




    end_time = time.perf_counter()
    print('Ending time: ' + str(end_time))
    print('Time taken: ' + str(end_time - start_time) + ' seconds')
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
