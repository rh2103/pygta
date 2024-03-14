from pygta import *
import win32api,json,os,threading,configparser as INI
import sounddevice as sd,soundfile as sf

#print('Enjoy modding! Read more about GTA SA memory: https://gtamods.com/wiki/Memory_Addresses_(SA)')
CONFIG_FILE=None
try:
    CONFIG_FILE=json.load(open(__file__.rsplit('\\',2)[0]+'\\config.json'))
except Exception as e:
    print(f"Warning loading 'config.json': {e}")
DEFAULT_GRAVITY=0.00800000038
DEFAULT_GAME_SPEED=1
PLAYER_ADDRESS=0xB6F5F0
KEY={
    "LeftMouse":0x01,
    "RightMouse":0x02,
    "MiddleMouse":0x04,
    "Backspace": 0x08,
    "Tab": 0x09,
    "Enter": 0x0D,
    "Shift": 0x10,
    "Ctrl": 0x11,
    "Alt": 0x12,
    "Pause": 0x13,
    "CapsLock": 0x14,
    "Escape": 0x1B,
    "Space": 0x20,
    "PageUp": 0x21,
    "PageDown": 0x22,
    "End": 0x23,
    "Home": 0x24,
    "LeftArrow": 0x25,
    "UpArrow": 0x26,
    "RightArrow": 0x27,
    "DownArrow": 0x28,
    "Insert": 0x2D,
    "Delete": 0x2E,
    "0": 0x30,
    "1": 0x31,
    "2": 0x32,
    "3": 0x33,
    "4": 0x34,
    "5": 0x35,
    "6": 0x36,
    "7": 0x37,
    "8": 0x38,
    "9": 0x39,
    "A": 0x41,
    "B": 0x42,
    "C": 0x43,
    "D": 0x44,
    "E": 0x45,
    "F": 0x46,
    "G": 0x47,
    "H": 0x48,
    "I": 0x49,
    "J": 0x4A,
    "K": 0x4B,
    "L": 0x4C,
    "M": 0x4D,
    "N": 0x4E,
    "O": 0x4F,
    "P": 0x50,
    "Q": 0x51,
    "R": 0x52,
    "S": 0x53,
    "T": 0x54,
    "U": 0x55,
    "V": 0x56,
    "W": 0x57,
    "X": 0x58,
    "Y": 0x59,
    "Z": 0x5A,
    "Windows": 0x5B,
    "RightWindows": 0x5C,
    "Applications": 0x5D,
    "Numpad0": 0x60,
    "Numpad1": 0x61,
    "Numpad2": 0x62,
    "Numpad3": 0x63,
    "Numpad4": 0x64,
    "Numpad5": 0x65,
    "Numpad6": 0x66,
    "Numpad7": 0x67,
    "Numpad8": 0x68,
    "Numpad9": 0x69,
    "Multiply": 0x6A,
    "Add": 0x6B,
    "Separator": 0x6C,
    "Subtract": 0x6D,
    "Decimal": 0x6E,
    "Divide": 0x6F,
    "F1": 0x70,
    "F2": 0x71,
    "F3": 0x72,
    "F4": 0x73,
    "F5": 0x74,
    "F6": 0x75,
    "F7": 0x76,
    "F8": 0x77,
    "F9": 0x78,
    "F10": 0x79,
    "F11": 0x7A,
    "F12": 0x7B,
    "NumLock": 0x90,
    "ScrollLock": 0x91
  }

subtitleCode=[]
stuntCompleteCode=[]

class TextCode:
    green='~g~'
    blue='~b~'
    red='~r~'
    orange='~o~'
    purple='~p~'
    white='~w~'
    yellow='~y~'

