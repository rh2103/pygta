from pygta import *

DEFAULT_GRAVITY=0.00800000038
DEFAULT_GAME_SPEED=1

class Player:
    def GetMoney():
        return rmem(0xB7CE50)
    def SetMoney(value):
        return wmem(0xB7CE50,value)
    

class Game:
    def GetGravity():
        return rmem(0x863984 )
    def SetGravity(value):
        return wmem(0x863984 ,value)
    
    def GetMinute():
        return rmem(0xB70152 )
    def SetMinute():
        return wmem(0xB70152 )
    
    def GetHour():
        return rmem(0xB70153 )
    def SetHour():
        return wmem(0xB70153 )

class Vehicle:
    def GetVehicleMass():
        return rmem(0xB6F980,offsets=[0x8C])
    def SetVehicleMass(value):
        return wmem(0xB6F980,value,offsets=[0x8C])
    