from pygta import *

while True:
    if GTA.Player.GetHealth()==0:
        if not GTA.Player.OnVehicle():
            for i in range(1000):
                if GTA.Player.GetHealth()==0:
                    GTA.Player.SetZ(GTA.Player.GetZ()+0.035)
                    time.sleep(0.01)
                else:
                    break
    time.sleep(.5)