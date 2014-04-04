'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell
import pygame
from numpy import array as Vector, linalg

class Shot(object):
    def __init__(self, x, y, endPos, drawTime):
        self.x = x
        self.y = y
        self.endPos = endPos
        self.drawTime = drawTime
        
    def draw(self, screen, x, y, endX, endY):
        pygame.draw.line(screen, (255, 0, 0), (x, y), (endX, endY))

class Tower(Cell):
    '''
    base class for different types of tower
    '''


    def __init__(self,x,y, world):
        super(Tower,self).__init__(x,y, world, walkable=False)
        '''
        Constructor
        '''
        
        self._cost=10
        
        self.range=6.0
        self.range2 = self.range*self.range
        #damage per shot
        self.damage=40
        
        self.coolDownTime=3.0
        #temperature is incremented by coolDownTime every time this tower fires.  It decreases at a rate of 1 a second
        self.temperature=0.0
        
        #self.pos = Vector(x,y)
        
        # Time to keep drawing each shot on screen
        self.shotDrawTime = 0.1
        self.shotDrawList = []
        
    def draw(self, screen, x, y, size):        
        self.drawStatic(screen, x, y, size, self.temperature)
        
    @staticmethod
    def drawStatic(screen,x,y,size, temperature=0.0):
        '''
        TODO review if htis is the best way of doing this
        
        in order to ahve the ability to draw the tower for the UI as well as the game, a seperate static draw is required
        
        when/if specific stuff is required to be drawn, use argumetns with defaults?
        '''
        # We want a blue rectangle of width and height size, with an inner rectangle
        # indicating the temperature of the tower
        pygame.draw.rect(screen, (0,0,255), pygame.Rect(x,y,size,size), 0)
        
        # Calculate inner rectangle size. We want it to be maximum size tempRectMaxSize
        # when temperature is => 3 and 0 when temperature is zero.
        tempRectMaxSize = size
        tempRectSize = int(round(tempRectMaxSize * (temperature / 3.0)))
        
        # Size must be odd
        if not tempRectSize % 2:
            tempRectSize += 1
        
        # Only bother drawing if our size is bigger than one pixel.
        if tempRectSize >= 1:
            diff = round((size - tempRectSize) / 2.0)
            pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(round(x + diff), round(y + diff), tempRectSize, tempRectSize))
    
    def towerable(self):
        return False
    
    def getCost(self):
        return self._cost
    
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
                    self.world.shots.append(Shot(self.x + 0.5, self.y + 0.5, (mobPos[0], mobPos[1]), self.shotDrawTime))
                    self.temperature = self.coolDownTime
                    return

class SlowTower(Tower):
    def __init__(self,x,y,world):

        Tower.__init__(self,x,y,world)
   
        self._cost=15
        
        self.range=3.0
        self.range2 = self.range*self.range
        #damage per shot is being hijacked to be 'slow amount'
        self.damage=0.5
     
        
    def update(self,dt,mobs):
        self.temperature=self.temperature-dt
        
        if self.temperature<=0:
        #only actually check for mobs to shoot at if we can shoot
            for mob in mobs:
                mobPos = mob.getPos()
                #if mobPos.distance_squared_to(self.posVector) < self.range2:
                if linalg.norm(mobPos - self.posVector) < self.range:
                    #mob in range
                    #slow it down
                    mob.slow(self.damage)
                    self.world.shots.append(Shot(self.x + 0.5, self.y + 0.5, (mobPos[0], mobPos[1]), self.shotDrawTime))
                    self.temperature = self.coolDownTime
                    return
        
