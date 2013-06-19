import pygame as p
import sound
import math

class mob:
    def __init__(self,position,path):
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
            self.path=newPath
        
        nextX,nextY = self.path[0]
        x,y = self.currentCell
        
        dx=(nextX-x)*self.speed
        dy=(nextY-y)*self.speed
        
        if not(x==nextX or y==nextY):
            #not travelling horizontally
            
            #this might be right. check tomorrow
            dx=dx/math.sqrt(2)
            dy=dy/math.sqrt(2)
        
        self._x+=dx*dt
        self._y+=dy*dt
        
        if math.floor(self._x) == nextX and math.floor(self._y)==nextY:
            #we are now on the next cell
            self.currentCell=self.path[0]
            self.path=self.path[1:]
            
            if len(self.path)==0:
                #reacehed the ened!!!
                self._dead=True
            
        