class Audio:
    def __init__(self,path,start_time=0):
        # Membaca file musik
        self.data, self.fs = sf.read(path)
        self.start_time=None
        self.last_start_index=-1
        self.played=False

        # Menghitung indeks awal dan akhir dari pemotongan
        self.start_index = int(start_time * self.fs)
        self.end_index = len(self.data)

        # Memotong array data sesuai dengan detik yang diinginkan
        self.cut_data = self.data[self.start_index:self.end_index]

        # Memainkan musik
        
    def play(self):
        if self.last_start_index!=-1:
            self.cut_data = self.data[int(self.last_start_index * self.fs):self.end_index]
            self.last_start_index=self.last_start_index
        #if self.start_time==None:
        self.start_time=time.time()-self.last_start_index
        self.thread=threading.Thread(target=self.play_audio)
        self.thread.start()
        self.played=True
        return True

    def play_audio(self):
        sd.play(self.cut_data, self.fs)
        sd.wait()


    def stop(self):
        end_time=time.time()
        sd.stop()
        self.thread.join()
        ret_val=end_time-self.start_time
        self.last_start_index=ret_val
        self.played=False
        return ret_val

def GetKeys():
    print(KEY)

def KeyPressed(vkey):
    if isinstance(vkey,str):
        vkey=KEY[vkey]
    if isfocused():
        if win32api.GetKeyState(vkey) < -5:
            return True
        return False
    return False

def TestCheat(cheat='test'):
    last_chars=memory.readStr(0x969110)
    last_chars=last_chars[:len(cheat)]
    last_chars=last_chars[::-1]
    if cheat.lower()==last_chars.lower():
        return True
    return False

def ShowTextbox(value):
    WriteStr(0xBAA7A0,value,150)

def ShowMissionPassed(value='MISSION PASSED!'):
    WriteStr(0xBAACC0,value,32)

def ShowMissionTitle(value='Mission Title'):
    for i in range(80):
        WriteStr(0xBAAD40,value,32)

def ShowSubtitle(value:str,duration=5):
    addr=0x00588FA9
    if len(subtitleCode)==0:
        for i in range(6):
            subtitleCode.append(ReadMem(addr+i))
    #startVal=subtitleCode[0]-(subtitleCode[0]%256)
    for i in range(6):
        WriteMem(addr+i,  (subtitleCode[i]-(subtitleCode[i]%256) + 0x90))
    #print(subtitleCode)
    #return
    #WriteStr(0xBAB040,'',96)
    WriteStr(0xBAB040,value,96)
    #return
    def timer():
        time.sleep(duration)
        for i in range(6):
            WriteMem(addr+i,subtitleCode[i])
            #print(subtitleCode[i])
        #return
    timerThread=threading.Thread(target=timer)
    timerThread.start()
    timerThread.join()
    return True

def ShowDialogue(value:list):
    def dialogue():
        count=0
        for i in value:
            ShowSubtitle(i[0],i[1])
            #if count+1 < len(value):
            time.sleep(i[1])
            count+=1
    dialogueThread=threading.Thread(target=dialogue)
    dialogueThread.start()
    dialogueThread.join()

def ShowStuntComplete(value='Stunt Bonus',duration=5):
    #for i in range(5):
    #    WriteStr(0xBAAE40,value)

    addr=0x0058905E
    if len(stuntCompleteCode)==0:
        for i in range(6):
            stuntCompleteCode.append(ReadMem(addr+i))
    #startVal=subtitleCode[0]-(subtitleCode[0]%256)
    for i in range(6):
        WriteMem(addr+i,  (stuntCompleteCode[i]-(stuntCompleteCode[i]%256) + 0x90))
    #print(subtitleCode)
    #return
    #WriteStr(0xBAB040,'',96)
    WriteStr(0xBAAE40,value,96)
    #return
    def timer():
        time.sleep(duration)
        for i in range(6):
            WriteMem(addr+i,stuntCompleteCode[i])
            #print(subtitleCode[i])
        #return
    timerThread=threading.Thread(target=timer)
    timerThread.start()
    timerThread.join()
    return True

def CreateGlobalVariable(size=4):
    pid = getpid()  # Ganti dengan PID proses yang sesuai
    process_handle = ctypes.windll.kernel32.OpenProcess(0x1F0FFF, False, pid)

    if process_handle:
        # Mengalokasikan memori di dalam proses
        size = 1024  # Ukuran memori yang ingin dialokasikan
        address = ctypes.windll.kernel32.VirtualAllocEx(process_handle, 0, size, 0x3000, 0x40)

        if address:
            return address
        else:
            return None
    else:
        return False

