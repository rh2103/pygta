import ctypes, win32gui, win32process,struct,win32gui,win32process,time,json,logging,os
from ctypes import wintypes
from ReadWriteMemory import ReadWriteMemory

PROCESS_ALL_ACCESS = 0x1F0FFF
SETTINGS_FILE=json.load(open(os.path.join(__file__.rsplit('\\',1)[0],'settings.json')))

GTA_SA_DIR=SETTINGS_FILE['pygta']['gta_sa_dir']
MOD_DIR=os.path.join(GTA_SA_DIR,'modloader/pygta')

rwm=ReadWriteMemory()

logging.basicConfig(filename=os.path.join(MOD_DIR,'log_output.log').replace('\\','/'),level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def getpid():
    window_title='GTA: San Andreas'
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        return None

    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return pid
def isfocused():
    hwnd = win32gui.GetForegroundWindow()
    _, pid = win32process.GetWindowThreadProcessId(hwnd)
    if pid==getpid():
        return True
    return False
def wmem(address,value,offsets=[]):
    process=rwm.get_process_by_id(getpid())
    process.open()
    pointer=process.get_pointer(address,offsets)
    process.write(pointer,value)
    result=process.read(pointer)
    process.close()
    return result
def rmem(address,offsets=[]):
    #print(getpid())
    process=rwm.get_process_by_id(getpid())
    process.open()
    pointer=process.get_pointer(address,offsets=offsets)
    return process.read(pointer)

def GetPointer(address,offsets):
    process=rwm.get_process_by_id(getpid())
    process.open()
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
    
    
def CreateModSaveFile(filename):
    mod_files=os.listdir(MOD_DIR)
    filename=filename.rsplit('\\',1)[0]
    filename_without_ext=filename.rsplit('.',1)[0]
    if not filename_without_ext+'.json' in mod_files:
        sv=open(os.path.join(MOD_DIR,filename_without_ext)+'.json','w')
        sv.write('{}')
        sv.close()
        logging.info(f'File {filename} loaded.')
        return os.path.join(MOD_DIR,filename_without_ext)+'.json'
    else:
        print('Mod Save File already created!')
        return os.path.join(MOD_DIR,filename_without_ext)+'.json'
#def StringToFourBytes(string):
#    bytes_data = string.encode('utf-8')
#    numeric_value = struct.unpack('i', bytes_data)[0]
#    return numeric_value
import pygta.gta as GTA