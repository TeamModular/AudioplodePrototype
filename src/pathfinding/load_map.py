# -*- coding: utf-8 -*-
"""load_map contains several shortcut functions to quickly load maps.
Custom map-loading routines will probably be desired, but load_map 
can be useful for testing new heuristics, pathfinding algorithms, etc."""
import nodes
import algorithms
import metrics

START = '0'
BLANK = ' '
WALL = '#'
TARGET = '@'

def read_tiles(f):
    """Read file `f` and yield (position, char) tuples"""
    # currently outputs in cartesian coordinates-- bad idea?
    lines = f.read().splitlines()
    for y, line in enumerate(reversed(lines)):
        for x, char in enumerate(line):
            yield (x, y), char

def file_to_tile(f, 
        start=START, blank=BLANK, wall=WALL, target=TARGET, 
        heuristic=metrics.manhattan):
    """Take an input file `f` and return RectNodes start_node, target_node
    (if a target is not found, start_node, None will be returned instead """
    walkable = {}
    start_pos = target_pos = None
    for pos, char in read_tiles(f):
        if char == wall:
            walkable[pos] = False
        elif char == target:
            target_pos = pos
        elif char == start:
            start_pos = pos
        elif char == blank:
            pass
        else:
            raise ValueError("Unknown tile type: '%s'" % char)
    if start_pos is None:
        raise ValueError("No starting position in map")
    start_node = nodes.RectNode(start_pos, 
        walkable=walkable, heuristic=heuristic)
    if target_pos is None:
        # target position is optional
        target_node = None
    else:
        target_node = nodes.RectNode(target_pos,
            walkable=walkable, heuristic=heuristic)
    return start_node, target_node
    
    