import bge
import random
#import dataclasses
from dataclasses import dataclass,fields
from KX_KI_DATACLASS import Genome,GenomeFunctions, SteeringFunctions, Digestion, TaskManager
G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects

class Bot(GenomeFunctions, SteeringFunctions, Digestion,TaskManager):
    
    def __init__(self,cont):
        super().__init__()
        # define: controller sensors, actuators
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.radar = self.cont.sensors["Radar"]
        
        self.motion = self.cont.actuators["Motion"]
        self.track = self.cont.actuators["Track"]
        
        self.father_genome = ""
        self.task = "stopp"
        self._task= "stopp"
        self.target = None
        
        self.debug = False
        
        # gets genome
        self.setGenome()

        #reset to birthage
        self.genome.age = 0

        # sets Properties og the genome 
        self.update_Properties()

    @property
    def task(self):
        return self._task
    
    @task.setter
    def task(self, value):
        if hasattr(self,"genome"):
            #print (self.owner["decision_time,self.genome["decision_time)
            if self.owner["decision_time"] > self.genome.decision_time:
                self._task = value
                self.owner["decision_time"] =0
                if hasattr(self, "task"):
                    if self.debug == True:
                        print (self._task)

    def update_Properties(self):
        self.always.skippedTicks = self.genome.always_skippedTicks
        self.always.seed = self.genome.always_seed
        self.radar.skippedTicks = self.genome.radar_skippedTicks
        #self.collision.skippedTicks = self.genome.collision_skippedTicks
        if self.genome.sex == 1:
            self.owner.replaceMesh("maleBeetle",True,True)
        else:
            self.owner.replaceMesh("femaleBeetle",True,True)
    

        self.owner.worldPosition.z = 0
    def follow(self):
        if not self.radar_hitObject_is_valid(): return
        self.track.object = self.radar.hitObject
        self.motion.dLoc = (0,self.genome.speed,0)
        self.cont.activate(self.track)
        self.cont.activate(self.motion)

        
        if self.owner.getDistanceTo(self.radar.hitObject) < 5.0:
            if self.radar.hitObject == "Food":
                #self.target = None
                self.task = "eat"
            if self.radar.hitObject == "Bot":
                if self.horny():
                    pass
                    

    def stopp(self):
        self.track.object = None
        self.motion.dLoc = (0,0,0)
        self.motion.dRot = (0,0,0)
        self.cont.deactivate(self.track)
        self.cont.deactivate(self.motion)
    def radar_hitObject_is_valid(self):
        if self.radar.hitObject == None:
            return False
        if self.radar.hitObject.name == "Food":
            return True
        else:
            if not "init" in self.radar.hitObject:
                return False
            
            if self.radar.hitObject["init"] == False:
                return False
            if hasattr(self.radar.hitObject, "bot"):
                return True
        
    
    def decide(self):
        
        #print (self.owner["timer"],self.genome.decision_time, float(self.owner["timer"]) > float(self.genome.decision_time) )
        if float(self.owner["timer"]) > float(self.genome.decision_time):
            self.owner["timer"] = 0.0
    
        if self.radar_hitObject_is_valid():
            #print ("dd")
            if self.radar.hitObject.name == "Food" and self.hungry() == True:
                self.target = self.radar.hitObject
                self.task = "follow"

            if self.radar.hitObject.name == "Bot" and self.horny() == True:
                self.target = self.radar.hitObject
                self.task = "follow"

            if self.target != None:
                if self.owner.getDistanceTo(self.target) < 5.0:
                    self.task = "eat"
            
        if self.task == "stopp":
            self.task = "walkaround"
        
    def display(self):
        if self.radar_hitObject_is_valid():
            if self.radar.hitObject.name == "Food":
                self.owner.children["target_display"].replaceMesh(self.radar.hitObject.name)
                

            if self.radar.hitObject.name == "Bot":
                if self.radar.hitObject["bot"].genome["sex"] == 1:
                    self.owner.children["target_display"].replaceMesh("maleBeetle")
                else:
                    self.owner.children["target_display"].replaceMesh("femaleBeetle")

        else:
            if self.task == "walkaround":
                self.owner.children["target_display"].replaceMesh("RadarCone")
                #self.owner.children["target_display"].visible = 0

        target_display_size = 0.3
        self.owner.children["target_display"].scaling = (target_display_size,target_display_size,target_display_size)
        self.owner.children["target_display"].visible = 1   
    def debugHitObject(self):
        if self.radar_hitObject_is_valid():
            bge.render.drawLine(self.owner.worldPosition, self.radar.hitObject.worldPosition, (1,0,0,0))
        #print("debugHitObject")
    def update(self):
        #print ("activities: ", self.activities)
        self.calls += 1
        self.genome.energy -= 1
        self.limit_positions()
        #self.debugHitObject()
        self.display()

        if float(self.owner["timer"]) < float(self.genome.decision_time):
            exec("self." + self.task + "()")
        else:
            self.decide()   
            self.owner["timer"] = 0.0

        
        #print(self.task)
        #if self.always.positive:
            #self.debug()   
def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        own["init"] = True
    else:
        own["bot"].update()
        #self.debug()

