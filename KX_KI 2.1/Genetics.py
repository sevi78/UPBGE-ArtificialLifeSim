import random
from dataclasses import dataclass,fields, asdict


def old(self):
    """
    self.genome_old = Genome_old(speed= 0.03999485472564734, 
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
    """
        

class Gene:
    # a gene is a dataset wich has min, max and value. setValue to set the value of the Gene. Atomatical restricted to min and max
    def __init__(self,name= "noname",value= 0.75,min= 0.0,max= 1.0, inherit= True, randomness = 0):
        self.name = name
        self.min = min
        self.max = max
        self.inherit = inherit
        self.default = None
        self.randomness = randomness

        if self.randomness == 0:
            self.setValue(value)
        else:
            self.setRandomValue(value, self.randomness)
    
    def setValue(self, value):
        # check for type
        if type(value) == int:
            self.min = int(self.min)
            self.max = int(self.max)

        # sets the value if in range min and max
        if value < self.min:
            self.value = self.min
        elif value > self.max:
            self.value = self.max
        else:
            self.value = value
        
        if self.default == None:
            self.default = self.value
        
    def setRandomValue(self,percent):
        # set a random value for the gene, in range of percent relative to value
        p = 1/100*percent
        self.setValue(random.uniform(self.value-p,self.value+p))

@dataclass  
class Genome:
    speed: Gene = None
    rotation: Gene = None
    track_time: Gene = None
    age: Gene = None
    generation: Gene = None
    always_skippedTicks: Gene = None
    always_seed: Gene = None
    radar_skippedTicks: Gene = None
    radar_angle: Gene = None
    radar_distance: Gene = None 
    sex: Gene = None
    pregnancy: Gene = None
    is_pregnant:Gene = None
    pregnancy_duration:Gene = None 
    pregnancy_grow_factor: Gene = None
    size: Gene = None
    energy: Gene = None
    stomach_size:Gene  = None
    stomach_load:Gene = None
    eat_treshold:Gene = None
    is_hungry: Gene = None
    is_horny: Gene = None
    
    decision_time: Gene = None
    growth_rate:Gene = None
    energy_usage:Gene = None
    mandible_size:Gene = None
    # legs_front_size:Gene = None
    # legs_middle_size:Gene = None
    # legs_back_size: Gene = None
    # eye_size: Gene = None
    # feeding_tool_size:Gene = None
    # antenna_size:Gene = None
    # head_size: Gene = None
    # backbody_size: Gene = None
    fertility_rate: Gene = None
    legs: Gene = None
    #has_mandibles: Gene = None
    color_r: Gene = None
    color_g: Gene = None
    color_b: Gene = None
    color_a: Gene = None
    
    
    def __iter__(self):
        return (getattr(self, field.name) for field in fields(self))
        
