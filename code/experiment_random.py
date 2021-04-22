from utils import read_input_file, get_file_names, view_graph
import networkx as nx
import random
import time
import sys
import os

vertices = set()


def reset_query_dict(query_dict):
    for key in query_dict:
        # Create disjoint vertices set based on input pair
        vertices.add(key[0])
        vertices.add(key[1])


def get_destinations(query_dict):
    dests = []
    for key in query_dict:
        dests.append(key[1])
    return dests


def next_pair_to_explore(query_dict):
    keys = list(query_dict.keys())
    random.shuffle(keys)
    for key in keys:
        if not query_dict[key]:
            return key
    return None


def find_path_dfs(graph, u, d, p, visited):
    visited[u] = True
    p.append(u)
    if u == d:
        return p
    adj_list = list(graph.adj[u])
    random.shuffle(adj_list)
    for n in adj_list:
        if not visited[n] and (n == d or n not in vertices):
            rec_path = find_path_dfs(graph, n, d, p, visited)
            if rec_path:
                return rec_path
    p.pop()
    return None

def find_path_bfs(graph, u, d):
    from_dict = {}
    for i in range(1, 101):
        from_dict[i] = None
    # Jugaad
    from_dict[u] = 101
    queue = []
    queue.append(u)
    found = False
    while queue:
        cur = queue.pop(0)
        if cur == d:
            found = True
            break
        adj_list = list(graph.adj[cur])
        random.shuffle(adj_list)
        for n in adj_list:
            if from_dict[n] == None and (n == d or n not in vertices):
                from_dict[n] = cur
                queue.append(n)
    if not found:
        return None
    path = []
    cur = d
    while cur != None and cur != 101:
        path.insert(0, cur)
        cur = from_dict[cur]
    return path


if __name__ == '__main__':
    inp_file, out_file = get_file_names(sys.argv[1:])
    for j in range(100):
        print('Iteration ' + str(j))
        start_time = time.perf_counter()
        print('Starting time: ' + str(start_time))
        graph, query_dict = read_input_file(inp_file)
        reset_query_dict(query_dict)
        key = next_pair_to_explore(query_dict)
        new_graph = graph.copy()
        i = 0
        while key and i < 10000:
            source = key[0]
            destination = key[1]
            edge_dict = {}
            final_destinations = []
            for node in vertices:
                if node == destination or node == source:
                    continue
                final_destinations.append(node)
                edge_dict[node] = []
                edge_dict[node].extend(list(new_graph.in_edges(node)))
                edge_dict[node].extend(list(new_graph.out_edges(node)))
            new_graph.remove_nodes_from(final_destinations)
            try:
                #path = nx.shortest_path(new_graph, source, destination)
                #path = find_path_bfs(new_graph, source, destination)
                path = find_path_dfs(new_graph, source, destination, [], [False] * 101)
                if path:
                    query_dict[key] = path
                    new_graph.remove_nodes_from(path)
                    vertices.remove(source)
                    vertices.remove(destination)
            except nx.NetworkXNoPath as e:
                print('Couldnt find path between ' + str(source) + ' and ' + str(destination))
            finally:
                new_graph.add_nodes_from(final_destinations)
                for node in edge_dict:
                    new_graph.add_edges_from(edge_dict[node])
            '''try:
                path = None
                #path = find_path_bfs(new_graph, source, destination)
                #path = find_path_dfs(new_graph, source, destination, [], [False]*101)
                if path:
                    query_dict[key] = path
                    new_graph.remove_nodes_from(path)
            except nx.NetworkXNoPath:
                print('Couldnt find path between ' + str(source) + ' and ' + str(destination))'''
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
