# -*- coding: utf-8 -*-
import unittest
from pathfinding import metrics
try:
    from itertools import product, permutations
except ImportError:
    from pathfinding import _compat 
    product, permutations = _compat.product, _compat.permutations


coord_range = range(-2, 3)
coords = list(product(coord_range, repeat=2))
coord_pairs = []
coord_triplets = list(permutations(coords, 3))
equal_coords = []
differing_coords = []

for a, b in permutations(coords, 2):
    coord_pairs.append((a, b))
    if a == b:
        equal_coords.append((a, b))
    else:
        differing_coords.append((a, b))

class TestAbstractPremetric(unittest.TestCase):
    __test__ = False
    def setUp(self):
        self.coord_range = coord_range
        self.coords = coords
        self.coord_pairs = coord_pairs
        self.equal_coords = equal_coords
        self.differing_coords = differing_coords
        self.coord_triplets = coord_triplets
    
    def test_dimension(self):
        """Ensure that vectors from different vector spaces cannot be
        compared"""
        self.assertRaises(ValueError, self.metric, (0, 1), (0, 1, 2))
    
    def test_nonnegativity(self):
        """Test non-negativity
            non-negativity: d(x, y) >=0 for all x, y"""
        for a, b in self.coord_pairs:
            self.assertTrue(self.metric(a, b) >= 0)
    
    def test_identity_of_indiscernables(self):
        """Test identity of indiscernables only to the extent required
        as a premetric
            identity of indiscernables: d(x, y) == 0 iff x==y
            only relevant portion: if x == y, d(x, y) == 0
                (converse excluded from test)"""
        for a, b in self.equal_coords:
            self.assertEqual(self.metric(a, b), 0)

class TestAbstractSemimetric(TestAbstractPremetric):
    __test__ = False
    
    def test_identity_of_indiscernables(self):
        """Test identity of indiscernables
            identity of indiscernables: d(x, y) == 0 iff x==y"""
        for a, b in self.differing_coords:
            self.assertNotEqual(self.metric(a, b), 0)
    
    def test_symmetry(self):
        """Test symmetry
            symmetry: d(x, y) == d(y, x) for all x, y"""
        for a, b in self.coord_pairs:
            self.assertEqual(self.metric(a, b), self.metric(b, a))

class TestAbstractMetric(TestAbstractSemimetric):
    __test__ = False
    
    def test_subadditivity(self):
        """Test subadditivity, also known as the triangle inequality
            d(x, y) <= d(x, z) + d(z, y)"""
        for a, b, c in self.coord_triplets:
            lhs = self.metric(a, c)
            p1, p2 = self.metric(a, b), self.metric(b, c)
            rhs = p1+p2 + 1e-10*lhs # adds an epsilon (a-b <= e === a <= b+e)
            self.assertTrue(lhs <= rhs,
                "%(func)s(%(a)s, %(c)s) == %(lhs)s is not "
                "<= %(rhs)s == %(p1)s + %(p2)s == %(func)s(%(a)s, %(b)s) + %(func)s(%(b)s, %(c)s)"
                % {
                    'func': self.metric.__name__, 
                    'a': a, 
                    'b': b, 
                    'c': c, 
                    'lhs': lhs, 
                    'rhs': rhs,
                    'p1': p1, 
                    'p2': p2
                })

class TestZeroPremetric(TestAbstractPremetric):
    __test__ = True
    def setUp(self):
        super(TestZeroPremetric, self).setUp()
        self.metric = metrics.zero
    
    def test_values(self):
        """Test a few key values of the zero premetric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 0)
        self.assertEquals(self.metric((0, 0), (1, 1)), 0)
        self.assertEquals(self.metric((0, 0), (-1, -1)), 0)

class TestEuclideanSquaredSemimetric(TestAbstractSemimetric):
    __test__ = True
    def setUp(self):
        super(TestEuclideanSquaredSemimetric, self).setUp()
        self.metric = metrics.euclidean_squared
    
    def test_values(self):
        """Test a few key values of the Chebyshev metric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 1)), 2)
        self.assertEquals(self.metric((0, 0), (3, 4)), 25)

class TestChebyshevMetric(TestAbstractMetric):
    __test__ = True
    def setUp(self):
        super(TestChebyshevMetric, self).setUp()
        self.metric = metrics.chebyshev
    
    def test_values(self):
        """Test a few key values of the Chebyshev metric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 2)), 2)

class TestManhattanMetric(TestAbstractMetric):
    __test__ = True
    def setUp(self):
        super(TestManhattanMetric, self).setUp()
        self.metric = metrics.manhattan
    
    def test_values(self):
        """Test a few key values of the manhattan metric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 1)), 2)
        self.assertEquals(self.metric((0, 0), (1, 2)), 3)

class TestEuclideanMetric(TestAbstractMetric):
    __test__ = True
    def setUp(self):
        super(TestEuclideanMetric, self).setUp()
        self.metric = metrics.euclidean
    
    def test_values(self):
        """Test a few key values of the euclidean metric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 1)
        self.assertEquals(self.metric((0, 0), (3, 4)), 5)

class TestDiscreteMetric(TestAbstractMetric):
    __test__ = True
    def setUp(self):
        super(TestDiscreteMetric, self).setUp()
        self.metric = metrics.discrete
    
    def test_values(self):
        """Test a few key values of the discrete metric"""
        self.assertEquals(self.metric((0, 0), (0, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 1)), 1)
        self.assertEquals(self.metric((0, 0), (1, 2)), 1)

if __name__ == '__main__':
    unittest.main()