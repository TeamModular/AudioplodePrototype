from astar_grid import AStarGrid, AStarGridNode
from itertools import product

def make_graph(mapinfo):
    nodes = [[AStarGridNode(x, y) for y in range(mapinfo.height)] for x in range(mapinfo.width)]
    graph = {}
    for x, y in product(range(mapinfo.width), range(mapinfo.height)):
        node = nodes[x][y]
        graph[node] = []
        for i, j in product([-1, 0, 1], [-1, 0, 1]):
            if not (0 <= x + i < mapinfo.width): continue
            if not (0 <= y + j < mapinfo.height): continue
            graph[nodes[x][y]].append(nodes[x+i][y+j])
    return graph, nodes

graph, nodes = make_graph({"width": 8, "height": 8})
paths = AStarGrid(graph)
start, end = nodes[1][1], nodes[5][7]
path = paths.search(start, end)
if path is None:
    print "No path found"
else:
    print "Path found:", path