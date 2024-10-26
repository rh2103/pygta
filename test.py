from pygta import *
import time
#HELLo
camera=[]
last_pos=[]
last_surface_phyics=None
index=0
while True:
    if GTA.KeyPressed(GTA.KEY['P']):
        camera.append(GTA.Player.GetPosition())
        time.sleep(3)
    if GTA.KeyPressed(GTA.KEY['O']):
        if len(camera)!=0 and index+1<len(camera):
            index+=1
        else:
            index=0
        time.sleep(1)
    if GTA.KeyPressed(GTA.KEY['L']):
        if GTA.Player.OnVehicle()==0 and GTA.Player.GetHealth()>=10:
            if len(last_pos)==0 and last_surface_phyics==None:
                last_pos=GTA.Player.GetPosition()
                last_surface_phyics=GTA.Player.GetSurfacePhysics()
            GTA.Player.SetIsInvisible(True)
            GTA.Player.SetSurfacePhysics(32)
            GTA.Player.SetPosition(camera[index])
            time.sleep(.08)
            continue
    if not GTA.KeyPressed(GTA.KEY['L']) and len(last_pos)!=0 and last_surface_phyics!=None:
        
        GTA.Player.SetPosition(last_pos)
        GTA.Player.SetSurfacePhysics(last_surface_phyics)
        GTA.Player.SetIsInvisible(False)

        last_pos=[]
        last_surface_phyics=None
    time.sleep(.6)