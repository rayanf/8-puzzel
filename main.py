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
import tracemalloc

exeMem = 0


# this function gets search algorithm and sample and returns the answer's actions if found
def findAns(alg,sample,max_depht=25):
    # max_depht = 25
    if alg == 'DFS':
        record = dfsMain(sample, max_depht)
    if alg == 'BFS':
        record = bfsMain(sample, max_depht)
    if alg == 'IDS':
        record = idsMain(sample, max_depht+10)
    if alg == 'UCS':
        record = ucsMain(sample, max_depht-5)
    if alg == 'Astar':
        record = aStarMain(sample, max_depht*5)
    return record


# main function
def main():
    examples = readExamples()
    global exeMem

    # list of algorithms strings to save in data frame
    algorithms = ['DFS', 'BFS', 'IDS', 'UCS', 'Astar']
   
    # data frame to save and compare results with each algorithm time and memory
    data = pd.DataFrame(columns=['DFSTime', 'DFSMemory', 'BFSTime', 'BFSMemory', 'IDSTime', 'IDSMemory', 'UCSTime', 'UCSMemory', 'AstarTime', 'AstarMemory']) 
    data = pd.read_csv("results.csv")
    # data frame for answers with each algorithm for each sample
    answers = pd.DataFrame(columns=['DFS', 'BFS', 'IDS', 'UCS', 'Astar'])
    answers = pd.read_csv('answers.csv')
    for i, sample in enumerate(examples[51:]):
        # solution actions with each algorithm for each sample
        actions = {}
        
        # memory and time with each algorithm for each sample
        timesMem = {}

        for alg in algorithms:
            print(f'{alg} {i+1}')
            # set start time to track execution time
            startTime = time.time()

            # set start memory to track memory usage
            tracemalloc.start()
            memStart, fpeak = tracemalloc.get_traced_memory()
            # tracemalloc.reset_peak()

            #find answer with each algorithm   
            record = findAns(alg,sample)
            
            # set end memory to track memory usage
            current, peak = tracemalloc.get_traced_memory()
            exeMem = peak / 10**6 - memStart / 10**6 - 8000
            tracemalloc.stop()

            # set end time to track execution time
            exeTime = time.time() - startTime
            
            
            algTime = alg+'Time'
            algMem = alg+'Memory'
            
            # if answer found save time and memory
            # else save nan
            if record != None:
                timesMem[algTime] = round(exeTime,3)
                timesMem[algMem] = exeMem
            else:
                timesMem[algTime] = np.nan
                timesMem[algMem] = np.nan
            
            actions[alg] = str(record)
        actions =  pd.DataFrame(actions, index=[0])
        answers = pd.concat([answers, actions], axis=0)

        dfTemp = pd.DataFrame(timesMem, index=[0])
        data = pd.concat([data, dfTemp], axis=0)

        if i % 5 == 0:
            # save data frame as CSV file
            data = data.reindex(columns=['DFSTime', 'BFSTime', 'IDSTime', 'UCSTime', 'AstarTime', 'DFSMemory', 'BFSMemory', 'IDSMemory', 'UCSMemory', 'AstarMemory'])
            data.to_csv('results.csv', index=False)

            answers.to_csv('answers.csv', index=False)


# read samples from file
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
