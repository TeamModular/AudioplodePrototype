'''
Created on 11 Jun 2013

@author: Luke

major TODO: namespaces/modules/whatever they are in python

'''

#import pygame

from AudiosplodeUI import AudiosplodeUI
from Cell import EmptyCell,BlockageCell
import math
import mob as mobclass
import sound
import random
from Tower import Tower

class Audiosplode():

    def __init__(self, width=500, height=500):
        '''
        Create an audiosplode world
        '''

        self.width=width
        self.height=height

        
        self.cells =  [ [EmptyCell(x,y, self) for y in range(height)] for x in range(width)  ]
         
        self.mobs = [mobclass.mob([5,6])]

        self.sound = sound.sound()

        self.pathdebug = []

        #print(self.cells)

    def draw(self,screen,cellSize,offsetX,offsetY):
        '''
        Purely graphical, this should not affect game state.
        '''
        #todo not render stuff that's not in view
        #and/or proper viewports?

        startX = int(math.floor(offsetX/cellSize))
        startY = int(math.floor(offsetY/cellSize))

        endX = int(startX + math.ceil(screen.get_width()/cellSize))+1
        endY = int(startY + math.ceil(screen.get_height()/cellSize))+1

        for col in self.cells[startX:endX]:
            for cell in col[startY:endY]:
                #if cell.x<20 and cell.y<20:
                cell.draw(screen,(cell.x)*cellSize-offsetX,(cell.y)*cellSize-offsetY,cellSize)

        for mob in self.mobs:
            mob.draw(screen,offsetX,offsetY,cellSize)
            
        # hacky addition to debug and demonstrate astar algorithm (you can remove if needs be)
        import pygame as p
        for x, y in self.pathdebug:
            p.draw.rect(screen, (255,0,0), p.Rect((x-0.4/2)*cellSize-offsetX,(y-0.4/2)*cellSize - offsetY,0.4*cellSize,0.4*cellSize), 0)
        

    def update(self,dt):
        '''
        update game state for a period of dt seconds
        '''
        for mob in self.mobs:
            mob.damage(5)
            mob.move([1,0])
        for mob in self.mobs[:]: # [:] creates a temporary copy
            if mob.isDead():
                self.mobs.remove(mob)
                self.sound.play(2)

        if (random.random()>0.7):
            x=5+int(random.random()*10)
            y=5+int(random.random()*10)
            self.mobs.append( mobclass.mob((x,y)) )
    
    def addTower(self,x,y):
        if x>=0 <self.width and y>=0 < self.height:  
            self.cells[x][y] = Tower(x,y, self)
            
        a.pathdebug = [node.pos for node in astar(a.cells[0][0], a.cells[30][30])]
        
if __name__ == '__main__':

    a = Audiosplode()

    a.cells[3][4]=BlockageCell(3,4, a)
    a.cells[4][4]=BlockageCell(4,4, a)
    a.cells[5][4]=BlockageCell(5,4, a)
    a.cells[6][4]=BlockageCell(6,4, a)
    a.cells[2][4]=BlockageCell(2,4, a)

    from pathfinding.algorithms import astar
    a.pathdebug = [node.pos for node in astar(a.cells[0][0], a.cells[30][30])]

    ui = AudiosplodeUI(a,1024,768)

    pass
