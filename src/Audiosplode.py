'''
Created on 11 Jun 2013

@author: Luke
'''

import pygame

if __name__ == '__main__':
    pygame.init()
    #with stealies from http://programarcadegames.com/python_examples/show_file.php?file=draw_module_example.py
    black = ( 0, 0, 0)
    white = (255,255,255)
    blue = ( 0, 0,255)
    green = ( 0,255, 0)
    red = (255, 0, 0)
    
    
    screen = pygame.display.set_mode((640, 480))
    
    running=True
    clock = pygame.time.Clock()
    
    while running:
        clock.tick(10)
        
        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                running=False # Flag that we are done so we exit this loop
                
        screen.fill(white)
        
        
        pygame.draw.line(screen,green,[0,0],[50,30],5)
        
        pygame.draw.circle(screen,blue,[60,250],40)
        
        pygame.display.flip()
    pass