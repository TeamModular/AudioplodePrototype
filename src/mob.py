import pygame as p
import sound
import math
from numpy import array,linalg
from pygame.math import Vector2 as Vector

class mob:
    def __init__(self,position,path):
        
        
        #position, (0,0) is the top left of cell[0][0], centre of cell[0][0] is (0.5,0.5)
        self._x = position[0]
        self._y=position[1]
        self._colour=(255,0,255)
        self._size=(0.4,0.4)
        self._health=100
        self._dead=False
        #did we make it to the sink?
        self._escaped=False
        self.speed=4
        #path to follow!  array of typles or lists, from mike's pathy stuff
        #it's a list of tuples
        self.path=path
        #current cell is not the first element of the array
        self.currentCell=self.getCellPos()
        #path is rest of the array
        self.path=self.path
        #how much money does the player get for killing this
        #TODO random bonus for some mobs?
        self._value=1


    def draw(self,screen,offsetX,offsetY,cellSize):
        
        size = [max(math.ceil(self._size[0]*cellSize),1),max(math.ceil(self._size[1]*cellSize),1)]
        
        p.draw.rect(screen, self._colour, p.Rect(self._x*cellSize-size[0]/2-offsetX,self._y*cellSize-size[1]/2 - offsetY,size[0],size[1]), 0)

    def move(self,relativePosition):
        self._x += relativePosition[0]
        self._y += relativePosition[1]

    def damage(self,amount):
        #assert type(amount)==int
        #TODO ask rich why damage must be int
        self._health-=amount
        if self._health<0:
            self._dead=True
    
    def getCellPos(self):
        return (int(math.floor(self._x)),int(math.floor(self._y)))
    
    def getNextCellPos(self):
        return self.path[0]
    
    def getPos(self):
        return Vector(self._x,self._y)
    
    def isDead(self):
        return self._dead
    
    def getValue(self):
        return self._value
    
    def hasEscaped(self):
        return self._escaped
    
    def update(self,dt,newPath=None):
        #find the path
        #move along the path
        
        if not newPath == None:
            #there is a new path!
            if len(newPath) > 0:
                self.path=newPath
            else:
                #in the case that we are *on* the final cell, but haven't reached its centre yet, this case will apply
                self.path=[self.getCellPos()]
        
        nextX = self.path[0][0]+0.5
        nextY = self.path[0][1]+0.5
        
        #TODO look into built in or good libraries for vectors for python!
        
        pos=array([float(self._x),float(self._y)])
        #copy
        #oldPos=pos[:]
        nextPos=array([float(nextX),float(nextY)])
        
        #vector for the direction we want to head in
        dir = nextPos - pos
        #get unit vector for this
        dir = dir/linalg.norm(dir)
        
        #update the position
        pos = pos + dir*self.speed*dt
        
        self._x,self._y = pos
#         self._x+=dir[0]*self.speed*dt
#         self._y+=dir[1]*self.speed*dt
        
        #work out how close we are to the centre of the next cell
        
        
        if linalg.norm(pos - nextPos) < self.speed*dt:
            #we are now on the next cell
            self.currentCell=self.path[0]
            self.path=self.path[1:]
#             self._x = nextX
#             self._y = nextY
            
            if len(self.path)==0:
                #reacehed the ened!!!
                self._escaped=True
            
        
