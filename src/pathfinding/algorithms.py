# -*- coding: utf-8 -*-
#py_algorithms.py
"""This module stores the implementations of the pathfinding algorithms"""
import heapq
__all__ = ['astar']

def astar(start_node, target_node):
    """The A* pathfinding algorithm"""
    closed = set()
    open_set = set()
    open = []
    # ensure start_node is terminating node in path reconstruction
    if hasattr(start_node, '_came_from'):
        del start_node._came_from
    
    h = start_node._h = start_node.heuristic(target_node)
    g = start_node._g = 0
    f = start_node._h # + start_node._g
    
    start_triplet = [f, h, start_node]
    heapq.heappush(open, start_triplet)
    open_d = {start_node: start_triplet}
    while open:
        f, h, node = heapq.heappop(open)
        del open_d[node]
        if node == target_node:
            return reconstruct_path(node)
        closed.add(node)
        for neighbor in node.get_neighbors():
            if neighbor in closed:
                continue
         
            tentative_g = node._g + node.move_cost(neighbor)
            if neighbor not in open_d:
                neighbor._came_from = node
                neighbor._g = tentative_g
                h = neighbor._h = neighbor.heuristic(target_node)
                d = open_d[neighbor] = [tentative_g + h, h, neighbor]
                heapq.heappush(open, d)
            else:
                neighbor = open_d[neighbor][2] # preserve identity, f/g/h
                if tentative_g < neighbor._g:
                    neighbor._came_from = node
                    neighbor._g = tentative_g
                    open_d[neighbor][0] = tentative_g + neighbor._h
                    heapq.heapify(open)
                
    
    return None # there is no path

def reconstruct_path(target_node):
    path = []
    node = target_node
    while hasattr(node, '_came_from'):
        path.append(node)
        node = node._came_from
    return reversed(path)
