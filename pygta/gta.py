from pygta import *
import win32api,json,os,threading

print('Enjoy modding! Read more about GTA SA memory: https://gtamods.com/wiki/Memory_Addresses_(SA)')

DEFAULT_GRAVITY=0.00800000038
DEFAULT_GAME_SPEED=1
PLAYER_ADDRESS=0xB6F5F0
KEY={
    "Backspace": "0x08",
    "Tab": "0x09",
    "Enter": "0x0D",
    "Shift": "0x10",
    "Control": "0x11",
    "Alt": "0x12",
    "Pause": "0x13",
    "CapsLock": "0x14",
    "Escape": "0x1B",
    "Space": "0x20",
    "PageUp": "0x21",
    "PageDown": "0x22",
    "End": "0x23",
    "Home": "0x24",
    "LeftArrow": "0x25",
    "UpArrow": "0x26",
    "RightArrow": "0x27",
    "DownArrow": "0x28",
    "Insert": "0x2D",
    "Delete": "0x2E",
    "0": "0x30",
    "1": "0x31",
    "2": "0x32",
    "3": "0x33",
    "4": "0x34",
    "5": "0x35",
    "6": "0x36",
    "7": "0x37",
    "8": "0x38",
    "9": "0x39",
    "A": "0x41",
    "B": "0x42",
    "C": "0x43",
    "D": "0x44",
    "E": "0x45",
    "F": "0x46",
    "G": "0x47",
    "H": "0x48",
    "I": "0x49",
    "J": "0x4A",
    "K": "0x4B",
    "L": "0x4C",
    "M": "0x4D",
    "N": "0x4E",
    "O": "0x4F",
    "P": "0x50",
    "Q": "0x51",
    "R": "0x52",
    "S": "0x53",
    "T": "0x54",
    "U": "0x55",
    "V": "0x56",
    "W": "0x57",
    "X": "0x58",
    "Y": "0x59",
    "Z": "0x5A",
    "Windows": "0x5B",
    "RightWindows": "0x5C",
    "Applications": "0x5D",
    "Numpad0": "0x60",
    "Numpad1": "0x61",
    "Numpad2": "0x62",
    "Numpad3": "0x63",
    "Numpad4": "0x64",
    "Numpad5": "0x65",
    "Numpad6": "0x66",
    "Numpad7": "0x67",
    "Numpad8": "0x68",
    "Numpad9": "0x69",
    "Multiply": "0x6A",
    "Add": "0x6B",
    "Separator": "0x6C",
    "Subtract": "0x6D",
    "Decimal": "0x6E",
    "Divide": "0x6F",
    "F1": "0x70",
    "F2": "0x71",
    "F3": "0x72",
    "F4": "0x73",
    "F5": "0x74",
    "F6": "0x75",
    "F7": "0x76",
    "F8": "0x77",
    "F9": "0x78",
    "F10": "0x79",
    "F11": "0x7A",
    "F12": "0x7B",
    "NumLock": "0x90",
    "ScrollLock": "0x91"
  }
  

def GetKeys():
    print(KEY)

def KeyPressed(vkey):
    if isfocused():
        if isinstance(vkey,str):
            vkey=int(vkey,16)
        if win32api.GetKeyState(vkey) < -5:
            return True
        return False
    return False

def TestCheat(cheat='test'):
    last_chars=''
    for i in range(0,17):
        last_chars=last_chars+(chr(FourBytesToSingleByte(rmem(0x969110+i))))
    last_chars=last_chars[:len(cheat)]
    last_chars=last_chars[::-1]
    if cheat.lower()==last_chars.lower():
        return True
    return False

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

    def GetMaxWantedLevel():
        return rmem(0x8CDEE4)
    def SetMaxWantedLevel(value):
        return wmem(0x8CDEE4,value)
    
    def GetWantedLevel():
        return rmem(0xBAA420)
    def SetWantedLevel(value):
        return wmem(0xBAA420,value)
    
    def OnVehicle():
        return rmem(0xBA18FC)
#
    #def GetPosition():
    #    x=FourBytesToFloat(rmem(0xB6F5F0,offsets=[0x14,0x30]))
    #    y=FourBytesToFloat(rmem(0xB6F5F0,offsets=[0x14,0x30+0x4]))
    #    z=FourBytesToFloat(rmem(0xB6F5F0,offsets=[0x14,0x30+0x8]))
    #    return [x,y,z]
    #def SetPosition(value:list):
    #    x=wmem(0xB6F5F0,FloatToFourBytes(value[0]),offsets=[0x14,0x30])
    #    y=wmem(0xB6F5F0,FloatToFourBytes(value[1]),offsets=[0x14,0x30+0x4])
    #    z=wmem(0xB6F5F0,FloatToFourBytes(value[2]),offsets=[0x14,0x30+0x8])
    #    return Player.GetPosition()
    #
    #def GetHealth():
    #    return FourBytesToFloat(rmem(0xB6F5F0,offsets=[0x540]))
    #def SetHealth(value):
    #    return wmem(0xB6F5F0,FloatToFourBytes(value),[0x540])
    #
    #def GetAttackerPointer():
    #    return GetPointer(0xB6F5F0,[0x764])
    #
    #def IsInvisble():
    #    if FourBytesToSingleByte(rmem(0xB6F5F0,[0x474]))==2:
    #        return True
    #    return False
    #def SetIsInvisible(value:bool):
    #    if value:
    #        return wmem(0xB6F5F0,738198530,[0x474])
    #    else:
    #        return wmem(0xB6F5F0,738198528,[0x474])
