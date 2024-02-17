import ctypes, win32gui, win32process
from ctypes import wintypes

PROCESS_ALL_ACCESS = 0x1F0FFF

def getpid():
    window_title='GTA: San Andreas'
    hwnd = win32gui.FindWindow(None, window_title)
    if hwnd == 0:
        return None

    pid = win32process.GetWindowThreadProcessId(hwnd)[1]
    return pid

def wmem(address, data):
    process_id=getpid()

    # Open the target process
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)

    if not process_handle:
        return False

    if isinstance(data, int):
        data_bytes = data.to_bytes(4, byteorder='little', signed=True)
    elif isinstance(data, str):
        data_bytes = data.encode('utf-8')
    else:
        return False  # Unsupported data type

    # Write the memory
    bytes_written = ctypes.wintypes.DWORD(0)
    result = ctypes.windll.kernel32.WriteProcessMemory(process_handle, address, data_bytes, len(data_bytes), ctypes.byref(bytes_written))

    # Close the process handle
    ctypes.windll.kernel32.CloseHandle(process_handle)

    return result

def rmem(address, size, type='int'):
    process_id=getpid()

    # Open the target process
    process_handle = ctypes.windll.kernel32.OpenProcess(PROCESS_ALL_ACCESS, False, process_id)

    if not process_handle:
        return None

    # Create a buffer to store the read data
    buffer = ctypes.create_string_buffer(size)

    # Read the memory
    bytes_read = ctypes.wintypes.DWORD(0)
    if ctypes.windll.kernel32.ReadProcessMemory(process_handle, address, buffer, size, ctypes.byref(bytes_read)):
        data = buffer.raw[:bytes_read.value]
    else:
        data = None

    # Close the process handle
    ctypes.windll.kernel32.CloseHandle(process_handle)
    if type=='int':
        data=int.from_bytes(data,'little')
    return data

class player:
    def add_money(amount:int):
        wmem(0xB7CE50,int(rmem(0xB7CE50,4))+amount)
    def remove_money(amount:int):
        wmem(0xB7CE50,int(rmem(0xB7CE50,4))-amount)
    def set_money(money:int):
        wmem(0xB7CE50,money)
    def money_val():
        return rmem(0xB7CE50,4)

    def add_health(amount:int):
        pass
        
    class stats:
        def add_lung_capacity(amount:int):
            wmem(0xB791A4,int(rmem(0xB791A4,4))+amount)
        def remove_lung_capacity(amount:int):
            wmem(0xB791A4,int(rmem(0xB791A4,4))-amount)
        def lung_capacity_val():
            return int(rmem(0xB791A4,4))
            
        def add_fat(amount:int):
            wmem(0xB793D4 ,int(rmem(0xB793D4 ,4))+amount)
        def remove_fat(amount:int):
            wmem(0xB793D4 ,int(rmem(0xB793D4 ,4))-amount)
        def fat_val():
            return int(rmem(0xB793D4 ,4))
            
        def add_stamina(amount:int):
            wmem(0xB793D8,int(rmem(0xB793D8,4))+amount)
        def remove_stamina(amount:int):
            wmem(0xB793D8,int(rmem(0xB793D8,4))-amount)
        def stamina_val():
            return int(rmem(0xB793D8,4))
            
        def add_muscle(amount:int):
            wmem(0xB793DC,int(rmem(0xB793DC,4))+amount)
        def remove_muscle(amount:int):
            wmem(0xB793DC,int(rmem(0xB793DC,4))-amount)
        def muscle_val():
            return int(rmem(0xB793DC,4))
            
        def add_muscle(amount:int):
            wmem(0xB793DC,int(rmem(0xB793DC,4))+amount)
        def remove_muscle(amount:int):
            wmem(0xB793DC,int(rmem(0xB793DC,4))-amount)
        def muscle_val():
            return int(rmem(0xB793DC,4))
    
class game:
    def freeze(condition:bool):
        if condition:
            wmem(0xB7CB49,1)
            return
        wmem(0)
    def menu(condition:bool):
        if condition:
            wmem(0xB7CB49,1)
            return
        wmem(0xB7CB49,0)
    def gravity(value:int):
        pass