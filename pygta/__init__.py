import ctypes, win32gui, win32process,struct
from ctypes import wintypes
from ReadWriteMemory import ReadWriteMemory

PROCESS_ALL_ACCESS = 0x1F0FFF
rwm=ReadWriteMemory()

def getpid():
    window_title='GTA: San Andreas'
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        return None

    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return pid
def wmem(address,value,offsets=[]):
    process=rwm.get_process_by_id(getpid())
    process.open()
    pointer=process.get_pointer(address,offsets)
    process.write(pointer,value)
    result=process.read(pointer)
    process.close()
    return result

def FourBytesToFloat(bytes):
    data_bytes = struct.pack('<I', bytes)

    # Mengubah 4 bytes menjadi nilai float
    value_float = struct.unpack('<f', data_bytes)[0]
    return value_float
def FloatToFourBytes(float):
    return struct.unpack('<I', struct.pack('<f', float))[0]

def rmem(address,offsets=[]):
    #print(getpid())
    process=rwm.get_process_by_id(getpid())
    process.open()
    pointer=process.get_pointer(address,offsets=offsets)
    return process.read(pointer)