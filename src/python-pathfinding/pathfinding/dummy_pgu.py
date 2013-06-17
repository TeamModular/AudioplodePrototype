# -*- coding: utf-8 -*-
#dummy_pgu.py
import nodes
from collections import defaultdict
import algorithms

try: 
    from functools import partial
except ImportError:
    from _compat import partial

__all__ = ['astar', 'LayerWrapper', 'layer_unwrapper']

class LayerWrapper(object):
    """Wrap a PGU-style layer into a pathfinding-style dict-like"""
    def __init__(self, layer):
        """wrap `layer`"""
        self.layer = layer
    
    def get(self, pos, default=None):
        """get cartesian coordinate `pos`. Allow layer to raise an exception
        if `pos` does not exist, to emulate the PGU API"""
        x, y = pos
        return not self.layer[y][x]
        # yes, the above raises IndexError
        # see: http://code.google.com/p/pgu/issues/detail?id=4

def layer_unwrapper(walkable):
    layer = defaultdict(partial(defaultdict, int))
    for (x, y), floor in walkable.iteritems():
        layer[y][x] = not floor
    return layer

def astar(start, end, layer, dist):
    """pathfinding-based replacement for pgu.algo.astar
    `start`, `end`, `layer`, and `dist` are used as they are with pgu.algo"""
    walkable = LayerWrapper(layer)
    start_node = nodes.RectNode(start, walkable=walkable,
        heuristic=dist)
    end_node = nodes.RectNode(end, walkable=walkable,
        heuristic=dist)
    return [node.pos for node in 
        algorithms.astar(start_node, end_node)]