def CreateFXTFile(data,path='fxtfile.fxt'):
    """
    data
    Use array or a plain string
    """
    out=''
    if isinstance(data,dict):
        for key,value in data.items():
            out+=f'{key} {value}\n'
        print(out)
    elif isinstance(data,str):
        out=data
    else:
        print('WARNING: Unknown data type:',type(data))

    file=open(path,'w')
    file.write(out)
    file.close()

def ReadFXTFile(path):
    file=open(path,'r')
    data=file.read()
    data=data.split('\n')
    out={}
    for i in data:
        split_data=i.split(' ',1)
        if len(split_data)>1:
            out[split_data[0]]=split_data[1]
    return out

def GetGlobalJSONData():
    try:
        raw=ReadStr(CONFIG_FILE['globalModsDataAddress'],CONFIG_FILE['globalModsDataLength']).replace('\n','').replace('\t','')
        print(raw)
    except Exception as e:
        return None
    if len(raw)==0:
        return None
    return json.loads(raw)

class Player:
    def GetMoney():
        return ReadMem(0xB7CE50)
    def SetMoney(value):
        return WriteMem(0xB7CE50,value)
        
    def GetIgnoredByCops():
        return ReadMem(0xB7CD9C,offsets=[0x1E])
    def SetIgnoredByCops(value):
        return WriteMem(0xB7CD9C,offsets=[0x1E])
        
    def GetIgnoredByEveryone():
        return ReadMem(0xB7CD9C,offsets=[0x298])
    def SetIgnoredByEveryone(value):
        return WriteMem(0xB7CD9C,offsets=[0x298])

    def GetMaxWantedLevel():
        return ReadMem(0x8CDEE4)
    def SetMaxWantedLevel(value):
        return WriteMem(0x8CDEE4,value)
    
    def GetWantedLevel():
        return ReadMem(0xBAA420)
    def SetWantedLevel(value):
        return WriteMem(0xBAA420,value)
    
    def OnVehicle():
        return ReadMem(0xBA18FC)
    
    def MakeBusted():
        return WriteMem(0xB6F5F0,63,[0x530])
    def MakeWasted():
        return WriteMem(0xB6F5F0,55,[0x530])
    
    class Stats:
        def GetEnergy():
            return ReadMem(0xB790B4)
        def SetEnergy(value):
            return WriteMem(0xB790B4,value)
        
        def GetLungCapacity():
            return ReadMem(0xB791A4)
        def SetLungCapacity(value):
            return WriteMem(0xB791A4,value)
        
        def GetFat():
            return ReadMem(0xB793D4,type='f')
        def SetFat(value:float):
            return WriteMem(0xB793D4,value,type='f')
        
        def GetStamina():
            return ReadMem(0xB793D8,type='f')
        def SetStamina(value:float):
            return WriteMem(0xB793D8,value,type='f')
        
        def GetMuscle():
            return ReadMem(0xB793DC,type='f')
        def SetMuscle(value:float):
            return WriteMem(0xB793DC,value,type='f')
        
        def GetHealth():
            return ReadMem(0xB793E0,type='f')
        def SetHealth(value:float):
            return WriteMem(0xB793E0,value,type='f')

        def GetSexAppeal():
            return ReadMem(0xB793E4,type='f')
        def SetSexAppeal(value:float):
            return WriteMem(0xB793E4,value,type='f')
        
        def GetRespect():
            return ReadMem(0xB79480,type='f')
        def SetRespect(value:float):
            return WriteMem(0xB79480,value,type='f')
        
        def GetPistol():
            return ReadMem(0xB79494,type='f')
        def SetPistol(value:float):
            return WriteMem(0xB79494,value,type='f')
        
        def GetSilencedPistol():
            return ReadMem(0xB79498,type='f')
        def SetSilencedPistol(value:float):
            return WriteMem(0xB79498,value,type='f')
