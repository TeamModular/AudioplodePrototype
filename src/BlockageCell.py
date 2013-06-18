'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame

class BlockageCell(Cell):
    '''
    classdocs
    '''

    def __init__(self,x,y, world):
        super(BlockageCell,self).__init__(x,y, world, walkable=False, move_cost=1)
        '''
        Constructor
        '''
        
    def update(self, dt):
        pass
        
    def draw(self, screen, x, y, size):
        #Cell.draw(self, screen, x, y, size)
        #black rectangle
        pygame.draw.rect(screen, (128,128,64), pygame.Rect(x-size/2,y-size/2,size,size), 0)
