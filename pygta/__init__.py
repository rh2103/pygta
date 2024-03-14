import win32gui, win32process,struct,win32gui,win32process,time,json,os,ctypes
import ctypes.wintypes
#import ReadWriteMemory as rwmem
from ReadWriteMemory import ReadWriteMemory
from rwmem import *

SETTINGS_FILE=json.load(open(os.path.join(__file__.rsplit('\\',1)[0],'settings.json')))

GTA_SA_DIR=SETTINGS_FILE['pygta']['gta_sa_dir']
MOD_DIR=os.path.join(GTA_SA_DIR,'modloader/pygta')
rwm=ReadWriteMemory()
pid=None

#logging.basicConfig(filename=os.path.join(MOD_DIR,'log_output.log').replace('\\','/'),level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


def getpid():
    global pid
    if pid==None:
        window_title='GTA: San Andreas'
        hwnd = win32gui.FindWindow(None, window_title)
        if hwnd == 0:
            return None

        gtapid = win32process.GetWindowThreadProcessId(hwnd)[1]
        pid=gtapid
        return gtapid
    return pid
memory.open(getpid())
def isfocused():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid==getpid():
        return True
    return False

def WriteStr(address,value,length=32,offsets=[]):
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    if len(value)>=0:
        text=list(value)
        text=[ord(char) for char in text]
        if len(text) > length:
            for _ in range(len(text) - length):
                text.pop()
        for index,i in enumerate(text):
            memory.write(address+index,i)
        #return memory.readStr(address,length)
    if len(value)==0:
        for i in range(0,length+1):
            memory.write(address+i,0)
    #return memory.readStr(address,length)
    return True
def WriteMem(address,value,offsets=[],type='ui',npc=False):
    if npc and len(offsets)>0:
        address+=offsets[0]
        del offsets[0]
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    memory.write(address,value,type)
    #return ReadMem(address,type=type)
    return True
def WriteOneByte(address,value,offsets=[],start_value=256,npc=False):
    if npc and len(offsets)>0:
        address+=offsets[0]
        del offsets[0]
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    memory.write(address,start_value+value)
    #return ReadOneByte(address)

def ReadMem(address,offsets=[],type='ui',npc=False):
    if npc and len(offsets)>0:
        address+=offsets[0]
        del offsets[0]
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    
    #print('\t\t\t',address,offsets)
    try:
        return memory.read(address,type)
    except Exception:
        return None
def ReadStr(address,length=32,offsets=[]):
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    return memory.readStr(address,length)
    #chars=[]
    #out=''
    #for i in range(length+1):
    #    chars.append(ReadMem(address+i))
    #print(chars)
    #for char in chars:
    #    out+=chr(char)
    #print(out)
    #return out
def ReadOneByte(address,offsets=[],npc=False):
    if npc and len(offsets)>0:
        address+=offsets[0]
        del offsets[0]
    if len(offsets)>0:
        address=GetPointer(address,offsets)
    try:
        return memory.read(address,'ui')%256
    except Exception:
        return None

def CallFunction(address):
    kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)

    # Buka proses target
    process_handle = kernel32.OpenProcess(0x1F0FFF, False, getpid())  # Sesuaikan target_process_id

    # Alamat fungsi yang akan dipanggil
    function_address = ctypes.c_void_p(address)  # Sesuaikan alamat fungsi

    # Alamat argumen untuk fungsi, jika diperlukan
    #argument_address = ctypes.c_void_p(0x733330)  # Sesuaikan alamat argumen

    # Buat thread di dalam proses target untuk memanggil fungsi
    thread_id = ctypes.wintypes.DWORD()
    kernel32.CreateRemoteThread(process_handle, None, 0, function_address, None, 0, ctypes.byref(thread_id))

    # Tunggu hingga thread selesai, jika diperlukan
    kernel32.WaitForSingleObject(thread_id, -1)

    # Tutup handle proses
    kernel32.CloseHandle(process_handle)

def GetPointer(address,offsets,npc=False):
    process=rwm.get_process_by_id(getpid())
    process.open()
    if npc and len(offsets)>0:
        address+=offsets[0]
        del offsets[0]
    return process.get_pointer(address,offsets=offsets)

def FourBytesToFloat(bytes):
    data_bytes = struct.pack('<I', bytes)

    # Mengubah 4 bytes menjadi nilai float
    value_float = struct.unpack('<f', data_bytes)[0]
    return value_float
def FloatToFourBytes(float):
    return struct.unpack('<I', struct.pack('<f', float))[0]

def FourBytesToSingleByte(bytes):
    return bytes % 256
    
def FourBytesToString(bytes):
    bytes_data = struct.pack('d', bytes)
    return bytes_data.decode('utf-8')
    
    
#def CreateModSaveFile(filename):
#    mod_files=os.listdir(MOD_DIR)
#    filename=filename.rsplit('\\',1)[0]
#    filename_without_ext=filename.rsplit('.',1)[0]
#    if not filename_without_ext+'.json' in mod_files:
#        sv=open(os.path.join(MOD_DIR,filename_without_ext)+'.json','w')
#        sv.write('{}')
#        sv.close()
#        logging.info(f'File {filename} loaded.')
#        return os.path.join(MOD_DIR,filename_without_ext)+'.json'
#    else:
#        print('Mod Save File already created!')
#        return os.path.join(MOD_DIR,filename_without_ext)+'.json'
##def StringToFourBytes(string):
#    bytes_data = string.encode('utf-8')
#    numeric_value = struct.unpack('i', bytes_data)[0]
#    return numeric_value
import pygta.gta as GTA