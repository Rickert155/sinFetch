MEMINFO_FILE = '/proc/meminfo'

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


def showSystemInfo():
    memTotal, memAvailable, memFree =  getMemInfo()
    print(
            f'Mem Total:\t{memTotal} MB\n'
            f'Mem Available:\t{memAvailable} MB\n'
            f'Mem Free:\t{memFree} MB'
            )


if __name__== '__main__':
    showSystemInfo()
