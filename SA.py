import numpy as np
import time
import pandas as pd

COST = 0
FACNUM = 0
CUSNUM = 0
CAPACITY = [] #理论最大值
LOAD = [] #实际装载量
OPENCOST = []
STATUS = []
DEMAND = []
ASSIGNCOST = []
ASSIGN = []

def readFile(filePath):
    global COST, FACNUM, CUSNUM, CAPACITY, LOAD, OPENCOST, DEMAND, ASSIGNCOST, STATUS, ASSIGN
    #清空
    COST = 0
    FACNUM = 0
    CUSNUM = 0
    CAPACITY = []
    OPENCOST = []
    DEMAND = []
    ASSIGNCOST = []

    fopen = open('Instances/' + filePath)
    line = fopen.readline().split()
    FACNUM = int(line[0])
    CUSNUM = int(line[1])
    STATUS = [0] * FACNUM
    ASSIGN = [0] * CUSNUM
    LOAD = [0] * FACNUM
    for i in range(FACNUM):
        line = fopen.readline().split()
        CAPACITY.append(int(line[0]))
        OPENCOST.append(int(line[1]))
    for i in range(int(CUSNUM/10)):
        line = fopen.readline().replace('.', '').split()
        for j in range(10):
            DEMAND.append(int(line[j]))

    for i in range(FACNUM):
        eachFac = []
        for j in range(int(CUSNUM/10)):
            line = fopen.readline().replace('.', '').split()
            for k in range(10):
                eachFac.append(int(line[k]))
        ASSIGNCOST.append(eachFac)
    #print(ASSIGNCOST)
    fopen.close()

def greedy():
    global COST, LOAD, ASSIGN, STATUS

    for cus in range(CUSNUM):
        availableFac = []
        for fac in range(FACNUM):
            if CAPACITY[fac] - LOAD[fac] >= DEMAND[cus]:
                availableFac.append(fac)
        index = availableFac[0]
        minCost = ASSIGNCOST[index][cus]
        for fac in availableFac:
            tempCost = ASSIGNCOST[fac][cus]
            if tempCost < minCost:
                index = fac
                minCost = tempCost
        if STATUS[index] == 0:
            STATUS[index] = 1
            COST += minCost + OPENCOST[index]
        else:
            COST += minCost
        LOAD[index] += DEMAND[cus]
        ASSIGN[cus] = index

def handle(filePath):
    readFile(filePath)
    greedy()
    start = time.time()
    SA()
    end = time.time()
    t = float(end - start)
    print(COST, t)

    f = open('SA.txt', 'a')
    f.write(str(filePath) + '\n')
    f.write(str(COST) + '\n')
    for i in range(FACNUM):
        f.write(str(STATUS[i]) + ' ')
    f.write('\n')
    for i in range(CUSNUM):
        f.write(str(ASSIGN[i]) + ' ')
    f.write('\n\n')
    f.close()

    return COST, t

# def handle(filePath):
#     readFile(filePath)
#     start = time.time()
#     greedy()
#     end = time.time()
#     t = float(end - start)
#     print(COST, t)
#     return COST, t

def SA():
    global COST, LOAD, ASSIGN, STATUS

    T0 = 100
    T = T0
    Tmin = 1
    alpha = 0.99
    innerIter = 100
    while T > Tmin:
        for i in range(innerIter):
            if np.random.rand() > 0.5: #选一个customo去别的fac
                randCus = np.random.randint(0, CUSNUM)
                initFacOfCus = ASSIGN[randCus]
                randFac = np.random.randint(0, FACNUM)
                while randFac == initFacOfCus:
                    randFac = np.random.randint(0, FACNUM)

                while LOAD[randFac] + DEMAND[randCus] > CAPACITY[randFac]:
                    randCus = np.random.randint(0, CUSNUM)
                    initFacOfCus = ASSIGN[randCus]
                    while randFac == initFacOfCus:
                        randFac = np.random.randint(0, FACNUM)
                dValue = ASSIGNCOST[randFac][randCus] - ASSIGNCOST[initFacOfCus][randCus]
                if dValue < 0:
                    COST += dValue
                    LOAD[randFac] += DEMAND[randCus]
                    LOAD[initFacOfCus] -= DEMAND[randCus]
                    if STATUS[randFac] == 0:
                        STATUS[randFac] = 1
                        COST += OPENCOST[randFac]
                    if LOAD[initFacOfCus] == 0:
                        STATUS[initFacOfCus] = 0
                        COST -= OPENCOST[initFacOfCus]
                    ASSIGN[randCus] = randFac
                else:
                    if np.random.rand() < np.exp(-(dValue) / T):  # 接受新解
                        COST += dValue
                        LOAD[randFac] += DEMAND[randCus]
                        LOAD[initFacOfCus] -= DEMAND[randCus]
                        if STATUS[randFac] == 0:
                            STATUS[randFac] = 1
                            COST += OPENCOST[randFac]
                        if LOAD[initFacOfCus] == 0:
                            STATUS[initFacOfCus] = 0
                            COST -= OPENCOST[initFacOfCus]
                        ASSIGN[randCus] = randFac

            else: #选两个cus对调fac
                randCus1 = 0
                randCus2 = 0
                while randCus1 == randCus2:
                    randCus1 = np.random.randint(0, CUSNUM)
                    randCus2 = np.random.randint(0, CUSNUM)
                initFac1 = ASSIGN[randCus1]
                initFac2 = ASSIGN[randCus2]

                while (LOAD[initFac1] - DEMAND[randCus1] + DEMAND[randCus2] > CAPACITY[initFac1]) or (LOAD[initFac2] - DEMAND[randCus2] + DEMAND[randCus1] > CAPACITY[initFac2]) :
                    randCus1 = 0
                    randCus2 = 0
                    while randCus1 == randCus2:
                        randCus1 = np.random.randint(0, CUSNUM)
                        randCus2 = np.random.randint(0, CUSNUM)
                    initFac1 = ASSIGN[randCus1]
                    initFac2 = ASSIGN[randCus2]
                dValue = ASSIGNCOST[initFac1][randCus2] + ASSIGNCOST[initFac2][randCus1] - ASSIGNCOST[initFac1][randCus1] - ASSIGNCOST[initFac2][randCus2]
                if dValue < 0:
                    COST += dValue
                    LOAD[initFac1] += DEMAND[randCus2] - DEMAND[randCus1]
                    LOAD[initFac2] += DEMAND[randCus1] - DEMAND[randCus2]
                    ASSIGN[randCus1] = initFac2
                    ASSIGN[randCus2] = initFac1
                else:
                    if np.random.rand() < np.exp(-(dValue) / T):  # 接受新解
                        COST += dValue
                        LOAD[initFac1] += DEMAND[randCus2] - DEMAND[randCus1]
                        LOAD[initFac2] += DEMAND[randCus1] - DEMAND[randCus2]
                        ASSIGN[randCus1] = initFac2
                        ASSIGN[randCus2] = initFac1
        T = T * alpha
        #print(T, COST)
    print("The Last Cost is:", COST)

if __name__ == "__main__":
    filePaths = []
    results = []
    times = []
    for i in range(71):
        if (i != 66):
            index = "p" + str(i + 1)
            filePaths.append(index)
            result, t = handle(index)
            results.append(result)
            times.append(t)

    data = {'file': filePaths, 'result': results, 'time': times}
    dataframe = pd.DataFrame(data)
    dataframe.to_csv("SA.csv", index=False, sep='|')
