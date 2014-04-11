'''
Created on 11 Jun 2013

@author: Luke
'''
from __future__ import print_function
import pygame
import math
from numpy import array as Vector,linalg
import Tower

class AudiosplodeUI:
    '''
    UI using pygame for Audiosplode
    
    How this is working:
    
    using pygame's sprite system and a rendering group.
    
    the whole screen is rendered by a rendering group.
    
    Audiosplode itself is currently a single sprite - haven't broken the game down into indivial sprites yet
    so think of the game as like a single updating texture
    
    Viewports are a view of the world - so the minimap and the main view are just different configerations of viewports
    
    Note: using pygame Vector2s for all x,y pairs
    
    
    general plan for tower selection UI:
    
    new class which is a sprite, is given a static draw function and an int which is a position in the towers array of the main AudiosplodeUI class
    when a mouse click occurs, all UI elememts are given this info
    the individual icons will then have enough info to let the main class know they were clicked, and therefore highlight themslves
    
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
        
        self.rightMouseDown=False
        
        
        '''
        
        General layout:
        
        [statusbar - money, points, etc]
        [  viewport into game]
        
        [  tower selection  ][minimap]
        
        '''
        
        self.pos=Vector([0,0])

        self.scrollSpeed=100
        
        self.cellSize=20

        self.fps=30
        self.dt = float(1)/float(self.fps)
        
        #self.mainWindowGroup = pygame.sprite.RenderUpdates()
        self.mainWindowGroup = pygame.sprite.OrderedUpdates()
        
        #height of the bit at the bottom
        navBarHeight = int(round(height*0.25))
        blurbWidth = int(round(width*0.3))
        statusBarHeight=int(round(height*0.05))
        #miniMapWidth = int(round(navBarHeight*1.5))
        miniMapWidth=blurbWidth
        navPadding = 2
        
        self.mainView = Viewport(width, height-navBarHeight-statusBarHeight, Vector([0,statusBarHeight]), self.audiosplode, self.cellSize, self.pos, True)
        
        self.statusBar = StatusBar(width, statusBarHeight, self.audiosplode, Vector([0,0]))
        
        self.miniMap = Viewport(miniMapWidth-navPadding*2,navBarHeight-navPadding*2,Vector([width-miniMapWidth+navPadding,height-navBarHeight+navPadding]),self.audiosplode, 3, Vector([0,0]),False)
        
        self.towerSelection = TowerSelection(width - miniMapWidth-navPadding-blurbWidth, navBarHeight-navPadding*2, self, Vector([blurbWidth+navPadding,height-navBarHeight+navPadding]))
        
        self.blurb = Blurb(blurbWidth-navPadding, navBarHeight-navPadding*2, self, Vector([navPadding,height-navBarHeight+navPadding]))
        
        self.mainWindowGroup.add(self.blurb)
        self.mainWindowGroup.add(self.towerSelection)
        self.mainWindowGroup.add(self.statusBar)
        self.mainWindowGroup.add(self.mainView)
        self.mainWindowGroup.add(self.miniMap)
        
        self.oldMousePos=Vector([0,0])
        self.gotOldMousePos=False
        
        #place all the tower icons
        
        self.iconSize=int(round(self.width*0.06))
        #padding is space between icons
        self.iconsPadding=int(round(self.width*0.01))
        #margin is width of line around icon
        self.iconsMargin=int(round(self.iconsPadding*0.5))
        #size of grid of icons
        self.iconsWide=3
        
        
        self.towerIcons=[];
        
        towers = self.audiosplode.availableTowers()
        i=0
         
        for tower in towers:
             
            x = self.iconsPadding + (i%self.iconsWide)*self.iconSize + self.towerSelection.getScreenPos()[0]
            y = self.iconsPadding + math.floor(float(i)/float(self.iconsWide)) + self.towerSelection.getScreenPos()[1]
             
            #tower.drawStatic(self.image,x,y,self.iconSize)
            #by default first tower is the selected tower
            icon = TowerIcon(self.iconSize, self, Vector([x,y]), tower,self.iconsMargin)#,i==0)
            self.mainWindowGroup.add(icon)
            self.towerIcons.append(icon)
             
            i=i+1
        
        
        
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
        mouseLeftDown=False
        mousePos=Vector([0,0])
        #mouseRightDown=False

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
                mousePos=Vector(event.pos)
                if event.button == 1:
                    #left mouse button
                    mouseLeftDown=True
                    
                elif event.button == 3:
                    self.rightMouseDown=True
                    
                    
                    
                    
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 3:
                    self.rightMouseDown=False
                    
                    #right mouse button!
#                 elif event.get_pressed()[1]:
#                     print "right mouse button"
                
                
        
        #scrolling around stuff:
        if self.scrollDown:
            self.pos[1]= self.pos[1] + self.scrollSpeed*self.dt
        if self.scrollLeft:
            self.pos[0]= self.pos[0] - self.scrollSpeed*self.dt
        if self.scrollRight:
            self.pos[0]= self.pos[0] + self.scrollSpeed*self.dt
        if self.scrollUp:
            self.pos[1]= self.pos[1] - self.scrollSpeed*self.dt

        
        
        if self.rightMouseDown:
            
            if self.mainView.mouseOnChunk(Vector(pygame.mouse.get_pos())) != None:
                #only move hte view around if the main view was waht was right clicked on?
                if self.gotOldMousePos:
                    #mouse has been down for a at least one iteration of uopdate
                    mouseDif = Vector(pygame.mouse.get_pos()) - self.oldMousePos
                    print(mouseDif)
                    print("oldpos="+str(self.pos))
                    self.pos +=  mouseDif#/self.cellSize
                    print("newpos="+str(self.pos))
                    #set the mouse pos back to where it was when it first right clicked, so when it reappars it's not somewehre weird
                    pygame.mouse.set_pos(self.oldMousePos)
                else:
                    #mouse has just been pressed
                    #make mouse invisible
                    pygame.mouse.set_visible(False)
                    self.oldMousePos = Vector(pygame.mouse.get_pos())
                    self.gotOldMousePos = True
                
            
            
            
        else:
            self.gotOldMousePos=False
            pygame.mouse.set_visible(True)
        
        
        #some limits to stop scrolling off top left
        self.pos[0] = max(self.pos[0],0)
        self.pos[1] = max(self.pos[1],0)
        #TODO something for bottom right too
        
        self.mainView.setPos(self.pos)
        
        #deal with mouse clicks
        if mouseLeftDown:
            
            #get hte mouse position on the main world viewport
            mousePosOnWorld = self.mainView.mouseOnChunk(mousePos)
            
            if not mousePosOnWorld == None:
                x = int(math.floor((mousePosOnWorld[0]+self.pos[0])/self.cellSize))
                y = int(math.floor((mousePosOnWorld[1]+self.pos[1])/self.cellSize))
                #print str(mousePos[0])+","+str(mousePos[1])+" -> ("+str(x)+","+str(y)+")"

                #place currently selected tower:
                for towerIcon in self.towerIcons:
                    if towerIcon.selected:
                        self.audiosplode.addTower(x,y,towerIcon.tower)
            
            #give the mouse click info to the other UI chunks that need it
            self.towerSelection.mouseOnChunk(mousePos)
            #TODO iterate through ALL UI elemnts!

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
    
    
    def availableTowers(self):
        return self.audiosplode.availableTowers()
    

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
    
    def mouseClickedHere(self,mousePos):
        '''
        this is called whenever mouseOnChunk has discovered the mouse has been pressed on this UIChunk
        override to use
        '''
        pass
    
    def getScreenPos(self):
        return Vector([self.rect.x,self.rect.y])
    
    #given a mouse screen position, return the mouse click positioni nthe world, or return None if outside this viewprot
    def mouseOnChunk(self,mousePos):
        
        if self.rect.x + self.width > mousePos[0] >= self.rect.x and self.rect.y + self.height >= mousePos[1] > self.rect.y:
            #mouse is in range of this viewport
            mousePos = Vector([mousePos[0]-self.rect.x, mousePos[1]-self.rect.y])
            self.mouseClickedHere(mousePos)
            return mousePos
        else:
            return None

class Blurb(UIChunk):
    def __init__(self,width,height,audiosplodeUI,screenPos):
        UIChunk.__init__(self,width,height,screenPos)
        
        self.audiosplodeUI=audiosplodeUI
        
    def update(self):
        self.image.fill((200,200,200))

class TowerSelection(UIChunk):
    '''
    bottom middle chunk of screen, for choosing which towers to place, etc
    '''
    
    def __init__(self,width,height,audiosplodeUI,screenPos):
        UIChunk.__init__(self,width,height,screenPos)
        
        self.audiosplodeUI=audiosplodeUI
        self.iconSize=int(round(self.width*0.2))
        
        #size of grid of icons
        self.iconsWide=3
        #self.iconsTall=2
        
        self.iconsPadding=int(round(self.width*0.02))
    
    def mouseClickedHere(self, mousePos):
        print ("mouse in tower seelction")
        for icon in self.audiosplodeUI.towerIcons:
            icon.selected=False
        for icon in self.audiosplodeUI.towerIcons:    
            offsetX = icon.rect.x-self.rect.x
            offsetY = icon.rect.y-self.rect.y
                                               
            if (offsetX + icon.width) > mousePos[0] >=offsetX and (offsetY + icon.height) > mousePos[1] >=offsetY:
                icon.mouseClickedHere(mousePos)    
                break            

    
    def update(self):
        self.image.fill((200,200,200))
        
#         towers = self.audiosplodeUI.availableTowers()
#         #TODO would it make more sense to have the tower buttons as individual sprites?
#         i=0
#         
#         for tower in towers:
#             
#             x = self.iconsPadding + (i%self.iconsWide)*self.iconSize
#             y = self.iconsPadding + math.floor(float(i)/float(self.iconsWide))
#             
#             tower.drawStatic(self.image,x,y,self.iconSize)
#             
#             i=i+1

class TowerIcon(UIChunk):
    '''
    A clickable icon to choose which tower is currently selected
    
    this might be abstracted further to any UI square?
    '''
    
    def __init__(self,size,audiosplodeUI,screenPos,tower,margin,selected=False):
        UIChunk.__init__(self,size,size,screenPos)
        self.audiosplodeUI=audiosplodeUI
        
        #this is a proper fudge, I need the tower colour
        #but its a property of an object whereas I only
        #have a function pointer, so instantiating
        #a None object and grabbing the colour.
        self.towerColour=tower(None,None,None).colour
        self.tower=tower 
        self.margin=margin
        self.selected=selected
        
    def update(self):
        
        if self.selected:
            #highlight with yellow
            pygame.draw.rect(self.image, (255,255,0), pygame.Rect(0,0,self.width,self.height), 0)
        else:
            #outline with black
            pygame.draw.rect(self.image, (0,0,0), pygame.Rect(0,0,self.width,self.height), 0)
        
        self.tower.drawStatic(self.image,self.margin,self.margin,self.width-self.margin*2,self.towerColour)
        
    def mouseClickedHere(self, mousePos):
        self.selected=True
        

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
    def __init__(self,width,height,screenPos,audiosplode,cellSize,pos,animations):
        UIChunk.__init__(self,width,height,screenPos)

        #will this viewport render animatinos?
        self.animations=animations
        
        self.cellSize=cellSize
        
        self.audiosplode=audiosplode
        
        #position of viewport in the game world
        #currently a reference, woops
        self.pos=pos
        
        #render it intially
        self.update()
        
    def update(self):
        self.audiosplode.draw(self.image,self.cellSize,self.pos[0],self.pos[1],self.animations)
        pass
    
    def setPos(self,pos):
        self.pos=pos
    
    
            
