import bge
from bge import logic
import random


G = bge.logic
#cont = G.getCurrentController()
sce = G.getCurrentScene()
ob = sce.objects
cam = logic.getCurrentScene().active_camera

def getWorldSize(cam_ortho_scale):
    world_size_x = cam_ortho_scale * (1920/1080)/4
    world_size_y = cam_ortho_scale/4
    return (world_size_x, world_size_y)

def objectToMousePosition(cont):
	moa = cont.sensors["MouseOverAny"]
	
	
	if moa.positive:
		if moa.hitObject != "particle":
			return
	
	screenx = 1920
	screeny = 1080
	screen_factor = screeny/screenx	
	obj = cont.owner
	cam = logic.getCurrentScene().active_camera
	x = (logic.mouse.position[0]*cam.ortho_scale) - cam.ortho_scale/2
	y = screen_factor*((logic.mouse.position[1]*cam.ortho_scale) - cam.ortho_scale/2)*-1
	obj.worldPosition = (x,y,0)
	#bge.render.drawLine((0,0,0),(mov.position[0],mov.position[1],0),(1,0,0,0))

def apply_mouse_gravity(cont,anti):
	own = cont.owner
	gravity_ = own["grav"]
	for obj in G.globalDict["agents"]:
		distance = obj.getDistanceTo(own)
		force = (gravity_ * own["mass_"] * obj["mass_"]) / (distance * distance)
		obj.applyForce(force * (own.worldPosition - obj.worldPosition)*anti)

def ZenModus(cont):
	own = cont.owner
	mb = cont.sensors["MouseMB"]
	if mb.positive:
		if own["zen"] == False:
			own["zen"] = True
		else:
			own["zen"] = False
				
		for i in ob:
			if not i.name == "particle":
				if not i.name == "FaderBar":
					i.visible = own["zen"]
			

	
	

	
def mouse_gravity(cont):
	own = cont.owner
	lb = cont.sensors["MouseLB"]
	rb = cont.sensors["MouseRB"]
	moa = cont.sensors["MouseOverAny"]
	mov = cont.sensors["MouseMovement"]

	if mov.positive:
		pass
		#print("mousexy:",mov.position) 
	grav_force = 2.5
	if moa.positive:
		return
	if lb.positive:
		objectToMousePosition(cont)
		own["grav"] += grav_force
		own["mass_"] +=grav_force
		apply_mouse_gravity(cont,1)
	elif rb.positive:
		objectToMousePosition(cont)
		own["grav"] -= grav_force
		own["mass_"] -= grav_force
		apply_mouse_gravity(cont,-1)
	else:
		own["grav"] = 0.0
		own["mass_"] = 0.0
	mov = moa
	#bge.render.drawLine((0,0,0),(mov.position[0],mov.position[1],0),(1,0,0,0))

def setZoom(cont):
	wu = cont.sensors["MouseWU"]
	wd = cont.sensors["MouseWD"]
	if wd.positive:
		ob["Camera"].lens += 100
		#ob["Camera"].ortho_scale += 100
		#print (ob["Camera"].ortho_scale,ob["CameraUI"].ortho_scale)
		"""
		G.globalDict["world_size_x"] = getWorldSize(cam.ortho_scale)[0]
		G.globalDict["world_size_y"] = getWorldSize(cam.ortho_scale)[1]
		#ob["Camera_overlay"].useViewport = True
		#ob["Camera_overlay"].setOnTop()
		"""
	if wu.positive:
		ob["Camera"].lens -= 100
		#ob["Camera"].ortho_scale -= 100
		"""
		G.globalDict["world_size_x"] = getWorldSize(cam.ortho_scale)[0]
		G.globalDict["world_size_y"] = getWorldSize(cam.ortho_scale)[1]
		#ob["Camera_overlay"].useViewport = True
		#ob["Camera_overlay"].setOnTop()
		"""
	
	"""
	for i in ob:
		if i.name.startswith("Camera"):
			print (i,i.ortho_scale)
			print (dir(i))
	#print("grav",own["grav"],"mass_",own["mass_"])
	"""
		
			
	
		
		
	

	