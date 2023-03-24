import bge
import random
G = bge.logic
#cont = G.getCurrentController()
sce = G.getCurrentScene()
#ob = sce.objects

class Genome:
    pass 

class Bot():
    
    def __init__(self,cont):
        # define: controller sensors, actuators
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.radar = self.cont.sensors["Radar"]
        self.collision = self.cont.sensors["Collision"]
        self.motion = self.cont.actuators["Motion"]
        self.track = self.cont.actuators["Track"]
        self.father_genome = ""
        self.task = "walkaround"
        self._task= "walkaround"
        self.target = None
        

        # gets genome
        self.setGenome()

        #reset to birthage
        self.genome["age"] = 0

        # sets Properties og the genome 
        self.update_Properties()

    @property
    def task(self):
        return self._task
    
    @task.setter
    def task(self, value):
        if hasattr(self,"genome"):
            #print (self.owner["decision_time"],self.genome["decision_time"])
            if self.owner["decision_time"] > self.genome["decision_time"]:
                self._task = value
                self.owner["decision_time"] =0
                # if hasattr(self, "task"):
                #     print (self._task)

    def createChildGenom(self):
        child_genome = {}
        
        for mother in self.genome.keys():
            for father in self.father_genome.keys():
                if mother == father:
                    value = (self.genome[mother] + self.father_genome[father])/2
                    if type(self.genome[mother]) is float: 
                        child_genome[mother] = value
                    elif type(self.genome[mother]) is int:
                        child_genome[mother] = int(value)

        return child_genome
           
    def setGenome(self):
        # if self is a spawned bot
        if self.owner["genome"] == "":
            # set properties to genome
            self.genome = {'speed': 0.03999485472564734, 
                        'max_speed': 0.26692713899472725,
                        'max_rotation': 0.04739626947680464, 
                        'track_time': 36, 
                        'age': 0, 
                        'max_age': 408, 
                        'generation': 0, 
                        'always_skippedTicks': 2, 
                        'always_seed': 54, 
                        'radar_skippedTicks': 48,
                        "radar_skippedTicks":0, 
                        'collision_skippedTicks':57, 
                        'radar_angle': 61, 
                        'radar_distance': 24, 
                        'sex': 0, 
                        'pregnancy': 0, 
                        'is_pregnant': 0, 
                        'pregnancy_duration': 150, 
                        'worldsize': G.globalDict["size"], 
                        'size': 1,
                        "energy":1000.0,
                        "hunger":250,
                        "decision_time":1.0,
                        "growth_rate":0.025}
            self.setRandomGenome()
        # if self is a child
        else:
            # if it is a newborn, get genome from mother
            self.genome = self.owner["genome"]

            #self.owner["genome"]
            self.genome["generation"] = self.owner["generation"]
            self.genome["sex"] = random.randint(0,1)
            self.genome["size"] = self.genome["size"]/5
            self.genome["energy"] = 1000.0
            self.owner.scaling = (self.genome["size"],self.genome["size"],self.genome["size"])
    def setRandomGenome(self):
        self.genome["speed"] = random.uniform(0.001,0.5)#0.05
        self.genome["max_speed"] = random.uniform(0.05,0.5)#0.25
        self.genome["max_rotation"] = random.uniform(0.001,0.25)#0.05
        self.genome["track_time"] = random.randint(1,40)#15
        self.genome["age"] = 0
        self.genome["max_age"] = random.randint(250,700)#1000
        self.genome["generation"] = 0
        # ticrates
        self.genome["always_skippedTicks"] = random.randint(1,50)#7
        self.genome["always_seed"] = random.randint(0,100)#40
        
        #print (cont.sensors)
        self.genome["radar_skippedTicks"] = random.randint(0,50)#0
        self.genome["collision_skippedTicks"] = random.randint(0,100)#0
        
        # radar
        #self.genome["radar_angle"] = random.randint(0,180)#60
        #cont.sensors["Radar"].angle = self.radar_angle 
        self.genome["radar_distance"] = random.randint(0,30)#30
        #cont.sensors["Radar"].distance = self.radar_distance

        # if self pregnancy reaches treshold, bot get pregnant,
        # if if pregant, after pregnancy_duration Bot sets birth
        self.genome["sex"] = random.randint(0,1)
        self.genome["pregnancy"] = 0
        self.genome["is_pregnant"] = 0
        self.genome["pregnancy_duration"] = random.randint(int(self.genome["max_age"]/100),int((self.genome["max_age"]-self.genome["age"])/2))

        #props =[p for p in dir(Bot) if isinstance(getattr(Bot,p),property)]
        #print (props) 

    
        self.genome["worldsize"] = G.globalDict["size"]
        self.genome["size"] = 1#random.uniform(0.5,1.5)
        self.genome["decision_time"] = random.uniform(1.0,5.0)
        self.genome["growth_rate"] = random.uniform(0.01,0.035)
        self.genome["hunger"] = random.randint(int(self.genome["energy"]/5),int(self.genome["energy"]/3))
        #cont.owner.scaling = (self.size,self.size,self.size)

    def update_Properties(self):
        self.always.skippedTicks = self.genome["always_skippedTicks"]
        self.always.seed = self.genome["always_seed"]
        self.radar.skippedTicks = self.genome["radar_skippedTicks"]
        #self.radar.distance = self.genome["radar_distance"]#not writeable!!
        #self.owner.children["RadarCone"].visible = False
        #self.owner.children["RadarCone"].scaling = (self.genome["radar_distance"],self.genome["radar_distance"],self.genome["radar_distance"])

        self.collision.skippedTicks = self.genome["collision_skippedTicks"]
        if self.genome["sex"] == 1:
            self.owner.replaceMesh("maleBeetle",True,True)
        else:
            self.owner.replaceMesh("femaleBeetle",True,True)

    def die(self):
        self.owner.endObject()
        G.globalDict["bots"] -=1

    def give_birth(self):
        # reset reproduction props
        self.genome["pregnancy"] = 0
        self.genome["is_pregnant"] = 0

        # create a child
        newborn = sce.addObject("Bot",self.owner,0.0)
        space = 5
        r = random.randint(-1,1)
        if r == 0:
            r = 1
        newborn.worldPosition.x = self.owner.worldPosition.x + (space * r)
        newborn.worldPosition.y = self.owner.worldPosition.y + (space * r)

        # give the genome of the mother to the child
        newborn["genome"] = self.createChildGenom()
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
        self.task = "walkaround"
        self.motion.dLoc = (0.0,random.uniform(self.genome["speed"], self.genome["max_speed"]),0.0)
        self.motion.dRot = ((0.0,0.0,random.uniform(-self.genome["max_rotation"],self.genome["max_rotation"])))
        self.cont.activate(self.motion)

    def debug(self):
        if self.track.object != None:

            bge.render.drawLine(self.owner.worldPosition,self.track.object.worldPosition,(1,1,1,1))
        #if self.task != "follow":
            #print (self.task)

    def limit_positions(self):
        buffer = 10
        if self.owner.worldPosition.x > self.genome["worldsize"]:
            self.owner.worldPosition.x = -self.genome["worldsize"]+buffer
        if self.owner.worldPosition.x < -self.genome["worldsize"]:
            self.owner.worldPosition.x = self.genome["worldsize"]-buffer
        if self.owner.worldPosition.y > self.genome["worldsize"]:
            self.owner.worldPosition.y = -self.genome["worldsize"]+buffer
        if self.owner.worldPosition.y < -self.genome["worldsize"]:
            self.owner.worldPosition.y = self.genome["worldsize"]-buffer

        self.owner.worldPosition.z = 0
        #print (self.owner.worldPosition)

    def follow(self):
        self.task = "follow"
        cont = self.cont
        radar = self.radar
        motion = self.motion
        track = self.track

        # only folloe something if no target is reached
        if self.target != None:
            return
        
        if radar.positive:
            track.time = self.genome["track_time"]
            
            motion.dRot = (0.0,0.0,0.0)
            motion.dLoc = (0.0,random.uniform(self.genome["speed"], self.genome["max_speed"]),0.0)
            #print ("got something on my radar!")

            if radar.hitObject.name == "Food":
                if self.genome["energy"] < self.genome["hunger"] or self.genome["size"] < 1.0:
                    #r = random.randint(0,len(radar.hitObjectList))
                    track.object = radar.hitObject
                    cont.activate(track)
                    motion.dLoc = (0.0,random.uniform(self.genome["speed"], self.genome["max_speed"])*1.5,0.0)
                    cont.activate(motion)
                    #set the target to make shure it follows until it reaches it
                    self.target = radar.hitObject
                    print ("i am hungry!, heading for food!")
                
            if radar.hitObject.name == "Bot":
                
                if "bot" in radar.hitObject:
                    #print ("got a bot in my radar")
                    # if not hasattr(radar.hitObject["bot"], "genome"):
                    #     return
                    # if hasattr(radar.hitObject["bot"].genome,"sex"):
                    #     print ("follow: OK")
                    if self.genome["size"] < 1.0:
                        return
                    try:
                        if radar.hitObject["bot"].genome["sex"] != self.genome["sex"]:
                            track.object = radar.hitObject
                            cont.activate(track)
                            motion.dLoc = (0.0,random.uniform(self.genome["speed"], self.genome["max_speed"])*1.5,0.0)
                            cont.activate(motion)
                            self.target = radar.hitObject
                    except:
                        pass
                        #print ("founnd partner!")

                    # else:
                    #     track.object = radar.hitObject
                    #     cont.activate(track)
                    #     motion.dLoc = (0.0,random.uniform(self.genome["speed"], self.genome["max_speed"])*1.5*-1,0.0)
                    #     cont.activate(motion)
                        #print ("avoiding conflicts with other!")
        #print (self.track.object, track.object)                
    def collide(self):
        coll = self.collision
        if coll.positive:
            #print ("OK")
            if coll.hitObject.name == "Food":
                # if is hungry, follow the food
                if self.genome["energy"] < self.genome["hunger"]:
                    coll.hitObject["energy"] -=1
                    self.genome["energy"] +=1
                    self.genome["size"] += self.genome["growth_rate"]#0.01

                    self.owner.scaling = (self.genome["size"],self.genome["size"],self.genome["size"])
                    self.target = None
                    print ("i am eating!")
                if self.genome["size"] < 1.0:
                    coll.hitObject["energy"] -=1
                    self.genome["energy"] +=1
                    self.genome["size"] += self.genome["growth_rate"]
                    print ("i am eating, because i need to grow!")
                self.owner["decision_time"] = 0.0
                self.wait()
            if coll.hitObject.name == "Bot":
                # if hitObject is not initialized
                if not hasattr(coll.hitObject["bot"], "genome"):
                    return

                # if inititialised, check for sex
                if coll.hitObject["bot"].genome["sex"] != self.genome["sex"]:

                    # if self is female, get pregnant
                    if self.genome["sex"] == 0:
                        if self.genome["is_pregnant"] == 0:
                            G.globalDict["pregnants"] +=1
                            self.genome["is_pregnant"] = 1
                            # give the genomes to mother
                            self.father_genome = coll.hitObject["bot"].genome
                            self.wait()
                            self.target = None                  
    def update(self):
        if self.always.positive:
            #self.debug()
            # let them die if too old or no energy
            if self.genome["age"] > self.genome["max_age"]:
                self.die()
            else:
                self.genome["age"] += 1
            self.genome["energy"] -= 1
            if self.genome["energy"] < 0:
                self.die()
            
            if self.genome["is_pregnant"] == 1:
                self.genome["pregnancy"] += 1
                
                # give birth
                if self.genome["pregnancy"] > self.genome["pregnancy_duration"]:
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

def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        own["init"] = True
    else:
        self = own["bot"]
        self.update()

