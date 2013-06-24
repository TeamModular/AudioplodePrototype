'''
Created on 11 Jun 2013

@author: Luke
'''
import pygame
import math

class AudiosplodeUI:
    '''
    UI using pygame for Audiosplode
    
    How this is working:
    
    using pygame's sprite system and a rendering group.
    
    the whole screen is rendered by a rendering group.
    
    Audiosplode itself is currently a single sprite - haven't broken the game down into indivial sprites yet
    so think of the game as like a single updating texture
    
    Viewports are a view of the world - so the minimap and the main view are just different configerations of viewports
    
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
        
        
        '''
        
        General layout:
        
        [statusbar - money, points, etc]
        [  viewport into game]
        
        [  tower selection  ][minimap]
        
        '''
        
        self.pos=[0,0]

        self.scrollSpeed=100
        
        self.cellSize=20

        self.fps=30
        self.dt = float(1)/float(self.fps)
        
        self.mainWindowGroup = pygame.sprite.RenderUpdates()
        
        #height of the bit at the bottom
        navBarHeight = int(round(height*0.25))
        statusBarHeight=int(round(height*0.05))
        miniMapWidth = int(round(navBarHeight*1.5))
        
        self.mainView = Viewport(width, height-navBarHeight-statusBarHeight, [0,statusBarHeight], self.audiosplode, self.cellSize, self.pos)
        
        self.statusBar = StatusBar(width, statusBarHeight, self.audiosplode, [0,0])
        
        self.miniMap = Viewport(miniMapWidth,navBarHeight,[width-miniMapWidth,height-navBarHeight],self.audiosplode, 3, [0,0])
        
        self.navBar = NavBar(width - miniMapWidth, navBarHeight, audiosplode, [0,height-navBarHeight])
        
        self.mainWindowGroup.add(self.navBar)
        self.mainWindowGroup.add(self.statusBar)
        self.mainWindowGroup.add(self.mainView)
        self.mainWindowGroup.add(self.miniMap)

        #TODO scootle running the window into another thread

        #MAJOR TODO sprites!  Should make everythign faster - pygame's sprite module is promising
        running=True
        clock = pygame.time.Clock()
        #TODO learn how to use pygame proper, this is hideously inefficient
        while running:
            clock.tick(self.fps)
            running = self.update()
        #if we leave the loop tidy up all the shizzle
        pygame.quit()
            
        
    def update(self):
        mouseDown=False
        mousePos=[0,0]

        for event in pygame.event.get(): # User did something
            if event.type == pygame.QUIT: # If user clicked close
                return False # Flag that we are done so we exit this loop
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
                mousePos=event.pos
                
        
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
            
            mousePos = self.mainView.mouseOnWorld(mousePos)
            
            if not mousePos == None:
                x = int(math.floor((mousePos[0]+self.pos[0])/self.cellSize))
                y = int(math.floor((mousePos[1]+self.pos[1])/self.cellSize))
                #print str(mousePos[0])+","+str(mousePos[1])+" -> ("+str(x)+","+str(y)+")"
                self.audiosplode.addTower(x,y)

        #blank screen before drawing
#         self.screen.fill((255,255,255))
# 
#         self.audiosplode.draw(self.screen,self.cellSize,self.pos[0],self.pos[1])
        self.audiosplode.update(self.dt)
# 
#         pygame.display.flip()
        self.mainWindowGroup.update()
        
        #draw the scene
        dirty = self.mainWindowGroup.draw(self.screen)
        pygame.display.update(dirty)
        
        return True

class UIChunk(pygame.sprite.Sprite):
    '''
    base class for any part of the UI that will be a sprite that forms part of a rendering group
    '''
    def __init__(self,width,height,screenPos):
        pygame.sprite.Sprite.__init__(self)
        self.width=width
        self.height=height
        #image and rect are required for the sprite to be part of a group
        self.image = pygame.Surface([width, height])
        
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = screenPos
        

class NavBar(UIChunk):
    '''
    bottom chunk of screen, for choosing which towers to place, etc
    '''
    
    #TODO this init is nearly identical across the three classes, abstract?
    def __init__(self,width,height,audiosplode,screenPos):
        UIChunk.__init__(self,width,height,screenPos)
        
        self.audiosplode=audiosplode
        
    def update(self):
        self.image.fill((200,200,200))
        
        
            

class StatusBar(UIChunk):
    '''
    Bar at the top of the screen.  Shows how much money and how many lives left
    '''
    def __init__(self,width,height,audiosplode,screenPos):
        UIChunk.__init__(self,width,height,screenPos)
        
        self.audiosplode=audiosplode
        
    def update(self):
        self.image.fill((200,200,200))
        
        if pygame.font:
            font = pygame.font.Font(None, self.height-2)
            text = font.render("Money: "+str(self.audiosplode.getMoney()), 1, (10, 10, 10))
            textpos = text.get_rect(x=0)#centerx=background.get_width()/2
            self.image.blit(text, textpos)
            
            text = font.render("Lives: "+str(self.audiosplode.getLives()), 1, (10, 10, 10))
            textpos = text.get_rect(x=self.width/2)#centerx=background.get_width()/2
            self.image.blit(text, textpos)
            

class Viewport(UIChunk):
    '''
    A viewport of the game world
    using this as an intermediate step to rendering everything with pygame's sprite system.
        '''
    def __init__(self,width,height,screenPos,audiosplode,cellSize,pos):
        UIChunk.__init__(self,width,height,screenPos)
        
        
        self.cellSize=cellSize
        
        self.audiosplode=audiosplode
        
        #position of viewport in the game world
        self.pos=pos
        
        #render it intially
        self.update()
        
    def update(self):
        self.audiosplode.draw(self.image,self.cellSize,self.pos[0],self.pos[1])
        pass
    
    #given a mouse screen position, return the mouse click positioni nthe world, or return None if outside this viewprot
    def mouseOnWorld(self,mousePos):
        
        if self.rect.x + self.width > mousePos[0] >= self.rect.x and self.rect.y + self.height >= mousePos[1] > self.rect.y:
            #mouse is in range of this viewport
            return [mousePos[0]-self.rect.x, mousePos[1]-self.rect.y]
        else:
            return None
            