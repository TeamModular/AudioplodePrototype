'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame
from numpy import array as Vector, linalg

omniTowerBaseSprite = pygame.image.load("../art/omni-tower/omni-tower-base.png")
omniTowerTopSprite = pygame.image.load("../art/omni-tower/omni-tower-gun-top.png")

class Tower(Cell):
    '''
    base class for different types of tower
    '''


    def __init__(self,x,y, world):
        super(Tower,self).__init__(x,y, world, walkable=False)
        '''
        Constructor
        '''
        self.rotation = 0
        self.range=6
        self.range2 = self.range*self.range
        #damage per shot
        self.damage=40
        
        self.coolDownTime=3
        #temperature is incremented by coolDownTime every time this tower fires.  It decreases at a rate of 1 a second
        self.temperature=0
        
        #self.pos = Vector(x,y)
        
    def draw(self, screen, x, y, size):
        self.drawStatic(screen, x, y, size, rotation=self.rotation)
        
    @staticmethod
    def drawStatic(screen,x,y,size,rotation=0):
        '''
        TODO review if htis is the best way of doing this
        
        in order to ahve the ability to draw the tower for the UI as well as the game, a seperate static draw is required
        
        when/if specific stuff is required to be drawn, use argumetns with defaults?
        '''
        # calculate x scale and y scale change
        xScale = float(size) / float(omniTowerTopSprite.get_width())
        yScale = float(size) / float(omniTowerTopSprite.get_height())
        
        topRotated = pygame.transform.rotate(omniTowerTopSprite, rotation)
        topResized = pygame.transform.smoothscale(topRotated, (int(float(topRotated.get_width()) * xScale), int(float(topRotated.get_height()) * yScale)))
        
        baseResized = pygame.transform.smoothscale(omniTowerBaseSprite, (size, size))
        
        #widthDiff = topResized.get_width() - baseResized.get_width()
        #heightDiff = topResized.get_height() - baseResized.get_height()
        
        # find centre of tower
        xCentre = float(x) + (float(size) / 2.0)
        yCentre = float(y) + (float(size) / 2.0)
        
        screen.blit(baseResized, (x, y))
        
        screen.blit(topResized, (round(xCentre - float(topResized.get_width()) / 2.0), round(yCentre - float(topResized.get_height()) / 2.0)))
        
        #pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,size,size), 0)
    
    def towerable(self):
        return False
    
    def update(self, dt, mobs):
        
        self.temperature=self.temperature-dt
        self.rotation += dt * 40
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
            