import bge
import random
G = bge.logic
#cont = G.getCurrentController()
sce = G.getCurrentScene()
ob = sce.objects


"""
import math
pi = math.pi

choice = input ("Enter a number between 1-5:")
choice = int (choice)

if choice == 1:
radius = float(input ("Enter x:"))
area = ( radius ** 2 ) * pi
print ("The Area of the circle is, " + str(area))
"""
class Species():
    
    def __init__(self,cont) -> None:
        
        self.speed = random.uniform(0.01,0.05)#0.05
        self.max_speed = random.uniform(0.05,0.35)#0.25
        self.max_rotation = random.uniform(0.001,0.05)#0.05
        self.track_time = random.randint(0,50)#15
        self.age = 0
        self.max_age = random.randint(250,1000)#1000
        self.generation = 0
        # ticrates
        self.always_ticrate = random.randint(1,15)#7
        self.always_seed = random.randint(0,100)#40
        
        #print (cont.sensors)
        self.radar_ticrate = random.randint(0,50)#0
        self.collision_ticrate = random.randint(0,100)#0
        
        # radar
        self.radar_angle = random.randint(0,180)#60
        #cont.sensors["Radar"].angle = self.radar_angle 
        self.radar_distance = random.randint(5,50)#30
        #cont.sensors["Radar"].distance = self.radar_distance

        # if self pregnancy reaches treshold, bot get pregnant,
        # if if pregant, after pregnancy_duration Bot sets birth
        self.sex = random.randint(0,1)
        self.pregnancy = 0
        self.is_pregnant = 0
        self.pregnancy_duration = random.randint(int(self.max_age/10),int(self.max_age/2))

        #props =[p for p in dir(Bot) if isinstance(getattr(Bot,p),property)]
        #print (props) 

    
        self.worldsize = G.globalDict["size"]
        self.size = 1#random.uniform(0.5,1.5)
        cont.owner.scaling = (self.size,self.size,self.size)


class Bot(Species):
    def __init__(self,cont):
        super().__init__(cont)
        self.species = Species(cont)
        #print(self.species.__dict__["speed"])
        
    def die(self,cont):
        cont.owner.endObject()
        G.globalDict["bots"] -=1

    def update_(self,cont):
        if self.age > self.max_age:
            self.die(cont)
        else:
            self.age += 1
        self.walkaround(cont)
        self.limit_positions(cont)
        
    def radar(self,cont):
        #cont.sensors["Radar"].angle = self.radar_angle 
        self.follow(cont)
        #print ("radar")  
    def walkaround(self,cont):
        motion = cont.actuators["Motion"]
        motion.dLoc = (0.0,random.uniform(self.speed, self.max_speed),0.0)
        motion.dRot = ((0.0,0.0,random.uniform(-self.max_rotation,self.max_rotation)))
        cont.activate(motion)
    def give_birth(self,cont):
        own = cont.owner
        newborn = sce.addObject("Bot",own,0.0)
        
        newborn["bot"] = Bot(cont) 
        newborn["bot"].__init__(cont)
        newborn["bot"].__dict__ = own["bot"].__dict__
        newborn["bot"].generation += 1
        
         
        G.globalDict["bots"] +=1
        #print ("give_birth(self,cont): ", newborn["bot"].__dict__)

    def collision(self,cont):
        own = cont.owner
        coll = cont.sensors["Collision"]
        if coll.positive:
            
            if coll.hitObject.name == "Food":
                #print ("collsion",coll.hitObject)
                coll.hitObject["energy"] -=1
                self.species.size += 0.01
                cont.owner.scaling = (self.size,self.size,self.size)
            
            if coll.hitObject.name == "Bot":
                if "bot" in coll.hitObject:
                    if hasattr(coll.hitObject["bot"],"sex"):
                        if coll.hitObject["bot"].sex != own["bot"].sex:
                            if own["bot"].sex == 0:
                                own["bot"].pregnancy += 1
                                if own["bot"].pregnancy > own["bot"].pregnancy_duration:
                                    self.give_birth(cont)
                                    own["bot"].pregnancy = 0

                                    
            
    def follow(self,cont):
        own = cont.owner
        radar = cont.sensors["Radar"]
        motion = cont.actuators["Motion"]
        track = cont.actuators["Track"]

        if radar.positive:
            track.time = self.track_time
            
            motion.dRot = (0.0,0.0,0.0)
            motion.dLoc = (0.0,random.uniform(self.speed, self.max_speed),0.0)
            rh = radar.hitObject

            if rh.name == "Food":
                #r = random.randint(0,len(radar.hitObjectList))
                
                
                track.object = rh
                cont.activate(track)
                motion.dLoc = (0.0,random.uniform(self.speed, self.max_speed)*1.5,0.0)
                cont.activate(motion)
            if rh.name == "Bot":
                if "bot" in rh:
                    #print ("bot")
                    if hasattr(rh["bot"],"sex"):
                        #print ("OK")
                
                        if rh["bot"].sex != own["bot"].sex:
                            track.object = radar.hitObject
                            cont.activate(track)
                            motion.dLoc = (0.0,random.uniform(self.speed, self.max_speed)*1.5,0.0)
                            cont.activate(motion)
                        else:
                            
                        
                            track.object = radar.hitObject
                            cont.activate(track)
                            motion.dLoc = (0.0,random.uniform(self.speed, self.max_speed)*1.5*-1,0.0)
                            cont.activate(motion)
                


    def limit_positions(self,cont):
        own = cont.owner
        
        if own.worldPosition.x > self.worldsize:
            own.worldPosition.x = -self.worldsize
        if own.worldPosition.x < -self.worldsize:
            own.worldPosition.x = self.worldsize
        if own.worldPosition.y > self.worldsize:
            own.worldPosition.y = -self.worldsize
        if own.worldPosition.y < -self.worldsize:
            own.worldPosition.y = self.worldsize
        own.worldPosition.z = 0
        
    def debug(self,cont):
        print ("____________________________________________")
        print ("debugging: ", self, cont.owner)
        for i in self.__dict__.keys():
            print (i, self.__dict__[i])

def main(cont):
    own = cont.owner
    if not "init" in own:
        own["bot"] = Bot(cont)
        cont.sensors["Always"].skippedTicks = own["bot"].always_ticrate
        cont.sensors["Always"].seed = own["bot"].always_seed
        cont.sensors["Radar"].skippedTicks = own["bot"].radar_ticrate
        cont.sensors["Collision"].skippedTicks = own["bot"].collision_ticrate
        
        own["init"] = True
    else:
        
        own["bot"].update_(cont)

def radar(cont):
    own = cont.owner
    
    if "init" in own:
        """
        # attribute 'angle' of 'SCA_RadarSensor' objects is not writable

        radar = cont.sensors["Radar"]
        radar.angle = own["bot"].radar_angle
        """
        own["bot"].radar(cont)

def collision_(cont):
    own = cont.owner
    if "init" in own:
        own["bot"].collision(cont)

def debug_(cont):
    own = cont.owner
    if "init" in own:
        own["bot"].debug(cont)
