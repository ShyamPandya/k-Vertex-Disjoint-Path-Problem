from utils import read_input_file, get_file_names, read_output_file
import sys

if __name__ == '__main__':
    inp_file, out_file = get_file_names(sys.argv[1:])
    graph, query_dict = read_input_file(inp_file)
    result_dict = read_output_file(out_file)
    print('First verification - Check if query pairs are present in result pairs')
    for key in query_dict:
        if key not in result_dict:
            print(str(key) + ' not present in result')
            sys.exit()
    print('Second verification - Check whether all nodes are disjoint and between 1 to 100')
    vertices = set()
    for key in result_dict:
        if key[0] < 1 or key[0] > 100 or key[1] < 1 or key[1] > 100:
            print(str(key) + ' key value error')
            sys.exit()
        for node in result_dict[key]:
            if node in vertices:
                print(str(key) + ' nodes not disjoint')
                sys.exit()
            vertices.add(node)
    print('Third verification - Check whether they are legit paths')
    for key in result_dict:
        path = result_dict[key]
        for i in range(0, len(path)-1):
            try:
                u = path[i]
                v = path[i+1]
                if v not in graph.adj[u]:
                    print(str(key) + ' not a valid path')
                    sys.exit()
            except:
                print('Exception')
    print('Done')