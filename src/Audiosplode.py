'''
Created on 11 Jun 2013

@author: Luke

major TODO: namespaces/modules/whatever they are in python

'''

import pygame
from EmptyCell import EmptyCell
from AudiosplodeUI import AudiosplodeUI
from BlockageCell import BlockageCell

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
        
        for col in self.cells:
            for cell in col:
                cell.draw(screen,(cell.x)*cellSize-offsetX,(cell.y)*cellSize-offsetY,cellSize)
    
    
if __name__ == '__main__':
    
    a = Audiosplode()
    
    a.cells[3][4]=BlockageCell(3,4)
    
    ui = AudiosplodeUI(a,1024,768)
    
#     pygame.init()
#     #with stealies from http://programarcadegames.com/python_examples/show_file.php?file=draw_module_example.py
#     black = ( 0, 0, 0)
#     white = (255,255,255)
#     blue = ( 0, 0,255)
#     green = ( 0,255, 0)
#     red = (255, 0, 0)
#     
#     
#     screen = pygame.display.set_mode((640, 480))
#     
#     running=True
#     clock = pygame.time.Clock()
#     
#     while running:
#         clock.tick(10)
#         
#         for event in pygame.event.get(): # User did something
#             if event.type == pygame.QUIT: # If user clicked close
#                 running=False # Flag that we are done so we exit this loop
#                 
#         screen.fill(white)
#         
#         
#         pygame.draw.line(screen,green,[0,0],[50,30],5)
#         
#         pygame.draw.circle(screen,blue,[60,250],40)
#         
#         pygame.display.flip()
    pass