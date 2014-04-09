__author__ = 'Luke Wallin'


'''
Ported from Javascript Animation class 2
 *main changes from first one - now assuming that self will be on a seperate
 *canvas and so got rid of a lot of bits and peices that are now longer relevent
 *
 *
 *finishedCallback - function reference - called when self has finished all animations
 *
 *ctx - reference to ctx object (canvas.getContext)
'''


class AnimationController:

    def __init__(self, framerate,screen):
        
        self.framerate=framerate
        self.framePeriod = 1000/self.framerate
    
    
        self.screen = screen
        
        # self.width=width
        # self.height=height
        
        self.animations = list()

        
        #ovverride self to detect when animations have finished
        self.finishedCallback=finishedCallback
        
        #running means animations are alive, not that the loop is being auto-run
        self.running=false
        
        self.thread = false
    self.loop = function()
    {	
        self.ctx.clearRect(0,0,self.width,self.height)
                
        if (self.animations.length == 0){
            self.stop()
            self.finishedCallback()
        }
		
        for (var i = 0 i < self.animations.length i++) {
            if (self.animations[i].drawNext(self.ctx,self)){
                #self has finished, remove it!
                self.animations.splice(i, 1)
                #decrease i so we don't skip an animation
                i--
            }
        }
    }
	
	
	
    self.stop=function()
    {
        if(self.selfRunning){
            self.ctx.clearRect(0,0,self.width,self.height)
            clearInterval(self.thread)
            self.running=false
        }
    }
	
    self.start = function()
    {
        if(self.selfRunning && !self.running){
            self.thread = setInterval(function(){self.loop.call(self)}, self.framePeriod)
            self.running=True
        }
    }
    
    self.clear=function(){
        self.ctx.clearRect(0,0,self.width,self.height)
        self.animations=[]
    }
    
    self.isRunning=function(){
        return self.running
    }
    
    self.add=function(animation){
        self.animations.push(animation)
        self.start()
    }
    
    self.getStagesFromTime=function(time){
        return time*1000/self.framePeriod
    }
}


/*
 * Animation 'interface:
 * 
 */

var ExampleAnimation=function(){
    self.drawNext=function(ctx,animationController){
        if(finished){
            return True
        }else{
            return false
        }
    }
}