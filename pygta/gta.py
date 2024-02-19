from pygta import *
import threading

print('Enjoy modding! Read more about GTA SA memory: https://gtamods.com/wiki/Memory_Addresses_(SA)')

DEFAULT_GRAVITY=0.00800000038
DEFAULT_GAME_SPEED=1

class Player:
    def GetMoney():
        return rmem(0xB7CE50)
    def SetMoney(value):
        return wmem(0xB7CE50,value)
        
    def GetIgnoredByCops():
        return rmem(0xB7CD9C,offsets=[0x1E])
    def SetIgnoredByCops(value):
        return wmem(0xB7CD9C,offsets=[0x1E])
        
    def GetIgnoredByEveryone():
        return rmem(0xB7CD9C,offsets=[0x298])
    def SetIgnoredByEveryone(value):
        return wmem(0xB7CD9C,offsets=[0x298])
    

class Game:
    def GetGravity():
        return FourBytesToFloat(rmem(0x863984))
    def SetGravity(value):
        return wmem(0x863984,FloatToFourBytes(value))
    
    def GetMinute():
        return rmem(0xB70152)
    def SetMinute():
        return wmem(0xB70152)
    
    def GetHour():
        return rmem(0xB70153)
    def SetHour():
        return wmem(0xB70153)
        
    def GetOneMinuteInMiliseconds():
        return rmem(0xB7015C)
    def SetOneMinuteInMiliseconds(value):
        return wmem(0xB7015C,value)
        
    def GetWeekday():
        return FourBytesToSingleByte(rmem(0xB7014E))        
    def SetWeekday(value):
        return wmem(0xB7014E,value)

    def GetDaysPassed():
        return rmem(0xB79038)
    def SetDaysPassed(value):
        return wmem(0xB79038,value)
        
    #def ShowTextBox(text,duration=3):
    #    def Reset():
    #        wmem()

class Vehicle:
    def GetVehicleMass():
        return FourBytesToFloat(rmem(0xB6F980,offsets=[0x8C]))
    def SetVehicleMass(value):
        return wmem(0xB6F980,FloatToFourBytes(value),offsets=[0x8C])
    
    def GetCameraViewMode():
        return rmem(0xB6F0DC)
    def SetCameraViewMode(value):
        return wmem(0xB6F0DC,value)
        
    def GetDirtyLevel():
        return FourBytesToFloat(rmem(0xBA18FC ,offsets=[0x4B0]))
    def SetDirtyLevel(value):
        return FourBytesToFloat(wmem(0xBA18FC ,FloatToFourBytes(value),offsets=[0x4B0]))