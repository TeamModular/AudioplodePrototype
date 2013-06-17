# -*- coding: utf-8 -*-
import unittest
import os
from pathfinding import load_map, nodes, algorithms
from StringIO import StringIO

class TestPathfinding(unittest.TestCase):
    def verify_path(self, walkable, path):
        for node in path:
            self.assertTrue(walkable.get(node.pos, True))
    
    def test_astar_noop(self):
        node = nodes.RectNode((0, 0))
        self.assertEquals(len(list(algorithms.astar(node, node))), 0)
    
    def test_astar_path(self):
        """Test that paths are constructed exclusive of start, inclusive of end
        """
        start = nodes.RectNode((0, 0))
        end = nodes.RectNode((5, 0))
        self.assertEquals(list(algorithms.astar(start, end)),
            [nodes.RectNode((i, 0)) for i in xrange(1, 6)])

def test_map_success(mapname):
    def test_astar_success(self):
        try:
            f = open(mapname)
            start, end = load_map.file_to_tile(f)
            walkable = start.walkable
            path = algorithms.astar(start, end)
            self.verify_path(walkable, path)
        finally:
            f.close()
    test_astar_success.__name__ += '_' + os.path.basename(mapname)
    return test_astar_success

def test_map_failure(mapname):
    def test_astar_failure(self):
        try:
            f = open(mapname)
            start, end = load_map.file_to_tile(f)
            walkable = start.walkable
            self.assertEquals(algorithms.astar(start, end), None)
        finally:
            f.close()
    test_astar_failure.__name__ += '_' + os.path.basename(mapname)
    return test_astar_failure

_dir = os.path.join(os.path.dirname(__file__), 'valid_maps')
for mapname in os.listdir(_dir):
    if os.path.splitext(mapname)[1] == '.map':
        f = test_map_success(os.path.join(_dir, mapname))
        setattr(TestPathfinding, f.__name__, f)

_dir = os.path.join(os.path.dirname(__file__), 'invalid_maps')
for mapname in os.listdir(_dir):
    if os.path.splitext(mapname)[1] == '.map':
        f = test_map_failure(os.path.join(_dir, mapname))
        setattr(TestPathfinding, f.__name__, f)

del f
del _dir
del test_map_success
del test_map_failure
del mapname

if __name__ == '__main__':
    unittest.main()