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
        #damage per shot
        self.damage=40
        
        self.coolDownTime=3
        #temperature is incremented by coolDownTime every time this tower fires.  It decreases at a rate of 1 a second
        self.temperature=0
        
        #self.pos = Vector(x,y)
        
    def draw(self, screen, x, y, size):
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,size,size), 0)
    
    def towerable(self):
        return False
    
    def update(self, dt, mobs):
        
        self.temperature=self.temperature-dt
        
        if self.temperature<=0:
        #only actually check for mobs to shoot at if we can shoot
            for mob in mobs:
                mobPos = mob.getPos()
                if mobPos.distance_squared_to(self.posVector) < self.range2:
                    #mob inn range!!
                    #damage it
                    mob.damage(self.damage)
                    self.temperature=self.coolDownTime
                    return
            