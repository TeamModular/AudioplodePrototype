'''
Created on 11 Jun 2013

@author: Luke

major TODO: namespaces/modules/whatever they are in python

'''

#import pygame
from EmptyCell import EmptyCell
from AudiosplodeUI import AudiosplodeUI
from BlockageCell import BlockageCell
import math

class Audiosplode():
    
    def __init__(self, width=500, height=500):
        '''
        Create an audiosplode world
        '''
        
        self.width=width
        self.height=height
        
        self.cells =  [ [EmptyCell(x,y) for y in range(height)] for x in range(width)  ]
        
        #print(self.cells)
    
    def draw(self,screen,cellSize,offsetX,offsetY):
        
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
    
    
if __name__ == '__main__':
    
    a = Audiosplode()
    
    a.cells[3][4]=BlockageCell(3,4)
    
    ui = AudiosplodeUI(a,1024,768)
    
    pass