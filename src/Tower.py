'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame

class Tower(Cell):
    '''
    base class for different types of tower
    '''


    def __init__(self,x,y, world):
        super(Tower,self).__init__(x,y, world, walkable=False)
        '''
        Constructor
        '''
        
    def draw(self, screen, x, y, size):
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(x-size/2,y-size/2,size,size), 0)
    
    
    def update(self, dt, mobs):
        pass