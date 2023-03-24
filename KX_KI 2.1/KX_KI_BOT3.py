import bge
import random
#import dataclasses
from dataclasses import dataclass,fields
from KX_KI_DATACLASS import Genome,GenomeFunctions, SteeringFunctions
G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects

class Bot(GenomeFunctions, SteeringFunctions):
    
    def __init__(self,cont):
        # define: controller sensors, actuators
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.radar = self.cont.sensors["Radar"]
        #self.collision = self.cont.sensors["Collision"]
        self.motion = self.cont.actuators["Motion"]
        self.track = self.cont.actuators["Track"]
        self.steering = self.cont.actuators["Steering"]
        self.father_genome = ""
        self.task = "seek"
        self._task= "seek"
        self.target = None
        

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
                # if hasattr(self, "task"):
                #     print (self._task)

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
    

    def update(self):
        
        if self.radar.positive:
            #print (self.radar.hitObject)# Bot, Food
            if not self.task == "eat":
                self.task = "seek"
        exec("self." + self.task + "()")
        self.genome.energy -= 1
        self.limit_positions()
        #print(self.genome.decision_time)
        #if self.always.positive:
            #self.debug()   
def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        own["init"] = True
    else:
        self = own["bot"]
        self.update()
        #self.debug()

