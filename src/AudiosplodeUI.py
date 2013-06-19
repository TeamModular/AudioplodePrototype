'''
Created on 11 Jun 2013

@author: Luke
'''
import pygame
import math

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

        self.scrollRight=False
        self.scrollLeft=False
        self.scrollUp=False
        self.scrollDown=False
        
        #to make up for the fact taht the screen origin and mouse click origin don't appear to be exactly the same
        self.permanentPosOffset=[-10,-10]
        
        self.pos=[0,0]

        self.scrollSpeed=100
        
        self.cellSize=20

        self.fps=10
        self.dt = float(1)/float(self.fps)

        #TODO scootle running the window into another thread

        #MAJOR TODO sprites!  Should make everythign faster - pygame's sprite module is promising
        running=True
        clock = pygame.time.Clock()
        #TODO learn how to use pygame proper, this is hideously inefficient
        while running:
            clock.tick(self.fps)
            
            mouseDown=False
            mousePos=[0,0]

            for event in pygame.event.get(): # User did something
                if event.type == pygame.QUIT: # If user clicked close
                    running=False # Flag that we are done so we exit this loop
                if event.type == pygame.KEYDOWN:
                    #deal with scrolling aorund
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.scrollUp=True
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.scrollRight=True
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.scrollDown=True
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.scrollLeft=True
                if event.type == pygame.KEYUP:
                    #deal with scrolling aorund
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        self.scrollUp=False
                    if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        self.scrollRight=False
                    if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        self.scrollDown=False
                    if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        self.scrollLeft=False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouseDown=True
                    mousePos=(event.pos[0]-self.permanentPosOffset[0] , event.pos[1]-self.permanentPosOffset[1])
                    
            
            #scrolling around stuff:
            if self.scrollDown:
                self.pos[1]= self.pos[1] + self.scrollSpeed*self.dt
            if self.scrollLeft:
                self.pos[0]= self.pos[0] - self.scrollSpeed*self.dt
            if self.scrollRight:
                self.pos[0]= self.pos[0] + self.scrollSpeed*self.dt
            if self.scrollUp:
                self.pos[1]= self.pos[1] - self.scrollSpeed*self.dt

            #some limits to stop scrolling off top left
            self.pos[0] = max(self.pos[0],0)
            self.pos[1] = max(self.pos[1],0)
            #TODO something for bottom right too


            #deal with mouse clicks
            if mouseDown:
                
                x = int(math.floor(mousePos[0]/self.cellSize))
                y = int(math.floor(mousePos[1]/self.cellSize))
                print str(mousePos[0])+","+str(mousePos[1])+" -> ("+str(x)+","+str(y)+")"
                self.audiosplode.addTower(x,y)

            #blank screen before drawing
            self.screen.fill((255,255,255))

            self.audiosplode.draw(self.screen,self.cellSize,self.pos[0],self.pos[1])
            self.audiosplode.update(self.dt)

            pygame.display.flip()

        #TODO clear up pygame?
