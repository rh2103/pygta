from pygta import gta
import pygta
while True:
    print(pygta.FourBytesToFloat(gta.Vehicle.GetVehicleMass()))
    print(gta.Vehicle.SetVehicleMass(pygta.FloatToFourBytes(-50)))