import bge
import random
G = bge.logic
cont = G.getCurrentController()
sce = G.getCurrentScene()
ob = sce.objects

G.globalDict = {}
G.globalDict["size"] = 50
size = G.globalDict["size"]
G.globalDict["bots"] = 0#int(size/1.5)
G.globalDict["pregnants"] = 0
G.globalDict["genome"] = None

def createObjects(cont,size,obj_,amount):
	own = cont.owner
	#create objects
	for i in range(int(amount)):
		#create object
		obj = sce.addObject(obj_,own,False) 

		#place in middle of screen
		x = random.uniform(-size,size)
		y = random.uniform(-size,size)
		z = 0.0
		obj.worldPosition = [x,y,z]
		obj.worldOrientation = (0,0,x*y)


		if obj_ == "Bot":
			G.globalDict["bots"] +=1
			obj["id"] = i
			
def calcSize(cont):
	sizex = bge.render.getWindowWidth() 
	sizey = bge.render.getWindowHeight()
	ratio = 1/sizex*sizey
	worldsize = G.globalDict["size"]*2

	ortho_scale = worldsize*ratio*2

	print (ratio,ortho_scale)

def main(cont):
	collection = cont.actuators["Collection"]
	cont.activate(collection)
	createObjects(cont,size,"Bot",int(size * 2))
	createObjects(cont,size,"Food",int(size/1.2))
	#ob["Camera"].worldPosition.z =  size *6
	ob["Camera"].ortho_scale = 62.0#489#150*(1080/1920)#size*1080/1920
	ob["bk"].scaling = (size,size,1)

	print ("WorldSize: ", G.globalDict["size"])
	print ("bots: ", int(size * 1.5))
	ob["Pointer"].visible = False
