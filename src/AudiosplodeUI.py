'''
Created on 11 Jun 2013

@author: Luke
'''
import pygame

class MyClass(object):
    '''
    UI using pygame for Audiosplode
    '''


    def __init__(self,width=640,height=480):
        '''
        setup pygame
        create the pygame window of the width and height
        '''
        pygame.init()
        self.width=width
        self.height=height
        self.screen = pygame.display.set_mode((width, height))
        
        #TODO scootle running the window into another thread
    
#         running=True
#         clock = pygame.time.Clock()
#         
#         while running:
#             clock.tick(10)
#             
#             for event in pygame.event.get(): # User did something
#                 if event.type == pygame.QUIT: # If user clicked close
#                     running=False # Flag that we are done so we exit this loop
#                     
#             screen.fill(white)
#             
#             
#             pygame.draw.line(screen,green,[0,0],[50,30],5)
#             
#             pygame.draw.circle(screen,blue,[60,250],40)
#             
#             pygame.display.flip()
        
        pass