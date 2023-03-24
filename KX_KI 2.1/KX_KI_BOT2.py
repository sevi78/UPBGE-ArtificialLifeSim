import bge
import random
#import dataclasses
from dataclasses import dataclass,fields
from KX_KI_DATACLASS import Genome,GenomeFunctions
G = bge.logic
#cont = G.getCurrentController()
sce = G.getCurrentScene()
#ob = sce.objects

class Bot(GenomeFunctions):
    
    def __init__(self,cont):
        # define: controller sensors, actuators
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.radar = self.cont.sensors["Radar"]
        #self.collision = self.cont.sensors["Collision"]
        self.motion = self.cont.actuators["Motion"]
        self.track = self.cont.actuators["Track"]
        self.father_genome = ""
        self.task = "walkaround"
        self._task= "walkaround"
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

    # def createChildGenom(self):
    #     child_genome = self.genome
        
    #     for mother in self.genome.keys():
    #         for father in self.father_genome.keys():
    #             if mother == father:
    #                 value = (self.genome[mother] + self.father_genome[father])/2
    #                 if type(self.genome[mother]) is float: 
    #                     child_genome[mother] = value
    #                 elif type(self.genome[mother]) is int:
    #                     child_genome[mother] = int(value)

    #     return child_genome
   

    def update_Properties(self):
        self.always.skippedTicks = self.genome.always_skippedTicks
        self.always.seed = self.genome.always_seed
        self.radar.skippedTicks = self.genome.radar_skippedTicks
        #self.collision.skippedTicks = self.genome.collision_skippedTicks
        if self.genome.sex == 1:
            self.owner.replaceMesh("maleBeetle",True,True)
        else:
            self.owner.replaceMesh("femaleBeetle",True,True)

    def die(self):
        self.owner.endObject()
        G.globalDict["bots"] -=1

    def give_birth(self):
        # reset reproduction props
        self.genome.pregnancy = 0
        self.genome.is_pregnant = 0

        # create a child
        newborn = sce.addObject("Bot",self.owner,0.0)
        space = 5
        r = random.randint(-1,1)
        if r == 0:
            r = 1
        newborn.worldPosition.x = self.owner.worldPosition.x + (space * r)
        newborn.worldPosition.y = self.owner.worldPosition.y + (space * r)

        # give the genome of the mother to the child
        newborn["genome"] = self.createChildGenome()
        newborn["generation"] += 1

        G.globalDict["bots"] +=1
        G.globalDict["pregnants"] -=1
        #print ("give_birth:",newborn["genome"])

    def wait(self):
        self.task = "wait"
        self.track.object = None
        self.motion.dLoc = (0,0,0)
        self.motion.dRot = (0,0,0)

    def walkaround(self):
        self.cont.deactivate(self.track)
        #self.task = "walkaround"
        self.motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed),0.0)
        self.motion.dRot = ((0.0,0.0,random.uniform(-self.genome.max_rotation,self.genome.max_rotation)))
        self.cont.activate(self.motion)
    def debug(self):
        # w = self.cont.sensors["W"]
        # f = self.cont.sensors["F"]
        # p = self.cont.sensors["P"]
        # if f.positive:
        #     self.follow()
        # if w.positive:
        #     self.walkaround
        # if p.positive:
        #     self.wait()

        # print ("debug: ")
        #self.task)
        
        self.update()





    def drawline(self):
        if self.track.object != None:
            bge.render.drawLine(self.owner.worldPosition,self.track.object.worldPosition,(1,1,1,1))

    def limit_positions(self):
        buffer = 10
        if self.owner.worldPosition.x > self.genome.worldsize:
            self.owner.worldPosition.x = -self.genome.worldsize+buffer
        if self.owner.worldPosition.x < -self.genome.worldsize:
            self.owner.worldPosition.x = self.genome.worldsize-buffer
        if self.owner.worldPosition.y > self.genome.worldsize:
            self.owner.worldPosition.y = -self.genome.worldsize+buffer
        if self.owner.worldPosition.y < -self.genome.worldsize:
            self.owner.worldPosition.y = self.genome.worldsize-buffer

        self.owner.worldPosition.z = 0
    def eat(self):
        self.task = "eat"
        motion = self.motion
        track = self.track
        self.genome.energy += 1
        if self.radar.hitObject.name == "Food":
            self.radar.hitObject["energy"] -= 1
        if self.genome.energy < self.genome.energy_max:
            motion.dRot = (0.0,0.0,random.uniform(0, self.genome.max_rotation))
            motion.dLoc = (0.0,0.0,0.0)
        else:
            self.task = "walkaround"
            self.walkaround()
        print ("eat:", self.genome.energy,self.genome.energy_max)
    def follow(self):
        #self.task = "follow"
        cont = self.cont
        radar = self.radar
        motion = self.motion
        track = self.track

        # # only folloe something if no target is reached
        # if self.target != None:
        #     print("follow(self): no target found")
        #     return
        
        if radar.positive:
            track.object = radar.hitObject
            #print("follow(self): radar.positive:")
            track.time = self.genome.track_time
            
            motion.dRot = (0.0,0.0,random.uniform(-self.genome.max_rotation, self.genome.max_rotation))
            motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed),0.0)
            #print ("got something on my radar!")

            if radar.hitObject.name == "Food":
                if self.genome.energy < self.genome.energy_max:

                    #if self.genome.energy < self.genome.hunger or self.genome.size < 1.0:
                    #r = random.randint(0,len(radar.hitObjectList))
                    d = self.owner.getDistanceTo(radar.hitObject)
                    cont.activate(track)
                    motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed)*d/10,0.0)
                    cont.activate(motion)
                    #set the target to make shure it follows until it reaches it
                    #self.target = radar.hitObject
                    #print(d)
                    if d < 3.5:
                        print ("OK")
                        self.task = "eat"
                        self.eat()
                        self.collide()
                #print ("i am hungry!, heading for food!")
                
            if radar.hitObject.name == "Bot":
                #print("follow(self): radar.positive: radar.hitObject.name == Bot:")
                if "bot" in radar.hitObject:
                    #print ("got a bot in my radar")
                    # if not hasattr(radar.hitObject.bot, "genome"):
                    #     return
                    # if hasattr(radar.hitObject.bot.genome,"sex"):
                    #     print ("follow: OK")
                    if self.genome.size < 1.0:
                        return
                    
                        #print("follow(self): radar.positive: radar.hitObject.name == Bot:")
                    if not hasattr(radar.hitObject["bot"].genome, "sex"):
                        return

                    if radar.hitObject["bot"].genome.sex != self.genome.sex:
                        track.object = radar.hitObject
                        cont.activate(track)
                        motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed)*1.5,0.0)
                        cont.activate(motion)
                        self.target = radar.hitObject
                    
                        #print ("founnd partner!")

                    # else:
                    #     track.object = radar.hitObject
                    #     cont.activate(track)
                    #     motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed)*1.5*-1,0.0)
                    #     cont.activate(motion)
                        #print ("avoiding conflicts with other!")
        #print (self.track.object, track.object)                
    def collide(self):
        coll = self.radar
        if coll.positive:
            #print ("OK")
            if coll.hitObject.name == "Food":
                # if is hungry, follow the food
                if self.genome.energy < self.genome.hunger:
                    coll.hitObject["energy"] -=1
                    self.genome.energy +=1
                    self.genome.size += self.genome.growth_rate#0.01

                    self.owner.scaling = (self.genome.size,self.genome.size,self.genome.size)
                    self.target = None
                    print ("i am eating!")
                if self.genome.size == 1.0:
                    coll.hitObject["energy"] -=1
                    self.genome.energy +=1
                    self.genome.size += self.genome.growth_rate
                    print ("i am eating, because i need to grow!")
                self.owner["decision_time"] = 0.0
                self.wait()
            if coll.hitObject.name == "Bot":
                # if hitObject is not initialized
                if not hasattr(coll.hitObject["bot"], "genome"):
                    return

                # if inititialised, check for sex
                if coll.hitObject["bot"].genome.sex != self.genome.sex:

                    # if self is female, get pregnant
                    if self.genome.sex == 0:
                        if self.genome.is_pregnant == 0:
                            G.globalDict["pregnants"] +=1
                            self.genome.is_pregnant = 1
                            # give the genomes to mother
                            self.father_genome = coll.hitObject["bot"].genome
                            self.wait()
                            self.target = None 
                            print("got pregnant!")                 
    def update_o(self):
        if self.always.positive:
            #self.debug()
            # let them die if too old or no energy
            if self.genome.age > self.genome.max_age:
                self.die()
            else:
                self.genome.age += 1
            self.genome.energy -= 1
            if self.genome.energy < 0:
                self.die()
            
            if self.genome.is_pregnant == 1:
                self.genome.pregnancy += 1
                
                # give birth
                if self.genome.pregnancy > self.genome.pregnancy_duration:
                    self.give_birth()

            self.walkaround()
            
        elif self.radar.positive:
            #print (self.radar.hitObject)# Bot, Food
            self.follow()
            
        elif self.collision.positive:
            #print (self.collision.hitObject) Bot, Food
            self.collide()
        else:
            if self.target == None:
                self.wait()
        
        self.limit_positions()
    
    def update(self):
        self.limit_positions()
        if self.radar.positive:
            #print (self.radar.hitObject)# Bot, Food
            if not self.task == "eat":
                self.task = "follow"
        exec("self." + self.task + "()")
        self.genome.energy -= 1
        self.limit_positions()
        #if self.always.positive:
            #self.debug()
            
            
            
        # elif self.radar.positive:
        #     #print (self.radar.hitObject)# Bot, Food
        #     self.follow()
            
        # elif self.collision.positive:
        #     #print (self.collision.hitObject) Bot, Food
        #     self.collide()
        # else:
        #     if self.target == None:
        #         self.wait()
        
        # # let them die if too old or no energy
        #     if self.genome.age > self.genome.max_age:
        #         self.die()
        #     else:
        #         self.genome.age += 1
            
        #     if self.genome.energy < 0:
        #         self.die()
            
        #     if self.genome.is_pregnant == 1:
        #         self.genome.pregnancy += 1
                
        #         # give birth
        #         if self.genome.pregnancy > self.genome.pregnancy_duration:
        #             self.give_birth()

        # self.genome.energy -= 1
        # self.limit_positions()

