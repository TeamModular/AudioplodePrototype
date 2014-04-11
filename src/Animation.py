__author__ = 'Luke Wallin'
'''
Note that all positions in animation are the same as for mobs - in units of cells.  To be drawn to the screen, the offset of the
viewport and cellsize are required
'''

import pygame
from numpy import array as Vector,linalg

class Animation(object):

    def __init__(self):
        self.time=0


    def update(self,dt):
        '''
        Update internal state based on time elapsed
        '''

        #return true when finished, false otherwise
        return True

    def draw(self,screen,offsetX,offsetY,cellSize):
        '''
        Draw the current state of this animation on the screen, given a position and size of a cell
        '''


class LaserAnimation(Animation):

    def __init__(self,startPos,endPos,lastsFor,colour=(255,0,0)):
        super(LaserAnimation,self).__init__()
        '''
        positions are in the form of (x,y)
        '''
        #TODO why on earth do I have to set this here? this should be done by the parent's constructor, no?
        # self.time=0

        self.startPos=Vector(startPos)
        self.endPos=Vector(endPos)
        self.lastsFor=lastsFor
        self.colour=colour

    def update(self,dt):
        self.time+=dt
        print "dt = " + str(dt) + " time = "+str(self.time)
        #animation finishes once time has elapsed lastsTime
        return self.time > self.lastsFor

    def draw(self,screen,offsetX,offsetY,cellSize):
        offset = Vector([offsetX,offsetY])
        pygame.draw.line(screen, self.colour, (self.startPos*cellSize-offset), (self.endPos*cellSize-offset))