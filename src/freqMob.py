import mob as mobClass

class mob(mobClass.mob):
    def __init__(self,position,path):
        mobClass.mob.__init__(self,position,path)
        #super(mob,self).__init__(position,path)
        self._frequency = 1
    
    def scale(self,multiple):
        self._frequency=multiple
        
    def update(self,dt,newPath=None):
        mobClass.mob.update(self,dt,newPath=None)
        self._colour = (255*self._frequency,0,255*self._frequency)
        
     
    def damage(self,amount):
        mobClass.mob.damage(self,amount)
        frac=self._health/100. #get a fraction of total life left
        self.scale(frac)
