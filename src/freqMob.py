import mob as mobClass

class mob(mobClass.mob):
    def __init__(self,position,path,size):
        mobClass.mob.__init__(self,position,path)
        #super(mob,self).__init__(position,path)
        self._frequency = 1
        
        self.speed

        if size>0.1:
            if size>0.9:
                size=0.9
        else:
            size=0.1
        self._sizeControl=size #this is used to reset any slowed towers           
        self._setSizeValues()
                
        self._timeToSlow=0
        self._beingSlowed=False
    
    def _setSizeValues(self):
        self._size=(self._sizeControl,self._sizeControl)
        self._health=100*self._sizeControl
        self._soundValue=int(10*self._sizeControl) #range 1..10
        self.speed=4*(1-self._sizeControl)
        
            
    def scale(self,multiple):
        self._frequency=multiple
                        
    def update(self,dt,newPath=None):
        mobClass.mob.update(self,dt,newPath)
        self._colour =(255*self._frequency,0,255*self._frequency)                 
        
        if self._beingSlowed:
            self._colour=(self._colour[0],128,self._colour[2])
            if self._timeToSlow>0:
                self._timeToSlow-=dt
            else:
                self._timeToSlow=0
                self._beingSlowed=False
                self._setSizeValues()
            
            
        
    def damage(self,amount):
        mobClass.mob.damage(self,amount)
        frac=self._health/(100.0*self._sizeControl) #get a fraction of total life left
        self.scale(frac)
        
    def slow(self,amount):
                        
        self._soundValue=int(10*(self._sizeControl-amount)) #range 1..10
        self.speed=4*((1-self._sizeControl)-amount)
        if self.speed<0.4: # 0.1*4
            self.speed=0.4
        if self._soundValue<1: #self._sizeControl-amount==0.1
            self._soundValue=1
        
        self._beingSlowed=True
        self._timeToSlow=3
        
