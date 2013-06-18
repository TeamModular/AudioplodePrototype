'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame

class EmptyCell(Cell):
    '''
    classdocs
    '''

    def __init__(self, x, y, world, move_cost=1):
        super(EmptyCell,self).__init__(x,y, world, walkable=True, move_cost=move_cost)
        '''
        Constructor
        '''
        
    def update(self, dt):
        pass

    def draw(self, screen, x, y, size):
        #Cell.draw(self, screen, x, y, size)
        #black rectangle
        pygame.draw.rect(screen, (0,0,0), pygame.Rect(x-size/2,y-size/2,size,size), 1)
