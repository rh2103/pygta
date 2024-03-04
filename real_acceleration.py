from pygta import *
max_gripd=3
min_gripd=1
adder=.5
delay=.56
KEY=GTA.KEY
while True:
    if GTA.Player.OnVehicle():
        current_gripd=GTA.Vehicle.GetGripDivider()
        gripd=GTA.Vehicle.SetGripDivider
        if current_gripd>max_gripd:
            gripd(max_gripd)
        if GTA.KeyPressed(KEY['W']):
            if current_gripd>min_gripd:
                gripd(current_gripd-adder)
                time.sleep(delay)
                continue
        time.sleep(delay)
        if current_gripd<max_gripd and current_gripd!=max_gripd:
            gripd(current_gripd+adder)
        print(current_gripd)
    time.sleep(.5)