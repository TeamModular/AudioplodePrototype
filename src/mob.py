import pygame as p
import sound
import math
from numpy import array,linalg

class mob:
    def __init__(self,position,path):
        
        
        #position, (0,0) is the top left of cell[0][0], centre of cell[0][0] is (0.5,0.5)
        self._x = position[0]
        self._y=position[1]
        self._colour=(255,0,255)
        self._size=(0.4,0.4)
        self._health=100
        self._dead=False
        self.speed=4
        #path to follow!  array of typles or lists, from mike's pathy stuff
        #it's a list of tuples
        self.path=path
        #current cell is first element of ara
        self.currentCell=self.path[0]
        #path is rest of the array
        self.path=self.path[1:]


    def draw(self,screen,offsetX,offsetY,cellSize):
        p.draw.rect(screen, self._colour, p.Rect((self._x-self._size[0]/2)*cellSize-offsetX,(self._y-self._size[1]/2)*cellSize - offsetY,self._size[0]*cellSize,self._size[1]*cellSize), 0)

    def move(self,relativePosition):
        self._x += relativePosition[0]
        self._y += relativePosition[1]

    def damage(self,amount):
        assert type(amount)==int
        self._health-=amount
        if self._health<0:
            self._dead=True
    
    def getCellPos(self):
        return (int(math.floor(self._x)),int(math.floor(self._y)))
    
    def getNextCellPos(self):
        return self.path[0]
    
    
    def isDead(self):
        return self._dead
    
    def update(self,dt,newPath=None):
        #find the path
        #move along the path
        
        if not newPath == None:
            #there is a new path!
            if len(newPath) > 1:
                self.path=newPath[1:]
            else:
                self.path=newPath
        
        nextX = self.path[0][0]+0.5
        nextY = self.path[0][1]+0.5
        
        #TODO look into built in or good libraries for vectors for python!
        
        pos=array([self._x,self._y])
        nextPos=array([nextX,nextY])
        
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
            
            if len(self.path)==0:
                #reacehed the ened!!!
                self._dead=True
            
        
