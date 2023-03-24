import bge
G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects


def showSex(cont):
    if cont.sensors[0].positive:
        for i in ob:
            if i.name == "Bot":
                # sex and pregnancy
                bot = i["bot"]
                if bot.genome["sex"] == 1:
                    obj = sce.addObject("Pointer",cont.owner,150)
                    obj.worldPosition = i.worldPosition
                    obj.setParent(i)
                    obj.color = (0,0,1,0)
                else:
                    
                    obj = sce.addObject("Pointer",cont.owner,150)
                    obj.worldPosition = i.worldPosition
                    obj.setParent(i)
                    if bot.genome["is_pregnant"] == 1:
                        obj.color = (1,1,0.5,0)
                    else:
                        obj.color = (1,0,0,0)

                # traxk to
                # if bot.track.object != None or str(""):

                #     bge.render.drawLine(i.worldPosition,bot.track.object.worldPosition,(1,1,1,1))

def showChilds(cont):
    if cont.sensors[0].positive:
        pass             
                # print ("setting color")