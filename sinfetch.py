import shutil

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


def showSystemInfo():
    memTotal, memAvailable, memFree =  getMemInfo()
    
    cpu_model, cpu_core = getCPUInfo()
    
    divide_line = (shutil.get_terminal_size().columns - 3)*('-')

    print(
            f'-{divide_line}\n'
            f'| Memory:\t{memAvailable} MB / {memTotal} MB\n'
            f'|{divide_line}\n'
            f'| CPU:\t\t{cpu_model}\n'
            f'| Core:\t\t{cpu_core}\n'
            )


if __name__== '__main__':
    showSystemInfo()
