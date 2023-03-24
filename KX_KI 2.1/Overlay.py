import bge
G = bge.logic
sce = G.getCurrentScene()
ob = sce.objects


def calculateFertility(cont):
    bots_on_start = cont.owner["bots_on_start"]
    bots = G.globalDict["bots"]
    pregnants = G.globalDict["pregnants"]
    
    #print (cont.owner["bots_on_start"],G.globalDict["pregnants"],G.globalDict["bots"])
    fertility_rate = str(bots + pregnants - bots_on_start)
    return fertility_rate


def main(cont):
    if not "bots_on_start" in cont.owner:
        cont.owner["bots_on_start"] = G.globalDict["bots"]

    if cont.sensors[0].positive:
        own = cont.owner
        bots = str(G.globalDict["bots"])
        own["Text"] = "Population: " + bots + "\n" #+"/" #+str(len([i for i in ob if i.name == "Bot"]))
        own["Text"] += "Fertility Rate: " + calculateFertility(cont)
