# -*- coding: utf-8 -*-
import unittest
import test_load_map
import test_pathfinding
import test_metrics
#import test_nodes
import pathfinding

__all__ = ['test_load_map', 'test_pathfinding', 'test_metrics', #'test_nodes',
    'main']

class ConcreteTestLoader(unittest.TestLoader):
    def loadTestsFromTestCase(self, testCaseClass):
        name = testCaseClass.__name__
        if 'abstract' in name.lower():
            return self.suiteClass()
        else:
            return super(ConcreteTestLoader, 
                self).loadTestsFromTestCase(testCaseClass)

test_loader = ConcreteTestLoader()
test_modules = [test_load_map, test_pathfinding, test_metrics,
    #test_nodes]
    ]
subsuites = [test_loader.loadTestsFromModule(mod) for mod in test_modules]
suite = unittest.TestSuite()
suite.addTests(subsuites)


TestRunner = unittest.TextTestRunner
def main(*args, **kwargs):
    TestRunner(*args, **kwargs).run(suite)
