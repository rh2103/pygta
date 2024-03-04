from pygta import *
import time
camera=[[1554.959716796875, -1675.43701171875, 18.984220504760742],[1611.8450927734375, -1666.39892578125, 10.177311897277832], [1539.708984375, -1618.42431640625, 15.277307510375977], [1576.6456298828125, -1632.74658203125, 15.232781410217285], [1607.4451904296875, -1602.941650390625, 15.083647727966309]]
last_pos=[]
last_surface_phyics=None
index=0
while True:
    if GTA.KeyPressed(GTA.KEY['P']):
        camera.append(GTA.Ped.GetPosition())
        time.sleep(3)
    if GTA.KeyPressed(GTA.KEY['O']):
        if len(camera)!=0 and index+1<len(camera):
            index+=1
            GTA.Game.ShowTextbox(f'CAM {index}')
        else:
            index=0
        time.sleep(1)
    if GTA.KeyPressed(GTA.KEY['L']):
        if GTA.Player.OnVehicle()==0 and GTA.Ped.GetHealth()>=10:
            if len(last_pos)==0 and last_surface_phyics==None:
                last_pos=GTA.Ped.GetPosition()
                last_surface_phyics=GTA.Ped.GetSurfacePhysics()
            GTA.Ped.SetIsInvisible(True)
            GTA.Ped.SetSurfacePhysics(32)
            GTA.Ped.SetPosition(camera[index])
            time.sleep(.25)
            continue
    if not GTA.KeyPressed(GTA.KEY['L']) and len(last_pos)!=0 and last_surface_phyics!=None:
        GTA.Ped.SetPosition(last_pos)
        GTA.Ped.SetSurfacePhysics(last_surface_phyics)
        GTA.Ped.SetIsInvisible(False)
        last_pos=[]
        last_surface_phyics=None
    time.sleep(.6)