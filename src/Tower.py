'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame
from numpy import array as Vector,linalg

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
        self.drawStatic(screen, x, y, size)
        
    @staticmethod
    def drawStatic(screen,x,y,size):
        '''
        TODO review if htis is the best way of doing this
        
        in order to ahve the ability to draw the tower for the UI as well as the game, a seperate static draw is required
        
        when/if specific stuff is required to be drawn, use argumetns with defaults?
        '''
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,size,size), 0)
    
    def towerable(self):
        return False
    
    def update(self, dt, mobs):
        
        self.temperature=self.temperature-dt
        
        if self.temperature<=0:
        #only actually check for mobs to shoot at if we can shoot
            for mob in mobs:
                mobPos = mob.getPos()
                #if mobPos.distance_squared_to(self.posVector) < self.range2:
                if linalg.norm(mobPos - self.posVector) < self.range:
                    #mob inn range!!
                    #damage it
                    mob.damage(self.damage)
                    self.temperature=self.coolDownTime
                    return
            