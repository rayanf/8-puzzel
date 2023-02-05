import os
import psutil 
import numpy as np
import pandas as pd
import time
from DFS import dfsMain
from BFS import bfsMain
from IDS import idsMain
from UCS import ucsMain
from Astar import aStarMain


exeMem = 0

def process_memory():
    process = psutil.Process(os.getpid())
    mem_info = process.memory_info()
    return mem_info.rss
 
 
def profile(func):
    global exeMem
    def wrapper(*args, **kwargs):
 
        mem_before = process_memory()
        result = func(*args, **kwargs)
        mem_after = process_memory()
        exeMem = (mem_after - mem_before)
 
        return result
    return wrapper
 

@profile
def findAns(alg,sample):
    max_depht = 50
    if alg == 'DFS':
        record = dfsMain(sample, max_depht)
    if alg == 'BFS':
        record = bfsMain(sample, max_depht)
    if alg == 'IDS':
        record = idsMain(sample, max_depht)
    if alg == 'UCS':
        record = ucsMain(sample, max_depht)
    if alg == 'Astar':
        record = aStarMain(sample, max_depht*5)
    return record


def main():
    examples = readExamples()
    global exeMem

    data = pd.DataFrame(columns=['DFSTime', 'DFSMemory', 'BFSTime', 'BFSMemory', 'IDSTime', 'IDSMemory', 'UCSTime', 'UCSMemory', 'AstarTime', 'AstarMemory'])

    with open('results.txt', 'w') as f:
        algorithms = ['DFS', 'BFS', 'IDS', 'UCS', 'Astar']
        for i, sample in enumerate(examples[:2]):
            timesMem = {}
            foundedd = False
            for alg in algorithms:
                print(f'{alg} {i+1}')
                startTime = time.time()
                # startMem = process_memory()
                record = findAns(alg,sample)
                # exeMem = process_memory() - startMem
                exeTime = time.time() - startTime
                algTime = alg+'Time'
                algMem = alg+'Memory'
                
                if record != None:
                    timesMem[algTime] = round(exeTime,3)
                    timesMem[algMem] = exeMem
                else:
                    timesMem[algTime] = np.nan
                    timesMem[algMem] = np.nan
                
                if record != None and not foundedd:
                    foundedd = True
                    f.write(f'{record}\n')
            dfTemp = pd.DataFrame(timesMem, index=[0])
            data = pd.concat([data, dfTemp], axis=0)

    data = data.reindex(columns=['DFSTime', 'BFSTime', 'IDSTime', 'UCSTime', 'AstarTime', 'DFSMemory', 'BFSMemory', 'IDSMemory', 'UCSMemory', 'AstarMemory'])
    data.to_csv('results.csv', index=False)



def readExamples():
    examples = []
    with open('examples.txt') as f:
        for line in f:
            sample = line[3:-3].split(",")
            if len(sample) == 9:
                sample = [int(i) for i in sample]
                examples.append(sample)
    return examples



if __name__ == "__main__":
    main()
    # data = pd.read_csv('results.csv')
    # print(data)
    # showSample([1,2,3,4,5,6,7,8,0])