class Ped:
    def GetNearestPed(distance=5,target=0xB6F5F0,all=False):
        out=[]
        for i in range(1,Ped.GetMaxPed()):
            npc=Ped.GetNPC(i)
            npcPos=Ped.GetPosition(npc,True)
            #print(npcPos)
            if npcPos!=None and Ped.InDistance(npcPos,distance,target) and all==False:
                return npc
            if npcPos!=None and Ped.InDistance(npcPos,distance,target) and all:
                out.append(npc)
        if all:
            return out
        return None


    def GetMaxPed():
        return ReadOneByte(0xB74498)

    def GetNPC(index=1):
        return GetPointer(0xB7CD98,[0x7c4*index])

    def GetPosition(target=0xB6F5F0,npc=False):
        try:
            x=ReadMem(target,[0x14,0x30],'f',npc)
            y=ReadMem(target,[0x14,0x30+0x4],'f',npc)
            z=ReadMem(target,[0x14,0x30+0x8],'f',npc)
        except Exception:
            return None
        if x==None or y==None or z==None:
            return None
        return [x,y,z]
    def SetPosition(value:list,target=0xB6F5F0,npc=False):
        try:
            x=WriteMem(target,value[0],[0x14,0x30],'f',npc=npc)
            y=WriteMem(target,value[1],[0x14,0x30+0x4],'f',npc=npc)
            z=WriteMem(target,value[2],[0x14,0x30+0x8],'f',npc=npc)
        except Exception:
            return False

        return True
    
    def GetX(target=0xB6F5F0,npc=False):
        return ReadMem(target,[0x14,0x30],'f',npc)
    def SetX(value,target=0xB6F5F0,npc=False):
        return WriteMem(target,value,[0x14,0x30],'f',npc)

    def GetY(target=0xB6F5F0,npc=False):
        return ReadMem(target,[0x14,0x30+0x4],'f',npc)
    def SetY(value,target=0xB6F5F0,npc=False):
        return WriteMem(target,value,[0x14,0x30+0x4],'f',npc)

    def GetZ(target=0xB6F5F0,npc=False):
        return ReadMem(target,[0x14,0x30+0x8],'f',npc)
    def SetZ(value,target=0xB6F5F0,npc=False):
        return WriteMem(target,value,[0x14,0x30+0x8],'f',npc)

    def GetHealth(target=0xB6F5F0,npc=False):
        return ReadMem(target,[0x540],'f',npc)
    def SetHealth(value:float,target=0xB6F5F0,npc=False):
        return WriteMem(target,value,[0x540],'f',npc)
    
    def GetArmor(target=0xB6F5F0,npc=False):
        return ReadMem(target,[0x548],'f',npc)
    def SetArmor(value,target=0xB6F5F0,npc=False):
        return WriteMem(target,value,[0x548],'f',npc)

    def GetAttackerPointer(target=0xB6F5F0,npc=False):
        return GetPointer(target,[0x764],npc)

    def GetCurrentVehiclePointer(target=0xB6F5F0,npc=False):
        return GetPointer(target,[0x58C],npc)
    
    def GetAttackerPointer(target=0xB6F5F0,npc=False):
        return GetPointer(target,[0x764],npc)
        #
    def IsInvisble(target=0xB6F5F0,npc=False):
        if ReadMem(target,[0x474],npc=npc)==2 or ReadMem(target,[0x474])==671089668:
            return True
        return False
    def SetIsInvisible(value:bool,target=0xB6F5F0,npc=False):
        if value:
            return WriteMem(target,738198530,[0x474],npc=npc)
        else:
            return WriteMem(target,738198528,[0x474],npc=npc)
    def GetSurfacePhysics(target=0xB6F5F0,npc=False):
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
        return ReadOneByte(target,[0x40+0x1],npc=npc)
    def SetSurfacePhysics(value,target=0xB6F5F0,npc=False):
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
        return WriteOneByte(target,value,[0x40+0x1],npc=npc)
    
    def GetSpecialPhysicsFlags(target=0xB6F5F0,npc=False):
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
        return ReadOneByte(target,[0x40+0x2],npc=npc)
    def SetSpecialPhysicsFlags(value,target=0xB6F5F0,npc=False):
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
        return WriteOneByte(target,value,[0x40+0x2],npc=npc)

    def GetAimedPedPointer(target=0xB6F5F0,npc=False):
        return GetPointer(target,[0x79C],npc=npc)
    
    def GetNearestVehiclePointer(target=0xB6F5F0,distance=None,npc=False):
        vehiclePointer=GetPointer(target,[0x47C,0x120],npc=npc)
        if distance==None:
            return vehiclePointer
        vehiclePos=Vehicle.GetPosition(vehiclePointer)
        print(vehiclePos)
        if GTA.Ped.InDistance(vehiclePos,distance,npc=npc):
            print('uhuy')
            return vehiclePointer
        return 0
        
    
    def GetState(target=0xB6F5F0,npc=False):
        """
        0 = leaving a car, falling down from a bike or something like this
        1 = normal case
        50 = driving
        55 = wasted
        63 = busted
        """
        return ReadMem(target,[0x530],npc=npc)
    def SetState(value,target=0xB6F5F0,npc=False):
        """
        0 = leaving a car, falling down from a bike or something like this
        1 = normal case
        50 = driving
        55 = wasted
        63 = busted
        """
        return WriteMem(target,value,[0x530],npc=npc)
    
    def InDistance(position,distance,target=0xB6F5F0,npc=False):
        ped_pos=Ped.GetPosition(target,npc=npc)
        if ped_pos[0]<=position[0]+distance and ped_pos[0]>=position[0]-distance:
            if ped_pos[1]<=position[1]+distance and ped_pos[1]>=position[1]-distance:
                if ped_pos[2]<=position[2]+distance and ped_pos[2]>=position[2]-distance:
                    return True
        return False
    
    def InDistanceXY(position,distance,target=0xB6F5F0,npc=False):
        ped_pos=Ped.GetPosition(target,npc=npc)
        if ped_pos[0]<=position[0]+distance and ped_pos[0]>=position[0]-distance:
            if ped_pos[1]<=position[1]+distance and ped_pos[1]>=position[1]-distance:
                return True
        return False
        
    def GetCurrentInterior():
        return ReadOneByte(0xB72914)
    def SetCurrentInterior(value:int):
        return WriteMem(0xB72914,00000000+value)
    
    def IsOnBuildingEnterance(posList:list,dist=3):
        """
        posList=[
            [posX,posY,posZ,intId], #Enterance pos
            [posX,posY,posZ,intId], #Spawn pos
            [posX,posY,posZ] #Exit pos
            [posX,posY,posZ,intId] #Exit spawn pos
        ]
        """

        inPos=posList[0]
        inPosInt=inPos[3]
        tpPos=posList[1]
        intId=tpPos[3]
        outPos=posList[2]
        exitPos=posList[3]
        exitInt=exitPos[3]

        if GTA.Ped.InDistance(inPos,dist) and GTA.Ped.GetCurrentInterior()==inPosInt:
            #GTA.ShowTextbox('')
            #GTA.ShowTextbox('Entering Building')
            #time.sleep(1.25)
            GTA.Ped.SetCurrentInterior(intId)
            GTA.Ped.SetPosition(tpPos)
    
        if GTA.Ped.InDistance(outPos,dist) and GTA.Ped.GetCurrentInterior()==intId:
            #GTA.ShowTextbox('')
            #GTA.ShowTextbox('Exiting Building')
            #time.sleep(1.25)
            GTA.Ped.SetCurrentInterior(exitInt)
            GTA.Ped.SetPosition(exitPos)
