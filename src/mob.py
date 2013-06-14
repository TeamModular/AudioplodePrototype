import pygame as p
import sound
class mob:
	def __init__(self,position,cellSize):
		self._x = position[0]*cellSize
		self._y=position[1]*cellSize
		self._colour=(255,0,255)
		self._size=(16,16)
		self._health=100
		self._dead=False
		
		self._cellSize=cellSize
				
	def draw(self,screen):
		p.draw.rect(screen, self._colour, p.Rect(self._x-self._size[0]/2,self._y-self._size[1]/2,self._size[0],self._size[1]), 0)
	
	def move(self,relativePosition):
		self._x += relativePosition[0]*self._cellSize
		self._y += relativePosition[1]*self._cellSize
				
	def damage(self,amount):
		assert type(amount)==int
		self._health-=amount
		if self._health<0:
			self._dead=True
	
	def isDead(self):
		return self._dead
		
		
