import mob as mobClass

class mob(mobClass.mob):
    def __init__(self,position,path,size):
        mobClass.mob.__init__(self,position,path)
        #super(mob,self).__init__(position,path)
        self._frequency = 1
        self._sizeControl=size
        if size>0.1:
            if size<1:
                self._size=(size,size)
                self._health=100*size
            else:
                self._size=(1.0,1.0)
                self._health=100
        else:
            self._size=(0.1,0.1)
            self._health=1
            
    def scale(self,multiple):
        self._frequency=multiple
        
    def update(self,dt,newPath=None):
        mobClass.mob.update(self,dt,newPath=None)
        self._colour = (255*self._frequency,0,255*self._frequency)
             
    def damage(self,amount):
        mobClass.mob.damage(self,amount)
        frac=self._health/(100.0*self._sizeControl) #get a fraction of total life left
        self.scale(frac)
        

