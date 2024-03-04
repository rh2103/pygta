from pygta import *
pos=[]
try:
    while True:
        if GTA.KeyPressed(GTA.KEY['P']):
            pos.append(GTA.Ped.GetPosition())
            print(pos)
            GTA.Game.ShowTextbox(f'{len(pos)}')
            time.sleep(3)
            continue
        time.sleep(.25)
except KeyboardInterrupt:
    print(pos)