import numpy as np
import math
import collections



GOAL_STATE = [1,2,3,4,5,6,7,8,0]
founded = False
max_depht = 100


def Astar(sample):
    global max_depht
    global founded

    hashtable = HashTable()
    hashtable.hash(sample)
    actionNode = ActionNode(None)
    queue = collections.deque([(sample,actionNode,0)])
    depht = 0
    action = None

    while queue:
        sample,actionNode,cost = queue.popleft()
        # print(cost)
        if cost > max_depht:
            return None

        for next in nextSamples(sample).values():
            for key in nextSamples(sample).keys():
                if nextSamples(sample)[key] == next:
                    action = key

            nextAction = ActionNode(action)
            nextAction.parent = actionNode

            if not hashtable.check(next):
                if next == GOAL_STATE:
                    records = printActions(nextAction)
                    founded = True
                    return records

                queue.append((next,nextAction,cost+h(next)))
                sorted(queue, key=lambda x: x[2])
                
                hashtable.hash(next)
    
def h(sample):
    matSample = np.array(sample).reshape(3,3)
    goalSample = np.array(GOAL_STATE).reshape(3,3)
    cost = 0
    for i in range(3):
        for j in range(3):
            ihat,jhat = np.where(goalSample == matSample[i][j])[0][0],np.where(goalSample == matSample[i][j])[1][0]
            cost += abs(ihat-i)
            cost += abs(jhat-j)

    return cost

def printActions(actionNode):
    actions = []
    while actionNode.parent != None:
        actions.append(actionNode.action)
        actionNode = actionNode.parent
    actions.reverse()
    return actions

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


class ActionNode:
    def __init__(self, action):
        self.action = action
        self.parent = None
    def setParent(self, parent):
        self.parent = parent


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


def aStarMain(saample, max_dephtt):
    global founded
    global max_depht
    founded = False
    max_depht = max_dephtt
    records = Astar(saample)
    return records

if __name__ == "__main__":
    records = Astar([1,2,3,0,7,6,5,4,8])

    print(records)

