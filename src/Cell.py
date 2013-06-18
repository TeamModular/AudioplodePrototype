'''
Created on 12 Jun 2013

@author: Luke
'''

from abc import abstractmethod, ABCMeta
import pathfinding.metrics  

#oject seems to be required for python 2.  I'm not asking why
class Cell(object):
    '''
    a base class for all cell things to extend
    '''
    __metaclass__ = ABCMeta

    def __init__(self, x, y, world, walkable=True, move_cost=1):
        '''
        Constructor
        
        Parameters:
            world -- hacky, but should be a reference to the Audiosplode instance allowing access to the
                     cell array though world.cells
        '''
        #this info probably not needed
        self.x=x
        self.y=y
        
        self.walkable = walkable                        # for pathfinding
        self.world = world                              # for pathfinding
        self._heuristic = pathfinding.metrics.manhattan # for pathfinding
        self._move_cost = move_cost                     # for pathfinding

    @property
    def pos(self):
        '''
        Needed for compatibility with python-pathfinding library.
        '''
        return (self.x, self.y)
    
    def __hash__(self):
        '''
        Needed for compatibility with the python-pathfinding library.
        '''
        return hash(self.pos)
    
    def __eq__(self, o):
        '''
        Needed for compatibility with the python-pathfinding library.
        '''
        return self.pos == o.pos

    def get_neighbors(self):
        """
        Needed for compatibility with the python-pathfinding library.
        
        Get all the traversable neighbor nodes
        use neighbor_gen to generate nodes given positions"""
        for i in ((1,0), (-1,0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)):
            x = self.x - i[0]
            y = self.y - i[1]
            if x < 0 or y < 0:
                continue
            
            neighbor = self.world.cells[x][y]
            if neighbor.walkable:
                yield neighbor

    def heuristic(self, node):
        """
        Needed for compatibility with the python-pathfinding library.
        
        Use the supplied heuristic to determine distance from `node`
        the heuristic may not always be used, depending on the pathfinding 
        algorithm used"""
        return self._heuristic(self.pos, node.pos)
    
    def move_cost(self, node):
        """
        Needed for compatibility with the python-pathfinding library.
        
        Find the cost for moving between self and `node`
        defaults to providing a constant cost, as provided on initialization"""
        return self._move_cost

    @abstractmethod
    def draw(self,screen,x,y,size):
        '''
        crude for now, draw centred about that x and y and with a cellSize of size on a pygame.screen
        '''
        
    @abstractmethod
    def update(self,dt):
        '''
        update over a time of dt seconds
        '''