def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        own["init"] = True
    else:
        self = own["bot"]
        self.update()
        #self.debug()



"""hi there, i know, it is an old topic, but still relevant. I run into a problem not litstet here: 

let say, we have an object, that replicates itself and overgive data to the child object--
For better understanding i try to explain it a little more, what causes the Problem. 

In a simulation of Bugs/Insects or similar. 
Once a object is born, it initialies itself:


```
 def main(cont):
     own = cont.owner
     if not "init" in own:
         own["bot"] = Bot(cont)
         own["init"] = True
     else:
         self = own["bot"]
         self.update()
```

by creating the Bot instance, the __init__(self) is run:


```
 def __init__(self,cont):
     self.setGenome()
```

self.setGenome basicly adds a Dataclass "Genome" into self.genome.

after some time, the Bugs interact with each other, the male gives its genome class to the female.
the female creates a new Genome Instance, with a mix of the Values of the mother and the Father.
after more time, the female reproduces itself:

```
newborn = sce.addObject("Bot",self.owner,0.0)
# here the code needs to wait somehow, wait for the initialisatin of the child
newborn["genome"] = self.createChildGenome()
```
here is the problem, because newborn is not initialised yet, gives Atribute error, because at this moment the property "bot" is still a string-
also other functions that needs acces to the class in own["bot"] will fail aslong the child is not initalised

-- At the moment of creation of the newborn, it needs a little time to initialize itself. BUT the parent wants to overgive the genom class already. Other bots checking the newborn for data they need to interact, needs to access to the own["bot"] of the child, but they cannot.
So i need to write a check for every function/interaction like:


```
if not hasattr(radar.hitObject.bot, "genome"):
        return
```

that leads to a lot of code repetition ... and its just ugly...

I am really scratching my head to solve the problem... maybe give a reference from the child to the parent? and then after some ticks, when it is initalized, ovrgive the class? 

Maybe some of you has a brilliant idea to solve it?


"""