# -*- coding: utf-8 -*-
#py_metrics.py
"""This module stores the python implementations of several metrics, premetrics,
and semimetrics, which may be used as heuristics

A premetric is defined as a function d(a, b) with a and b in some vector space,
with the following properties:
    1.: d(a, b)>=0 for all a, b (non-negativity)
    2.: d(a, a)=0 for all a

A semimetric strengthens condition 2., and adds a third condition:
    1.: d(a, b)>=0 for all a, b (non-negativity)
    2.: d(a, b)=0 if and only if a=b, for all a, b (identity of indiscernibles)
    3.: d(a, b)=d(b, a) for all a, b (symmetry)

a metric is the most strictly defined such function, adding a fourth condition:
    1.: d(a, b)>=0 for all a, b (non-negativity)
    2.: d(a, b)=0 if and only if a=b, for all a, b (identity of indiscernibles)
    3.: d(a, b)=d(b, a) for all a, b (symmetry)
    4.: d(a, c)<=d(a, b)+d(b, c) for all a, b, c (triangle inequality)"""
import math
try:
    from functools import wraps
except ImportError:
    from _compat import wraps

__all__ = ['chebyshev', 'manhattan', 'euclidean_squared', 'euclidean', 
    'discrete', 'zero']

def on_vector_space(f):
    @wraps(f)
    def g(pos1, pos2):
        if len(pos1) != len(pos2):
            raise ValueError("The arguments are not in the same vector space "
                "(they are in %s- and %s-dimensional spacse respectively)" %
                (len(pos1), len(pos2)))
        return f(pos1, pos2)
    return g

@on_vector_space
def chebyshev(pos1, pos2):
    """Find the Chebyshev distance from pos1 to pos2
    where pos1 and pos2 are n-dimensional vectors
    this is the greatest of all differences along the coordinate dimensions"""
    return max(abs(a-b) for a, b in zip(pos1, pos2))

@on_vector_space
def manhattan(pos1, pos2):
    """Find the manhattan (taxicab, L[1]) distance from pos1 to pos2
    where pos1 and pos2 are n-dimensional vectors
    this is the sum of all differences along the coordinate dimensions"""
    return sum(abs(a - b) for a, b in zip(pos1, pos2))

@on_vector_space
def euclidean_squared(pos1, pos2):
    """Find the euclidean distance, squared, from pos1 to pos2
    where pos1 and pos2 are n-dimensional vectors
    euclidean_squared is a semimetric, but not a metric as it violates
    the triangle inequality
    it is not generally suitable as a heuristic, but is included 
    for completeness"""
    return sum((a - b)**2 for a, b in zip(pos1, pos2))

def euclidean(pos1, pos2):
    """Find the euclidean distance between pos1 and pos2
    where pos1 and pos2 are n-dimensional vectors"""
    return math.sqrt(euclidean_squared(pos1, pos2))

@on_vector_space
def discrete(pos1, pos2):
    """0 when pos1 is equal to pos2, 1 in all other cases"""
    return (not pos1 == pos2)

@on_vector_space
def zero(pos1, pos2):
    """constant-function d(a, b) = 0
    because of this, it is only a premetric. However, it is useful in that
    it transforms A* into Dijkstra's Algorithm"""
    return 0