#
    #def GetSurfacePhysics():
    #    """
    #    1 = Submerged In Water
    #    2 = On Solid Surface
    #    4 = Broken
    #    8 = Unknown
    #    16 = Unknown
    #    32 = Don't Apply Speed
    #    64 = Unknown
    #    128 = Unknown
    #    """
    #    return FourBytesToSingleByte(rmem(0xB6F5F0,[0x40+0x1]))
    #def SetSurfacePhysics(value):
    #    """
    #    1 = Submerged In Water
    #    2 = On Solid Surface
    #    4 = Broken
    #    8 = Unknown
    #    16 = Unknown
    #    32 = Don't Apply Speed
    #    64 = Unknown
    #    128 = Unknown
    #    """
    #    return wmem(0xB6F5F0,value,[0x40+0x1])

class Ped:
    def GetPosition(target=0xB6F5F0):
        x=FourBytesToFloat(rmem(target,offsets=[0x14,0x30]))
        y=FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x4]))
        z=FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x8]))
        return [x,y,z]
    def SetPosition(value:list,target=0xB6F5F0):
        x=wmem(target,FloatToFourBytes(value[0]),offsets=[0x14,0x30])
        y=wmem(target,FloatToFourBytes(value[1]),offsets=[0x14,0x30+0x4])
        z=wmem(target,FloatToFourBytes(value[2]),offsets=[0x14,0x30+0x8])
        return Ped.GetPosition()
    
    def GetX(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30]))
    def SetX(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30])

    def GetY(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x4]))
    def SetY(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30+0x4])

    def GetZ(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x8]))
    def SetZ(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30+0x8])

    def GetHealth(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x540]))
    def SetHealth(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),[0x540])
    
    def GetArmor(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x548]))
    def SetArmor(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),[0x548])

    def GetAttackerPointer(target=0xB6F5F0):
        return GetPointer(target,[0x764])

    def GetCurrentVehiclePointer(target=0xB6F5F0):
        return GetPointer(target,[0x58C])
    
    def GetHealth(target=0xB6F5F0):
        return FourBytesToFloat(rmem(target,offsets=[0x540]))
    def SetHealth(value,target=0xB6F5F0):
        return wmem(target,FloatToFourBytes(value),[0x540])
        #
    def GetAttackerPointer(target=0xB6F5F0):
        return GetPointer(target,[0x764])
        #
    def IsInvisble(target=0xB6F5F0):
        if FourBytesToSingleByte(rmem(target,[0x474]))==2:
            return True
        return False
    def SetIsInvisible(value:bool,target=0xB6F5F0):
        if value:
            return wmem(target,738198530,[0x474])
        else:
            return wmem(target,738198528,[0x474])
    def GetSurfacePhysics(target=0xB6F5F0):
        """
        1 = Submerged In Water
        2 = On Solid Surface
        4 = Broken
        8 = Unknown
        16 = Unknown
        32 = Don't Apply Speed
        64 = Unknown
        128 = Unknown
        """
        return FourBytesToSingleByte(rmem(target,[0x40+0x1]))
    def SetSurfacePhysics(value,target=0xB6F5F0):
        """
        1 = Submerged In Water
        2 = On Solid Surface
        4 = Broken
        8 = Unknown
        16 = Unknown
        32 = Don't Apply Speed
        64 = Unknown
        128 = Unknown
        """
        return wmem(target,value,[0x40+0x1])
    
    def GetSpecialPhysicsFlags(target=0xB6F5F0):
        """
        1 = Soft (in other words noclip)
        2 = Freeze
        4 = Bullet-Proof
        8 = Fire-Proof
        16 = Collision-Proof (prevent fall damage)
        32 = Melee-Proof
        64 = Melee-Proof, Bullet-Proof, Collision-Proof
        128 = Explosion-Proof
        """
        return rmem(target,[0x40+0x2])
    def SetSpecialPhysicsFlags(value,target=0xB6F5F0):
        """
        1 = Soft (in other words noclip)
        2 = Freeze
        4 = Bullet-Proof
        8 = Fire-Proof
        16 = Collision-Proof (prevent fall damage)
        32 = Melee-Proof
        64 = Melee-Proof, Bullet-Proof, Collision-Proof
        128 = Explosion-Proof
        """
        return wmem(target,value,[0x40+0x2])

    def GetAimedPedPointer(target=0xB6F5F0):
        return GetPointer(target,[0x79C])
    
    def GetNearestVehiclePointer(target=0xB6F5F0):
        return GetPointer(target,[0x47C,0x120])
    
    def GetState(target=0xB6F5F0):
        """
        0 = leaving a car, falling down from a bike or something like this
        1 = normal case
        50 = driving
        55 = wasted
        63 = busted
        """
        return FourBytesToSingleByte(rmem(target,[0x530]))
    def SetState(value,target=0xB6F5F0):
        """
        0 = leaving a car, falling down from a bike or something like this
        1 = normal case
        50 = driving
        55 = wasted
        63 = busted
        """
        return rmem(target,value,[0x530])
    
    def InDistance(position_x,position_y,distance,target=0xB6F5F0):
        ped_pos=Ped.GetPosition(target)
        if ped_pos[0]<=position_x+distance and ped_pos[0]>=position_x-distance:
            if ped_pos[1]<=position_y+distance and ped_pos[1]>=position_y-distance:
                return True
        return False
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
        
    def IsGameFreezed():
        return rmem(0xB7CB49)
    def SetIsGameFreezed(value):
        return wmem(0xB7CB49,value)
    
    def ShowTextbox(value):
        if len(value)!=0:
            text=list(value)
            text=[ord(char) for char in text]
            if len(text) > 150:
                for _ in range(len(text) - 150):
                    text.pop()
            for index,i in enumerate(text):
                wmem(0xBAA7A0+index,i)
            return True
        else:
            for i in range(0,151):
                wmem(0xBAA7A0+i,0)

    def ShowMissionPassed(value='MISSION PASSED!'):
        text=list(value)
        text=[ord(char) for char in text]
        if len(text) > 32:
            for _ in range(len(text) - 150):
                text.pop()
        for index,i in enumerate(text):
            wmem(0xBAACC0+index,i)
        return True
    def ShowMissionTitle(value='Mission Title'):
        text=list(value)
        text=[ord(char) for char in text]
        if len(text) > 32:
            for _ in range(len(text) - 150):
                text.pop()
        start_time=time.time()
        for j in range(80):
            for index,i in enumerate(text):
                wmem(0xBAAD40+index,i)
        print(start_time-time.time())
        return True

