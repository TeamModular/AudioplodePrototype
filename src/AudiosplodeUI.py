'''
Created on 11 Jun 2013

@author: Luke
'''
import pygame

class AudiosplodeUI:
    '''
    UI using pygame for Audiosplode
    '''


    def __init__(self,audiosplode,width=640,height=480):
        '''
        setup pygame
        create the pygame window of the width and height
        '''
        pygame.init()
        self.width=width
        self.height=height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("THE AWESOME AUDIOSPLODE")
        
        self.audiosplode=audiosplode
        
        #TODO scootle running the window into another thread
        
        #MAJOR TODO sprites!  Should make everythign faster - pygame's sprite module is promising
        running=True
        clock = pygame.time.Clock()
        #TODO learn how to use pygame proper, this is hideously inefficient
        while running:
            clock.tick(10)
             
            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    running=False # Flag that we are done so we exit this loop
                     
            self.screen.fill((255,255,255))
            
            self.audiosplode.draw(self.screen,20,0,0)
            
             
            pygame.display.flip()
        
        #TODO clear up pygame?