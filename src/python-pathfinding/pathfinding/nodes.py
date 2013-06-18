# -*- coding: utf-8 -*-
#nodes.py
import algorithms
import metrics
import itertools

class RectNode(object):
    __slots__ = ('walkable', 'neighbor_gen', '_move_cost', 'pos', 
        'default_walkable', '_heuristic',
        '_came_from', '_h', '_g') # set by algorithms.astar
    def __init__(self, pos, 
            move_cost=1, walkable=None, default_walkable=True, 
            neighbor_gen=None, heuristic=metrics.manhattan):
        """Create a RectNode 
        with position `pos` and that generates neighbors by calling 
        `neighbor_gen` with similar arguments
        `move_cost` is a constant cost for moving directly from one node to 
            the next
        `walkable` is a map from position->walkable for any tile position
            if a position is not in `walkable`, it is assumed 
            `default_walkable` (default_walkable is True by default)"""
        if walkable is None:
            walkable = {}
        self.walkable = walkable
        if neighbor_gen is None:
            neighbor_gen = type(self)
        self.neighbor_gen = neighbor_gen
        self._move_cost = move_cost
        self.pos = pos
        self.default_walkable = default_walkable
        self._heuristic = heuristic
    
    def __hash__(self):
        return hash(self.pos)
    
    def __eq__(self, o):
        return self.pos == o.pos
    
    def _get_x(self):
        return self.pos[0]
    
    def _get_y(self):
        return self.pos[1]
    
    x = property(fget=_get_x)
    y = property(fget=_get_y)
    
    def get_neighbors(self):
        """Get all the traversable neighbor nodes
        use neighbor_gen to generate nodes given positions"""
        for i in ((1,0), (-1,0), (0, 1), (0, -1)):
            pos = self.x - i[0], self.y - i[1]
            if self.walkable.get(pos, self.default_walkable):
                yield self.neighbor_gen(pos, walkable=self.walkable, 
                        default_walkable=self.default_walkable, 
                        neighbor_gen=self.neighbor_gen,
                        heuristic=self._heuristic)
    
    def heuristic(self, node):
        """Use the supplied heuristic to determine distance from `node`
        the heuristic may not always be used, depending on the pathfinding 
        algorithm used"""
        return self._heuristic(self.pos, node.pos)
    
    def move_cost(self, node):
        """Find the cost for moving between self and `node`
        defaults to providing a constant cost, as provided on initialization"""
        return self._move_cost
