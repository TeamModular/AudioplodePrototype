# -*- coding: utf-8 -*-
import unittest
from pathfinding import load_map
from StringIO import StringIO

class TestLoadMap(unittest.TestCase):
    def test_read_tiles(self):
        f = StringIO("ab\ncd")
        self.assertEquals(set(load_map.read_tiles(f)),
            set([((0, 0), 'c'), ((0, 1), 'a'), ((1, 0), 'd'), ((1, 1), 'b')]))

    def test_file_to_tile(self):
        f = StringIO(load_map.START + load_map.TARGET)
        start, end = load_map.file_to_tile(f)
        self.assertEquals(start.pos, (0,0))
        self.assertEquals(end.pos, (1, 0))

if __name__ == '__main__':
    unittest.main()