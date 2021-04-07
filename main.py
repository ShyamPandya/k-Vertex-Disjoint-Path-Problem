from utils import create_graph, save_graph, view_graph, retrieve_graph

graph = create_graph(5, 0.5)
save_graph(graph, 'graph_store.txt')
view_graph(graph)
# Before reading make sure there aren't any empty lines in the file at the end or the library breaks
view_graph(retrieve_graph('graph_store.txt'))
