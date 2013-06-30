'''
Created on 12 Jun 2013

@author: Luke
'''

from abc import abstractmethod, ABCMeta
import pathfinding.metrics  
import pygame
from numpy import array as Vector, linalg

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
        
        self.posVector=Vector([x,y])
        
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

    def cell_in_range(self, x, y):
        return not (x < 0 or x >= len(self.world.cells) or y < 0 or y >= len(self.world.cells[0]))

    # Tuple structure:
    # (x, y, (additional cells that must be walkable for this cell to be walkable)
    _adjacents = ((1,0, ()), (-1,0, ()), (0, 1, ()), (0, -1, ()))
    _diagonals = ((1, 1, ((1, 0), (0, 1))), (-1, -1, ((-1, 0), (0, -1))), (1, -1, ((1, 0), (0, -1))), (-1, 1, ((-1, 0), (0, 1))))
    

    def get_neighbors(self):
        """
        Needed for compatibility with the python-pathfinding library.
        
        Get all the traversable neighbor nodes
        use neighbor_gen to generate nodes given positions"""

        for i in self._adjacents + self._diagonals:
            x = self.x - i[0]
            y = self.y - i[1]
            additional_cells = i[2]
            
            if not self.cell_in_range(x, y):
                continue
            
            neighbor = self.world.cells[x][y]
            if neighbor.walkable:
                walkable = True
                for additional_cell in additional_cells:
                    if not self.world.cells[self.x - additional_cell[0]][self.y - additional_cell[1]].walkable:
                        walkable = False
                        break
                
                if walkable:
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
    def towerable(self):
        '''
        Is it possible to place a tower to replace this cell?
        '''
#     @abstractmethod
#     def update(self,dt,mobs):
#         '''
#         update over a time of dt seconds
#         '''
        
        
class EmptyCell(Cell):
    '''
    classdocs
    '''

    def __init__(self, x, y, world, move_cost=1):
        super(EmptyCell,self).__init__(x,y, world, walkable=True, move_cost=move_cost)
        '''
        Constructor
        '''
        
#     def update(self, dt, mobs):
#         pass

    def draw(self, screen, x, y, size):
        #Cell.draw(self, screen, x, y, size)
        #black rectangle
        pass
        #pygame.draw.rect(screen, (0,0,0), pygame.Rect(x,y,size,size), 1)
        
    def towerable(self):
        return True
        
        
class BlockageCell(Cell):
    '''
    classdocs
    '''

    def __init__(self,x,y, world):
        super(BlockageCell,self).__init__(x,y, world, walkable=False, move_cost=1)
        '''
        Constructor
        '''
        
#     def update(self, dt, mobs):
#         pass
        
    def draw(self, screen, x, y, size):
        #Cell.draw(self, screen, x, y, size)
        #black rectangle
        pygame.draw.rect(screen, (128,128,64), pygame.Rect(x,y,size,size), 0)
        
    def towerable(self):
        return False
        
class Spawn(Cell):
    '''
    One of potnteianly many places that the little minions can spawn
    '''
    def __init__(self,x,y,world):
        super(Spawn,self).__init__(x,y,world,walkable=True,move_cost=1)
#         
#     def update(self, dt, mobs):
#         pass
    
    def draw(self, screen, x, y, size):
        #green square
        pygame.draw.rect(screen, (0,255,0), pygame.Rect(x,y,size,size), 0)
    
    def towerable(self):
        return False
        
class Sink(Cell):
    '''
    TODO think of ao better name than sink
    this is the place that all the mobses want to go ot
    if they make if there hte player loses points
    this is bad
    
    '''
    
    def __init__(self,x,y,world):
        super(Sink,self).__init__(x,y,world,walkable=True,move_cost=1)
        
#     def update(self, dt, mobs):
#         pass
#     
    def draw(self, screen, x, y, size):
        #green square
        pygame.draw.rect(screen, (255,128,0), pygame.Rect(x,y,size,size), 0)
        
    def towerable(self):
        return False