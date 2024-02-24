from pygta import *

while True:
    if GTA.Player.GetHealth()==0 and not GTA.Player.OnVehicle():
        ppos=GTA.Player.GetPosition()
        for i in range(1000):
            if GTA.Player.GetHealth()==0:
                ppos=GTA.Player.GetPosition()
                GTA.Player.SetPosition([ppos[0],ppos[1],ppos[2]+0.05])
                time.sleep(0.01)
            else:
                break
    time.sleep(1.5)