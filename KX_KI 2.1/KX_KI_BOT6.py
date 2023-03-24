import bge
import random
#import dataclasses

G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects
from dataclasses import dataclass,fields
from Genetics import Gene, Genome, GenomeHandler

import random

                
class Bot(GenomeHandler):
    
    def __init__(self,cont):
        super().__init__()
        self.father_genome = None
        # define: controller sensors, actuators
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.radar = self.cont.sensors["Radar"]
        self.motion = self.cont.actuators["Motion"]
        self.track = self.cont.actuators["Track"]

        self.id = self.owner["id"]
        self.state = 0
        self.is_selected = False
        self.hitObject = None
        self.setGenome(Genome())
        self.setGenomeValues()
        self.setGenomeValuesRandomly(15)
        self.update_Properties()
        self.setColor()

    def setColor(self):
        color = [self.genome.color_r.value,
                 self.genome.color_g.value,
                 self.genome.color_b.value,
                 self.genome.color_a.value]
        
        self.owner.color = color

        # for i in self.owner.childrenRecursive:
        #     i.color = color
    def update_Properties(self):
        self.always.skippedTicks = int(self.genome.always_skippedTicks.value)
        self.always.seed = int(self.genome.always_seed.value)
        self.radar.skippedTicks = int(self.genome.radar_skippedTicks.value)
        #self.collision.skippedTicks = self.genome.collision_skippedTicks
        if self.genome.sex.value == 1:
            self.owner.replaceMesh("maleBeetle",True,True)
        else:
            self.owner.replaceMesh("femaleBeetle",True,True)

        self.setColor()

        self.owner.worldPosition.z = 0

    def limit_positions(self):
        buffer = 10
        worldsize = G.globalDict["size"]
        if self.owner.worldPosition.x > worldsize:
            self.owner.worldPosition.x = -worldsize+buffer
        if self.owner.worldPosition.x < -worldsize:
            self.owner.worldPosition.x = worldsize-buffer
        if self.owner.worldPosition.y > worldsize:
            self.owner.worldPosition.y = -worldsize+buffer
        if self.owner.worldPosition.y < -worldsize:
            self.owner.worldPosition.y = worldsize-buffer

    def follow(self):
        self.motion.dLoc = (0,self.genome.speed.value,0)
        self.cont.activate(self.track)
        self.cont.activate(self.motion)
    
    def walkaround(self):
        self.cont.deactivate(self.track)
        self.motion.dLoc = (0.0,random.uniform(self.genome.speed.value, self.genome.speed.max),0.0)
        self.motion.dRot = ((0.0,0.0,random.uniform(-self.genome.rotation.max,self.genome.rotation.max)))
        self.cont.activate(self.motion)

    def stopp(self):
        self.track.object = None
        self.motion.dLoc = (0,0,0)
        self.motion.dRot = (0,0,0)
        self.cont.deactivate(self.track)
        self.cont.deactivate(self.motion)

    def walkaround(self):
        self.cont.deactivate(self.track)
        #self.task = "walkaround"
        self.motion.dLoc = (0.0,random.uniform(self.genome.speed.value, self.genome.speed.max),0.0)
        self.motion.dRot = ((0.0,0.0,random.uniform(-self.genome.rotation.value,self.genome.rotation.value)))
        self.cont.activate(self.motion)

    def eat(self):
        fac = 1.0
        if self.genome.stomach_load.value < self.genome.stomach_size.value:
            self.genome.stomach_load.value += self.genome.mandible_size.value * fac
        else:
            self.genome.is_hungry.value == False
            self.state = 3

        print ("eating: ",self.track.object)
        
    def digest(self):
        self.genome.stomach_load.value -= self.genome.energy_usage.value
        if self.genome.stomach_load.value < self.genome.eat_treshold.value:
            self.genome.is_hungry.value = True
        if self.genome.stomach_load.value < 0.0:
            self.die()

    def die(self):
        if ob["Pointer"] in self.owner.childrenRecursive:
            ob["Pointer"].removeParent()
        self.owner.endObject()

    def copulate(self):
        if self.track.object["bot"].genome.sex != self.genome.sex:
            if self.genome.sex.value == 0:
                if not self.genome.is_pregnant.value:
                    self.father_genome = self.track.object["bot"].genome
                    self.genome.is_pregnant.value = True
                

    def give_birth(self):
        child = sce.addObject(self.owner.name, self.owner, 0)
        child["father_genome"] = self.father_genome
        self.genome.is_pregnant.value = False
        self.genome.pregnancy.value = 0


    def update_old(self):
        # things that must be dnne always:
        self.digest()

        # make decisiions
        # if no hit object, set. goto follow
        if self.state == 0:
            self.state = 1
            self.track.object = self.radar.hitObject

        # follow the hitObject
        elif self.state == 1:
            self.follow()


            # if taret reached, stopp
            if self.track.object != None:
                if self.owner.getDistanceTo(self.track.object) < 2.0:
                    if self.track.object.name == "Food":
                        if self.genome.is_hungry == True:
                            self.state = 2
                    else:
                        self.state = 1

        elif self.state == 2:
            self.stopp()
            self.eat()
            #self.walkaround()
            #self.state = 0
        #print (self.state)
        self.limit_positions()

    def update_bodyFunction(self):
        # things that must be done always:
        self.digest()

        if self.genome.is_pregnant.value == True:
            self.genome.pregnancy.value += self.genome.pregnancy_grow_factor.value

        if self.genome.pregnancy.value > self.genome.pregnancy_duration.value:
            self.give_birth()

        self.limit_positions()

    def update(self):
        self.update_bodyFunction()
        
        # make decisions
        # if self is in initialstaten 0, goto state 1 "follow"

        # initial state (0):
        if self.state == 0:
            self.state = 1

        # if in "follow" mode (1):
        elif self.state == 1:
            if self.radar.positive:
                self.track.object = self.radar.hitObject
               
            # follow the hitObject
            if self.track.object != None:
                # if hungry, stopp and eat
                
                if self.track.object.name == "Food" and self.genome.is_hungry.value == True:
                    #print ("moving to state2")
                    self.state = 2

                elif self.track.object.name == "bot" and self.genome.is_horny.value == True:
                    self.follow()

                # if target reached, stop
                if self.owner.getDistanceTo(self.track.object) < 2.0:
                    if self.track.object.name == "Food":
                        if self.genome.is_hungry.value == True:
                            self.state = 2

                    elif self.track.object.name == "bot":
                        if self.genome.is_horny.value == True:
                            self.copulate()
                            self.state = 0
                    else:
                        self.state = 1

        # if in "eat" mode (2)
        elif self.state == 2:
            self.stopp()
            self.eat()
            #self.walkaround()
            #self.state = 0

        # if in "walkaround" mode (3)     
        elif self.state == 3:
            self.walkaround()
            
        

        # debugging
        if self is ob["Camera"]["selectedBot"]: 
            print (self.state)
            #print (self.id)
   
def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        own["init"] = True
    else:
        own["bot"].update()