class Game:
    def GetGameSpeed():
        return ReadMem(0xB7CB64,type='f')
    def SetGameSpeed(value:float):
        return WriteMem(0xB7CB64,value,type='f')

    def ForceClose():
        os.system(f'taskkill /f /pid {getpid()}')
        if getpid()==None:
            return True
        return False
    def GetGravity():
        return ReadMem(0x863984,type='f')
    def SetGravity(value):
        return WriteMem(0x863984,type='f')
    
    def GetMinute():
        return ReadOneByte(0xB70152)
    def SetMinute():
        return WriteOneByte(0xB70152)
    
    def GetHour():
        return ReadOneByte(0xB70153)
    def SetHour(value):
        return WriteOneByte(0xB70153,value)
        
    def GetOneMinuteInMiliseconds():
        return ReadMem(0xB7015C)
    def SetOneMinuteInMiliseconds(value):
        return WriteMem(0xB7015C,value)
        
    def GetWeekday():
        return ReadOneByte(0xB7014E)       
    def SetWeekday(value):
        return WriteMem(0xB7014E,value)

    def GetDaysPassed():
        return ReadMem(0xB79038)
    def SetDaysPassed(value):
        return WriteMem(0xB79038,value)
        
    def IsGameFreezed():
        return ReadOneByte(0xB7CB49)
    def SetIsGameFreezed(value):
        return WriteOneByte(0xB7CB49,value)
    
    def GetIsPaynSprayFree():
        return ReadOneByte()
