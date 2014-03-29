'''
Created on 11 Jun 2013

@author: Luke

major TODO: namespaces/modules/whatever they are in python

'''

#import pygame

from AudiosplodeUI import AudiosplodeUI
from Cell import EmptyCell,BlockageCell, Sink,Spawn
import math
#import mob as mobClass
import freqMob as mobclass
import sound
import random
from Tower import Tower
from pathfinding.algorithms import astar

class Audiosplode():

    def __init__(self, width=100, height=100):
        '''
        Create an audiosplode world
        '''


        self.width=width
        self.height=height

        
        self.cells =  [ [EmptyCell(x,y, self) for y in range(height)] for x in range(width)  ]
        
        #cell [0][0] has it's top left at the (0,0) pixel
        #the centre of this cell is (0.5,0.5)
        #this seems a little confusing, but I think it's overall less confusing than the alternative
        #Luke
        
         
        #self.mobs = [mobclass.mob([5,6])]
        self.mobs=[]
        
        #how many mobs escaped
        self.escaped=0
        
        self.money=50
        
        self.sound = sound.sound()

        self.pathdebug = []
        
        #wjere te amopbs are trying to get to
        self.sink=None
        #array of Spawn cells
        self.spawns=[]
        
        #are there are new towers so pathfindinw will have to be redone?
        self.newTowers=False
        
        #towers seperate to cells because updating all the cells was insanely slow
        self.towers=[]
        
        self.shots = []
        

        #print(self.cells)

    def draw(self,screen,cellSize,offsetX,offsetY):
        '''
        Purely graphical, this should not affect game state.
        '''
        #todo not render stuff that's not in view
        #and/or proper viewports?
        screen.fill((255,255,255))
        startX = int(math.floor(offsetX/cellSize))
        startY = int(math.floor(offsetY/cellSize))

        endX = int(startX + math.ceil(screen.get_width()/cellSize))+2
        endY = int(startY + math.ceil(screen.get_height()/cellSize))+2
        
        worldXToScreen = lambda x: x * cellSize - offsetX
        worldYToScreen = lambda y: y * cellSize - offsetY  

        for col in self.cells[startX:endX]:
            for cell in col[startY:endY]:
                #if cell.x<20 and cell.y<20:
                cell.draw(screen,worldXToScreen(cell.x),worldYToScreen(cell.y),cellSize)

        for mob in self.mobs:
            mob.draw(screen,offsetX,offsetY,cellSize)
            
        for shot in self.shots:
            shot.draw(screen, worldXToScreen(shot.x), worldYToScreen(shot.y), worldXToScreen(shot.endPos[0]), worldYToScreen(shot.endPos[1]))
    
    def getMoney(self):
        return self.money
    
    def spendMoney(self,amount):
        assert self.money>=amount
        self.money -= amount
    
    def getLives(self):
        #TODO life system
        return -self.escaped
    
    def availableTowers(self):
        '''
        return a list of towers which are avaiable to be built
        for use just with the UI atm, might be more useful for controlling which twoers the player can use later
        '''
        return [Tower]
    
    def update(self,dt):
        '''
        update game state for a period of dt seconds
        '''
        for mob in self.mobs:
            #mob.damage(5)
            #mob.move([1,0])
            if self.newTowers:
                #a new tower has been placed, give the mobs new paths!!
                mobX,mobY=mob.getCellPos()
                mob.update(dt,self.getPath(self.cells[mobX][mobY], self.sink))
            else:
                mob.update(dt)
        for mob in self.mobs[:]: # [:] creates a temporary copy
            if mob.isDead():
                self.mobs.remove(mob)
                self.sound.play(mob.getSoundValue())
                self.money=self.money + mob.getValue()
            if mob.hasEscaped():
                if not mob.isDead():
                    #only remove if it hasn't *just* been removed above.  can happen otherwise!
                    self.mobs.remove(mob)
                self.escaped = self.escaped + 1
        
        #mobs are spawned in waves and added to self.mobs              
        for spawn in self.spawns:
            spawn.update(dt,self.mobs)     
        
        # Update the shot draw list
        self.shots[:] = [shot for shot in self.shots if shot.drawTime > 0]
        for shot in self.shots:
            shot.drawTime -= dt
        
        """
        bit of a hack:
            mobs now get added in spawner, so they need a path.
            Can't do this from mobs as they don't have access
            to the pathfinder, so doing it here.
            But, don't want to update all mobs positions,
            so adding a newpath from their location to the sink,
            progressing their movement by 0.
        """
        for mob in self.mobs:
            mobX,mobY=mob.getCellPos()
            mob.update(0,self.getPath(self.cells[mobX][mobY], self.sink))
                
        for tower in self.towers:
            tower.update(dt,self.mobs)
        
        self.newTowers=False
        
        
#         for col in self.cells:
#             for cell in col:
#                 cell.update(dt,self.mobs)
    
    #also returns true or false for if successfully placed
    def addTower(self,x,y,towerType=None):
        #TODO check that there is a path between every source and the sink before allowing the tower.
        
        for mob in self.mobs:
            mobX,mobY = mob.getCellPos()
            if x == mobX and y == mobY:
                return False
         
        if towerType is None: #default tower
            towerToAdd = Tower(x,y,self)
        else:
            print "New towers are not implemented"
            quit()
                
        if self.getMoney() < towerToAdd.getCost():
            return False 
                
        #this is in the range of the board and also not ontop of a mob
        if x>=0 <self.width and y>=0 < self.height and self.cells[x][y].towerable():#
            
            #test if there are still paths from the sources to the sink
            
            #make it not walkable for purposes of this test
            self.cells[x][y].walkable=False
            
            path=True
            
            for spawn in self.spawns:
                if astar(spawn, self.sink) == None:
                    path=False
            
            
            #put cell back to normal
            self.cells[x][y].walkable=True
            
            if not path:
                #was no path for at least one of the spawns
                return False
            
            
            self.cells[x][y] = towerToAdd
            
            self.newTowers=True
            self.towers.append(self.cells[x][y])
            
            self.spendMoney(towerToAdd.getCost())
            
            return True
            
        return False
    
    #set the place th mobs want to go to
    def setSink(self,x,y):
        self.sink = Sink(x, y, self)
        self.cells[x][y]=self.sink
        
    def addSpawn(self,x,y):
        '''
        Any number of spawns may be added, but at least one is required for a valid map
        '''
        self.cells[x][y]=Spawn(x, y, self)
        self.spawns.append(self.cells[x][y])
    
    #does what ti says on teh ink
    #NOTE this does not include the fromCell
    def getPath(self,fromCell,toCell):
        return  [node.pos for node in astar(fromCell, toCell)]
    
if __name__ == '__main__':

    a = Audiosplode()

#     a.cells[3][4]=BlockageCell(3,4, a)
#     a.cells[4][4]=BlockageCell(4,4, a)
#     a.cells[5][4]=BlockageCell(5,4, a)
#     a.cells[6][4]=BlockageCell(6,4, a)
#     a.cells[2][4]=BlockageCell(2,4, a)
    
    a.setSink(20,20)
    
    a.addSpawn(5,5)
    a.addSpawn(50,5)

    ui = AudiosplodeUI(a,1024,768)

    pass
