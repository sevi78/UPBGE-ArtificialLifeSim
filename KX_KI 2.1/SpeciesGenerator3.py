import bge
import random
from dataclasses import dataclass,fields
from Genetics import Gene,Genome, GenomeHandler

G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects

class SpeciesGenerator(GenomeHandler):
    def __init__(self,cont):
        super().__init__()
        self.cont = cont 
        self.owner = self.cont.owner
        self.always = self.cont.sensors["Always"]
        self.keyboard = self.cont.sensors["Keyboard"]
        self.screenshot = self.cont.actuators["Screenshot"]

    def reset(self):
        # apply rotation
        for i in self.owner.childrenRecursive:
            i.worldOrientation = ([1.0, 0.0, 0.0], [ 0.0, 1.0, 0.0], [0.0, 0.0, 1.0])
            i.visible = True

    def setRandomColor(self):
        c = 0.4
        color = [ random.uniform(0.0,c),random.uniform(0.0,c),random.uniform(0.0,c),random.uniform(0.0,c)]
        for i in self.owner.childrenRecursive:
            i.color = color

    def setColor(self):
        color = [self.genome.color_r.value,
                 self.genome.color_g.value,
                 self.genome.color_b.value,
                 self.genome.color_a.value]
        
        self.owner.color = color
        for i in self.owner.childrenRecursive:
            i.color = color

    def applyRandomRotation(self):
        excluded = ["head","backbody","middle_body", "eye_l_clipart", "eye_r_clipart" ]
        
        # rotate the game object 1.570796327 radians (90 degrees)
        f = 0.2
        

        # use the world axis
        local = False

        # apply rotation
        for i in self.owner.childrenRecursive:
            if not i.name in excluded:
                rot = [ 0.0, 0.0, random.uniform(-f,f)]
                i.applyRotation(rot,local)

    def setBodyPartSize(self):
        headv = self.genome.decision_time.value
        heady = self.genome.always_skippedTicks.max/self.genome.always_skippedTicks.value/5
        headx = self.genome.radar_angle.value /200
        self.owner.childrenRecursive["head"].scaling = (headv-headx,heady,headv)
        self.owner.childrenRecursive["backbody"].scaling = (self.genome.stomach_load.value, self.genome.stomach_load.value*self.genome.speed.value*8, self.genome.stomach_load.value)
        self.owner.childrenRecursive["middle_body"].scaling = (self.genome.stomach_load.value, self.genome.stomach_load.value, self.genome.stomach_load.value)


        mandv = self.genome.stomach_load.value/self.genome.stomach_size.value
        self.owner.childrenRecursive["mandible_l"].scaling = (mandv,mandv,mandv)
        self.owner.childrenRecursive["mandible_r"].scaling = (mandv,mandv,mandv)

        self.owner.childrenRecursive["feeding_tools_l"].scaling = (self.genome.eat_treshold.value,self.genome.eat_treshold.value,self.genome.eat_treshold.value )
        self.owner.childrenRecursive["feeding_tools_r"].scaling = (self.genome.eat_treshold.value,self.genome.eat_treshold.value,self.genome.eat_treshold.value )

        #eyes
        eyev = 15
        self.owner.childrenRecursive["eyes_l"].scaling = (self.genome.radar_distance.value/eyev, self.genome.radar_distance.value/eyev, self.genome.radar_distance.value/eyev)
        self.owner.childrenRecursive["eyes_r"].scaling = (self.genome.radar_distance.value/eyev, self.genome.radar_distance.value/eyev, self.genome.radar_distance.value/eyev)
        
        self.owner.childrenRecursive["antennas_l"].scaling = (self.genome.radar_angle.value/self.genome.radar_angle.default, self.genome.radar_angle.value/self.genome.radar_angle.default, self.genome.radar_angle.value/self.genome.radar_angle.default)
        self.owner.childrenRecursive["antennas_r"].scaling = (self.genome.radar_angle.value/self.genome.radar_angle.default, self.genome.radar_angle.value/self.genome.radar_angle.default, self.genome.radar_angle.value/self.genome.radar_angle.default)
        
        
        # set legs
        legsize_fac = 3.0
        self.owner.childrenRecursive["legs_front_l"].scaling = (self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac)
        self.owner.childrenRecursive["legs_front_r"].scaling = (self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac)

        self.owner.childrenRecursive["legs_middle_l"].scaling = (self.genome.speed.value*1.2*legsize_fac, self.genome.speed.value*1.2*legsize_fac, self.genome.speed.value*1.2*legsize_fac)
        self.owner.childrenRecursive["legs_middle_r"].scaling = (self.genome.speed.value*1.2*legsize_fac, self.genome.speed.value*1.2*legsize_fac, self.genome.speed.value*1.2*legsize_fac)

        self.owner.childrenRecursive["legs_middle_l1"].scaling = (self.genome.speed.value*1.3*legsize_fac, self.genome.speed.value*1.3*legsize_fac, self.genome.speed.value*1.3*legsize_fac)
        self.owner.childrenRecursive["legs_middle_r1"].scaling = (self.genome.speed.value*1.3*legsize_fac, self.genome.speed.value*1.3*legsize_fac, self.genome.speed.value*1.3*legsize_fac)

        self.owner.childrenRecursive["legs_back_l"].scaling = (self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac)
        self.owner.childrenRecursive["legs_back_r"].scaling = (self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac, self.genome.speed.value*legsize_fac)


        
        # set the amount of legs
        if self.genome.legs.value in range(6,8):#6legs
            self.owner.childrenRecursive["legs_back_l"].visible = 0
            self.owner.childrenRecursive["legs_back_r"].visible = 0

        elif self.genome.legs.value in range(4,6):#4legs
            self.owner.childrenRecursive["legs_back_l"].visible = 0
            self.owner.childrenRecursive["legs_back_r"].visible = 0
            self.owner.childrenRecursive["legs_middle_l1"].visible = 0
            self.owner.childrenRecursive["legs_middle_r1"].visible = 0
        
        # finally set the clipart eyes to symetrical
        # print ("before:",self.owner.childrenRecursive["eye_l_clipart"].scaling)
        # x = self.owner.childrenRecursive["eye_l_clipart"].scaling.x
        # self.owner.childrenRecursive["eye_l_clipart"].scaling = (x,x,1.0)
        # self.owner.childrenRecursive["eye_r_clipart"].scaling = (x,x,1.0)

        self.owner.childrenRecursive["eye_l_clipart"].scaling.x = self.owner.childrenRecursive["eye_l_clipart"].scaling.y 
        self.owner.childrenRecursive["eye_r_clipart"].scaling.x = self.owner.childrenRecursive["eye_r_clipart"].scaling.y
        #print ("after:",self.owner.childrenRecursive["eye_l_clipart"].scaling)

    def makeScreenshot_doesnt_work(self):
        path = bge.logic.expandPath("//")
        path += "/generated_SpeciesTextures/"
        print ("makeScreenshot:" ,path)

        bge.render.makeScreenshot(path+"Testimage")

    def makeScreenshot(self):
        path = bge.logic.expandPath("//")
        path += "/generated_SpeciesTextures/"

        self.screenshot.fileName = "//generated_SpeciesTextures/Testimage.png"
        self.cont.activate(self.screenshot)

    def update(self):
        self.reset()
        self.setGenome(G.globalDict["genome"])
        
        # self.setGenomeValues()  
        # self.setGenomeValuesRandomly(20)
        self.setBodyPartSize()
        #self.setRandomColor()
        self.setColor()
        self.applyRandomRotation()

# callers
def main(cont):
    own = cont.owner
    if not "init" in own:
        own["generator"] = SpeciesGenerator(cont)
        own["init"] = True
    else:
        own["generator"].update()

        if cont.sensors["Keyboard"].positive:
            own["generator"].makeScreenshot()
    