class GenomeHandler:
    def __init__(self):
        self.genome = Genome()
        self.setGenomeValues()

    def setGenomeValuesLeveled(self):
        for field in self.genome.__dataclass_fields__:
            setattr(self.genome,field,Gene(name= field,value= 0.75,min= 0.0,max= 1.0, inherit= True) )

    def setGenomeValuesRandomly(self, percent):
        for field in self.genome.__dataclass_fields__:
            genome = getattr(self.genome, field)
            if genome != None:
                genome.setRandomValue(percent)

        self.genome.legs.value = random.randint(4,8)

    
        

    def setGenomeValues(self):
        setattr(self.genome,"size",Gene(name= "size",value= 1.0,min= 0.1,max= 2.0, inherit= True) )
        setattr(self.genome,"speed",Gene(name= "speed",value= 0.2,min= 0.05,max= 0.3, inherit= True) )
        setattr(self.genome,"rotation",Gene(name= "rotation",value= 0.15,min= 0.01,max= 0.35, inherit= True) )
        setattr(self.genome,"track_time",Gene(name= "track_time",value= 5,min= 2,max= 10, inherit= True) )

        setattr(self.genome,"always_skippedTicks",Gene(name= "always_skippedTicks",value= 15,min= 10,max= 100, inherit= True) )
        setattr(self.genome,"always_seed",Gene(name= "always_seed",value= 0,min= 0,max= 100, inherit= True) )
        setattr(self.genome,"radar_skippedTicks",Gene(name= "radar_skippedTicks",value= 25,min= 15,max= 100, inherit= True) )
        setattr(self.genome,"radar_distance",Gene(name= "radar_distance",value= 15,min= 5,max= 30, inherit= True) )
        setattr(self.genome,"radar_angle",Gene(name= "radar_angle",value= 45,min= 15,max= 60, inherit= True) )

        setattr(self.genome,"age",Gene(name= "age",value= 0,min= 0,max= 700, inherit= True) )
        setattr(self.genome,"generation",Gene(name= "generation",value= 0,min= 0,max= 10000, inherit= True) )
        setattr(self.genome,"sex",Gene(name= "sex",value= random.randint(0,1),min= 0,max= 1, inherit= True) )
        setattr(self.genome,"pregnancy",Gene(name= "pregnancy",value= 0.0,min= 0.0,max= 1.0, inherit= True) )
        setattr(self.genome,"pregnancy_grow_factor",Gene(name= "pregnancy_grow_factor",value= 0.005,min= 0.001,max= 0.01, inherit= True) )
        setattr(self.genome,"is_pregnant",Gene(name= "is_pregnant",value= 0,min= 0,max= 1, inherit= True) )
        setattr(self.genome,"fertility_rate",Gene(name= "fertility_rate",value= 1.1,min= 1.0,max= 100.0, inherit= True) )
        setattr(self.genome,"pregnancy_duration",Gene(name= "pregnancy_duration",value=self.genome.age.value/self.genome.fertility_rate.value ,min= 1.0,max= 50.0, inherit= True) )

        setattr(self.genome,"decision_time",Gene(name= "decision_time",value= 1.0,min= 1.0,max= 5.0, inherit= True) )
        setattr(self.genome,"growth_rate",Gene(name= "growth_rate",value= 1.05,min= 1.01,max= 1.1, inherit= True) )
        setattr(self.genome,"stomach_size",Gene(name= "stomach_size",value= 1.0,min= 0.5,max= 1.5, inherit= True) )
        setattr(self.genome,"stomach_load",Gene(name= "stomach_load",value= 1.0,min= 0.5,max= 1.5, inherit= True) )
        setattr(self.genome,"eat_treshold",Gene(name= "eat_treshold",value= 0.8,min= 0.5,max= self.genome.stomach_size.value*0.9, inherit= True) )
        setattr(self.genome,"is_hungry",Gene(name= "is_hungry",value= 0,min= 0,max= 1, inherit= True) )
        setattr(self.genome,"legs",Gene(name= "legs",value= 6,min= 4,max= 8, inherit= True) )
        setattr(self.genome,"color_r",Gene(name= "color",value= 0.4,min= 0.0,max= 0.7, inherit= True) )
        setattr(self.genome,"color_g",Gene(name= "color",value= 0.4,min= 0.0,max= 0.7, inherit= True) )
        setattr(self.genome,"color_b",Gene(name= "color",value= 0.4,min= 0.0,max= 0.7, inherit= True) )
        setattr(self.genome,"color_a",Gene(name= "color",value= 0.4,min= 0.0,max= 0.7, inherit= True) )
        setattr(self.genome,"energy_usage",Gene(name= "energy_usage",value= 0.005,min= 0.001,max= 0.05, inherit= True) )
        setattr(self.genome,"mandible_size",Gene(name= "mandible_size",value= 1.0,min= 0.01,max= 1.5, inherit= True) )
        #setattr(self.genome,"has_mandibles",Gene(name= "has_mandibles",value= 0,min= 0,max= 1, inherit= True) )


    def setGenome(self,genome):
        self.genome = genome 


"""
gh = GenomeHandler()
#print (bot.genome.speed.value)
#bot.setGenomeValuesLeveled()
gh.setGenomeValues()
print(gh.genome.speed.min)

gene = Gene("test", 0.7,0.1, 1.5, True)

gene.setValue(1.45)
gene.setRandomValue(20)
print (gene.value)
"""