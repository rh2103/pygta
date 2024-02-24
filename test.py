from pygta import *
import time
while True:
    ppos=GTA.Player.GetPosition()
    print(GTA.Player.SetPosition([ppos[0],ppos[1],ppos[2]+.01]))
    