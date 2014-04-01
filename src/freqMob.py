import mob as mobClass

class mob(mobClass.mob):
    def __init__(self,position,path,size):
        mobClass.mob.__init__(self,position,path)
        #super(mob,self).__init__(position,path)
        self._frequency = 1
        
        self.speed

        if size>0.1:
            if size>1:
                size=1
        else:
            size=0.1
        self._sizeControl=size                
        
        self._size=(size,size)
        self._health=100*size
        self._soundValue=int(10*size) #range 1..10
        self.speed=4*(1-size)
            
    def scale(self,multiple):
        self._frequency=multiple
                        
    def update(self,dt,newPath=None):
        mobClass.mob.update(self,dt,newPath)
        self._colour =(255*self._frequency,0,255*self._frequency)                 
        
    def damage(self,amount):
        mobClass.mob.damage(self,amount)
        frac=self._health/(100.0*self._sizeControl) #get a fraction of total life left
        self.scale(frac)
        