class Menu:

    class CreateMenu:
        def __init__(self,menuType=0) -> None:
            """
            menuType
            0 = Yes or No
            """
            self.menuType=menuType
            self.lastMenu=Menu.GetCurrentMenuID()
            self.returnVal=None

            if menuType==0:
                main=threading.Thread(target=self.YesNo)
                main.start()

        def YesNo(self):
            while self.returnVal==None:
                Menu.SetCurrentMenuID(12)
                if Menu.GetCurrentHoveredMenuItem()==1:
                    if KeyPressed(KEY['Enter']) or KeyPressed(KEY['LeftMouse']):
                        self.returnVal=1
                if Menu.GetCurrentHoveredMenuItem()==2:
                    if KeyPressed(KEY['Enter']) or KeyPressed(KEY['LeftMouse']):
                        self.returnVal=2
                time.sleep(.081)
            Menu.SetCurrentMenuID(self.lastMenu)

    def IsShowingMenu():
        return ReadOneByte(0xB7CB49)
    def ShowMenu(value):
        return WriteOneByte(0xB7CB49,value)
    
    def IsGameFreezed():
        return ReadOneByte(0xB7CB49)
    def SetIsGameFreezed(value):
        return WriteOneByte(0xB7CB49,value)
    
    def GetCurrentMenuID():
        return ReadOneByte(0xBA6748+0x15D)
    def SetCurrentMenuID(value):
        """
        0 = Stats
        1 = Start game
        2 = Brief
        3 = Audio options
        4 = Display settings
        5 = Map
        6 = Question start new game
        7 = Game selection
        8 = Question load mission pack
        9 = Load game
        10 = Delete game
        11 = Question load save game
        12 = Question delete game
        13 = Loads first savegame? *crash
        14 = Delete successful
        15 = Delete successful
        16 = Save game
        17 = Question save
        18 = Save successful
        19 = Save successful
        20 = Save game ok
        21 = Load game ok
        22 = Game affected, do not save
        23 = Display default settings
        24 = Audio default settings
        25 = Controller default settings
        26 = User track options
        28 = Language
        29 = Save game ok
        30 = Save unsuccessful
        31 = Load game (save unsuccessful)
        32 = Load unsuccessful, file corrupted
        33 = Options
        34 = Main menu
        35 = Quit game
        36 = Controller setup
        37 = Redefine controls
        38 = Foot/vehicle controls
        39 = Mouse settings
        40 = Joypad settings
        41 = Game running main menu
        42 = Quit game
        43 = Empty
        Note: If you have modloader
        44 = Mod configuration
        45 = Modifications
        46 = Current mod menu (in modifications)
        """
        return WriteOneByte(0xBA6748+0x15D,value)
    
    def GetCurrentHoveredMenuItem():
        return ReadOneByte(0xBA6748+0x54)
    def SetCurrentHoveredMenuItem(value):
        return WriteOneByte(0xBA6748+0x54,value)

    def IsPlayerInMenu():
        return ReadOneByte(0xBA6748+0x5C)
    def SetIsPlayerInMenu(value):
        return WriteOneByte(0xBA6748+0x5C,value)
    
    def GetSelectedSaveGame():
        return ReadOneByte(0xBA6748+0x15F)
    
    def SetSelectedSaveGame(value:int):
        return WriteOneByte(0xBA6748+0x15F,value)
    
