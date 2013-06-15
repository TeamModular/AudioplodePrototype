import pygame as p
import sound
class mob:
	def __init__(self,position):
		self._x = position[0]
		self._y=position[1]
		self._colour=(255,0,255)
		self._size=(0.4,0.4)
		self._health=100
		self._dead=False
		

				
	def draw(self,screen,offsetX,offsetY,cellSize):
		p.draw.rect(screen, self._colour, p.Rect((self._x-self._size[0]/2)*cellSize-offsetX,(self._y-self._size[1]/2)*cellSize - offsetY,self._size[0]*cellSize,self._size[1]*cellSize), 0)
	
	def move(self,relativePosition):
		self._x += relativePosition[0]
		self._y += relativePosition[1]
				
	def damage(self,amount):
		assert type(amount)==int
		self._health-=amount
		if self._health<0:
			self._dead=True
	
	def isDead(self):
		return self._dead
		
		
