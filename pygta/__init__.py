import ctypes, win32gui, win32process,struct,win32gui,win32process
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
    
#def StringToFourBytes(string):
#    bytes_data = string.encode('utf-8')
#    numeric_value = struct.unpack('i', bytes_data)[0]
#    return numeric_value

