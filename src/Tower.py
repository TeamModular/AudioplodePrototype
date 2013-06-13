'''
Created on 12 Jun 2013

@author: Luke
'''

from Cell import Cell

class Tower(Cell):
    '''
    base class for different types of tower
    '''


    def __init__(self,x,y):
        super(Tower,self).__init__(x,y)
        '''
        Constructor
        '''
        