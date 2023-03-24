import bge
import random
from dataclasses import dataclass,fields
G = bge.logic
@dataclass
class Genome:
    speed: float 
    max_speed: float
    max_rotation: float 
    track_time: int 
    age: int 
    max_age: int 
    generation: int 
    always_skippedTicks: int 
    always_seed: int 
    radar_skippedTicks: int 
    collision_skippedTicks:int 
    radar_angle: int 
    radar_distance: int 
    sex: int 
    pregnancy: int 
    is_pregnant:int 
    pregnancy_duration: int 
    worldsize: G.globalDict["size"] 
    size:int
    energy:float
    energy_max:int
    stomach_size:int
    stomach_load:int
    eat_treshold:int 
    is_hungry:bool
    decision_time:1.0
    growth_rate:float

class Digestion:
    def hungry(self):
        #print (self.genome)
        if self.genome.stomach_load < self.genome.eat_treshold:
            self.genome.is_hungry = True
        else:
            self.genome.is_hungry = False
        return self.genome.is_hungry
    def eat(self):
        #d = self.owner.getdDistaneTo(self.track.object)
        food = self.radar.hitObject
        print("OKOKKOKO")
        if not food == None: 
            
            food["energy"] -= 1
            self.genome.stomach_load += 2
            if food["energy"] < 0:
                food.endObject()
            self.hungry()
class TaskManager:
    def __init__(self):
        self.calls = 0
        self.tasks = []
        self.is_busy = False
        self.target_reached =  False
        self.start_time = 0.0
        self.activities = {"radar":0,"always":0,"track":0,"motion":0}
    def getActivities(self):
        self.activities["radar"] = self.cont.sensors["radar"].positive
        self.activities["always"] = self.cont.sensors["always"].positive
        #self.activities["track"] = self.cont.actuators["track"].
        return self.activities

class SteeringFunctions:
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
    
    def seek(self):
        if self.radar.hitObject != None:
            self.steering.target = self.radar.hitObject 
            self.steering.behavior = random.randint(0,2)
            self.cont.activate(self.steering)
    
    def walkaround(self):
        self.cont.deactivate(self.track)
        #self.task = "walkaround"
        self.motion.dLoc = (0.0,random.uniform(self.genome.speed, self.genome.max_speed),0.0)
        self.motion.dRot = ((0.0,0.0,random.uniform(-self.genome.max_rotation,self.genome.max_rotation)))
        self.cont.activate(self.motion)
class Sequence:
    def __init__(self, length, task):
        self.length = length
        self.task = task



class GenomeFunctions:
    def createChildGenome(self):
        child_genome = self.genome
        for mother_gene in fields(self.genome):
            for father_gene in fields(self.father_genome):
                if mother_gene == father_gene:
                    mvalue = getattr(self.genome, mother_gene.name)
                    fvalue = getattr(self.father_genome, father_gene.name)
                    value = (mvalue + fvalue)/2
                    
                    if type(getattr(self.genome, mother_gene.name)) == int:
                        value = int(value)
                        
                    if type(getattr(self.genome, mother_gene.name)) == float:
                        value = float(value)
                        
                    setattr(child_genome,mother_gene.name,value)
                        
        return child_genome
           
    def setGenome(self):
        # if self is a spawned bot
        if self.owner["genome"] == "":
            # set properties to genome
            self.genome = Genome(speed= 0.03999485472564734, 
                        max_speed= 0.26692713899472725,
                        max_rotation= 0.04739626947680464, 
                        track_time= 36, 
                        age= 0, 
                        max_age= 408, 
                        generation= 0, 
                        always_skippedTicks= 2, 
                        always_seed= 54, 
                        radar_skippedTicks= 48,
                        collision_skippedTicks=57, 
                        radar_angle= 61, 
                        radar_distance= 24, 
                        sex= 0, 
                        pregnancy= 0, 
                        is_pregnant= 0, 
                        pregnancy_duration= 150, 
                        worldsize= G.globalDict["size"], 
                        size= 1,
                        energy=1000.0,
                        energy_max=1050,
                        stomach_size=250,
                        eat_treshold = 150,
                        stomach_load = 0,
                        is_hungry = True,
                        decision_time=200.0,
                        growth_rate=0.025)
            self.setRandomGenome()
        # if self is a child
        else:
            # if it is a newborn, get genome from mother
            self.genome = self.owner["genome"]

            #self.owner["genome"]
            self.genome.generation = self.owner["generation"]
            self.genome.sex = random.randint(0,1)
            self.genome.size = self.genome.size/5
            self.genome.energy = 1000.0
            self.owner.scaling = (self.genome.size,self.genome.size,self.genome.size)
    def setRandomGenome(self):
        self.genome.speed = random.uniform(0.001,0.3)#0.05
        self.genome.max_speed = random.uniform(0.05,0.3)#0.25
        self.genome.max_rotation = random.uniform(0.001,0.35)#0.05
        self.genome.track_time = random.randint(1,40)#15
        self.genome.age = 0
        self.genome.max_age = random.randint(250,700)#1000
        self.genome.generation = 0
        # ticrates
        self.genome.always_skippedTicks = random.randint(1,50)#7
        self.genome.always_seed = random.randint(0,100)#40
        self.genome.radar_skippedTicks = random.randint(0,50)#0
        self.genome.collision_skippedTicks = random.randint(0,100)#0
        
        # radar
        self.genome.radar_distance = random.randint(0,30)#30

        # if self pregnancy reaches treshold, bot get pregnant,
        # if if pregant, after pregnancy_duration Bot sets birth
        self.genome.sex = random.randint(0,1)
        self.genome.pregnancy = 0
        self.genome.is_pregnant = 0
        self.genome.pregnancy_duration = random.randint(int(self.genome.max_age/100),int((self.genome.max_age-self.genome.age)/2))

        self.genome.worldsize = G.globalDict["size"]
        self.genome.size = 1#random.uniform(0.5,1.5)
        self.genome.decision_time = random.uniform(1.0,5.0)
        self.genome.growth_rate = random.uniform(0.01,0.035)
        self.genome.stomach_size = random.randint(int(self.genome.energy/5),int(self.genome.energy/3))
    def horny(self):
        if hasattr(self.radar.hitObject, "bot"):
            if self.genome["sex"] != self.radar.hitObject["bot"].genome["sex"]:
                if self.genome["sex"] == 1:
                    return True
                else:
                    return False