class Settings:
    def GetCanCameraMove():
        if ReadMem(0xB6EC1C,type='f')==0:
            return True
        return False
    def SetCanCameraMove(value:bool):
        if value:
            return WriteMem(0xB6EC1C,Settings.Controller.defaultMouseSensitivity,type='f')
        return WriteMem(0xB6EC1C,0,type='f')
    
    class Controller:
        defaultMouseSensitivity=0.002499999944
        def GetMouseSensitivity():
            return ReadMem(0xB6EC1C,type='f')
        def SetMouseSensitivity(value:float):
            return WriteMem(0xB6EC1C,value,type='f')
        
        def GetSteerWithMouse():
            return ReadOneByte(0xC1CC02)
        def SetSteerWithMouse(value:int):
            return WriteOneByte(0xC1CC02,value)
        
        def GetFlyWithMouse():
            return ReadOneByte(0xC1CC03)
        def SetFlyWithMosue(value:int):
            return WriteOneByte(0xC1CC03)
        
        def GetAimingMode():
            return ReadOneByte(0xB6EC2E)
        def SetAimingMode(value:int):
            return WriteOneByte(0xB6EC2E,value)
    class Display:
        #WANTED_LEVEL_START_RED=ReadMem(0x58DD50)
        #WANTED_LEVEL_START_GREEN=ReadMem(0x58DD4E)
        #WANTED_LEVEL_START_BLUE=ReadMem(0x58DD4C)
        def GetBrightness():
            return ReadMem(0xBA6784)
        def SetBrightness(value):
            """
            max: 384
            i prefer: 240
            min: 0
            """
            return WriteMem(0xBA6784,value)

        def GetLegend():
            if ReadMem(0xBA6792):
                return True
            return False
        def SetLegend(value):
            """
            on: 1>
            off: 0
            """
            return WriteMem(0xBA6792,value)

        def SetWantedStarsColor(value:list):
            """
            [R,G,B]
            """
            red=ReadMem(0x58DD50)-ReadOneByte(0x58DD50)+value[0]
            WriteOneByte(0x58DD50,red,start_value=0)
            green=ReadMem(0x58DD4E)-ReadOneByte(0x58DD4E)+value[1]
            WriteOneByte(0x58DD4E,green,start_value=0)
            blue=ReadMem(0x58DD4C)-ReadOneByte(0x58DD4C)+value[2]
            WriteOneByte(0x58DD4C,blue,start_value=0)
            print(red,green,blue)

        def SetWantedStarsSize(value:float):
            """
            Really useless...
            0 = Star Icon
            1 = ]
            """
            return WriteMem(0x866C60,value,type='f')

        def SetWantedStarsBorderSize(value):
            return WriteOneByte(0x58DD41,value)

        def GetRadarMode():
            return ReadOneByte(0xBA676C)
        def SetRadarMode(value):
            return WriteOneByte(0xBA676C,value)

        def GetHUDMode():
            return ReadOneByte(0xBA6769)
        def SetHUDMode(value):
            return WriteOneByte(0xBA6769,value)