class Vehicle:
    def GetVehicleMass(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,offsets=[0x8C]))
    def SetVehicleMass(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),offsets=[0x8C])
    
    def GetCameraViewMode(target=0xBA18FC):
        return rmem(0xB6F0DC)
    def SetCameraViewMode(value,target=0xBA18FC):
        return wmem(0xB6F0DC,value)
        
    def GetDirtyLevel(target=0xBA18FC):
        return FourBytesToFloat(rmem(target ,offsets=[0x4B0]))
    def SetDirtyLevel(value,target=0xBA18FC):
        return FourBytesToFloat(wmem(target ,FloatToFourBytes(value),offsets=[0x4B0]))
    
    def GetGripDivider(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,[0x94]))
    def SetGripDivider(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),[0x94])
    
    def GetEngineState(target=0xBA18FC):
        return FourBytesToSingleByte(rmem(target,[0x428]))
    def SetEngineState(value,target=0xBA18FC):
        if value:
            return wmem(target,16,[0x428])
        return wmem(target,0,[0x428])
    
    def GetTiresSize(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,[0x458]))
    def SetTiresSize(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),[0x458])
    
    def GetDriverPointer(target=0xBA18FC):
        return GetPointer(target,[0x460])
    
    def GetPosition(target=0xBA18FC):
        x=FourBytesToFloat(rmem(target,offsets=[0x14,0x30]))
        y=FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x4]))
        z=FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x8]))
        return [x,y,z]
    def SetPosition(value:list,target=0xBA18FC):
        x=wmem(target,FloatToFourBytes(value[0]),offsets=[0x14,0x30])
        y=wmem(target,FloatToFourBytes(value[1]),offsets=[0x14,0x30+0x4])
        z=wmem(target,FloatToFourBytes(value[2]),offsets=[0x14,0x30+0x8])
        return Vehicle.GetPosition(target)

    def GetX(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30]))
    def SetX(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30])
    def GetY(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x4]))
    def SetY(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30+0x4])
    def GetZ(target=0xBA18FC):
        return FourBytesToFloat(rmem(target,offsets=[0x14,0x30+0x8]))
    def SetZ(value,target=0xBA18FC):
        return wmem(target,FloatToFourBytes(value),offsets=[0x14,0x30+0x8])