'''
Created on 12 Jun 2013

@author: Luke
'''
#oject seems to be required for python 2.  I'm not asking why
class Cell(object):
    '''
    a base class for all cell things to extend
    '''
    

    def __init__(self,x,y):
        '''
        Constructor
        '''
        #this info probably not needed
        self.x=x
        self.y=y

    def draw(self,screen,x,y,size):
        '''
        crude for now, draw centred about that x and y and with a cellSize of size on a pygame.screen
        '''
        
    def update(self,dt):
        '''
        update over a time of dt seconds
        '''