class Vehicle:
    def GetVehicleMass(target=0xBA18FC):
        return ReadMem(target,[0x8C],'f')
    def SetVehicleMass(value,target=0xBA18FC):
        return WriteMem(target,value,[0x8C],'f')
    
    def GetCameraViewMode(target=0xBA18FC):
        return ReadMem(0xB6F0DC)
    def SetCameraViewMode(value,target=0xBA18FC):
        return WriteMem(0xB6F0DC,value)
        
    def GetDirtyLevel(target=0xBA18FC):
        return ReadMem(target ,[0x4B0],'f')
    def SetDirtyLevel(value,target=0xBA18FC):
        return WriteMem(target,value,[0x4B0],'f')
    
    def GetGripDivider(target=0xBA18FC):
        return ReadMem(target,[0x94],'f')
    def SetGripDivider(value,target=0xBA18FC):
        return WriteMem(target,value,[0x94],'f')
    
    def GetEngineState(target=0xBA18FC):
        return ReadOneByte(target,[0x428])
    def SetEngineState(value,target=0xBA18FC):
        if value:
            return WriteMem(target,16,[0x428])
        return WriteMem(target,0,[0x428])
    
    def GetTiresSize(target=0xBA18FC):
        return ReadMem(target,[0x458],'f')
    def SetTiresSize(value,target=0xBA18FC):
        return WriteMem(target,value,[0x458],'f')
    
    def GetDriverPointer(target=0xBA18FC):
        return GetPointer(target,[0x460])
    
    def GetPosition(target=0xBA18FC):
        x=ReadMem(target,[0x14,0x30],'f')
        y=ReadMem(target,[0x14,0x30+0x4],'f')
        z=ReadMem(target,[0x14,0x30+0x8],'f')
        return [x,y,z]
    def SetPosition(value:list,target=0xBA18FC):
        x=WriteMem(target,value[0],[0x14,0x30],'f')
        y=WriteMem(target,value[1],[0x14,0x30+0x4],'f')
        z=WriteMem(target,value[2],[0x14,0x30+0x8],'f')
        return Vehicle.GetPosition(target)

    def GetX(target=0xBA18FC):
        return ReadMem(target,[0x14,0x30],'f')
    def SetX(value,target=0xBA18FC):
        return WriteMem(target,value,[0x14,0x30],'f')
    def GetY(target=0xBA18FC):
        return ReadMem(target,[0x14,0x30+0x4],'f')
    def SetY(value,target=0xBA18FC):
        return WriteMem(target,value,[0x14,0x30+0x4],'f')
    def GetZ(target=0xBA18FC):
        return ReadMem(target,[0x14,0x30+0x8],'f')
    def SetZ(value,target=0xBA18FC):
        return WriteMem(target,value,[0x14,0x30+0x8],'f')

    #Auto accelerate code
    accCode0=[]
    #Activator code
    accCode1=[]

    def Accelerate(value:int,duration=5,actDelay=.025):
        if isfocused() and Menu.IsPlayerInMenu():
            if len(Vehicle.accCode0)==0:
                for i in range(4):
                    Vehicle.accCode0.append(ReadMem(0x0053EFBD+i))
            if len(Vehicle.accCode1)==0:
                for i in range(2):
                    Vehicle.accCode1.append(ReadMem(0x00541C74+i))
            print(Vehicle.accCode0,Vehicle.accCode1)
            for i in range(4):
                print(WriteMem(0x0053EFBD+i,(Vehicle.accCode0[i]-( Vehicle.accCode0[i]%256 )+ 0x90 )))

            WriteOneByte(0xB73458 +0x20,value)
            for i in range(2):
                WriteMem(0x00541C74+i,(Vehicle.accCode1[i]-( Vehicle.accCode1[i]%256 )+ 0x90 ))
            time.sleep(actDelay)
            for i in range(2):
                WriteMem(0x00541C74+i,Vehicle.accCode1[i])
            
            def stop():
                time.sleep(duration)
                for i in range(4):
                    WriteMem(0x0053EFBD+i,(Vehicle.accCode0[i]-( Vehicle.accCode0[i]%256 )+ 0x90 ))

            stopThread=threading.Thread(target=stop)
            stopThread.start()
            stopThread.join()
            return

class Locations:
    losSantos=[2505.39208984375, -1682.944091796875, 13.546875]
    sanFierro=[-2022.945556640625, 143.93690490722656, 28.8359375]
    lasVenturas=[2027.4886474609375, 1000.4976806640625, 10.8203125]
    libertyCity=[-738.2490844726562, 482.49835205078125, 1371.703369140625]

