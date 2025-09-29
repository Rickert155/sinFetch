import shutil, subprocess

RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
RESET = "\033[0m"

MEMINFO_FILE = '/proc/meminfo'
CPUINFO_FILE = '/proc/cpuinfo'

def parseLine(line:str, pattern:str):
    kb = 'kB'
    value = line.split(pattern)[1]
    if kb in value:value = value.split(kb)[0].strip()
    value = round(int(value) / 1024, 1)
    return value

def getMemInfo():
    memTotal = None
    memAvailable = None
    memFree = None

    with open(MEMINFO_FILE, 'r') as file:
        for line in file:
            line = line.strip()
            memTotalPattern = 'MemTotal:'
            memAvailablePattern = 'MemAvailable:'
            memInactivePattern = 'Inactive(file):'
            memBuffersPattern = 'Buffers:'
            memCachedPattern = 'Cached:'

            if memTotalPattern in line:
                memTotal = parseLine(line=line, pattern=memTotalPattern)
            if memAvailablePattern in line:
                memAvailable = parseLine(line=line, pattern=memAvailablePattern)
            if memBuffersPattern in line:
                memBuffers = parseLine(line=line, pattern=memBuffersPattern)
            if memCachedPattern in line:
                memCached = parseLine(line=line, pattern=memCachedPattern)
            if memInactivePattern in line:
                memFree = parseLine(line=line, pattern=memInactivePattern)
    memAvailable = round(memTotal - memAvailable - memBuffers - memCached, 1) 
    return memTotal, memAvailable, memFree

def getCPUInfo():
    cpu_model = None 
    cpu_core = 0 
    
    patternLineModeleName = 'model name'
    patternLineCore = 'processo'

    with open(CPUINFO_FILE, 'r') as file:
        for line in file.readlines():
            line = line.strip()
            if patternLineModeleName in line:
                cpu_model = line.split(': ')[1].strip()
            if patternLineCore in line:
                cpu_core+=1


    return cpu_model, cpu_core

def getGPUInfo():
    command = 'lspci | grep -E "VGA|3D"'
    gpu = run_command(command=command)
    gpu = gpu.split(': ')[1]
    return gpu

def getWM():
    commands = ['echo $XDG_SESSION_DESKTOP', 'echo $DESKTOP_SESSION']
    wm = run_command(command=commands[0])
    if len(wm) < 1:
        wm = run_command(command=commands[1])
    return wm

def run_command(command:str):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip()


def run_command(command:str):
    result = subprocess.run(command, capture_output=True, text=True, shell=True)
    return result.stdout.strip()

def showSystemInfo():
    memTotal, memAvailable, memFree =  getMemInfo()
    cpu_model, cpu_core = getCPUInfo()
    gpu = getGPUInfo()
    wm = getWM()

    divide_line = (shutil.get_terminal_size().columns - 2)*('-')

    print(
            f'{RED}-{divide_line}\n{RESET}'
            f'{RED}|{RESET} Memory:\t{memAvailable} MB / {memTotal} MB\n'
            f'{RED}|{divide_line}\n{RESET}'
            f'{RED}|{RESET} CPU:\t\t{cpu_model}\n'
            f'{RED}|{RESET} Core:\t\t{cpu_core}\n'
            f'{RED}-{divide_line}\n{RESET}'
            f'{RED}|{RESET} GPU:\t\t{gpu}\n'
            f'{RED}-{divide_line}\n{RESET}'
            f'{RED}|{RESET} WM:\t\t{wm}\n'
            f'{RED}-{divide_line}\n{RESET}'
            )


if __name__== '__main__':
    showSystemInfo()
