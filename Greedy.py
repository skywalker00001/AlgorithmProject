import time
import pandas as pd

COST = 0 #目标函数
FACNUM = 0 #工厂数量
CUSNUM = 0 #顾客数量
CAPACITY = [] #理论最大值
LOAD = [] #实际装载量
OPENCOST = [] #每个fac的打开开销
STATUS = [] #工厂状态，打开为1，关闭为0
DEMAND = [] #每个顾客的需求
ASSIGNCOST = [] #每个工厂对于每个人存放其需求的开销
ASSIGN = [] #顾客将其需求存放在哪些工厂

def readFile(filePath):
    global COST, FACNUM, CUSNUM, CAPACITY, OPENCOST, DEMAND, ASSIGNCOST, STATUS, ASSIGN
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
    global COST
    global CAPACITY
    global STATUS
    global ASSIGN

    for cus in range(CUSNUM):
        availableFac = []
        for fac in range(FACNUM):
            if CAPACITY[fac] >= DEMAND[cus]:
                availableFac.append(fac)
        if len(availableFac) == 0:
            return
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
        CAPACITY[index] -= DEMAND[cus]
        ASSIGN[cus] = index

def handle(filePath):
    readFile(filePath)
    start = time.time()
    greedy()
    end = time.time()
    t = float(end - start)
    print(COST, t)

    f = open('Greedy.txt', 'a')
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
    dataframe.to_csv("Greedy.csv", index=False, sep='|')
