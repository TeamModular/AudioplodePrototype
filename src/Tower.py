'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame
from pygame.math import Vector2 as Vector

class Tower(Cell):
    '''
    base class for different types of tower
    '''


    def __init__(self,x,y, world):
        super(Tower,self).__init__(x,y, world, walkable=False)
        '''
        Constructor
        '''
        
        self.range=6
        self.range2 = self.range*self.range
        #damage per seconed
        self.dps=40
        
        #self.pos = Vector(x,y)
        
    def draw(self, screen, x, y, size):
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,size,size), 0)
    
    
    def update(self, dt, mobs):
        for mob in mobs:
            mobPos = mob.getPos()
            if mobPos.distance_squared_to(self.posVector) < self.range2:
                #mob inn range!!
                #damage it
                mob.damage(self.dps*dt)
            