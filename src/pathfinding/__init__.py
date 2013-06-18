# -*- coding: utf-8 -*-
"""A simple pathfinding package.
"""
import algorithms
import metrics
import nodes
import load_map
_exp = []
try:
    import dummy_pgu
except ImportError:
    pass
else:
    _exp.append('dummy_pgu')

try:
    from pathfinding import test
except ImportError:
    pass
else:
    _exp.append('test')

__all__ = ['algorithms', 'metrics', 'nodes', 'load_map', 'dummy_pgu', 
    'dummy_dijkstar'] + _exp
