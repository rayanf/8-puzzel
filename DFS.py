import numpy as np
import math



GOAL_STATE = [1,2,3,4,5,6,7,8,0]
founded = False
max_depht = 50

Ans = None

def DFS(sample, hashtable = None,records = None,depht = 0):
    global max_depht
    global founded
    global Ans

    if hashtable == None:
        hashtable = HashTable()
    if records == None:
        records = []
    
    depht += 1
    if depht > max_depht:
        return None
    
    hashtable.hash(sample)
    action = None
    for next in nextSamples(sample).values():

        for key in nextSamples(sample).keys():
            if nextSamples(sample)[key] == next:
                action = key
                
        if not hashtable.check(next):   
            records.append(action)
            if next == GOAL_STATE:
                founded = True
                Ans = records.copy()
                return records
            
            DFS(next, hashtable,records,depht)
            records.pop()
            if founded:
                break
    

def nextSamples(sample):
    nexts = {}
    MatSample = np.array(sample).reshape(3,3)
    zeroIndex = np.where(MatSample == 0)
    index = [zeroIndex[0][0], zeroIndex[1][0]]
    i,j = index[0], index[1]
    if i > 0:
        nextt = MatSample.copy()
        nextt[i-1][j], nextt[i][j] = nextt[i][j], nextt[i-1][j]
        nexts['up'] = nextt.reshape(9).tolist()
    if i < 2:
        nextt = MatSample.copy()
        nextt[i+1][j], nextt[i][j] = nextt[i][j], nextt[i+1][j]
        nexts['down'] = nextt.reshape(9).tolist()
    if j > 0:
        nextt = MatSample.copy()
        nextt[i][j-1], nextt[i][j] = nextt[i][j], nextt[i][j-1]
        nexts['left'] = nextt.reshape(9).tolist()
    if j < 2:
        nextt = MatSample.copy()
        nextt[i][j+1], nextt[i][j] = nextt[i][j], nextt[i][j+1]
        nexts['right'] = nextt.reshape(9).tolist()
    return nexts




class HashTable:
    def __init__(self):
        self.table = np.zeros(1000000000)
    
    def hash(self, sample):
        string = ''
        for i in sample:
            string += str(i)
        intger = int(string)
        self.table[intger] = 1
    
    def check(self, sample):
        string = ''
        for i in sample:
            string += str(i)
        intger = int(string)
        return self.table[intger] == 1


def dfsMain(sample,max_dephtt):
    global Ans
    global founded
    global max_depht
    max_depht = max_dephtt
    founded = False
    Ans = None
    records = DFS(sample)
    return(Ans)    

if __name__ == "__main__":

    # print(dfsMain([1,2,3,4,5,6,7,8,0],50))
    records = DFS([1,2,3,0,7,6,5,4,8])
    print(Ans)