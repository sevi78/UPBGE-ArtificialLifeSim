import bge
from dataclasses import fields
G = bge.logic
#cont = G.getCurrentController()
sce = G.getCurrentScene()
ob = sce.objects

def Zoom(cont):
	own = cont.owner
	wu = cont.sensors["MouseWU"]
	wd = cont.sensors["MouseWD"]
	up = cont.sensors["UpArrow"]
	down = cont.sensors["DownArrow"]
	value = own.ortho_scale/10

	if wd.positive or down.positive:
		own.ortho_scale += value
		#own.worldPosition.z += 100
	if wu.positive or up.positive:
		
		if own.ortho_scale-value > 0.01:
			own.ortho_scale -= value
		else:
			own.ortho_scale = 0.02

def setDebugText(cont,name,moa,text):
	bots = G.globalDict["bots"]
	displaytext = "bots in the scene: " +str(bots)  +"\n"
	displaytext += str(moa.hitObject.name) +"\n"

	if name== "Food":
		displaytext += str(moa.hitObject["energy"]) +"\n"

	elif name== "Bot":
		displaytext += "state: " + str(getattr(moa.hitObject["bot"],"state")) +"\n"
		#displaytext += "Task: " + str(moa.hitObject["bot"].task) + ": \n"
		for i in fields(moa.hitObject["bot"].genome):
			#print (str(getattr(moa.hitObject["bot"].genome,i.name)))
			if not getattr(moa.hitObject["bot"].genome,i.name) == None:
				displaytext += str(i.name) +": "
				displaytext += str(getattr(moa.hitObject["bot"].genome,i.name).value)+ " \n"

		displaytext += "Timer:" + str(moa.hitObject["timer"])
	else:
		return
	
	ob["DebugText"]["Text"] = displaytext

def updateDebugText(cont):

	if cont.owner["selectedBot"] != "":
		bots = G.globalDict["bots"]
		displaytext = "bots in the scene: " +str(bots)  +"\n"
		displaytext += str(cont.owner["selectedBot"]) +"\n"
		displaytext += "state: " + str(getattr(cont.owner["selectedBot"]["bot"],"state")) +"\n"
		#displaytext += "Task: " + str(moa.hitObject["bot"].task) + ": \n"
		for i in fields(cont.owner["selectedBot"]["bot"].genome):
			#print (str(getattr(moa.hitObject["bot"].genome,i.name)))
			if not getattr(cont.owner["selectedBot"]["bot"].genome,i.name) == None:
				displaytext += str(i.name) +": "
				displaytext += str(getattr(cont.owner["selectedBot"]["bot"].genome,i.name).value)+ " \n"

		displaytext += "Timer:" + str(cont.owner["selectedBot"]["timer"])
		ob["DebugText"]["Text"] = displaytext

		#print ("updateDebugText:")

def getGenome(cont, hitObject):
	
	if hitObject.name == "Bot":
		G.globalDict["genome"] = hitObject["bot"].genome
		#ob["generator"]["genome"] = hitObject["bot"].genome
		ob["Generator"]["trigger"] += 1

def moveCamera(cont):
	own = cont.owner
	x = bge.logic.mouse.position[0]-0.5
	y = bge.logic.mouse.position[1]-0.5
	d = own.getDistanceTo(ob["Circle"])/10
	steps = 1080/d
	own.worldPosition.x += x*own.ortho_scale/d
	own.worldPosition.y -= y*own.ortho_scale/d
	
def selectBot(cont, hitObject, value):
	if value == True:
		hitObject["bot"].is_selected = value
		cont.owner["selectedBot"] = hitObject
		

		ob["Pointer"].worldPosition = cont.owner["selectedBot"].worldPosition
		ob["Pointer"].setParent(cont.owner["selectedBot"])
		
		getGenome(cont,hitObject)
		print (cont.owner["selectedBot"], cont.owner["selectedBot"]["id"])
	else:
		if not cont.owner["selectedBot"] == "":
			cont.owner["selectedBot"]["bot"].is_selected = value
			cont.owner["selectedBot"] = ""

	ob["Pointer"].visible = value

def Mouse(cont):
	x = 1920
	y = 1080
	own = cont.owner
	moa = cont.sensors["Mouse"]
	lb = cont.sensors["MouseLB"]
	mb = cont.sensors["MouseMB"]
	circle = ob["Circle"]
	
	# the text right to the Circle, set invisible for now
	text = ob["Text"]
	text.visible = False

	scaling_factor =20
	if moa.positive:
		if moa.hitObject.name == "bk":
			circle.worldPosition = moa.hitPosition
			circle.worldPosition.z = 0
			circle.scaling = (own.ortho_scale/scaling_factor,own.ortho_scale/scaling_factor,own.ortho_scale/scaling_factor)
		if moa.hitObject != None:
			if moa.hitObject.name == "Bot" or "Food":
				if lb.positive:
					setDebugText(cont,moa.hitObject.name, moa,text)
					
					if moa.hitObject.name == "Bot":
						selectBot(cont, moa.hitObject, True)
					else:
						selectBot(cont, moa.hitObject, False)
						
	if lb.positive:
		moveCamera(cont)

	if mb.positive:
		sce.active_camera = ob["CameraFocus"]
	else:
		sce.active_camera = own